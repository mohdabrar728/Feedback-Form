from django import forms
from .models import FormCreateModel, FormTokenModel


class FormCreateForm(forms.ModelForm):
    class Meta:
        model = FormCreateModel
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"})
        }


class FormChoiceMaker(forms.Form):
    question = forms.CharField(max_length=255)
    CHOICES = (
        ("1", "Text Box"),
        ("2", "Radio"),
        ("3", "Check Box"),
        ("4", "Boolean Field"),
        ("5", "Text Area"),
    )
    type = forms.ChoiceField(choices=CHOICES,widget=forms.Select(attrs={'onchange': "changetextbox();", 'id': "mfi_4_a_i"}))
    options = forms.CharField(max_length=255,widget=forms.TextInput(attrs={'disabled': 'true'}))


class EmailAdderForm(forms.Form):
    email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
