from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView,ListView
from EkartApp.models import Category,Product,Cart
from EkartApp.forms import UserRegisterForm,LoginForm,CartForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.utils.decorators import method_decorator 
from EkartApp.authentication import login_required


# Create your views here.
class HomeView(TemplateView):
    template_name="index.html"

    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context["item"]=Product.objects.all()
        return context
    

class ProductView(View):
    def get(self,request,**kwargs):
        item = Product.objects.get(id=kwargs.get("id"))
        return render(request,"details.html",{"item":item})
    
class RegisterView(View):
    def get(self,request):
        form = UserRegisterForm()
        return render(request,"reg.html",{"form":form})
    
    def post(self,request):
        form_instance = UserRegisterForm(request.POST)
        if form_instance.is_valid():
            User.objects.create_user(**form_instance.cleaned_data)
            messages.success(request,"User Registered Succesfully")
            return redirect("login")
        else:
            messages.error(request,"Registration Failed !")
            return redirect("register")

class LoginView(View):
    def get(self,request):
        form = LoginForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        res = authenticate(request,username=username,password=password)
        if res:
            login(request,res)
            messages.success(request,"Login Succesfull")
            return redirect("home_view")
        else:
            messages.error(request,"Invalid Credentials")
            return redirect("login")

@method_decorator(login_required,name="dispatch")
class AddToCartView(View):
    def get(self,request,*args,**kwargs):
        form=CartForm()
        return render(request,"add_to_cart.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        product=Product.objects.get(id=kwargs.get("id"))
        user=request.user
        quantity = request.POST.get("quantity")
        Cart.objects.create(product=product,user=user,quantity=quantity)
        return redirect("home_view")

    

class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect("login")