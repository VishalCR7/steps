# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='users', blank=True, null=True)
    dob = models.DateField(null=True, blank=True, verbose_name='Date Of Birth')
    gender = models.CharField(null=True, blank=True, max_length=1, choices=(('F', 'Female'), ('M', 'Male')), verbose_name="gender")
    aadhar_no = models.BigIntegerField(blank=True, null=True)
    nationality = models.CharField(blank=True, null=True, default='Indian')
