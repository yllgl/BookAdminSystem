from crispy_forms.helper import FormHelper
from django import forms

from account.models import Book, User, Record
from account.utils.encrypt import md5


class BookModelForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = []
class UserEditModelForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ["password"]
class RecordModelForm(forms.ModelForm):
    class Meta:
        model = Record
        exclude = []
class NewUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.update({"auto_id": "new-id-%s"})
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'formNew'
        self.helper.form_method = 'post'
    class Meta:
        model = User
        exclude = []
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)
class UserPasswordForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    def __init__(self, *args, **kwargs):
        kwargs.update({"auto_id":"password-id-%s"})
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'formPassword'
        self.helper.form_method = 'post'
    class Meta:
        model=User
        fields=['password']
    def clean(self):
        cleaned_data = super(UserPasswordForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("confirm_password")
        return md5(pwd)