# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse

# Create your models here.

VIS_TYPES = (
        ('Me', 'Only Me'),
        ('All', 'All'),
        ('INC', 'Incubator'),
        ('SU', 'Start ups'),
        ('SUT', 'Start Up Team'),
        ('INCT', 'Incubator Team'),
    )


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='users', blank=True, null=True)
    dob = models.DateField(null=True, blank=True, verbose_name='Date Of Birth')
    gender = models.CharField(null=True, blank=True, max_length=1, choices=(('F', 'Female'), ('M', 'Male')), verbose_name="gender")
    aadhar_no = models.BigIntegerField(blank=True, null=True)
    nationality = models.CharField(max_length = 100,blank=True, null=True, default='Indian')
    def get_name(self):
        return self.user.first_name+' '+self.user.last_name
    def __str__(self):
        return str(self.user.username)

""" For creating a UserProfile object by default after a user object is created"""
@receiver(post_save, sender=User)
def create_user_userProfile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_userProfile(sender, instance, **kwargs):
    instance.userprofile.save()


class Contact(models.Model):
    TYPES = (
        ('Mob', 'Mobile No.'),
        ('Email', 'Email'),
    )
    contact_type = models.CharField(max_length=10, choices=TYPES, verbose_name="Contact Type")
    user = models.ForeignKey(User, verbose_name="User",related_name='contacts', on_delete=models.CASCADE)
    value = models.TextField()
    visibility = models.CharField(max_length=10, choices=VIS_TYPES, verbose_name="Contact Visibility")

    def __str__(self):
        return self.contact_type + '-' + self.user.username

    class Meta:
        verbose_name_plural = "Contacts"
        ordering = ["user"]


class Social(models.Model):
    TYPES = (
        ('FB', 'Facebook'),
        ('TW', 'Twitter'),
        ('IN', 'Instagram'),
        ('SC', 'Snap Chat'),
        ('LI', 'Linked In'),
        ('GH', 'Github'),
    )

    social_type = models.CharField(max_length=10, choices=TYPES, verbose_name="Contact Type")
    user = models.ForeignKey(User, verbose_name="User",related_name='socials', on_delete=models.CASCADE)
    value = models.URLField()
    visibility = models.CharField(max_length=10, choices=VIS_TYPES, verbose_name="Social Visibility")

    def __str__(self):
        return self.social_type + '-' + self.user.username

    class Meta:
        verbose_name_plural = "Social Accounts"


class Skill(models.Model):
    users = models.ManyToManyField(User, related_name='skills', blank=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return '%s' % self.name


class Organisation(models.Model):
    TYPES = (
        ('UN', 'University'),
        ('CG', 'Campus Group'),
        ('C', 'Company'),
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6,blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,blank=True, null=True)
    latlong = models.CharField(max_length=30, blank=True, null=True)
    org_type = models.CharField(max_length=10, choices=TYPES, verbose_name="Organisation Type")
    name  = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='logos', blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return '%s' % self.name


class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    org = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='experiences')
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return '%s' % self.user.name + ' '+ self.org.name

    class Meta:
        ordering = ["user"]
