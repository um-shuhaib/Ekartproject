from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView,ListView
from EkartApp.models import Product,Cart,Order
from EkartApp.forms import UserRegisterForm,LoginForm,CartForm,OrderPlacedForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.utils.decorators import method_decorator 
from EkartApp.authentication import login_required
from django.core.mail import send_mail,settings


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
        cart_instance=Cart.objects.filter(user=user,product=product,status="in-cart")  #[]
        if cart_instance:
            cart_instance[0].quantity+=int(quantity)
            cart_instance[0].save()
            messages.success(request,"added to cart")
            return redirect("home_view")
        else:
            Cart.objects.create(product=product,user=user,quantity=quantity)
            return redirect("home_view")

    
class CartListView(View):
    def get(self,request):
        user=request.user
        cart_list=Cart.objects.filter(user=user,status="in-cart")
        return render(request,"cart.html",{"cart_list":cart_list})

class Order_placed_View(View):
    def get(self,request,**kwargs):
        cart_item=Cart.objects.get(id=kwargs.get("id"))
        form=OrderPlacedForm()
        return render(request,"order_placed.html",{"form":form,"cart":cart_item})
    def post(self,request,**kwargs):
        user=request.user
        cart_instance=Cart.objects.get(id=kwargs.get("id"))
        address=request.POST.get("address")
        Order.objects.create(user=user,cart=cart_instance,address=address)
        messages.success(request,"Order Placed succesfully")
        cart_instance.status="order-placed"
        cart_instance.save()

        sub="Order Placed"
        msg="Confirmation for your purchase ! Order placed from your EKartApp"
        mail_from=settings.EMAIL_HOST_USER
        email_to=user.email
        res=send_mail(sub,msg,mail_from,[email_to])
        if res:
            messages.success(request,"Email send successful")
        else:
            messages.warning(request,"Email send Not successful")
        return redirect("home_view")





class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect("login")