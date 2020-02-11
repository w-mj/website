from django import forms


class photoForm(forms.Form):
    image = forms.ImageField(required=False)