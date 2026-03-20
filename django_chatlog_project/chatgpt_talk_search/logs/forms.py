from django import from .forms import 

class UploadForm(forms.Form):
    file = forms.FileField()