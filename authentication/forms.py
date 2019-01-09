from django.forms import ModelForm
from authentication.models import User


class UserCreateForm(ModelForm):

    class Meta:
        model = User
        fields = ('email', 'ci', 'name', 'last_name', 'is_superuser',
                  'is_active', 'is_staff', 'role', 'level',)  # '__all__'



class UserUpdateForm(ModelForm):

    class Meta:
        model = User
        fields = ('email', 'ci', 'name', 'last_name', 'role', 'level',
                  'is_active', 'is_staff', 'is_superuser', 'password')  # '__all__'
