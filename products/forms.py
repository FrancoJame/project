from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    new_category = forms.CharField(
        max_length=100, 
        required=False, 
        help_text="Type a new category name here if you want to create one, or choose from the list above.",
        widget=forms.TextInput(attrs={'placeholder': 'Enter new category name...'})
    )

    class Meta:
        model = Product
        fields = ['name', 'category', 'new_category', 'description', 'price', 'stock_quantity', 'image', 'is_active']

    def save(self, commit=True):
        new_category_name = self.cleaned_data.get('new_category')
        if new_category_name:
            # Create or get the category
            category, created = Category.objects.get_or_create(name=new_category_name)
            self.instance.category = category
        
        return super().save(commit=commit)
