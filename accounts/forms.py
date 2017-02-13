from django import forms
from django.contrib.auth import authenticate,get_user_model



User=get_user_model()
class UserLoginForm(forms.Form):
    username=forms.CharField(label="User Name")
    password=forms.CharField(widget=forms.PasswordInput)

    def clean(self,*args,**kwargs):
        username=self.cleaned_data.get("username")
        password=self.cleaned_data.get("password")
        if username and password:
            user=authenticate(username=username,password=password)
            if not user:
             raise forms.ValidationError("User does not exist")
            if not user.is_active:
             raise forms.ValidationError("User is not active")

class UserRegisterForm(forms.ModelForm):
    email=forms.EmailField()
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Password",widget=forms.PasswordInput)
    username=forms.CharField(label="User Name")
    first_name=forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    class Meta:
        model=User
        fields=[
            "username",
            "first_name",
            "last_name",
            "password",
            "password2",
            "email"
        ]

    def clean_password2(self):
        password=self.cleaned_data.get("password")
        password2= self.cleaned_data.get("password2")

        if password!=password2:
            raise forms.ValidationError("Password does not match")
        return password;

    # def save(self, commit=True):
    #     user = super(UserRegisterForm, self).save(commit=False)
    #     user.first_name = self.cleaned_data["firstname"]
    #     user.last_name = self.cleaned_data["lastname"]
    #     if commit:
    #         user.save()
    #     return user

