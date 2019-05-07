from json import loads, dumps
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from app.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from info_sender import email_sender
from info_sender import message_templates

from project.init_network import setup_network as setup

# Create your views here.
@csrf_exempt
def setup_network(request):
    if request.method == 'POST':

        net_ip = request.POST['net_ip']
        net_user = request.POST['net_user']
        net_pass = request.POST['net_pass']
        net_type = request.POST['net_type']
        bot_token = request.POST['bot_token']

        status, msg = setup(net_ip, net_user, net_pass, net_type, bot_token)

        return JsonResponse({'status': status, 'msg': msg }, safe=False)

    else:
        return JsonResponse({'status': False, 'msg': 'Method POST expected'}, safe=False)


def get_devices_info(request):
    if request.method == 'GET':
        devices = Device.objects.filter(network__current=True).values()

        return JsonResponse({'status': True, 'data': list(devices)}, safe=False)
    else:
        return JsonResponse({'status': False, 'msg': 'Method GET expected'}, safe=False)

def get_issue_list(request, user):
    if request.method == 'GET':
        if user == '':
            issues = IssueLogMessage.objects.filter(device__network__current=True).values('id', 'date',
                                                                                          'date_end',
                                                                                          'date_start',
                                                                                          'decision_unit__full_name',
                                                                                          'decision_unit__role__role',
                                                                                          'decision_unit__user__username',
                                                                                          'device__network__ip',
                                                                                          'device__ip',
                                                                                          'text',
                                                                                          'issue_type__value',
                                                                                          'status__value',
                                                                                          'reject_msg')
        else:
            issues = IssueLogMessage.objects.filter(device__network__current=True,
                                                    decision_unit__user__username=user).values('id', 'date',
                                                                                               'date_end',
                                                                                               'date_start',
                                                                                               'decision_unit__full_name',
                                                                                               'decision_unit__role__role',
                                                                                               'decision_unit__user__username',
                                                                                               'device__network__ip',
                                                                                               'device__ip',
                                                                                               'text',
                                                                                               'issue_type__value',
                                                                                               'status__value',
                                                                                               'reject_msg')

        solvers = UserProfile.objects.filter(role__role='DevOps').values('full_name', 'user__username')

        try:
            network = Network.objects.get(current=True)
        except ObjectDoesNotExist as e:
            network = Network(mttr=None, mttri=None, service_availability=0, customer_satisfaction=0)

        print('MTTR', network.mttr, type(network.mttr))

        return JsonResponse({'status': True,
                             'data': list(issues),
                             'solvers': list(solvers),
                             'mttr': str(network.mttr),
                             'mttri': str(network.mttri),
                             'service_availability': network.service_availability,
                             'customer_satisfaction': network.customer_satisfaction}, safe=False)
    else:
        return JsonResponse({'status': False, 'msg': 'Method GET expected'}, safe=False)

@csrf_exempt
def set_solver(request):
    if request.method == 'POST':
        solver_name = request.POST['solver']
        issue_id = request.POST['issue_id']

        print('Set solver/api: ', solver_name, issue_id)

        try:
            solver = UserProfile.objects.get(user__username=solver_name)
            issue = IssueLogMessage.objects.get(id=issue_id)
        except:
            return JsonResponse({'status': False, 'msg': 'Object not found'}, safe=False)
        else:
            issue.decision_unit = solver

            if issue.status.value == 'new':
                issue.status = Status.objects.get(value='in_progress')

            issue.date_start = timezone.now()

            issue.save()

            message = message_templates.NEW_TICKET_ASSIGNED % (solver.full_name, issue.id)

            email_sender.send_email([solver.user.email], message)

        return JsonResponse({'status': True}, safe=False)
    else:
        return JsonResponse({'status': False, 'msg': 'Method POST expected'}, safe=False)


@csrf_exempt
def reject_ticket(request):
    if request.method == 'POST':
        issue_id = request.POST['issue_id']
        reject_msg = request.POST['reject_msg']

        try:
            issue = IssueLogMessage.objects.get(id=issue_id)
        except:
            return JsonResponse({'status': False, 'msg': 'Object not found'}, safe=False)
        else:
            issue.status = Status.objects.get(value='rejected')
            issue.date_end = timezone.now()
            issue.reject_msg = reject_msg
            issue.save()

        return JsonResponse({'status': True}, safe=False)
    else:
        return JsonResponse({'status': False, 'msg': 'Method POST expected'}, safe=False)


@csrf_exempt
def set_issue_as_solved(request):
    if request.method == 'POST':
        issue_id = request.POST['issue_id']

        try:
            issue = IssueLogMessage.objects.get(id=issue_id)
        except:
            return JsonResponse({'status': False, 'msg': 'Object not found'}, safe=False)
        else:
            if issue.status.value == 'in_progress':
                issue.status = Status.objects.get(value='close')
                issue.date_end = timezone.now()
            issue.save()

            return JsonResponse({'status': True}, safe=False)
    else:
        return JsonResponse({'status': False, 'msg': 'Method POST expected'}, safe=False)

@csrf_exempt
def sending_mail(request):
    if request.method == "POST":
        data = loads(request.POST['data'])

        print(data, type(data))

        for user in data:

            subject = "Hello my dear " + user['name']

            message = "This is the message for " + user['name'] + " position " + user['position']

            from_mail = settings.EMAIL_HOST_USER

            to_mail = [ user['email'] ]

            send_mail(subject, message, from_mail, to_mail, fail_silently=False)

        return JsonResponse({'msg': 'all ok'}, safe=False)

    return JsonResponse({'error': 'method POST expected'}, safe=False)

@csrf_exempt
def daily_notification(request):
    if request.method == 'GET':
        try:
            net = Network.objects.get(current=True)
            users = UserProfile.objects.all()
            tickets_count = IssueLogMessage.objects.all().exclude(status__value='close').exclude(
                status__value='rejected').count()

            cio_users = users.filter(role__role='CIO')
            director_users = users.filter(role__role='ITDirector')

        except:
            return JsonResponse({'status': False, 'msg': 'Object not found'}, safe=False)
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
    else:
        return JsonResponse({'status': False, 'msg': 'Method GET expected'}, safe=False)