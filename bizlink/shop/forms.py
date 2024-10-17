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
                'class': INPUT_CLASSES,
                'placeholder': 'Enter shop name',
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Enter a brief description of your shop',
            }),
            'address': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Enter shop address',
            }),
            'contact': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
               'placeholder': 'Enter phone number',
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
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter product name',
                'class': INPUT_CLASSES,
            }),
            'description': forms.Textarea(attrs= {
                'placeholder': 'Add product description ...',
                'class': INPUT_CLASSES,
                'maxlength': '430',
            }),
            'specifications': forms.Textarea(attrs= {
                'placeholder': 'Add product specifications ...',
                'class': INPUT_CLASSES,
                'maxlength': '430',
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': 'Enter price',
                'class': INPUT_CLASSES,
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'placeholder': 'Enter quantity in stock',
                'class': INPUT_CLASSES,
            }),
            'tags': forms.TextInput(attrs={
                'placeholder': 'Add tags (comma-separated)',
                'class': INPUT_CLASSES,
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

        widgets = {
            'description': forms.Textarea(attrs={
                'placeholder': 'Add a brief description for the video',
                'class': INPUT_CLASSES,
            })
        }

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

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter category name',
                'class': INPUT_CLASSES,
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Add a description for the category',
                'class': INPUT_CLASSES,
                'maxlength': '230',
            })
        }

        labels = {
            'name': 'Name',
            'image': 'Image',
            'description': 'Description',
        }

class EditCategoryForm(CreateCategoryForm):
    pass
        
