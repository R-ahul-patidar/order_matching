from django import forms
from .models import PendingOrder

class OrderForm(forms.ModelForm):
    class Meta:
        model = PendingOrder
        fields = ['buyer_qty', 'buyer_price','seller_price','seller_qty']


