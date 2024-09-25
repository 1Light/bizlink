from django import forms

from .models import Shop, Feature

INPUT_CLASSES = 'input-box form-control'

""" Form for Creating a Shop """
class CreateShop(forms.ModelForm):
    
    class Meta:
        model = Shop
        fields = ('name', 'description', 'address', 'contact', 'image')

        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'address': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'contact': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            })
        }

        labels = {
            'name': 'Name',
            'description': 'Description',
            'address': 'Address',
            'contact': 'Contact',
            'image': 'Image'
        }

class EditShop(CreateShop):
    pass

""" Form for Creating a Feature """
class CreateFeature(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ('name', 'image')
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }
        labels = {
            'name': 'Name',
            'image': 'Image'
        }