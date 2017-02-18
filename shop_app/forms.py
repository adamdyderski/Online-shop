from django import forms

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label='',initial=1)

class OrderbyForm(forms.Form):
   choices = (
       ('name', 'nazwa A-Z'), 
       ('-name', 'nazwa Z-A'),
       ('price', 'cena rosnąco'),
       ('-price', 'cena malejąco'),
   )
   orderby = forms.ChoiceField(label='Sortuj',choices=choices, widget=forms.Select(attrs={'onchange': 'this.form.submit();', 'data-toggle':'select','class':'select select-default'}))
