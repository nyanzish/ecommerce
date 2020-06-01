from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import Item, Farmer

PAYMENT_CHOICES = (
    ('Mobile money', 'Mobile money'),
    
)


#DataFlair #File_Upload
class Uploadform(forms.ModelForm):

    class Meta:
        model = Item
        fields = [
        'title',
        'price',
        'discount_price',
        'category',
        'slug',
        'description',
        'saler',
        'image'
        ,]
    def __init__(self, *args, **kwargs):
       super(Uploadform, self).__init__(*args, **kwargs)
       self.fields['saler'].widget.attrs['readonly'] = True


class Farmerform(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = [
        'firstname',
        'lastname',
        'email',
        'farmname',
        'farmlocation',
        'phone'
        ,]

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    shipping_city = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    shipping_village = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    customer_phone = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    customer_mobilemoneyphone = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    shipping_notes = forms.CharField(required=False,widget=forms.Textarea(attrs={
        'class': 'form-control'
    }))
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()