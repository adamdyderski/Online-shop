from django import forms
from .models import ShippingMethod

class ShippingMethodForm(forms.Form):

    shippingmethod = forms.ModelChoiceField(label='Sposób wysyłki',initial=1, queryset = ShippingMethod.objects.all(), widget=forms.Select(attrs={'onchange': 'this.form.submit();', 'data-toggle':'select','class':'select select-default'}) )

    def __init__(self,request,*args,**kwargs):
        super (ShippingMethodForm,self).__init__(*args,**kwargs)
        self.fields['shippingmethod'].initial = request.session.get('shippingmethod', 1)
