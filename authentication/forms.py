from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from authentication.models import User


class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'ci', 'name', 'last_name', 'is_superuser',
                  'is_active', 'is_staff', 'role', 'level',)  # '__all__'



class UserUpdateForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'ci', 'name', 'last_name', 'role', 'level',
                  'is_active', 'is_staff', 'is_superuser', 'password')  # '__all__'
