# -*- coding: utf-8 -*-
from django import forms

class UploadForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )
