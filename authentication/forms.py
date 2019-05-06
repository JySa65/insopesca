from django import forms
from authentication.models import User, SecurityQuestion
from core.models import Account

class UserCreateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'ci', 'name', 'last_name', 'is_superuser',
                  'is_active', 'is_staff', 'role', 'level',)  # '__all__'

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        for key, field in self.fields.items():
            if (key == 'email' or key == 'ci'):
                field.widget.attrs.update(
                    {'data_type': 'user'})

    def clean_ci(self):
        document = self.cleaned_data['ci']
        account = Account.objects.filter(document=document).exists()
        if account:
            raise forms.ValidationError(
                'Usuario Ya Existe')
        return document

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'ci', 'name', 'last_name', 'role', 'level',
                  'is_active', 'is_staff', 'is_superuser', 'password')  # '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update(
            {'hidden': 'hidden'})
        
        self.fields['email'].widget.attrs.update(
            {'readonly': 'readonly'})
    
    def clean_ci(self):
        document = self.cleaned_data['ci']
        account = Account.objects.filter(document=document).exists()
        if account:
            raise forms.ValidationError(
                'Usuario Ya Existe')
        return document


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


class ForgotPasswordForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'form-control', 'autocomplete': 'off',
                    'placeholder': "Correo Electronico"})
