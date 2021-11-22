from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import fields
from system.forms import *
from django.forms import ModelForm

from system.models import Item, Sales

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

class SalesForm(ModelForm):
    class Meta:
        model = Sales
        fields = '__all__'

