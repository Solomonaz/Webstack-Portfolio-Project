from django import forms
from .models import Account

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))



class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password'
    }))
    role = forms.ChoiceField(choices=Account.ROLES, widget=forms.Select(attrs={
        'placeholder': 'Select Role',
        'class': 'form-control'
    }))
    profile_picture = forms.ImageField(required=False,widget=forms.FileInput(attrs={
        'class': 'form-control-file'}),
)
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password', 'role','profile_picture']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter first Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phone number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(
    widget=forms.TextInput(
        attrs={
            "placeholder": "First Name",
            "class": "form-control"
        }
    ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control"
            }
        ))
    phone_number = forms.CharField(
    widget=forms.TextInput(
        attrs={
            "placeholder": "First Name",
            "class": "form-control"
        }
    ))
    email = forms.CharField(
     widget=forms.TextInput(
        attrs={
            "placeholder": "First Name",
            "class": "form-control"
        }
    ))
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            "class": "form-control-file",
        })
    )
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'profile_picture']