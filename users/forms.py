from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import ugettext_lazy as _
from .models import QuestrUserProfile


class QuestrUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for fieldname in ['username']:
            self.fields[fieldname].help_text = None
            del self.fields['password']

            #changed label for form items
        self.fields['privacytoggle'].label = "Privacy"
        self.fields['biography'].label = "Your biography"

    class Meta:
        model = QuestrUserProfile
        fields = ['first_name','last_name','username','email','phone','biography','privacytoggle']
        exclude = ('username.help_text',)


class QuestrUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given data
    """
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.\.+-]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                      "./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "./+/-/_ characters.")})
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = QuestrUserProfile
        fields = ['first_name','last_name','username','email',]
        widget = {
            'first_name' : forms.TextInput(attrs = { 'placeholder': 'First Name'}),
            'last_name' : forms.TextInput(attrs = { 'placeholder': 'Last Name'}),
            'email' : forms.TextInput(attrs = { 'placeholder': 'Email Address: me@example.com'}),
            'username' : forms.TextInput(attrs = { 'placeholder': 'Username: Can contain .,+,- OR _'}),
            'password1' : forms.PasswordInput(attrs = { 'placeholder': 'Password'}),
            'password2' : forms.PasswordInput(attrs = { 'placeholder': 'Confirm Password'}),
        }

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            QuestrUserProfile._default_manager.get(username=username)
        except QuestrUserProfile.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(QuestrUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user