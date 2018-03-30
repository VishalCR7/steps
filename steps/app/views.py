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
from math import cos, asin, sqrt

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
            'type': 'I',
            'recommended': recommend_startup(profile)

        }
        return render(request, 'app/incubator.html', context)
    if hasattr(user, 'startup'):
        profile = user.startup
        context = {
            'profile': profile,
            'feed': feed,
            'type': 'S',
            'recommended': recommend_incubator(profile)
        }
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
        return render(request, "app/userprofile.html", context)
    if hasattr(user, 'incubator'):
        profile = get_object_or_404(Incubator, user=user)
        posts = profile.posts.all()
        context = {
            'profile': profile,
            'userp': user,
            'type': 'I',
            'posts': posts,
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

def leaderboard(request):
    return render(request, 'app/leaderboard.html')

def comparator(request):
    s1 = request.GET.get('s1')
    s2 = request.GET.get('s2')
    t = request.GET.get('t')
    context={}
    if t == 'I':
        i1 = User.objects.get(username=s1).incubator
        i2 = User.objects.get(username=s2).incubator
        context = {
            'profile1' : i1,
            'profile2' : i2
        }
    elif t == 'S':
        i1 = User.objects.get(username=s1).startup
        i2 = User.objects.get(username=s2).startup
        context = {
            'profile1' : i1,
            'profile2' : i2
        }
    return render(request, 'app/comparator.html', context)

def recommend_incubator(startup):
    incu = Incubator.objects.all()
    d = []
    for inc in incu:
        a={}
        itags = set(inc.tags.all())
        stags = set(startup.tags.all())
        common = len(itags & stags)
        a['name'] = inc.name
        a['id'] = inc.id
        a['common'] = common
        a['obj'] = inc
        cr = (common/2)+1
        if common == 0:
            cr = 0
        elif cr > 5:
            cr = 5
        lat1 = float(inc.location.latitude)
        lon1 = float(inc.location.longitude)
        lat2 = float(startup.location.latitude)
        lon2 = float(startup.location.longitude)
        p = 0.017453292519943295
        au = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
        distance = 12742 * asin(sqrt(au))
        a['distance'] = distance
        if distance<=500:
            dr = (500-distance)/500*5
        else:
            dr=0
        rate = inc.ratings.all()
        n = len(rate)
        if n!=0:
            s=0
            for rat in rate:
                s = s+rat
            av = (s+0.00)/n
        else:
            av = 0
        a['rating'] = av
        a['sparam'] = int(3*cr+4*dr+5*av)
        d.append(a)
    s = sorted(d, key=lambda k: k['sparam'])
    i = map(lambda k:k['obj'],s)
    return i[0:5]


def recommend_startup(startup):
    incu = Startup.objects.all()
    d = []
    for inc in incu:
        a={}
        itags = set(inc.tags.all())
        stags = set(startup.tags.all())
        common = len(itags & stags)
        a['name'] = inc.name
        a['id'] = inc.id
        a['common'] = common
        a['obj'] = inc
        cr = (common/2)+1
        if common == 0:
            cr = 0
        elif cr > 5:
            cr = 5
        lat1 = float(inc.location.latitude)
        lon1 = float(inc.location.longitude)
        lat2 = float(startup.location.latitude)
        lon2 = float(startup.location.longitude)
        p = 0.017453292519943295
        au = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
        distance = 12742 * asin(sqrt(au))
        a['distance'] = distance
        if distance<=500:
            dr = (500-distance)/500*5
        else:
            dr=0
        a['sparam'] = int(3*cr+4*dr)
        d.append(a)
    s = sorted(d, key=lambda k: k['sparam'])
    i = map(lambda k:k['obj'],s)
    return i[0:5]

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



def contact_add(request):
    if request.method == 'GET':
        user = request.user
        typ = request.GET['contact_type']
        visibility = request.GET['visibility']
        value = request.GET['contact_value']
        if hasattr(user, 'incubator'):
            achievement = IncubatorContact.objects.create(value=value, contact_type=typ,visibility=visibility, incubator = user.incubator )
            ctx = {'status': True}
        if hasattr(user, 'startup'):
            achievement = StartupContact.objects.create(value=value, contact_type=typ,visibility=visibility, startup = user.startup )
            ctx = {'status': True}
        return HttpResponse(json.dumps(ctx), content_type='application/json')


def achievement_add(request):
    if request.method == 'GET':
        user = request.user
        title = request.GET['achievement']
        value = request.GET['achievement_value']
        if hasattr(user, 'incubator'):
            achievement = IncubatorAchievement.objects.create(value=value, title=title, incubator = user.incubator )
            ctx = {'status': True}
        if hasattr(user, 'startup'):
            achievement = StartupAchievement.objects.create(value=value, title=title, startup = user.startup )
            ctx = {'status': True}
        return HttpResponse(json.dumps(ctx), content_type='application/json')


def social_add(request):
    if request.method == 'GET':
        user = request.user
        typ = request.GET['social_type']
        visibility = request.GET['visibility']
        value = request.GET['social_value']
        if hasattr(user, 'incubator'):
            achievement = IncubatorSocial.objects.create(value=value, social_type=typ,visibility=visibility, incubator = user.incubator )
            ctx = {'status': True}
        if hasattr(user, 'startup'):
            achievement = StartupSocial.objects.create(value=value, social_type=typ,visibility=visibility, startup = user.startup )
            ctx = {'status': True}
        return HttpResponse(json.dumps(ctx), content_type='application/json')

from dal import autocomplete
from django.db.models import Q

class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = User.objects.exclude(userprofile=None)

        if self.q:
            qs = qs.filter( Q(first_name__icontains = self.q) | Q(last_name__icontains = self.q)  | Q(username__icontains = self.q)|
                Q(first_name__contains = self.q) | Q(last_name__contains = self.q)  | Q(username__contains = self.q))
        return qs


def incubator_member_add(request):
    user = request.user

    form = IncubatorMemberForm()
    context = {
        'form':form,
    }
    if request.method == 'POST':
        profile = user.incubator
        form = StartupForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.incubator = profile
            form.save_m2m()
            f.save()


            return HttpResponseRedirect(reverse('app:incubator_member_add'))
        else :
            context = {
            'form'  : form,
            }

    return render(request, 'app/memberadd.html', context)