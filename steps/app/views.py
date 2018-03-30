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
    incubators = user.incubator_members.all()
    startups = user.startup_members.all()
    userprofile = user.userprofile
    context = {
        'incubators': incubators,
        'startups': startups,
        'userprofile': userprofile
    }
    return render(request, 'app/dashboard.html')

def incubator(request):
    return render(request, 'app/incubator.html')

def startup(request):
    return render(request, 'app/startup.html')

def leaderboard(request):
    return render(request, 'app/leaderboard.html')

def comparator(request):
    return render(request, 'app/comparator.html')

