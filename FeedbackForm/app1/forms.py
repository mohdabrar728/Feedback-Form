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
    type = forms.ChoiceField(choices=CHOICES)
    options = forms.CharField(max_length=255)


class EmailAdderForm(forms.Form):
    email = forms.EmailField(max_length=100)


class DropdownForm(forms.Form):
    data = FormTokenModel.objects.all()
    lister = []
    for i in data:
        lister.append((i.form_name, i.form_name))
    select_form = forms.CharField(widget=forms.Select(choices=lister))
