# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import *


class IncubatorAdmin(admin.ModelAdmin):
    list_display = ('name','status','approve_field', 'reject_field' )
    def approve_field(self, obj):
        if obj.status!='S':
            return 'NA'
        return '<a href="%s">%s</a>' % (reverse('app:approve_incubator', kwargs={'id':obj.id,}),'Approve',)
    def reject_field(self, obj):
        if obj.status!='S':
            return 'NA'
        return '<a href="%s">%s</a>' % (reverse('app:reject_incubator', kwargs={'id':obj.id,}),'Reject',)
    approve_field.allow_tags = True
    approve_field.short_description = 'Approve'
    reject_field.allow_tags = True
    reject_field.short_description = 'Reject'



class StartupAdmin(admin.ModelAdmin):
    list_display = ('name','status','approve_field', 'reject_field' )
    def approve_field(self, obj):
        if obj.status!='S':
            return 'NA'
        return '<a href="%s">%s</a>' % (reverse('app:approve_startup', kwargs={'id':obj.id,}),'Approve',)
    def reject_field(self, obj):
        if obj.status!='S':
            return 'NA'
        return '<a href="%s">%s</a>' % (reverse('app:reject_startup', kwargs={'id':obj.id,}),'Reject',)
    approve_field.allow_tags = True
    approve_field.short_description = 'Approve'
    reject_field.allow_tags = True
    reject_field.short_description = 'Reject'



admin.site.register(UserProfile)
admin.site.register(Contact)
admin.site.register(Social)
admin.site.register(Skill)
admin.site.register(Organisation)
admin.site.register(Experience)
admin.site.register(Location)

admin.site.register(Incubator, IncubatorAdmin)
admin.site.register(IncubatorMember)
admin.site.register(IncubatorContact)
admin.site.register(IncubatorSocial)
admin.site.register(IncubatorAchievement)
admin.site.register(IncubatorFile)
admin.site.register(IncubatorImage)
admin.site.register(IncubatorPost)
admin.site.register(IncubatorStartup)
admin.site.register(IncubatorRating)

admin.site.register(Startup, StartupAdmin)
admin.site.register(StartupMember)
admin.site.register(StartupContact)
admin.site.register(StartupSocial)
admin.site.register(StartupAchievement)
admin.site.register(StartupFile)


admin.site.register(Room)
admin.site.register(Link)
admin.site.register(Message)
admin.site.register(ConnectionRequest)

