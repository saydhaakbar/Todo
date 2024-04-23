from django.shortcuts import render,redirect
from django.views.generic import View
from work.forms import Register,LoginForm,Taskform
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from work.models import Taskmodel
from django.contrib import messages
from django.utils.decorators import method_decorator
# Create your views here.


def signin_required(fn):
    def wrapper(request,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,**kwargs)
    return wrapper

def mylogin(fn):
    def wrapper(request,**kwargs):
        id=kwargs.get("pk")
        obj=Taskmodel.objects.get(id=id)
        if obj.user!=request.user:
            return redirect("signin")
        else:
            return fn(request,**kwargs)
    return wrapper

class Registration(View):
    def get(self,request,**kwargs):
        form=Register()
        return render(request,"register.html",{"form":form})
    
    def post(self,request,**kwargs):
        form=Register(request.POST)
        if form.is_valid():

            User.objects.create_user(**form.cleaned_data)
            form=Register()
            return render(request,"register.html",{"form":form})
class Signin(View):

    def get(self,request,**kwargs):

        form=LoginForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,**kwargs):

        form=LoginForm(request.POST)

        if form.is_valid():

            print(form.cleaned_data)

            u_name=form.cleaned_data.get("username")

            pwd=form.cleaned_data.get("password")

            user_obj=authenticate(username=u_name,password=pwd)

            if user_obj:
                print("valid credentials")
                login(request,user_obj)
                return redirect("index")
            else:
                form=LoginForm()
                return render(request,"login.html",{"form":form})
@method_decorator(signin_required,name="dispatch")             
class Add_Task(View):
    def get(self,request,**kwargs):
        form=Taskform()
        data=Taskmodel.objects.filter(user=request.user).order_by('completed')
        return render(request,"index.html",{"form":form,"data":data})
    
    def post(self,request,**kwargs):

        form=Taskform(request.POST)
        
        if form.is_valid():

            form.instance.user=request.user

            form.save()
            messages.success(request,"Task added successfully")
        form=Taskform()
        data=Taskmodel.objects.filter(user=request.user).order_by('completed')
        return render(request,"index.html",{"form":form,"data":data})
    
    # delete task
@method_decorator(signin_required,name="dispatch") 
@method_decorator(mylogin,name="dispatch") 
class Delete_task(View):

    def get(self,request,**kwargs):
        id=kwargs.get("pk")
        Taskmodel.objects.get(id=id).delete()
        return redirect("index")
# update

class Taskedit(View):
    def get(self,request,**kwargs):
        id=kwargs.get("pk")
        obj=Taskmodel.objects.get(id=id)

        if obj.completed==False:
            obj.completed=True
            obj.save()
        return redirect("index")
# logout

class Signout(View):
    def get(self,request):
        logout(request)
        return redirect('signin')
    
class User_del(View):
    def get(self,request,**kwargs):
        id=kwargs.get("pk")
        User.objects.get(id=id).delete()
        return redirect("signin")

class Update_user(View):
    def get(self,request,**kwargs):
        id=kwargs.get("pk")
        data=User.objects.get(id=id)
        form=Register(instance=data)
        return render(request,"register.html",{"form":form})
    def post(self,request,**kwargs):
        id=kwargs.get("pk")
        data=User.objects.get(id=id)
        form=Register(request.POST,instance=data)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return redirect("signin")
