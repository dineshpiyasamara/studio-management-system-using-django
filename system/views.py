from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView

from system.forms import *
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib import messages


def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    title = ''
    if request.user.is_authenticated:
        title = "Welcome {}".format(request.user)

    return render(request, 'home.html',{
        'title':title,
    })




@login_required(login_url='login')
def purchase(request):
    title = "Purchase Items"

    if request.method == 'POST':
        prod = request.POST.get('product_code',"error")
        cat = request.POST.get('category')
        col = request.POST.get('color')
        des = request.POST.get('description')
        purch = request.POST.get('purchase_price')
        sell = request.POST.get('selling_price')

        item_obj = Item(product_code = prod, category = cat, color = col, description = des, purchase_price = purch)
        item_obj.save()

        items = Item.objects.all()
        for item in items:
            if item.product_code == prod:
                sell_obj = SellingPrice(item = item, selling_price = sell)
                sell_obj.save()      
        return redirect('inventory')

    else:
        return render(request, 'purchase.html', {
            'title':title,
        })



@login_required(login_url='login')
def sell(request):
    title = "Sell Items"
    if request.method=="POST":
        return render(request, 'sell.html', {
            'title':title,
        })
    else:
        itemObjectList = Item.objects.all().order_by('product_code')


        return render(request, 'sell.html', {
            'title':title,
           'itemObjectList':itemObjectList,
        })

def json_item_data(request):
    val = list(Item.objects.values())
    return JsonResponse({
        'data':val,
    })

def json_item_data_others(request, *args, **kwargs):
    selectedProduct = kwargs.get('product')
    obj_data = list(Item.objects.filter(product_code=selectedProduct).values())
    obj_price = SellingPrice.objects.raw("SELECT id,selling_price FROM system_sellingprice Where item_id='"+selectedProduct+"' ORDER BY id DESC LIMIT 1")

    return JsonResponse({
        'data':obj_data,
        'price':obj_price[0].selling_price,
    })



@login_required(login_url='login')
def items(request):
    title = "Inventory"
    item_table = Item.objects.all()
    selling_price_table = SellingPrice.objects.all()

    datalist = []
    for item in item_table:
        data = []
        data.append(item.product_code)
        data.append(item.category)
        data.append(item.color)
        data.append(item.description)
        data.append(item.purchase_price)

        price = ''
        for sell in selling_price_table:
            if item.product_code == sell.item.product_code:
                price = sell.selling_price
        data.append(price)

        purchases_tot = Purchases.objects.filter(product_code=item.product_code).aggregate(Sum('qty'))
        sales_tot = Sales.objects.filter(product_code=item.product_code).aggregate(Sum('qty'))

        if purchases_tot['qty__sum']==None:
            purchases_tot['qty__sum'] = 0
        if sales_tot['qty__sum']==None:
            sales_tot['qty__sum'] = 0

        data.append(purchases_tot['qty__sum'] - sales_tot['qty__sum'])

        datalist.append(data)

    return render(request, 'inventory.html', {
        'title': title,
        'item_table': datalist,
    })


@login_required(login_url='login')
def item_selling_price(request, product):
    title = "Change Selling Price"

    selling_price_table = SellingPrice.objects.all()

    price = ''
    for sell in selling_price_table:
        if sell.item.product_code == product:
            price = sell.selling_price
    
    if request.method == "POST":
        new_price = request.POST.get('price')
        item_obj = ''
        items = Item.objects.filter(product_code=product)
        for item in items:
            item_obj = item
        
        if str(new_price).isdecimal():
            sell_obj = SellingPrice(item=item_obj, selling_price=new_price)
            sell_obj.save()
            messages.success(request, ('Selling Price of {} is updated'.format(product)))
        else:
            messages.error(request, "Please enter a valid price")
            return render(request, 'change_price.html', {
                'title' : title,
                'product': product,
                'price' : price,
            })
            

        return redirect('inventory')

    return render(request, 'change_price.html', {
        'title' : title,
        'product': product,
        'price' : price,
    })



@login_required(login_url='login')
def employee(request):
    title = 'Employee'
    employee_table = User.objects.all()
    account_table = Account.objects.all()

    datalist = []
    for employee in employee_table:
        if employee.is_superuser == False:
            data = []
            data.append(employee.username)
            data.append('{} {}'.format(employee.first_name, employee.last_name))
            data.append(employee.email)

            address = ''
            phone_number = ''
            gender = ''

            for account in account_table:
                if employee.username == account.user.username:
                    address = account.address
                    phone_number = account.phone_number
                    gender = account.gender
            data.append(address)
            data.append(phone_number)
            data.append(gender)

            datalist.append(data)

    newdatalist = []
    for y in datalist:
        data = [x if x!=None else "" for x in y]
        newdatalist.append(data)

    return render(request, 'employees.html', {
        'me': request.user.username,
        'title': title,
        'employee_table': newdatalist,
        'control': request.user.is_staff,
    })


@login_required(login_url='login')
def registerUser(request):
    title = 'Register'
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()           

            emp_obj = Account(user = User.objects.all().last())
            emp_obj.save()
            messages.success(request, "User successfully registered")
            return redirect("../")
        else:
            name = form.cleaned_data.get('username')
            pass1 = form.cleaned_data.get('password1')
            pass2 = form.cleaned_data.get('password2')
            print(name)
            users = User.objects.filter(username=str(name)).count()

            if users != 0 or name == None:
                messages.error(request, "User Already exist")
            else:
                messages.error(request, "Password invalid or mismatch")

    form = NewUserForm()
    return render (request, "register.html", {
        'title':title,
        'form':form,
    })

@login_required(login_url='login')
def editUser(request, name):
    title = name

    userdata = User.objects.get(id=request.user.id)
    accountdata = Account.objects.get(user=request.user.id)

    data = []
    data.append(userdata.first_name)
    data.append(userdata.last_name)
    data.append(accountdata.address)
    data.append(accountdata.phone_number)
    data.append(userdata.email)
    data.append(accountdata.gender)

    data = [x if x!=None else "" for x in data]

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        gender = request.POST.get("Gender")

        userdata.first_name = first_name
        userdata.last_name = last_name
        userdata.email = email
        userdata.save()

        accountdata.phone_number = phone_number
        accountdata.address = address
        accountdata.gender = gender
        accountdata.save()

        messages.info(request, "Your bios save successful")

        userdata = User.objects.get(id=request.user.id)
        accountdata = Account.objects.get(user=request.user.id)

        data = []
        data.append(userdata.first_name)
        data.append(userdata.last_name)
        data.append(accountdata.address)
        data.append(accountdata.phone_number)
        data.append(userdata.email)
        data.append(accountdata.gender)

        data = [x if x!=None else "" for x in data]
        return redirect('employees')

    return render(request, "emp_details.html", {
        'title': title,
        'data':data,
    })


class MpPasswordChangeView(PasswordChangeView):
    model = User
    template_name = "change-password.html"
    success_url = reverse_lazy('employees')
    success_message = "Password Changed Successfull"

