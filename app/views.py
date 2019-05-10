#
# Copyright (c) 2019 Cisco Systems
# Licensed under the MIT License
#

import django.views.generic
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from app.models import UserProfile

def home(request):
    if request.method == 'GET':
        user = request.user

        if user.is_authenticated:
            profile = UserProfile.objects.get(user=user)

        return render(request, "index.html", locals())
    else:
        return JsonResponse({'err': 'Method GET expected'}, safe=False)

def app(request):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
            profile = UserProfile.objects.get(user=user)
            user_role = profile.role.role
            return render(request, "app.html", locals())
        else:
            return redirect('/login')
    else:
        return JsonResponse({'err': 'Method GET expected'}, safe=False)
