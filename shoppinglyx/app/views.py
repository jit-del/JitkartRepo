from django.shortcuts import render,redirect
from .models import Product,Cart,Orderplaced,Customer
from django.views import View
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
# log in for function based view
from django.contrib.auth.decorators import login_required
# login for class based view
from django.utils.decorators import method_decorator







class ProductView(View):
    def get(self,request):
        topwears=Product.objects.filter(category='TW')
        bottomwears=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')
        return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,"mobiles":mobiles})




class ProductDetailView(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        item_already_in_cart=False
        if request.user.is_authenticated:
            item_already_in_cart=Cart.objects.filter(Q(product=product.id)& Q(user=request.user)).exists()

        return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart})



@login_required()
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    # print(product_id)
    return redirect('/cart')
@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_roduct=[ p for p in Cart.objects.all() if p.user == user]
        print(cart_roduct)
        if cart_roduct:
            for p in cart_roduct:
                tempamount=(p.quantity*p.product.discount_price)
                amount+=tempamount
                total_amount=amount+shipping_amount
    #             some work pending is here
    return render(request, 'app/addtocart.html',{'carts':cart,'totalamount':total_amount,'amount':amount})

def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        print(prod_id)
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[ p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount
            # totalamount = amount + shipping_amount

        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount + shipping_amount
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount
            # totalamount = amount + shipping_amount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)
@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.delete()
        amount=0.0
        shipping_amount=70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount


        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)










def buy_now(request):
 return render(request, 'app/buynow.html')

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',{'form':form,'active':'btn-primary'})
    def post(self,requst):
        form=CustomerProfileForm(requst.POST)
        if form.is_valid():
            usr=requst.user
            name=form.cleaned_data['name']
            zipcode=form.cleaned_data['zipcode']
            locality=form.cleaned_data['locality']
            state=form.cleaned_data['state']
            city=form.cleaned_data['city']
            reg=Customer(name=name,zipcode=zipcode,locality=locality,state=state,city=city,user=usr)
            reg.save()
            messages.success(requst,'Congratilation Profile Update Successfully')
        return render(requst, 'app/profile.html', {'form':form,'active': 'btn-primary'})




@login_required
def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def orders(request):
    op=Orderplaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})



def mobile(request ,data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')

    elif data == 'mi' or data == 'Samsung':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles=Product.objects.filter(category='M').filter(discount_price__lt=15000)
    elif data == 'above':
        mobiles=Product.objects.filter(category='M').filter(discount_price__gt=12000)
    elif data == 'Hightolow':
        mobiles=Product.objects.filter(category='M').order_by('-discount_price')
    elif data == 'lowtohigh':
        mobiles=Product.objects.filter(category='M').order_by('discount_price')

    return render(request, 'app/mobile.html',{'mobiles':mobiles})


def laptop(request , data=None):
    if data == None:
        laptops=Product.objects.filter(category='L')
    elif data == 'Hp' or data == 'Asus':
        laptops=Product.objects.filter(category='L').filter(brand=data)
    elif data == 'below':
        laptops=Product.objects.filter(category='L').filter(discount_price__lt=60000)
    elif data == 'above':
        laptops=Product.objects.filter(category='L').filter(discount_price__gt=60000)
    elif data == 'Hightolow':
        laptops=Product.objects.filter(category='L').order_by('-discount_price')
    elif data == 'lowtohigh':
        laptops=Product.objects.filter(category='L').order_by('discount_price')

    return render(request,'app/laptop.html',{'laptops':laptops})




class CustomerRegiistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()#blank form
        return render(request, 'app/customerregistration.html',{'form':form})
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,"Congratulation!! Registered Successflly")
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})
@login_required
def checkout(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount=0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount
        totalamount=amount+shipping_amount

    return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items})

@login_required
def payment_done(request):
    custid=request.GET.get('custid')
    user=request.user
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        Orderplaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")


def topwear(request,data=None):
    if data == None:
        topwears = Product.objects.filter(category='TW')
    elif data == 'Nike' or data== 'lee':
        topwears = Product.objects.filter(category='TW').filter(brand=data)
    elif data == 'above':
        topwears=Product.objects.filter(category='TW').filter(discount_price__gt=1200)
    elif data == 'below':
        topwears=Product.objects.filter(category='TW').filter(discount_price__lt=500)
    elif data == 'Hightolow':
        topwears=Product.objects.filter(category='TW').order_by('-discount_price')
    elif data == 'lowtohigh':
        topwears=Product.objects.filter(category='TW').order_by('discount_price')

    return render(request,'app/topware.html',{"topwears":topwears})


def bottomwear(request,data=None):
    if data == None:
        bottom = Product.objects.filter(category='BW')
    elif data == 'Nike' or data== 'lee':
        bottom = Product.objects.filter(category='BW').filter(brand=data)
    elif data == 'above':
        bottom=Product.objects.filter(category='BW').filter(discount_price__gt=1200)
    elif data == 'below':
        bottom=Product.objects.filter(category='BW').filter(discount_price__lt=500)
    elif data == 'Hightolow':
        bottom=Product.objects.filter(category='BW').order_by('-discount_price')
    elif data == 'lowtohigh':
        bottom=Product.objects.filter(category='BW').order_by('discount_price')

    return render(request,'app/bottom.html',{"topwears":bottom})

