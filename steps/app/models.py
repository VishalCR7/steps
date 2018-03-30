# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

VIS_TYPES = (
        ('Me', 'Only Me'),
        ('All', 'All'),
        ('INC', 'Incubator'),
        ('SU', 'Start ups'),
        ('SUT', 'Start Up Team'),
        ('INCT', 'Incubator Team'),
    )

STATUS_TYPES = (
        ('A', 'Approved'),
        ('P', 'In Progress'),
        ('R', 'Rejected'),
        ('S', 'Submitted'),
)

ACCESS_TYPES = (
        ('A', 'Admin'),
        ('M', 'Member'),
)

class Tag(models.Model):
    name = models.CharField(max_length=300)
    followers = models.ManyToManyField(User, related_name='tags', blank=True)

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


class Location(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latlong = models.CharField(max_length=30,blank=True, null=True)

class Organisation(models.Model):
    TYPES = (
        ('UN', 'University'),
        ('CG', 'Campus Group'),
        ('C', 'Company'),
    )
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
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



# models for Startup
class Startup(models.Model):
    user  = models.OneToOneField(User,related_name='startup', on_delete=models.CASCADE)
    name  = models.CharField(max_length=200)
    website = models.URLField(blank=True, null=True)
    short_description = models.CharField(max_length = 300)
    description = models.TextField(blank=True,null=True)
    request_designation = models.CharField(max_length=200)
    request_user = models.ForeignKey(User, related_name='startup_request', blank=True,null=True,on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, related_name='startups', blank=True)
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    email = models.EmailField(blank=False)
    status = models.CharField(max_length=10, choices=STATUS_TYPES, default='S')
    members = models.ManyToManyField(User, related_name='startup_members', through='StartupMember')
    is_incubated = models.BooleanField(default=False)


class StartupFile(models.Model):
    title = models.CharField(max_length=50)
    file_added = models.FileField(blank=False,upload_to='media/startups/docs')
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE )
    def __str__(self):
        return self.title


class StartupsImage(models.Model):
    title = models.CharField(max_length=50)
    file_added = models.ImageField(blank=False,upload_to='media/startups/imgs')
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE )
    def __str__(self):
        return self.title


class StartupMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)
    access_level = models.CharField(max_length=10, default='M', choices=ACCESS_TYPES)
    role = models.CharField(max_length=100)
    joining_date = models.DateTimeField(auto_now_add=True)


class StartupAchievement(models.Model):
    startup = models.ForeignKey(Startup, related_name='achievements', on_delete=models.CASCADE)
    value = models.TextField(blank=True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title + '-' + self.startup.name

    class Meta:
        verbose_name_plural = "Achievements - Startup"
        ordering = ["startup"]


class StartupContact(models.Model):
    TYPES = (
        ('Mob', 'Mobile No.'),
        ('Email', 'Email'),
    )
    contact_type = models.CharField(max_length=10, choices=TYPES, verbose_name="Contact Type")
    startup = models.ForeignKey(Startup, related_name='contacts', on_delete=models.CASCADE)
    value = models.TextField()
    visibility = models.CharField(max_length=10, default='All', choices=VIS_TYPES, verbose_name="Contact Visibility")

    def __str__(self):
        return self.contact_type + '-' + self.startup.name

    class Meta:
        verbose_name_plural = "Contacts - Startup"
        ordering = ["startup"]


class StartupSocial(models.Model):
    TYPES = (
        ('FB', 'Facebook'),
        ('TW', 'Twitter'),
        ('IN', 'Instagram'),
        ('SC', 'Snap Chat'),
        ('LI', 'Linked In'),
        ('GH', 'Github'),
    )

    social_type = models.CharField(max_length=10, choices=TYPES, verbose_name="Contact Type")
    startup = models.ForeignKey(Startup, related_name='socials', on_delete=models.CASCADE)
    value = models.URLField()
    visibility = models.CharField(max_length=10, default='All', choices=VIS_TYPES, verbose_name="Social Visibility")

    def __str__(self):
        return self.social_type + '-' + self.startup.name

    class Meta:
        verbose_name_plural = "Social Accounts - Startup"





# models for Incubator
class Incubator(models.Model):
    user  = models.OneToOneField(User,related_name='incubator', on_delete=models.CASCADE)
    name  = models.CharField(max_length=200)
    website = models.URLField(blank=True, null=True)
    short_description = models.CharField(max_length = 300)
    description = models.TextField(blank=True,null=True)
    request_designation = models.CharField(max_length=200)
    request_user = models.ForeignKey(User, related_name='incubator_request', blank=True,null=True,on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, related_name='incubators', blank=True)
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    space_info = models.CharField(max_length=30)
    email = models.EmailField(blank=False)
    status = models.CharField(max_length=10, choices=STATUS_TYPES, default='S')
    members = models.ManyToManyField(User, related_name='incubator_members', through='IncubatorMember')
    followers = models.ManyToManyField(User, related_name='incubator_follows')
    ratings = models.ManyToManyField(User, related_name='rated_incubators',through='IncubatorRating')
    incubated_startup = models.ManyToManyField(Startup, related_name = 'incubators', through='IncubatorStartup')


class IncubatorRating(models.Model):
    RATING_TYPES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    incubator = models.ForeignKey(Incubator, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_TYPES)


class IncubatorStartup(models.Model):

    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)
    incubator = models.ForeignKey(Incubator, on_delete=models.CASCADE)
    incubated_on = models.DateField(auto_now_add=True)
    incubated_upto = models.DateField(blank=True)
    is_incubated = models.BooleanField(default=True)


class IncubatorMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    incubator = models.ForeignKey(Incubator, on_delete=models.CASCADE)
    access_level = models.CharField(max_length=10, default='M', choices=ACCESS_TYPES)
    role = models.CharField(max_length=100)
    joining_date = models.DateTimeField(auto_now_add=True)


class IncubatorContact(models.Model):
    TYPES = (
        ('Mob', 'Mobile No.'),
        ('Email', 'Email'),
    )
    contact_type = models.CharField(max_length=10, choices=TYPES, verbose_name="Contact Type")
    incubator = models.ForeignKey(Incubator, related_name='contacts', on_delete=models.CASCADE)
    value = models.TextField()
    visibility = models.CharField(max_length=10, default='All', choices=VIS_TYPES, verbose_name="Contact Visibility")

    def __str__(self):
        return self.contact_type + '-' + self.incubator.name

    class Meta:
        verbose_name_plural = "Incubator Contacts"
        ordering = ["incubator"]


class IncubatorSocial(models.Model):
    TYPES = (
        ('FB', 'Facebook'),
        ('TW', 'Twitter'),
        ('IN', 'Instagram'),
        ('SC', 'Snap Chat'),
        ('LI', 'Linked In'),
        ('GH', 'Github'),
    )


    social_type = models.CharField(max_length=10, choices=TYPES, verbose_name="Contact Type")
    incubator = models.ForeignKey(Incubator, related_name='socials', on_delete=models.CASCADE)
    value = models.URLField()
    visibility = models.CharField(max_length=10, default='All', choices=VIS_TYPES, verbose_name="Social Visibility")

    def __str__(self):
        return self.social_type + '-' + self.incubator.name

    class Meta:
        verbose_name_plural = "Social Accounts - Incubator"


class IncubatorAchievement(models.Model):
    incubator = models.ForeignKey(Incubator, related_name='achievements', on_delete=models.CASCADE)
    value = models.TextField(blank=True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title + '-' + self.incubator.name

    class Meta:
        verbose_name_plural = "Achievements - Startup"
        ordering = ["incubator"]


class IncubatorFile(models.Model):
    title = models.CharField(max_length=50)
    file_added = models.FileField(blank=False,upload_to='media/incubators/docs')
    incubator = models.ForeignKey(Incubator, on_delete=models.CASCADE )
    def __str__(self):
        return self.title


class IncubatorImage(models.Model):
    title = models.CharField(max_length=50)
    file_added = models.ImageField(blank=False,upload_to='media/incubators/imgs')
    incubator = models.ForeignKey(Incubator, on_delete=models.CASCADE )
    def __str__(self):
        return self.title


class IncubatorPost(models.Model):
    POST_TYPES = (
        ('P', 'Post'),
        ('C', 'Competition'),
    )
    incubator = models.ForeignKey(Incubator, related_name='posts', on_delete=models.CASCADE)
    value = models.TextField(blank=True)
    title = models.CharField(max_length=255)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='postlikes')
    created_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True, upload_to='media/incubators/posts')
    post_type = models.CharField(max_length=10, choices=POST_TYPES, verbose_name="Contact Visibility")

    def __str__(self):
        return self.title + '-' + self.incubator.name

    class Meta:
        verbose_name_plural = "Posts - Incubator"
        ordering = ["incubator"]


class Comment(models.Model):
    POST_TYPES = (
        ('P', 'Post'),
        ('C', 'Competition'),
    )
    post = models.ForeignKey(IncubatorPost, on_delete=models.CASCADE)
    value = models.TextField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.value + '-' + self.added_by.username

    class Meta:
        verbose_name_plural = "Posts - Incubator"


# Models for CHAT
class Room(models.Model):
    room_name = models.CharField(max_length=20, unique=True)
    links = models.ManyToManyField(User, through='Link')
    def __str__(self):
        return self.room_name


class Link(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    def __str__(self):
        return "%s [%s]" % (self.room.room_name, self.user.username)

class Message(models.Model):
    links = models.ForeignKey(Link, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    deleted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)


class ConnectionRequest(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)
    incubator = models.ForeignKey(Incubator, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_TYPES, default='S')