from django import forms
from authentication.models import User, SecurityQuestion


class UserCreateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'ci', 'name', 'last_name', 'is_superuser',
                  'is_active', 'is_staff', 'role', 'level',)  # '__all__'


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'ci', 'name', 'last_name', 'role', 'level',
                  'is_active', 'is_staff', 'is_superuser', 'password')  # '__all__'


class SecurityQuestionForm(forms.ModelForm):
    question_one = forms.CharField(max_length=1000, required=True)
    answer_one = forms.CharField(max_length=1000, required=True)
    question_two = forms.CharField(max_length=1000, required=True)
    answer_two = forms.CharField(max_length=1000, required=True)
    question_three = forms.CharField(max_length=1000, required=True)
    answer_three = forms.CharField(max_length=1000, required=True)

    class Meta:
        model = SecurityQuestion
        fields = ('question_one', 'answer_one', 'question_two',
                  'answer_two', 'question_three', 'answer_three',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'form-control', 'autocomplete': 'off'})
