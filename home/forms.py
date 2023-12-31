from django import forms
from . models import Category, TableFile, File
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


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

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = '__all__'

    file_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "File name",
                "class": "form-control"
            }
        ))
    uploaded_by = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Uploaded By",
                "class": "form-control"
            }
        ))

    class Meta:
        model = File
        fields = ['file_name', 'uploaded_by', 'file']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.file_size = instance.file.size
        if commit:
            instance.save()
        return instance


class TableFileForm(forms.ModelForm):
    class Meta:
        model = TableFile
        fields = '__all__'

    accusor_name = forms.CharField(
    widget=forms.TextInput(
        attrs={
            "placeholder": "ከሳሽ መልስ ሰጭ",
            "class": "form-control"
        }
    ))
    defendent_name = forms.CharField(
    widget=forms.TextInput(
        attrs={
            "placeholder": "ተከሳሽ መልስ  ሰጭ",
            "class": "form-control"
        }
    ))
    house_number = forms.CharField(
    widget=forms.TextInput(
        attrs={
            "placeholder": "የቤት ቁጥር",
            "class": "form-control"
        }
    ))
    id_number = forms.CharField(
    widget=forms.TextInput(
        attrs={
            "placeholder": "የመ.ቁ ",
            "class": "form-control"
        }
    ))
    court_house = forms.CharField(
    widget=forms.TextInput(
        attrs={
            "placeholder": "ጉዳዩ ያለበት ፍ/ቤት",
            "class": "form-control"
        }
    ))
    debate_type = forms.CharField(
    widget=forms.TextInput(
        attrs={
            "placeholder": "የጉዳዩ አይነት",
            "class": "form-control"
        }
    ))
    date_archive_initiated = forms.DateField(
    widget=forms.DateInput(
        attrs={
            "placeholder": "መዝገቡ የመጣበት ቀን",
            "class": "form-control"
        }
    ))
    date_court_decision_made = forms.DateField(
    widget=forms.DateInput(
        attrs={
            "placeholder": "ፍርድ ቤቱ ውሳኔ የሰጠበት ቀን",
            "class": "form-control"
        }
    ))
    date_court_decision_copy_sent = forms.DateTimeField(
    widget=forms.DateInput(
        attrs={
            "placeholder": "የውሳኔ ግልባጭ የተላከበት ቀን",
            "class": "form-control"
        }
    ))
    prosecutor = forms.CharField(
    widget=forms.TextInput(
        attrs={
            "placeholder": "ጉዳዩን የያዘው ዐቃቤ ህግ ስም",
            "class": "form-control"
        }
    ))
    status = forms.CharField(
    widget=forms.TextInput(
        attrs={
            "placeholder": "በፍ/ቤቱ ውሳኔ መሰረት ተፈፅሞል/አልተፈፀመም",
            "class": "form-control"
        }
    ))
