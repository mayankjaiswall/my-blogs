from django import forms

from blogs.models import Category, Blog


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name',)
        widgets = {
            'category_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name',
            }),
        }


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = (
            'title',
            'category',
            'featured_image',
            'short_description',
            'blog_body',
            'status',
            'is_featured',
        )
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'featured_image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter a short description',
            }),
            'blog_body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Write your post content here',
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
