# coding: utf-8
"""
sentry_opsgenie.forms
"""
from django import forms


class OpsGenieConfigForm(forms.Form):
    api_key = forms.CharField(
        max_length=255,
        help_text='OpsGenie API key used for authenticating API requests',
        required=True
    )

    recipients = forms.CharField(
        max_length=255,
        help_text='The user names of individual users or groups (comma seperated)',
        required=True
    )

    alert_url = forms.CharField(
        max_length=255,
        label='OpsGenie Alert URL',
        widget=forms.TextInput(attrs={'class': 'span6', 'placeholder': 'e.g. "https://api.opsgenie.com/v1/json/alert"'}),
        help_text='It must be visible to the Sentry server',
        required=True
    )
