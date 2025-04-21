from django import forms
from .models import Boletin
from tinymce.widgets import TinyMCE

class BoletinForm(forms.ModelForm):
    contenido = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Boletin
        fields = ['titulo', 'contenido']
