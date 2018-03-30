# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(UserProfile)
admin.site.register(Contact)
admin.site.register(Social)
admin.site.register(Skill)
admin.site.register(Organisation)
admin.site.register(Experience)
admin.site.register(Location)

admin.site.register(Incubator)
admin.site.register(IncubatorMember)
admin.site.register(IncubatorContact)
admin.site.register(IncubatorSocial)
admin.site.register(IncubatorAchievement)
admin.site.register(IncubatorFile)
admin.site.register(IncubatorImage)
admin.site.register(IncubatorPost)
admin.site.register(IncubatorStartup)
admin.site.register(IncubatorRating)

admin.site.register(Startup)
admin.site.register(StartupMember)
admin.site.register(StartupContact)
admin.site.register(StartupSocial)
admin.site.register(StartupAchievement)
admin.site.register(StartupFile)


admin.site.register(Room)
admin.site.register(Link)
admin.site.register(Message)
admin.site.register(ConnectionRequest)

