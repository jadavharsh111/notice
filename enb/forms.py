
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms import *
class DashForm(Form):
    topic = CharField(
        label='Title',
        widget=forms.TextInput(attrs={'size':64})
    )
    desc = CharField(
        label='Desc',
        widget=Textarea(attrs={'cols': 50, 'rows': 10})
    )
    tags = CharField(
        label='Tags',
        required=False,
        widget= TextInput(attrs= {'size': 64})
    )

    img = ImageField(
        label='Image',
        required=False
    )

    file = FileField(
        label='File',
        required=False
    )

class RegistrationForm(Form):
    username = CharField(label='Username', max_length=30 )
    email = EmailField(label='Email')
    password1 = CharField(
        label='Password',
        widget= PasswordInput()
    )
    password2 = CharField(
        label='Password(Again)',
        widget= PasswordInput()
    )

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise ValidationError('Password do not match!')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise ValidationError('User can only contain alphanumeric characters and underscore')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise ValidationError('Username is already taken')
