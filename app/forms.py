from django import forms
from app.models import UserImages


class Imageform(forms.ModelForm):
    class Meta:
        model = UserImages
        fields = "__all__"
        
        # forms.py


class CertificateForm(forms.Form):
    ACTIVITY_CHOICES = (
        ('essay', 'Essay'),
        ('drawing', 'Drawing'),
        ('fancy_dress', 'Fancy Dress'),
    )

    activity = forms.MultipleChoiceField(
        choices=ACTIVITY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,  # Allows for no activities to be selected
    )
