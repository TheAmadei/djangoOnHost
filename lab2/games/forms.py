from .models import Game_list
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea, Select, CheckboxInput, NumberInput
from django import forms
from django.contrib.auth.models import User

class GamesForm(ModelForm):
    class Meta:
        model = Game_list
        fields = ['title', 'anounce', 'discription', 'date', 'user', 'Ganre', 'GanreTwo', 'price']

        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название игры' 
            }),
            "anounce": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Анонс игры'
            }),
            "date": DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата публикации'
            }),
            "discription": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание игры'
            }),
            "user": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Пользователь'
            }),
            "Ganre": CheckboxInput(attrs={
                'id': 'test',
                'class': '',
                'placeholder': 'ММО'
            }),
            "GanreTwo": CheckboxInput(attrs={
                'class': '',
                'placeholder': 'ММО'
            }),
            "price": NumberInput(attrs={
                'step': '0.25',
                'class': 'form-control',
                'placeholder': 'Цена'
            })
        }

class PurchaseForm(forms.Form):
    amount = forms.DecimalField(label='Сумма покупки', min_value=0.01, required=False, widget=forms.HiddenInput())