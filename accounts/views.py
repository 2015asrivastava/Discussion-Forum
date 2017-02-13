from django.contrib.auth import authenticate,logout,login,get_user_model
from django.shortcuts import render,redirect
from .forms import UserLoginForm,UserRegisterForm
from django.contrib import messages
def login_view(requset):
    title="Login"
    form = UserLoginForm(requset.POST or None)
    if requset.method=="POST":

        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=authenticate(username=username,password=password)
            login(requset,user)
            return redirect("/")

    context={
        "form":form,
        "title":title
    }
    return render(requset,"login.html",context)

def register_view(requset):
    title="Register"
    RegisterForm=UserRegisterForm(requset.POST or None)
    if RegisterForm.is_valid():
        user=RegisterForm.save(commit=False)
        password=RegisterForm.cleaned_data.get("password")
        user.set_password(password)
        user.save()
        new_user=authenticate(username=user.username,password=password)
        messages.success(requset,"Yay! Successfully Registered")
        login(requset,new_user)
        return redirect("/")
    context = {
        "form": RegisterForm,
        "title": title
    }
    return render(requset, "login.html", context)
def logout_view(requset):
    logout(requset)
    return redirect("/")