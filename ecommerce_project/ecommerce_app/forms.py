from account.models import Account
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['email','username','password1','password2']