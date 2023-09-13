from django import forms
from . models import Category, TableFile

class SidenavForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    category_name = forms.CharField(
    widget=forms.TextInput(
        attrs={
            "placeholder": "Category name",
            "class": "form-control"
        }
    ))

# class TableFileForm(forms.ModelForm):
#     class Meta:
#         model = TableFile
#         fields = '__all__'

#     category_name = forms.CharField(
#     widget=forms.TextInput(
#         attrs={
#             "placeholder": "Category name",
#             "class": "form-control"
#         }
#     ))

