#
# Copyright (c) 2019 Cisco Systems
# Licensed under the MIT License
#

from __future__ import absolute_import, unicode_literals
from celery import shared_task

from app.models import *

from api.api_requests.check_device_name import *
from api.api_requests.path_trace import *
from api.api_requests.get_device_config import apic_get_device_config
from api.api_requests.apic_access_module.dnaapicem import apic_get_X_auth_token

from project.init_network import check_reachability
from info_sender.bot_for_np1 import printMessage
from info_sender.message_templates import *

from django.core.exceptions import ObjectDoesNotExist

import itertools
import difflib

@shared_task
def device_reachability():
    check_reachability()

@shared_task
def check_name():
    status, nodes = phisical_topology()

    if not status:
        return
    try:
        devices = Device.objects.filter(network__current=True).values('hostname', 'device_id')
    except ObjectDoesNotExist:
        return ''
    node_dev = list(devices)

    for node in nodes:

        device_from_db = [el for el in node_dev if el['device_id'] == node['id']]

        if device_from_db and device_from_db[0]['hostname'] != node["label"]: #the function that gets device id and returns device label from DB
            device = Device.objects.get(device_id=node['id'], network__current=True)

            text = ISSUE_NAME_CHANGED_TEXT % (device_from_db[0]['hostname'], node['label'])

            IssueLogMessage.objects.create(device=device,
                                           text=text,
                                           issue_type = IssueType.objects.get(value='configuration_changed'))

            printMessage(device.network.webex_room_id,
                         ISSUE_CONFIG_CHANGED_MSG % (device.network.ip, text),
                         device.network.bot_token)

            device.hostname = node['label']
            device.save()

        elif not device_from_db:
            print('new device')
        else:
            print('all ok')

@shared_task
def path_trace_check():
    try:
        ip_status_id = Device.objects.filter(network__current=True).values('ip', 'status', 'hostname', 'device_id')
    except ObjectDoesNotExist:
        return ''
    node_ip = list(ip_status_id)
    status_up = []
    dict_host_ip = {}

    for val in node_ip:
        # REMOVE or val['status'] == False ONLY FOR TESTING
        if val['status'] == True or val['status'] == False:
            status_up.append(val['ip'])
            dict_host_ip[val['ip']] = val['hostname']

    list_problem_ip = list()

    for source_ip, destination_ip in itertools.combinations(status_up, 2):
        if apic_path_trace(source_ip, destination_ip) != 'COMPLETED':

            problem_ip = source_ip + "-" + destination_ip
            if problem_ip not in list_problem_ip: #todo: need to check this row because messadge allwais sending. Seems to this id statement doesn't work
                device = Device.objects.get(ip=source_ip, network__current=True)

                text = ISSUE_CONNECTION_PROBLEM_TEXT % (source_ip,
                                                        destination_ip)

                IssueLogMessage.objects.get_or_create(device=device,
                                                      text=text,
                                                      issue_type = IssueType.objects.get(value='traffic'))

                printMessage(device.network.webex_room_id,
                             ISSUE_TRAFFIC_MSG % (device.network.ip, text),
                             device.network.bot_token)

                list_problem_ip.append(problem_ip)

@shared_task
def update_ticket():

    network = Network.objects.get(current=True)

    token = apic_get_X_auth_token(ip=network.ip,
                                  uname=network.user_name,
                                  pword=network.password)

    network.service_ticket = token

    network.save()

@shared_task
def config_check():
    try:
        id_and_config = Device.objects.filter(network__current=True).values('device_id', 'config', 'status')
    except ObjectDoesNotExist:
        return ''

    node_config = list(id_and_config)
    status_up = []

    for val in node_config:
        # REMOVE or val['status'] == False ONLY FOR TESTING
        if val['status'] == True:
            status_up.append(val['device_id'])

    for element in node_config:
        if element["status"] == True:
            dbConfig = element["config"]
            status, newConfig = apic_get_device_config(element["device_id"])

            if not status:
                continue

            diff = difflib.ndiff(dbConfig.splitlines(1), newConfig.splitlines(1))
            string = ''.join(diff)

            if dbConfig != newConfig:
                all_text = string.split('\n')
                listChangeAdd = []
                listChangeSubtract = []
                for row in all_text:
                    if row == '':
                        pass
                    elif row[0] == '+':
                        listChangeAdd.append(row)
                    elif row[0] == '-':
                        listChangeSubtract.append(row)

                print ("Add", listChangeAdd)
                print ("Subtract ", listChangeSubtract)

                device = Device.objects.get(device_id=element["device_id"], network__current=True)
                device.config = newConfig
                device.save()

                text = ISSUE_CONFIG_CHANGED_TEXT % (element["device_id"],
                                                    str(listChangeAdd),
                                                    str(listChangeSubtract))

                IssueLogMessage.objects.create(device=device,
                                               text=text,
                                               issue_type = IssueType.objects.get(value='configuration_changed'))

                printMessage(device.network.webex_room_id,
                             ISSUE_CONFIG_CHANGED_MSG % (device.network.ip, text),
                             device.network.bot_token)

@shared_task
def daily_report():

    try:
        net = Network.objects.get(current=True)
        users = UserProfile.objects.all()
        tickets_count = IssueLogMessage.objects.filter(device__network__current=True).exclude(status__value='close').exclude(status__value='rejected').count()

        cio_users = users.filter(role__role='CIO')
        director_users = users.filter(role__role='ITDirector')

    except:
        pass
    else:

        for user in cio_users:
            message = message_templates.SLA_INFO_FOR_CIO.format(user.full_name,
                                                                net.ip,
                                                                net.service_availability,
                                                                str(net.mttri).split('.')[0],
                                                                net.customer_satisfaction)
            send_email([user.user.email], message)

        for user in director_users:
            message = message_templates.MTTR_FOR_IT_DIRECTOR.format(user.full_name,
                                                                    net.ip,
                                                                    str(net.mttr).split('.')[0],
                                                                    tickets_count)
            send_email([user.user.email], message)

        return JsonResponse({'status': True}, safe=False)
