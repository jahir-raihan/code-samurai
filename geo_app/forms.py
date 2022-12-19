from django import forms
from .models import UploadDetails


class UploadDetailsForm(forms.ModelForm):

    """This form is for uploading details file """

    class Meta:
        model = UploadDetails
        fields = ['file']