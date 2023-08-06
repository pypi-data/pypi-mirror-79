# coding: utf-8

from django import forms
CHOICES = (
    (1, "title1"),
    (2, "title2"),
    (3, "title3"),
    (4, "title4"),
)
print('_dingding _dingding plugin')
class DingDingOptionsForm(forms.Form):
    access_token = forms.CharField(
        max_length=255,
        help_text='DingTalk robot access_token',
    )
    select = forms.TypedChoiceField(
        label='携带字段',
        coerce=lambda x: x == '1',
        choices=CHOICES,
        widget=forms.CheckboxSelectMultiple()
    )
