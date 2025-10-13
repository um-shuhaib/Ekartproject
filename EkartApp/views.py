from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView,ListView
from EkartApp.models import Category,Product

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
    
