from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import render, redirect
from app.models import UserProfile, Role, Network
from django.core.validators import validate_email
from django.core.exceptions import (ValidationError, ObjectDoesNotExist)
from info_sender.bot_for_np1 import addPeopleToSpace

def registration(request):
    if request.method == 'POST':
        print(request.POST)
        login = request.POST['login']
        password = request.POST['pass']
        conf_password = request.POST['conf-pass']
        role = request.POST['role']
        first_name = request.POST['first_name']
        second_name = request.POST['second_name']
        email = request.POST['email']

        if conf_password == password:
            try:
                validate_email(email)
            except ValidationError:
                return render(request, 'user-auth/auth_error.html',
                              {'error': 'Email is not valid',
                               'action': 'Registration'})

            try:
                role = Role.objects.get(role=role)
                user = User.objects.create_user(login, password=password, email=email)
                profile = UserProfile.objects.create(user=user,
                                                     role=role,
                                                     first_name=first_name,
                                                     second_name=second_name)
            except IntegrityError:
                return render(request, 'user-auth/auth_error.html', {'error': 'Username is already exists',
                                                                     'action': 'Registration'})
            except ValueError as e:
                return render(request, 'user-auth/auth_error.html', {'error': e,
                                                                     'action': 'Registration'})
            else:
                user.save()

                try:
                    network = Network.objects.get(current=True)
                except ObjectDoesNotExist:
                    pass
                else:
                    try:
                        addPeopleToSpace(network.webex_room_id, [email], network.bot_token)
                    except BaseException as e:
                        return render(request, 'user-auth/auth_error.html', {'error': e,
                                                                             'action': 'Registration'})

                user = auth.authenticate(username=login, password=password)

                if user is not None:
                    if user.is_active:
                        auth.login(request, user)
                        return redirect('/app/')

                return render(request, 'index.html', locals())
        else:
            return render(request, 'user-auth/auth_error.html', {'error': 'Password and confirm password isn\'t equal',
                                                                 'action': 'Registration'})
    else:
        roles = Role.objects.all()
        return render(request, 'user-auth/registration_form.html', locals())

def login(request):
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']

        user = auth.authenticate(username=login, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return redirect('/app/')
        else:
            return render(request, 'index.html', locals())
    else:
        return render(request, 'user-auth/login.html', locals())

def logout(request):
    auth.logout(request)
    return render(request, 'index.html', locals())