from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email',)



class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('profile_image', 'first_name', 'email',)
        exclude = ('password',)