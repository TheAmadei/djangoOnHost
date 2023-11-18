from games.models import CustomUser
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError

class PurchaseForm(forms.Form):
    game_id = forms.IntegerField(widget=forms.HiddenInput())

class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
