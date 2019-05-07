from django.conf.urls import url
from api import views

urlpatterns = [
	url(r"send_mail/$", views.send_mail, name="send_mail"),
	url(r"get_devices_info/$", views.get_devices_info, name="get_devices_info"),
	url(r"get_issue_list/(?P<user>.*)$", views.get_issue_list, name="get_issue_list"),
	url(r"set_solver/$", views.set_solver, name="set_solver"),
	url(r"reject_ticket/$", views.reject_ticket, name="reject_ticket"),
	url(r"set_issue_as_solved/$", views.set_issue_as_solved, name="set_issue_as_solved"),
	url(r"setup_network/$", views.setup_network, name="setup_network"),
	url(r"sending_mail/$", views.sending_mail, name="send_mail"),
	url(r"daily_notification/$", views.daily_notification, name="daily_notification"),
]