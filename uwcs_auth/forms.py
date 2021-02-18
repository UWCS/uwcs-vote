from django import forms
from django.contrib.auth.models import User

from uwcs_auth.models import WarwickVoteUser


class ProfileForm(forms.ModelForm):
    class Meta:
        model = WarwickVoteUser
        fields = ['nickname']


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class DeleteUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DeleteUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ['email']


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    uni_id = forms.CharField(max_length=11)
    nickname = forms.CharField(max_length=50, required=False)

    def signup(self, request, user):
        pass
