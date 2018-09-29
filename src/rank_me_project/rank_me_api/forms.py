from django import forms
from uploads.core.models import Document

class PictureUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'photo', )
