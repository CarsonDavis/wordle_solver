from django import forms
from django.db import models


class GameForm(forms.Form):
    class Results(models.TextChoices):
        WRONG = 'wrong'
        RIGHT = 'right'
        POSITION = 'position'

    first = forms.CharField(label='First', max_length=1)
    first_results = forms.ChoiceField(choices=Results.choices)

    second = forms.CharField(label='Second', max_length=1)
    second_results = forms.ChoiceField(choices=Results.choices)

    third = forms.CharField(label='Third', max_length=1)
    third_results = forms.ChoiceField(choices=Results.choices)

    fourth = forms.CharField(label='Fourth', max_length=1)
    fourth_results = forms.ChoiceField(choices=Results.choices)

    fifth = forms.CharField(label='Fifth', max_length=1)
    fifth_results = forms.ChoiceField(choices=Results.choices)
