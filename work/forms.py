from django import forms
from work.models import User,Taskmodel

class Register(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","first_name","last_name","email","password"]


class Taskform(forms.ModelForm):
    class Meta:
        model=Taskmodel
        fields=["task_name","task_description"]
        widgets={
                'task_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter task'}),
                'task_description':forms.Textarea(attrs={'class':'form_control','column':80,"rows":5,'placeholder':'Enter description'})
                }
        

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()
    
