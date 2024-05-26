from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import CustomUser
from pages.models import Person
from django.core.mail import send_mail
from django.conf import settings




class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': 'Email Address'})
        self.fields['full_name'].widget.attrs.update({'placeholder': 'Full Name'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})
       
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email  # Set the username to be the same as the email
        if commit:

            print(user.email)
            print(user.password)
            subject = 'Test Email from Django'
            message = 'willcome ' + user.full_name + " your account has benn created secssfly you can login now using  your "
            recipient_list = [user.email]



            user1 =  Person.objects.create(name = user.full_name , email= user.email ,password = self.cleaned_data.get('password1'))
       
            user.save()
            user1.save
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
                context = {'message': 'Email sent successfully!'}
            except Exception as e:
                context = {'message': f'Failed to send email: {str(e)}'}
    
            

            
        return user




class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Invalid email or password')
        return self.cleaned_data
