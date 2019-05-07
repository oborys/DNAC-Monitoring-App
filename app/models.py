from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from .analytics import calc_mttr
from django_celery_beat.models import PeriodicTask
from info_sender.email_sender import *
from django.utils import timezone

import datetime

class Role(models.Model):
    role = models.CharField(max_length=64, blank=True, unique=True)

    def __str__(self):
        return self.role

class Status(models.Model):
    value = models.CharField(max_length=64, blank=True, unique=True)

    def __str__(self):
        return self.value

class IssueType(models.Model):
    value = models.CharField(max_length=64, blank=True, unique=True)

    def __str__(self):
        return self.value

class NetType(models.Model):
    value = models.CharField(max_length=64, blank=True, unique=True)

    def __str__(self):
        return self.value

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, blank=False, null=True)
    first_name = models.CharField(max_length=64, blank=True)
    second_name = models.CharField(max_length=64, blank=True)
    full_name = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return "%s (%s)" % (self.user.username, self.role.role)

    def save(self, **kwargs):
        self.full_name = "%s %s" % (self.first_name, self.second_name)

        super(UserProfile, self).save()

class NetworkManager(models.Manager):
    def create_network(self, ip=None, user_name=None, password=None, net_type=None, service_ticket=None, bot_token=None):

        # set current flag to 'False' for previous active network

        nets = Network.objects.all()

        if ip in [el['ip'] for el in list(nets.values('ip'))]:
            raise IntegrityError

        for net in nets:
            if net.current:
                net.current = False
                net.save()

        net_type = NetType.objects.get(value=net_type)

        network = self.create(ip=ip,
                              user_name=user_name,
                              password=password,
                              type=net_type,
                              service_ticket=service_ticket,
                              bot_token=bot_token,
                              current=True)

        return network

    def change_current(self, new_current):
        # set current flag to 'False' for previous active network
        old_current_nets = Network.objects.filter(current=True)

        if old_current_nets:
            for net in old_current_nets:
                net.current = False
                net.save()

        if isinstance(new_current, Network):
            new_current.current = True
            new_current.save()

        elif isinstance(new_current, str):
            new_current = Network.objects.get(ip=new_current)
            new_current.current = True
            new_current.save()
        else:
            raise TypeError('Wrong argument type passed to change current network method')

        return new_current

class Network(models.Model):
    ip = models.CharField(unique=True, max_length=64, blank=False)
    user_name = models.CharField(max_length=128, blank=True)
    password = models.CharField(max_length=50, blank=True)
    type = models.ForeignKey(NetType, on_delete=models.SET_NULL, blank=True, null=True)
    service_ticket = models.CharField(max_length=128, blank=True)
    mttr = models.DurationField(blank=True, null=True)
    mttri = models.DurationField(blank=True, null=True)
    service_availability = models.PositiveSmallIntegerField(default=0)
    customer_satisfaction = models.PositiveSmallIntegerField(default=0)
    bot_token = models.CharField(max_length=128, blank=True)
    current = models.BooleanField(default=True)
    webex_room_id = models.CharField(max_length=128, blank=True)

    objects = NetworkManager()

    def __str__(self):
        return self.ip

    class Meta:
        db_table = 'network'
        verbose_name = 'Existing networks'
        verbose_name_plural = 'Existing networks'

class Device(models.Model):
    status = models.BooleanField(default=True)
    unreach_reason = models.CharField(max_length=128, blank=True)
    type = models.CharField(max_length=128, blank=True)
    family = models.CharField(max_length=128, blank=True)
    device_id = models.CharField(max_length=128, blank=True)
    hostname = models.CharField(max_length=128, blank=True)
    ip = models.GenericIPAddressField()
    network = models.ForeignKey(Network, on_delete=models.CASCADE, blank=True, null=True)
    config = models.TextField(blank=True, null=True)

    def __str__(self):
        return 'Net: ' + self.network.ip + ' Device: ' + self.ip + ' ' + self.hostname

    class Meta:
        db_table = 'device'
        verbose_name = 'All devices'
        verbose_name_plural = 'All devices'

class IssueLogMessage(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_start = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)
    issue_type = models.ForeignKey(IssueType, on_delete=models.CASCADE, blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, blank=True, null=True)
    decision_unit = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, blank=True, null=True)
    reject_msg = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):

        if not self.pk:
            # Set status to new ticket as 'new'
            status, is_created = Status.objects.get_or_create(value='new')
            self.status = status
            # Recalculate customer satisfaction when new ticket create
            today_issues = IssueLogMessage.objects.filter(date__range=[datetime.date.today(), datetime.datetime.now()])
            closed = today_issues.filter(status__value='close')

            customer_satisfaction = int(len(closed) / (len(today_issues) + 1) * 100)

            network = Network.objects.get(current=True)
            network.customer_satisfaction = customer_satisfaction
            network.save()

        elif self.date_end and not self.status.value == 'rejected':
            current_issue = {
                'date': self.date,
                'date_end': self.date_end,
                'date_start': self.date_start
            }
            dates_list = list(IssueLogMessage.objects.filter(status__value='close').values('date', 'date_start', 'date_end'))
            dates_list.append(current_issue)
            mttr, mttri = calc_mttr(dates_list)

            # Recalculate customer satisfaction when ticket is close
            today_issues = IssueLogMessage.objects.filter(date__range=[datetime.date.today(), datetime.datetime.now()])
            closed = today_issues.filter(status__value='close')

            try:
                customer_satisfaction = int((len(closed) + 1) / len(today_issues) * 100)
            except ZeroDivisionError:
                customer_satisfaction = 0

            network = Network.objects.get(current=True)
            users = UserProfile.objects.all()

            send_update_mttr(network, users, mttr, mttri)
            send_update_sla(network, users, customer_satisfaction)

            network.mttr = mttr
            network.mttri = mttri
            network.customer_satisfaction = customer_satisfaction
            network.save()

        super(IssueLogMessage, self).save(*args, **kwargs)

    class Meta:
        db_table = 'issue_log_message'
        verbose_name = 'Issue log messages'
        verbose_name_plural = 'Issue messages'

def run_tasks(enable=None):

    if enable is None:
        enable = True

    tasks = PeriodicTask.objects.all()

    for task in tasks:
        task.enabled = enable
        task.save()
