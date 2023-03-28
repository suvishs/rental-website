from django.shortcuts import render,redirect,HttpResponse
from django.http import HttpResponseBadRequest
from django.contrib.auth.models import User, auth
from django.contrib import messages
from ecomapp.decorators import Admin_only
from ecomapp.models import Products,Cart,Customer,RentedItems
from ecomapp.forms import ApplicationForm
import PyPDF2
import re
import os
from django.conf import settings

import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

razorpay_client = razorpay.Client(
  auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
# Create your views here.

def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        if password == confirmpassword:
            if User.objects.filter(username=username).exists():
                msg = "Username already Taken"
                return render(request, "register.html",{"msg":msg})
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                return redirect('usrlogin')
        else:
            msg = "Both passwords are not matching"
            return render(request, "register.html",{"msg":msg})
    return render(request, "register.html")

def usrlogin(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages = 'Username or password incorrect'
            return render(request, "usrlogin.html",{"messages":messages})
    return render(request, "usrlogin.html")

def logout(request):
    auth.logout(request)
    return redirect('index')

def usr_details(request):
    try:
        usr = User.objects.get(username=request.user)
        if Customer.objects.filter(usr=request.user).exists():
            customer_det = Customer.objects.get(usr=request.user)
            return render(request,"usr_details.html",{"usr":usr,"customer_det":customer_det})
        else:
            return render(request,"usr_details.html",{"usr":usr})
    except:
        return HttpResponse("Please Fill Your Both Two application Completely")

def systemadmin(request):
    name = request.user
    customer = Customer.objects.all()
    return render(request, "systemadmin.html",{"name":name,"customer":customer})

def admin_odr(request):
    name = request.user
    rented_pro = RentedItems.objects.all()
    return render(request, "admin_odr.html",{"name":name,"rented_pro":rented_pro})

@Admin_only
def home(request):
    products = Products.objects.filter(product_category = "home")
    product_com = Products.objects.filter(product_category ="computer")
    return render(request, "home.html",{"products":products, "product_com":product_com})

def cart(request, id):
    cart_item = Cart.objects.filter(product_id=id, user=request.user).first()
    if cart_item:
        pass
    else:
        cart_item = Cart(product_id=id, user=request.user)
        cart_item.save()
    try:
        customer = Customer.objects.get(usr=request.user)
        cart_items = Cart.objects.filter(user=request.user)
        products = []
        for cart in cart_items:
            product = Products.objects.get(id=cart.product_id)
            products.append(product)
        return render(request, "cart.html", {"products": products,"customer":customer})
    except:
        cart_items = Cart.objects.filter(user=request.user)
        products = []
        for cart in cart_items:
            product = Products.objects.get(id=cart.product_id)
            products.append(product)
        return render(request, "cart.html", {"products": products})


def view_cart(request):
    try:
        customer = Customer.objects.get(usr=request.user)
        cart_items = Cart.objects.filter(user=request.user)
        products = []
        for cart in cart_items:
            product = Products.objects.get(id=cart.product_id)
            products.append(product)
        return render(request, "cart.html", {"products": products,"customer":customer})
    except:
        cart_items = Cart.objects.filter(user=request.user)
        products = []
        for cart in cart_items:
            product = Products.objects.get(id=cart.product_id)
            products.append(product)
        return render(request, "cart.html", {"products": products})


def contact(request):
    return render(request, "contact.html")

def gamingsec(request):
    product_vr = Products.objects.filter(product_category ="vr")
    return render(request, "gamingsec.html", {'product_vr':product_vr})

def domesticsec(request):
    product_tv = Products.objects.filter(product_category ="tv")
    return render(request, "domesticsec.html", {'product_tv':product_tv})

def application(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        maritial_status = request.POST.get("maritial_status")
        occupation = request.POST.get("occupation")
        email = request.POST.get("email")
        anual_income = request.POST.get("anual_income")
        aadhar_number = request.POST.get("aadhar_number")
        pan_number = request.POST.get("pan_number")
        permanant_adress = request.POST.get("permanant_adress")

        if Customer.objects.filter(usr=request.user).exists():
            return HttpResponse("YOU CAN'T REGISTER APPLICATION FORM MORE THAN ONCE, YOU CAN DELETE FIRST LEVEL OR CHOOSE SECOND LEVEL BUTTON")
        else:
            cos_info = Customer(first_name=first_name, last_name=last_name, gender=gender, maritial_status=maritial_status,
                                occupation=occupation, email=email, anual_income=anual_income,
                                aadhar_number=aadhar_number, pan_number=pan_number, permanant_adress=permanant_adress, usr=request.user)
            cos_info.save()
            return redirect("application2")
    return render(request, "application.html")

def application2(request):
    try:
        customer = Customer.objects.get(usr=request.user)
        if request.method == 'POST':
            form = ApplicationForm(request.POST, request.FILES)
            if form.is_valid():
                pancard_image_front = form.cleaned_data['pancard_image_front']
                pancard_image_back = form.cleaned_data['pancard_image_back']
                bankstatement = form.cleaned_data['bankstatement']
                customer.pancard_image_front = pancard_image_front
                customer.pancard_image_back = pancard_image_back
                customer.bankstatement = bankstatement
                customer.save()
                return redirect('validate_customer')
            else:
                return HttpResponse('Form is not valid. Please fill correctly.')
        else:
            form = ApplicationForm()
    except:
        return HttpResponse("Please Fill Application 1 Properly")
    return render(request, 'application2.html', {'form': form})


def validate_customer(request):
    # customer = Customer.objects.get(usr=request.user)
    # npay = customer.bankstatement.url
    # print(npay)

    customer = Customer.objects.get(usr=request.user)
    npay_url = customer.bankstatement.url
    npay_path = os.path.join(settings.MEDIA_ROOT, npay_url[len(settings.MEDIA_URL):])
    print(npay_path)

    pdfFileObj = open(npay_path,'rb')
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    num_pages = len(pdfReader.pages)

    count = 0
    text = ""

    while count < num_pages:
        pageObj = pdfReader.pages[count]
        count +=1
        text += pageObj.extract_text()
    
    text = text.lower()
    numbers = re.findall(r'\d+', text)

    # print(numbers)
    # print(type(numbers))
    print(numbers[-2])
    
    npay = int(numbers[-2])
    print(npay)

    if npay>=15000 and npay<=20000:
        customer.lender_score = 5
        customer.save()
    
    elif npay>=20001 and npay<=30000:
        customer.lender_score = 6
        customer.save()
    
    elif npay>=30001 and npay<=40000:
        customer.lender_score = 7
        customer.save()

    elif npay>=40001 and npay<=50000:
        customer.lender_score = 8
        customer.save()
    
    elif npay>=50001 and npay<=65000:
        customer.lender_score = 9
        customer.save()
    
    elif npay>=65001:
        customer.lender_score = 9.5
        customer.save()
    
    else:
        customer.lender_score = 4.5
        customer.save()
    
    customer.net_pay = npay
    customer.save()

    return redirect("usr_details")


def del_application(request,id):
    customer = Customer.objects.get(id=id)
    customer.delete()
    return redirect("application")

def adm_del_application(request,id):
    name = request.user
    customer = Customer.objects.all()
    cust = Customer.objects.get(id=id)
    cust.delete()
    return render(request,"systemadmin.html",{"name":name,"customer":customer})

def adm_approve(request,id):
    name = request.user
    customer = Customer.objects.all()
    cust = Customer.objects.get(id=id)
    cust.approval = True
    cust.save()
    return redirect("systemadmin")

def buyproduct(request,id):
    product = Products.objects.get(id=id)
    rented_pro = RentedItems.objects.filter(user=request.user)
    customer = Customer.objects.get(usr=request.user.id)
    if request.method == "POST":
        user = request.user
        rent_start_date = request.POST.get("rent_start_date")
        rent_end_date = request.POST.get("rent_end_date")
        quantity = request.POST.get("quantity")
        total_amount = request.POST.get("total_amount")

        total_amount_dis = request.POST.get("total_amount_dis")
        buy = RentedItems(product=product, user=user, rent_start_date=rent_start_date, rent_end_date=rent_end_date, quantity=quantity, total_amount=total_amount,total_amount_dis=total_amount_dis)
        buy.save()
        # message = "Item Purchased For Rental Successfully"
        rented_pro = RentedItems.objects.filter(user=request.user)
        products = []
        for rent in rented_pro:
            product = Products.objects.get(id=rent.product_id)
            products.append(product)
        return render(request, "renteditems.html",{"products":products,"rented_pro":rented_pro})
    return render(request,"buyproduct.html",{"product":product,"customer":customer})

def payment(request,id):
    return render(request, "payment.html")

def renteditems(request):
    rented_pro = RentedItems.objects.filter(user=request.user)
    return render(request,"renteditems.html",{"rented_pro":rented_pro})

@csrf_exempt
def paymenthandler(request):
    # ckeckoutitem  = CheckOut.objects.filter(customer = request.user, Payment_status = False)
    # total = 0
    # for i in ckeckoutitem:
    #     total += i.product.Product_Price
        
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

      # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                amount = 100 * 100 # Rs. 200
                try:
                    print("working 1")
                    x = razorpay_client.payment.capture(payment_id, amount)
                    print(x)
                    # item  = CheckOut.objects.filter(customer = request.user, Payment_status = False)
                    # for i in item:
                    #     newitem = CheckOut.objects.get(id = i.id)
                    #     newitem.Payment_status = True
                    #     newitem.save()
                    return render(request,"afterplaceorder.html")
          # render success page on successful caputre of payment
                except:
                    print("working 2")
                    return HttpResponse("not done")
                    
                    
          # if there is an error while capturing payment.
            else:
                return render(request, 'paymentfail.html')
        # if signature verification fails.    
        except:
            return HttpResponseBadRequest()
        
      # if we don't find the required parameters in POST data
    else:
  # if other than POST request is made.
        return HttpResponseBadRequest()



