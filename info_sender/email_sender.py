from django.core.mail import send_mail
from django.conf import settings
from info_sender.message_templates import EMAIL_MTTR_UPDATED, EMAIL_SLA_UPDATED
from info_sender import message_templates
# from app.models import Network, UserProfile, IssueLogMessage

def send_email(address_list, message):

    subject = "DNA-C notification service"

    from_mail = settings.EMAIL_HOST_USER

    # send_mail(subject, message, from_mail, address_list, fail_silently=False)

def send_update_mttr(network, users, new_mttr, new_mttri):

    it_directors_emails = users.filter(role__role='ITDirector')

    emails = [user['user__email'] for user in list(it_directors_emails.values('user__email'))]

    msg = EMAIL_MTTR_UPDATED.format(network.ip,
                                str(network.mttr).split('.')[0],
                                str(new_mttr).split('.')[0],
                                str(network.mttri).split('.')[0],
                                str(new_mttri).split('.')[0])

    send_email(emails, msg)

def send_update_sla(network, users, new_sla):

    sio_emails = users.filter(role__role='CIO')

    emails = [user['user__email'] for user in list(sio_emails.values('user__email'))]

    msg = EMAIL_SLA_UPDATED.format(network.ip,
                               network.service_availability,
                               network.customer_satisfaction,
                               new_sla)

    send_email(emails, msg)

def send_daily_cio_report(net, users):

    # net = Network.objects.get(current=True)
    #
    # users = UserProfile.objects.all().filter(role__role='CIO')

    for user in users:
        message = message_templates.SLA_INFO_FOR_CIO.format(user.full_name,
                                                            net.ip,
                                                            net.service_availability,
                                                            str(net.mttri).split('.')[0],
                                                            net.customer_satisfaction)
        send_email([user.user.email], message)

def send_daily_director_report(net, users, count):
    # net = Network.objects.get(current=True)
    #
    # users = UserProfile.objects.all().filter(role__role='ITDirector')

    # tickets_count = IssueLogMessage.objects.all().exclude(status__value='close').exclude(status__value='rejected').count()

    for user in users:
        message = message_templates.MTTR_FOR_IT_DIRECTOR.format(user.full_name,
                                                                net.ip,
                                                                str(net.mttr).split('.')[0],
                                                                count)
        send_email([user.user.email], message)
