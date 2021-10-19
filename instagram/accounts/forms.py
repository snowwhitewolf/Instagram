from .auth_forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    user_name = forms.CharField(max_length=20)
    email = forms.EmailField()
    profile_image = ImageField

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name')

