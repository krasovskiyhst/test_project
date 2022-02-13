from django import forms
from datetime import datetime


class DateForm(forms.Form):
    date_from = forms.DateTimeField(label='date_from', initial=datetime.now(), required=False,
                                    widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    date_to = forms.DateTimeField(label='date_to', initial=datetime.now(), required=False,
                                  widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))


class IPForm(forms.Form):
    ip = forms.CharField(label='IP', required=False, max_length=200, widget=forms.TextInput())
