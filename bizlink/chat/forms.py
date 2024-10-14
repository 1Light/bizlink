from django import forms

from .models import *

INPUT_CLASSES = 'input-box form-control'

class ChatMessageCreateForm(forms.ModelForm):

    class Meta:
        model = GroupMessage
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs= {
                'Placeholder': 'Add message ...',
                'class': INPUT_CLASSES,
                'maxlength': '300',
                'autofocus': 'autofocus',
            })
        }