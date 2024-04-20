import jdatetime
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User
from django.core import validators
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="گذرواژه", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="تکرار گذرواژه", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['phone', 'email']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


def start_with_09(value):
    if value[0] != '0':
        raise forms.ValidationError("تلفن همراه باید با 09 اغاز شود")
    if value[1] != '9':
        raise forms.ValidationError("تلفن همراه باید با 09 اغاز شود")


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["phone", "email", "password", "is_active", "is_admin"]


class LoginForm(forms.Form):
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'register-form', 'placeholder': 'ایمیل یا تلفن همراه'}),
        validators=[validators.MinLengthValidator(11), validators.MaxLengthValidator(50)])

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'register-form', 'placeholder': 'گذرواژه'}),
                               validators=[validators.MinLengthValidator(5)])


class RegisterForm(forms.ModelForm):
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'register-form', 'placeholder': 'شماره تلفن همراه'}),
                            validators=[start_with_09, validators.MinLengthValidator(11),
                                        validators.MaxLengthValidator(11)])

    fullname = forms.CharField(widget=forms.TextInput(attrs={'class': 'register-form', 'placeholder': 'نام کامل'}),
                               validators=[validators.MaxLengthValidator(100)])

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'register-form', 'placeholder': 'ایمیل '}))

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'register-form', 'placeholder': 'گذرواژه'}), validators=[validators.MinLengthValidator(8),
                                                                                 validators.MaxLengthValidator(30)])
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'register-form', 'placeholder': 'تکرار ' 'گذرواژه'}))

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", ]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("گذرواژه ها با هم مطابقت ندارند")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ChecKOtpForm(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد چهار رقمی اعتبار سنجی'}),
        validators=[validators.MaxLengthValidator(4), validators.MinLengthValidator(4)])


class EditUserProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ('address', 'birthday', 'sex', 'image',)


class EditAdminProfile(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('password',)
        widgets = {
            'is_admin': forms.CheckboxInput(),
            'is_active': forms.CheckboxInput(),
        }


class AdminCreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('password', 'last_login', 'image')
        widgets = {
            'is_admin': forms.CheckboxInput(),
            'is_active': forms.CheckboxInput(),
        }