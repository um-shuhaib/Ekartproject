from EkartApp.models import Cart

def Cart_count(request):
    if request.user.is_authenticated:
        count=Cart.objects.filter(user=request.user,status="in-cart").count()
        return {"count":count}
    else:
        return {"count":0}