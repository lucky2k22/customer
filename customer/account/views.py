from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string


from django.shortcuts import render
from .models import *
from .forms import *

def dashboard(request):
    order = Order.objects.all()
    total_orders = order.count()
    orders_delivered = Order.objects.filter(status='Delivered').count()
    pending_delivered = Order.objects.filter(status='Pending').count()
    context = {'order': order, 'total_orders':total_orders, 'Pending_delivered': pending_delivered,
               'orders_delivered':orders_delivered}
    return render(request, 'dashboard.html', context)



def CreateOrder(request):
    form = Orderform()
    if request.method == 'POST':
        form = Orderform(request.POST)
        if form.is_valid():
            form.save ()
            template = render_to_string('email_template.html',{'name':request.user})
            email = EmailMessage(
                'Transactional Email',
                template,
                settings.Email_Host_user,
                [request.user.email],
            )
            email.fail_silently = False
            email.send()

    context = {'form':form}
    return render(request, 'order_form.html', context)




def updateOrder(request, id):
    action = 'update'
    product = Order.objects.get(id=id)
    form = Orderform(instance=product)
    if request.method == 'POST':
        form = Orderform(request.POST, instance=product)
        if form.is_valid():
            form.save ()
            return redirect('/')
    context = {'action':action, 'form':form, 'product':product}
    return render(request, 'order_form.html', context)   

def deleteOrder(request, id):
    product = Order.objects.get (id=id)
    form = Orderform (instance=product)
    if request.method == 'POST':
        form = Orderform (request.POST, instance=product)
        if form.is_valid ():
            form.save ()
            return redirect ('/')
    context = {'form':form}
    return render(request, 'order_form.html', context)



def registerPage(request):
    if request.user.is_authenticated:
        return  redirect('/')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid()():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'account was created for' + user)

                return redirect('/')

        context = {'form':form}
        return render(request, 'signup.html', context)


def login(request):
    return render(request,'login.html')

def loginProcess(request):
   username = request.POST.get("username")
   password = request.POST.get("password")
   # print(username)

   user = authenticate(request=request, username=username, password=password)
   if user is not None:
       login(request=request, user=user)
       messages.success(request, "Login! Successfull")
       return redirect("home")
   else:
       messages.error(request, "Error in login! Invalid login Details!")
       return redirect("login")

def logoutProcess(request):
    logout(request)
    messages.success(request, "Logout Successfully!")
    return redirect("Login")



