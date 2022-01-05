from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from . models import Photo, Signup
from . forms import LoginForm, SignupForm, UpdateForm,ChangepasswordForm
from django.contrib.auth import logout as logouts
# Create your views here.
def welcome(request):
    return HttpResponse("welcome django")
def index(request):
    var5="lavanya"
    return render(request,'index.html',{'var5':var5})
def signup(request):
    if request.method=='POST':
        f=SignupForm(request.POST or None,request.FILES or None)
        if f.is_valid():
            name=f.cleaned_data['Name']
            age=f.cleaned_data['Age']
            place=f.cleaned_data['Place']
            photo=f.cleaned_data['Photo']
            email=f.cleaned_data['Email']
            password=f.cleaned_data['Password']
            cpassword=f.cleaned_data['Confirmpassword']
            user=Signup.objects.filter(Email=email).exists()
            if user:
                messages.warning(request,"user already exists")
                return redirect('/signup')
            elif password!=cpassword:
                messages.warning(request,"password does not matches")
                return redirect('/signup')
            else:
                tab=Signup(Name=name,Age=age,Place=place,Photo=photo,Email=email,Password=password)
                tab.save()
                messages.success(request,"account created successfully")
                return redirect('/')

    else:
        f=SignupForm()
    return render(request,'signup.html',{'form':f}) 
def login(request):
    if request.method=='POST':
        f=LoginForm(request.POST)
        if f.is_valid():
            email=f.cleaned_data['Email']
            password=f.cleaned_data['Password']
            user=Signup.objects.get(Email=email)
            if not user:
                messages.warning(request,"user does not exists")
                return redirect('/login')
            elif user.Password!=password:
                messages.warning(request,"Password does not exists")
                return redirect('/login')
            else:
                messages.success(request,"login successfull")
                return redirect('/home/%s' % user.id)
    else:
        f=LoginForm()
    return render(request,'login.html',{'form':f})
def home(request,id):
    user=Signup.objects.get(id=id)
    return render(request,'home.html',{'user':user})
def update(request,id):
    user=Signup.objects.get(id=id)
    if request.method=='POST':
       f=UpdateForm(request.POST or None,request.FILES or None,instance=user)
       if f.is_valid():
            name=f.cleaned_data['Name']
            age=f.cleaned_data['Age']
            place=f.cleaned_data['Place']
            photo=f.cleaned_data['Photo']
            email=f.cleaned_data['Email']
            f.save()
            return redirect('/home/%s' % user.id)
    else:
        f=UpdateForm(instance=user)
    return render(request,'update.html',{'user':user,'form':f})
def changepassword(request,id):
    user=Signup.objects.get(id=id)
    if request.method=='POST':
         f=ChangepasswordForm(request.POST or None,request.FILES or None) 
         if f.is_valid():
           opassword=f.cleaned_data['Oldpassword']
           npassword=f.cleaned_data['Newpassword']
           ncpassword=f.cleaned_data['Newconfirmpassword']
           if user.Password!=opassword:
               messages.warning(request,"incorrect password")
               return redirect('/changepassword/%s' % user.id)
           elif npassword!=ncpassword:
               messages.warning(request,"password mismatch")
               return redirect('/changepassword/%s' % user.id)
           else:
               user.Password=npassword
               user.save()
               messages.success(request,"password changed successfully")
               return redirect('/home/%s' % user.id)
    else:
        f=ChangepasswordForm()
    return render(request,'changepassword.html',{'user':user,'form':f})
def logout(request):
    logouts(request)
    messages.success(request,"logout successfully")
    return redirect('/')
def gallery(request):
    photos=Photo.objects.all()
    return render(request,'gallery.html',{'photos':photos})
def viewphoto(request,pk):
    photo=Photo.objects.get(id=pk)
    return render(request,'photo.html',{'photo':photo})

        
               
             
        
            
      
        
    
        
        
        
                

        
