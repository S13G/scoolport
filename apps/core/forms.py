import string

from django import forms
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from apps.core.emails import send_account_email
from apps.core.models import StudentProfile

User = get_user_model()


class CustomUserCreationForm(forms.ModelForm):
    raw_password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'is_staff', 'raw_password')

    def save(self, commit=True):
        user = super().save(commit=False)

        if user.pk:  # Only for new objects
            # Generate a random password if none is provided
            raw_password = self.cleaned_data.get('raw_password')
            if not raw_password:
                characters = string.ascii_letters + string.digits + string.punctuation
                raw_password = get_random_string(length=12, allowed_chars=characters)
                user.set_password(raw_password)
            else:
                user.set_password(raw_password)

            # Send email with account details asynchronously
            send_account_email(
                recipient=user.email,
                full_name=user.get_full_name(),
                password=raw_password,
                template="account_details.html"
            )
            StudentProfile.objects.create(user=user)

        return user


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'is_staff', 'raw_password')

    def save(self, commit=True):
        user = super().save(commit=False)
        raw_password = self.cleaned_data.get('raw_password')

        if raw_password and raw_password != user.raw_password:
            user.set_password(raw_password)

            # Send email with account details asynchronously
            send_account_email(
                recipient=user.email,
                full_name=user.get_full_name(),
                password=raw_password,
                template="account_details.html"
            )

        return user
