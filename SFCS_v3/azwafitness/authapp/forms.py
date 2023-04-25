from django import forms
from .models import Bot

class BotForm(forms.ModelForm):
    GOAL_CHOICES = [
        ('lose_weight', 'Lose weight'),
        ('gain_muscle_mass', 'Gain muscle mass'),
        ('get_shredded', 'Get shredded'),
    ]

    BODY_CHOICES = [
        ('ectomorph', 'Ectomorph'),
        ('mesomorph', 'Mesomorph'),
        ('endomorph', 'Endomorph'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    goal = forms.ChoiceField(choices=GOAL_CHOICES)
    body_type = forms.ChoiceField(choices=BODY_CHOICES)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    height = forms.IntegerField()
    weight = forms.IntegerField()
    birthday = forms.DateField()

    class Meta:
        model = Bot
        fields = '__all__'