from django.forms import ModelForm
from base.models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        