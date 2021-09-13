from django import forms
from .models import FormTokenModel


class FormCreateForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

class FormChoiceMaker(forms.Form):
    question = forms.CharField(max_length=255)
    CHOICES = (
        ("None","Select an Option"),
        ("1", "Text Box"),
        ("2", "Radio"),
        ("3", "Check Box"),
        ("4", "Boolean Field"),
        ("5", "Text Area"),
        ("6","Rating")
    )
    type = forms.ChoiceField(choices=CHOICES,
                             widget=forms.Select(attrs={'onchange': "changetextbox();", 'id': "mfi_4_a_i"}))
    options = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'disabled': 'true'}))


class EmailAdderForm(forms.Form):
    email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
