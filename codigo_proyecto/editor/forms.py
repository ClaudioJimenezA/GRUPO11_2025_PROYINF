from django import forms
from .models import Boletin



class BoletinForm(forms.ModelForm):
    class Meta:
        model = Boletin
        fields = ['titulo', 'contenido']
        widgets = {
           'contenido': forms.Textarea(attrs={'id': 'id_contenido'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contenido'].required = False
