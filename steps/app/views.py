# -*- coding: utf-8 -*-
from __future__ import unicode_literals


# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .forms import *
from .models import *
import datetime
from django.db.models import Q
from django.utils import timezone
try:
    from django.utils import simplejson as json
except ImportError:
    import json

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('app/acc_active_email.html', {
                'user':user,
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your Inventory management account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')

    else:
        form = SignupForm()

    return render(request, 'app/signup.html', {'form': form})



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def index(request):
    return render(request, 'app/index.html')


def dashboard(request):
    user = request.user
    feed = IncubatorPost.objects.all()
    if hasattr(user, 'userprofile'):
        incubators = user.incubator_members.all()
        startups = user.startup_members.all()
        profile = user.userprofile
        context = {
            'incubators': incubators,
            'startups': startups,
            'profile': profile,
            'feed': feed,
            'type': 'U'
        }
        print startups
        return render(request,'app/dashboard.html', context)
    if hasattr(user, 'incubator'):
        profile = user.incubator
        context = {
            'profile': profile,
            'feed': feed,
            'type': 'I'
        }
        print profile.members
        print context
        return render(request, 'app/incubator.html', context)
    if hasattr(user, 'startup'):
        profile = user.startup
        context = {
            'profile': profile,
            'feed': feed,
            'type': 'S'
        }
        print profile.members.all()
        return render(request, 'app/startup.html', context)


@login_required(login_url='/')
def profile(request, username):
    user  = get_object_or_404(User, username=username)
    if hasattr(user, 'userprofile'):
        profile = get_object_or_404(UserProfile, user=user)
        context = {
            'profile': profile,
            'userp': user,
            'type': 'U'
        }
        return render(request, "main/userprofile.html", context)
    if hasattr(user, 'incubator'):
        profile = get_object_or_404(Incubator, user=user)
        posts = profile.posts.all()
        context = {
            'profile': profile,
            'userp': user,
            'type': 'I',
            'posts': posts
        }
        return render(request, "app/incubator_profile.html", context)
    if hasattr(user, 'startup'):
        profile = get_object_or_404(Startup, user=user)
        context = {
            'profile': profile,
            'userp': user,
            'type': 'S'
        }
        return render(request, "app/startup_profile.html", context)



def incubatorid():
    name = 'INC'
    try:
        incubator = Incubator.objects.all()[Incubator.objects.count()-1]
        if incubator:
            lst_id = int((incubator.user.username).split(name)[1])
            return (name + str(lst_id + 1).zfill(8)).replace(' ', '0')
        else:
            return name + '00000001'
    except AssertionError:
        return name + '00000001'


def startupid():
    name = 'STP'
    try:
        startup = Startup.objects.all()[Incubator.objects.count()-1]
        if incubator:
            lst_id = int((startup.user.username).split(name)[1])
            return (name + str(lst_id + 1).zfill(8)).replace(' ', '0')
        else:
            return name + '00000001'
    except AssertionError:
        return name + '00000001'


def incubator_request(request):
    form = IncubatorRequestForm()
    fileform = IncubatorFileForm()
    locationform = LocationForm()
    context = {
        'form': form,
        'fileform': fileform,
        'status': 'get',
        'locationform':locationform
    }
    if request.method == "POST":
        form = IncubatorRequestForm(request.POST)
        fileform = IncubatorFileForm(request.POST,request.FILES)
        locationform = LocationForm(request.POST)
        if form.is_valid() and fileform.is_valid() and locationform.is_valid():
            username = incubatorid()
            location = locationform.save()
            incubator = form.save(commit=False)
            user = User.objects.create_user(username=username,password=username,email=request.POST['email'])
            incubator.user = user
            incubator.request_user = request.user
            incubator.location = location
            incubator.save()
            file = fileform.save(commit=False)
            file.incubator = incubator
            file.save()
            context = {
                'status': 'success'
            }
        else:
            context = {
                'status': 'error',
                'form': form,
                'fileform': fileform,
                'locationform': locationform
            }
    return render(request, 'app/incubator_request.html', context)



def startup_request(request):
    form = StartupRequestForm()
    fileform = StartupFileForm()
    locationform = LocationForm()
    context = {
        'form': form,
        'fileform': fileform,
        'locationform':locationform,
        'status': 'get'
    }
    if request.method == "POST":
        form = StartupRequestForm(request.POST)
        fileform = StartupFileForm(request.POST,request.FILES)
        locationform = LocationForm(request.POST)
        if form.is_valid() and fileform.is_valid():
            username = startupid()
            location = locationform.save()
            startup = form.save(commit=False)
            user = User.objects.create_user(username=username,password=username,email=request.POST['email'])
            startup.user = user
            startup.request_user = request.user
            startup.location = location
            startup.save()
            file = fileform.save(commit=False)
            file.startup = startup
            file.save()
            context = {
                status: 'success'
            }
        else:
            context = {
                'status': 'error',
                'form': form,
                'fileform': fileform,
                'locationform':locationform
            }
    return render(request, 'app/incubator_request.html', context)


def incubator_update(request):
    form = IncubatorForm()
    imageform = IncubatorImageForm()
    contactform = IncubatorContactForm()
    achievementform = IncubatorAchievementForm()
    socialform = IncubatorSocialForm()
    context = {
        'form':form,
        'imageform':  imageform,
        'contactform': contactform,
        'achievementform': achievementform,
        'socialform': socialform
    }

    return render(request, 'app/profile_update.html', context)

def startup_update(request):
    return render(request, 'app/profile_update.html')

def user_update(request):
    return render(request, 'app/profile_update.html')

def leaderboard(request):
    return render(request, 'app/leaderboard.html')

def comparator(request):
    return render(request, 'app/comparator.html')


def incubator_update(request):
    user = request.user
    profile = user.incubator
    form = IncubatorForm(instance=profile)
    context = {
        'form':form,
    }
    if request.method == 'POST':
        form = IncubatorForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('app:incubator_update'))
        else :
            context = {
            'form'  : form,
            }
    else:
        form = IncubatorForm(instance=profile)
        context = {
            'form'  : form,
        }
        return render(request, 'app/profile_update.html', context)

    return render(request, 'app/profile_update.html', context)

def startup_update(request):
    user = request.user
    profile = user.startup
    form = StartupForm(instance=profile)
    context = {
        'form':form,
    }
    if request.method == 'POST':
        form = StartupForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('app:startup_update'))
        else :
            context = {
            'form'  : form,
            }
    else:
        form = IncubatorForm(instance=profile)
        context = {
            'form'  : form,
        }
        return render(request, 'app/profile_update.html', context)

    return render(request, 'app/profile_update.html', context)

def user_update(request):
    if request.method == 'POST':
        user = request.user
        profile = UserProfile.objects.get(user=user)
        userform = UserForm(request.POST, instance=user)
        profileform = UserProfileForm(request.POST, instance=profile)
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            f = profileform.save(commit=False)
            f.user = request.user
            f.save()
            context = {
            'userform'  : userform,
            'profileform': profileform
            }
            return HttpResponseRedirect(reverse('app:user_update'))
        else :
            context = {
            'userform'  : userform,
            'profileform': profileform
            }
            return render(request, 'app/editProfile.html', context)
    else:
        profile = UserProfile.objects.get(user = request.user)
        userform = UserForm(instance=request.user)
        profileform = UserProfileForm(instance=profile)
        context = {
            'userform'  : userform,
            'profileform': profileform
        }
        return render(request, 'app/editProfile.html', context)



