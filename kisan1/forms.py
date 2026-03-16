from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from kisan1.models import (
    LaborBooking,
    PesticideInventory,
    PesticideProfile,
    TractorBooking,
)


mobile_validator = RegexValidator(
    regex=r'^[6-9][0-9]{9}$',
    message='Mobile number must be a valid 10-digit Indian mobile number.',
    code='invalid_mobile',
)


class PesticideForm(forms.ModelForm):
    class Meta:
        model = PesticideProfile
        fields = ['shop_name', 'license_id', 'since_years', 'products_sold']
        widgets = {
            'shop_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shop Name'}),
            'license_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'License ID'}),
            'since_years': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'products_sold': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Products separated by | (e.g., Urea|Seeds)'}
            ),
        }

    def clean_shop_name(self):
        value = (self.cleaned_data.get('shop_name') or '').strip()
        if len(value) < 3:
            raise forms.ValidationError('Shop name must be at least 3 characters long.')
        return value

    def clean_license_id(self):
        value = (self.cleaned_data.get('license_id') or '').strip()
        if len(value) < 4:
            raise forms.ValidationError('License ID must be at least 4 characters long.')
        return value


class ShopItemForm(forms.ModelForm):
    class Meta:
        model = PesticideInventory
        fields = ['item_name', 'category', 'price', 'stock_quantity']
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def clean_item_name(self):
        value = (self.cleaned_data.get('item_name') or '').strip()
        if len(value) < 2:
            raise forms.ValidationError('Item name must be at least 2 characters.')
        return value

    def clean_price(self):
        value = self.cleaned_data.get('price')
        if value is None or value <= 0:
            raise ValidationError('Price must be greater than 0.')
        return value

    def clean_stock_quantity(self):
        value = self.cleaned_data.get('stock_quantity')
        if value is None or value <= 0:
            raise ValidationError('Stock quantity must be greater than 0.')
        return value


class LaborBookingRequestForm(forms.ModelForm):
    class Meta:
        model = LaborBooking
        fields = ['booking_date', 'start_time', 'duration', 'location']


class TractorBookingRequestForm(forms.ModelForm):
    class Meta:
        model = TractorBooking
        fields = ['booking_date', 'start_time', 'duration_hours', 'location']


class ServiceSettingsForm(forms.Form):
    rate = forms.IntegerField(min_value=1)
    is_available = forms.BooleanField(required=False)
    service_status = forms.ChoiceField(choices=[('Active', 'Active'), ('Paused', 'Paused')])
