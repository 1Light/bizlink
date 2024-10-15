from django import forms

from .models import Shop, Feature, Product, MoreProductImage, MoreProductVideo, Category

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
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'image': forms.FileInput(attrs={'class': INPUT_CLASSES})
        }
        labels = {
            'name': 'Name',
            'image': 'Image'
        }

class EditFeature(CreateFeature):
    pass

class CreateProductForm(forms.ModelForm):

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        to_field_name='categoryId',  # Ensures the lookup happens by categoryId
        label="Category"
    )
    
    class Meta:
        model = Product
        fields = [
            'name', 'category', 'image', 'video',
            'description', 'specifications', 
            'price', 'stock_quantity', 'tags',
        ]

        widgets = {
            'description': forms.Textarea(attrs= {
                'Placeholder': 'Add description ...',
                'class': INPUT_CLASSES,
                'maxlength': '430',
            }),
            'specifications': forms.Textarea(attrs= {
                'Placeholder': 'Add specifications ...',
                'class': INPUT_CLASSES,
                'maxlength': '430',
            })
        }

        labels = {
            'name': 'Name',
            'category': 'Category',
            'video': 'Video',
            'price': 'Price',
            'tags': 'Tags',
            'image': 'Image',
            'stock_quantity': 'In Stock',
            'specifications': 'Specifications',
            'description': 'Description',
        }

class EditProductForm(CreateProductForm):
    pass
    
class MoreProductImageForm(forms.ModelForm):
    class Meta:
        model = MoreProductImage
        fields = ['image']

        labels = {
            'image': 'Image',
        }

class MoreProductVideoForm(forms.ModelForm):
    class Meta:
        model = MoreProductVideo
        fields = ['video', 'description']

        labels = {
            'video': 'Video',
            'description': 'Description'
        }

class CreateCategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = [
            'name', 'image', 'description'
        ]

        labels = {
            'name': 'Name',
            'image': 'Image',
            'description': 'Description',
        }
class EditCategoryForm(CreateCategoryForm):
    pass
        
