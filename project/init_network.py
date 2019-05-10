#
# Copyright (c) 2019 Cisco Systems
# Licensed under the MIT License
#

from app.models import *
from api.api_requests.apic_access_module.dnaapicem import apic_get_X_auth_token
from api.api_requests.devices_info import apic_devices_info
from api.api_requests.reach_info import apic_reach_info
from api.api_requests.get_device_config import apic_get_device_config
from info_sender.bot_for_np1 import *
from info_sender.email_sender import send_email
from info_sender.message_templates import *
from requests.exceptions import Timeout

from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

DEF_NET_TYPES = ('DNA-C', 'APIC-EM')
DEF_USER_ROLES = ('Admin', 'CIO', 'ITDirector', 'DevOps')
DEF_ISSUE_TYPES = ('configuration_changed', 'traffic', 'unreachable', 'unknown')
DEF_TICKET_STATUSES = ('close', 'in_progress', 'new', 'rejected')

def init_db():
    """
    Create default value on DB
    :return: nothing
    """
    [NetType.objects.get_or_create(value=type) for type in DEF_NET_TYPES]
    [Role.objects.get_or_create(role=role) for role in DEF_USER_ROLES]
    [IssueType.objects.get_or_create(value=issue_type) for issue_type in DEF_ISSUE_TYPES]
    [Status.objects.get_or_create(value=status) for status in DEF_TICKET_STATUSES]

def init_bot(network, reachable_devices=0, unreachable_devices=0):
    """
    Create team and add all users with existing emails.
    Send welcome message to team and email messages for all users
    :param network: Network query object.                         :TODO Implement function to add new user to Spark room when user register after adjust network
    :param reachable_devices: Number of reachable devices (need to show in welcome message)
    :param unreachable_devices: Number of unreachable devices (need to show in welcome message)
    :return: Spark room id
    """

    listOfEmails = set(user['email'] for user in User.objects.all().values('email') if user['email'])

    accessToken = network.bot_token
    teamId      = createTeam(accessToken)
    roomId      = createRoomInTeam(accessToken, teamId)

    addPeopleToSpace(roomId, listOfEmails, accessToken)

    # Send welcome message

    printMessage(roomId,
                 WEBEX_WELCOME_MSG % (reachable_devices,
                                      unreachable_devices),
                 accessToken)

    # Send welcome email

    send_email(listOfEmails, EMAIL_WELCOME_MSG % (reachable_devices,
                                                  unreachable_devices))

    return roomId


def check_reachability(network=None, on_init=False):
    """
    Checking devices in current network if they are reachable and exist in db.
    If device doesn't exists in db it will create new table row for device.
    Finally it will update Service Availability param for current network
    :param network: Take query object of network we want to check device reachability
    :return: List [ 0. number-of-all-devices,
                    1. number-of-reachable-devices,
                    2. number-of-unreachable-devices ]
    """

    if not network:
        try:
            network = Network.objects.get(current=True)
        except ObjectDoesNotExist:
            return False, 'Can\'t find network in DB'

    status, all_devices = apic_reach_info()

    if not status:
        return False, all_devices

    status, devices_info = apic_devices_info()

    if not status:
        return False, devices_info

    devices_from_db = Device.objects.filter(network=network)

    for device in all_devices:
        if device['reachabilityStatus'] == 'REACHABLE' or device['reachabilityStatus'] == 'Reachable':
            current_device = [item for item in devices_info if item["managementIpAddress"] == device["managementIpAddress"]][0]
            status, config = apic_get_device_config(current_device['id'])
            # Check if current device already exist in db
            if current_device['managementIpAddress'] not in [device['ip'] for device in devices_from_db.values('ip')]:

                new_device = Device.objects.create(type=current_device['type'],
                                    ip=current_device['managementIpAddress'],
                                    family=current_device['family'],
                                    device_id=current_device['id'],
                                    hostname=current_device['hostname'],
                                    network=network,
                                    config=config)
                # new_device.save()

        else:
            # Check if current device already exist in db
            if device['managementIpAddress'] not in [device['ip'] for device in devices_from_db.values('ip')]:
                new_device = Device(status=False,
                                    ip=device['managementIpAddress'],
                                    unreach_reason=device['reachabilityFailureReason'],
                                    network=network)

                new_device.save()

                text = ISSUE_DEVICE_UNREACHABLE_TEXT % (device['managementIpAddress'])

                IssueLogMessage.objects.create(device=new_device,
                                               text=text,
                                               issue_type=IssueType.objects.get(value='unreachable'))
                if not on_init:
                    printMessage(new_device.network.webex_room_id,
                                 ISSUE_UNREACHABLE_MSG % (new_device.network.ip, text),
                                 new_device.network.bot_token)

    # update Service Availability statistic

    reachable_devices = Device.objects.filter(network=network, status=True)

    number_reachable_devices = len(reachable_devices)
    number_all_devices = len(devices_from_db)
    number_unreachable_devices = number_all_devices - number_reachable_devices

    network.service_availability = int(number_reachable_devices / number_all_devices * 100)
    network.save()

    return True, [number_all_devices, number_reachable_devices, number_unreachable_devices]


def setup_network(net_ip, net_user, net_pass, net_type, bot_token):

    init_db()

    try:
        api_token = apic_get_X_auth_token(ip=net_ip,
                                          uname=net_user,
                                          pword=net_pass)
    except PermissionError:
        return False, "Wrong user name or password"
    except Timeout:
        return False, "Can't reach service controller"

    try:
        network = Network.objects.create_network(ip=net_ip,
                                                 user_name=net_user,
                                                 password=net_pass,
                                                 net_type=net_type,
                                                 service_ticket=api_token,
                                                 bot_token=bot_token)
    except IntegrityError:
        return False, "Network with given IP already exists"

    status, devices_count_array = check_reachability(network, on_init=True)

    if not status:
        network.delete()
        return False, 'Error while scaning devices'

    if bot_token:
        # try:
        network.webex_room_id = init_bot(network,
                                         reachable_devices=devices_count_array[1],
                                         unreachable_devices=devices_count_array[2])
        # except BaseException as e:
        #     network.delete()
        #     return False, str(e)
        # except Timeout as e:
        #     network.delete()
        #     return False, 'Bot API timeout: ' + str(e)

    network.save()
    run_tasks()

    return True, "New network adjusted and prepeare to work"

#TODO: Implement feature for change current network
