from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *



class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    first_name = forms.CharField(required=True, label="First Name")
    last_name = forms.CharField(required=True, label="Last Name")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email already used")
        return data



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['latitude', 'longitude']


class IncubatorForm(forms.ModelForm):
    class Meta:
        model = Incubator
        fields = ['name', 'website', 'short_description', 'description', 'tags',
         'space_info']


class IncubatorRequestForm(forms.ModelForm):
    class Meta:
        model = Incubator
        exclude = ['user', 'request_user', 'status', 'members', 'is_incubated',
         'location', 'followers', 'ratings', 'incubated_startup']


class IncubatorFileForm(forms.ModelForm):
    class Meta:
        model = IncubatorFile
        fields = ['title', 'file_added']


class IncubatorImageForm(forms.ModelForm):
    class Meta:
        model = IncubatorImage
        fields = ['title', 'file_added']


class IncubatorContactForm(forms.ModelForm):
    class Meta:
        model = IncubatorContact
        fields = ['contact_type', 'value', 'visibility']


class IncubatorSocialForm(forms.ModelForm):
    class Meta:
        model = IncubatorSocial
        fields = ['social_type', 'value', 'visibility']


class IncubatorAchievementForm(forms.ModelForm):
    class Meta:
        model = IncubatorAchievement
        fields = ['title', 'value']


#############################################


class StartupForm(forms.ModelForm):
    class Meta:
        model = Incubator
        fields = ['name', 'website', 'short_description', 'description', 'tags', 'email']


class StartupRequestForm(forms.ModelForm):
    class Meta:
        model = Startup
        exclude = ['user', 'request_user', 'status', 'members', 'is_incubated', 'location']


class StartupFileForm(forms.ModelForm):
    class Meta:
        model = StartupFile
        fields = ['title', 'file_added']

class StartupImageForm(forms.ModelForm):
    class Meta:
        model = StartupsImage
        fields = ['title', 'file_added']


class StartupContactForm(forms.ModelForm):
    class Meta:
        model = StartupContact
        fields = ['contact_type', 'value', 'visibility']


class StartupSocialForm(forms.ModelForm):
    class Meta:
        model = StartupSocial
        fields = ['social_type', 'value', 'visibility']


class StartupAchievementForm(forms.ModelForm):
    class Meta:
        model = StartupAchievement
        fields = ['title', 'value']


from dal import autocomplete


class IncubatorMemberForm(forms.ModelForm):
    class Meta:
        model =  IncubatorMember
        fields = ['user', 'access_level', 'role']
        widgets = {'user' :autocomplete.ModelSelect2(url='user-autocomplete') }


class StartupMemberForm(forms.ModelForm):
    class Meta:
        model = StartupMember
        fields = ['user', 'access_level', 'role']
        widgets = {'user' :autocomplete.ModelSelect2(url='user-autocomplete') }