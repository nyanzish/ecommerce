from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import Uploadform, Farmerform,CheckoutForm, CouponForm, RefundForm
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Item, Order, OrderItem,Address,OrderItem2,Farmer
from django.contrib.auth.models import Group, Permission 
import http.client, urllib, base64, uuid,json
import requests 
import io
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import FileResponse
from reportlab.pdfgen import canvas
from twilio.rest import Client
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,Frame
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
# Create your views here.

def staff_required(login_url=None):
    #return user_passes_test(lambda u: u.is_staff, login_url=login_url)
    pass


def not_in_farmer_group(user):
    if user:
        #print(User.objects.filter(groups__name='farmer'))
        #return User.objects.filter(groups__name='farmer').count() == 0
        print(user.groups.filter(name__in=['farmer']))

        return user.groups.filter(name__in=['farmer'])
        
    else:
        return False
def farmer_group(request):
    
    if request.user:
        #print(User.objects.filter(groups__name='farmer'))
        #return User.objects.filter(groups__name='farmer').count() == 0
        farma= request.user.groups.filter(name__in=['farmer']).count()
        context={
            'farma':farma
        }
        print(farma)
        
        return render(request, 'shop/base.html', context)
        
    else:
        messages.info(request, "You are not authorised to access this page")
        return False
        
 


IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
#@staff_required(login_url="/error1")
@user_passes_test(not_in_farmer_group, login_url='/error1')
def post_product(request):
    name=Farmer.objects.get(user=request.user)
    print(name)

    order = OrderItem2.objects.filter(saler=name,ordered=True)
    print(order)
    total=0
    for order_item in order:
        total+=order_item.item.price
        print(order_item,order_item.item.price)
    deduct=total*0.1
    netamount=total- (total*0.1)
    #for item in queryset2:
    #     for order_item in item.items.all():
    #       order_saler=order_item.item.saler
    #        order_item_name=order_item.item.title
     #       print(order_item, 'sold by',order_saler,'--',order_item_name,order_item.saler)
            #count=order_item.item.filter(saler='shaf_farm')
            #if 'shaf_farm' in order_saler:
            #print(count)

    form = Uploadform(initial={'saler': name.id})
    if request.method == 'POST':
        form = Uploadform(request.POST, request.FILES)
        if form.is_valid():
            form.fields['saler'].initial=name.id
            form.fields['saler'].type='hidden'
            #form.fields['user'].initial=request.user
            user_pr = form.save(commit=True)
            user_pr.image = request.FILES['image']
            file_type = user_pr.image.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                return render(request, 'shop/error1.html')
            #Item(saler=result.farmname).save()
            user_pr.save()
            return redirect("shop:home")
    context = {"form": form,'object':order,'total':total,'deduct':deduct,'netamount':netamount}
    return render(request, 'shop/farmer.html', context)

def reg_farmer(request):

    form = Farmerform()
    if request.method == 'POST':
        form = Farmerform(request.POST)
        if form.is_valid():
            user_pr = form.save(commit=False)
            user_pr.save()
            messages.info(request, "Your request to sale on this site has been sent to the administrator and awaits activation")
            # Your Account Sid and Auth Token from twilio.com/user/account
            account_sid = "ACd1ab94afd548f8d02497399aa7185930"
            auth_token  = "f90d4d12e0c5b981e3567dac86b68bc3"
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                body="""User {} has applied to be come a saler and awaits your approval
                For any Questions contact us on +256702346241.
                www.wolm.com. Westnile Online Livestock Market.""".format(request.user.username),
                
                from_="+17542601075",
                to="+256702346241"
                )
            return render(request, 'shop/product.html', {'user_pr': user_pr})
    context = {"form": form,}
    return render(request, 'shop/farmer_register.html', context)

def index(request):
    #name=Farmer.objects.get(user=request.user)
    #print(name.farmname,';;;;;')
    
    
    queryset=Item.objects.filter(category='Cows',ratings__isnull=False).order_by('ratings__average')
    item1=Item.objects.filter(category='Chicken')
    item2=Item.objects.filter(category='Cows')
    item3=Item.objects.filter(category='Goats')
    item4=Item.objects.filter(category='Ducks')
    item5=Item.objects.filter(category='Sheep')
    item6=Item.objects.filter(category='Rabits')
    for cow in item2:
        print(cow) 

    
    print(queryset)

    return render(request,'shop/home.html',{'chickens':item1,'queryset':queryset,'rabits':item6,'sheep':item5,'cows':item2,'ducks':item4,'goats':item3})

def cow_search(request):
    global item2
    item2=Item.objects.filter(category='Cows')
    print(item2)
    context={'cows':item2}

    return render(request,'shop/mymarket2.html',context)

class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            shipping_price=5000
            amount= order.get_total() + shipping_price
            form = CheckoutForm()
            context = {
                'form': form,
                'shipping_price':shipping_price,
                'amount':amount
                
            }
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("shop:checkout")
    
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            queryset2 = Order.objects.get(user=self.request.user,ordered=False)
           
            for order_item in order.items.all():
                order_saler=order_item.item.saler
                queryset2 = OrderItem.objects.filter(user=self.request.user, saler=order_saler,ordered=False)
                print(order_item,order_item.item, order_item.user, order_item.item.saler,order_item.quantity)
            
            if form.is_valid():
                #order = Order.objects.get(user=self.request.user, ordered=False)
                shipping_country= form.cleaned_data.get("shipping_country")
                shipping_address= form.cleaned_data.get("shipping_address")
                shipping_city= form.cleaned_data.get("shipping_city")
                shipping_village= form.cleaned_data.get("shipping_village")
                customer_phone= form.cleaned_data.get("customer_phone")
                shipping_notes= form.cleaned_data.get("shipping_notes")
                payment_option= form.cleaned_data.get("payment_option")
                customer_mobilemoneyphone= form.cleaned_data.get("customer_mobilemoneyphone")
                billing_address = Address(
                                user=self.request.user,
                                country=shipping_country,
                                shipping_address=shipping_address,
                                shipping_city=shipping_city,
                                shipping_village=shipping_village,
                                shipping_notes=shipping_notes,
                                customer_phone=customer_phone,
                                payment_option=payment_option,
                                customer_mobilemoneyphone=customer_mobilemoneyphone
                                
                            )
                billing_address.save()
                order.billing_address=billing_address
                shipping_price=5000
                amount= order.get_total() + shipping_price

                print(amount)
                print(order.order_id)
                #try #except error --filter output

                API_ENDPOINT = 'https://www.easypay.co.ug/api/'
                # data to be sent to api 
                data = json.dumps({
                "username": "3716cb0e05152f94",
                "password": "2b2f11b32e92346e",
                "action":"mmdeposit",
                "amount":amount,
                "currency":"UGX",
                "phone":customer_phone,
                "reference":str(order.order_id),
                "reason":'Testing MM DEPOSIT'})
                r = requests.post(url = API_ENDPOINT, data = data)
                pastebin_url = r.text 
                data2=r.json()
                print(data2)
                print("The pastebin URL is:%s"%pastebin_url)

                #if successfull
                OrderItem2(
                    user=order_item.user,
                    ordered=True,
                    item=order_item.item,
                    quantity=order_item.quantity,
                    saler=order_item.item.saler

                    ).save()
                order.save()
                #empty cart
                messages.warning(self.request, "order Successful")
            
                return redirect("shop:checkout")
                #else error
            messages.warning(self.request, "You do not have an active order")
            context={
                'shipping_price':shipping_price,
                'amount':amount

            }
            #return render(self.request, "checkout.html", context)

            return redirect("shop:checkout")
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("shop:order-summary")
        print(self.request.POST)
        

class PaymentView(View):
    def get(self, *args, **kwargs):
        context={

        }
        return render(self.request, "payment.html", context)





def pay(request):
    #Get the variables
    order = Order.objects.get(user=self.request.user, ordered=False)
    shipping_price=5000
    amount= order.get_total() + shipping_price

    print(amount)
    print(order.order_id)

    
    data_visa= {
    "username": "your client Id",
    "password": "your secret",
    "action":"cardpayment",
    "amount":"amount in usd",
    "currency":"USD",
    "name":"name on card",
    "cardno":"card number",
    "cvv":"security code back of card",
    "month":"expiry month eg 01 for jan",
    "year":"year of expiry",
    "email":"card holders email",
    "address":"billing address",
    "city":"billing city",
    "state":"state",
    "zip":"zip code",
    "country":"billing country",
    "phone":"phone number",
    "reference":"your order reference",
    "reason":"Reason eg book payment"}
    # sending post request and saving response as response object 
    #r = requests.post(url = API_ENDPOINT, data = data) 

    # extracting response text 
    #pastebin_url = r.text 
    #data2=r.json()
    #print(data2)
    #print("The pastebin URL is:%s"%pastebin_url) 
    context ={
        'order':order,
        'shipping_price':shipping_price,
        'amount':amount

    }
    return render(request,'shop/pay.html', context)


def cart(request):
	return render(request,'shop/cart.html')



@login_required
def checkout(request):
    
    context={

    }
    return render(request,'shop/checkout.html', context)

def product(request,slug):
    obj= Item.objects.get(id=slug)
    item6=Item.objects.filter(category=obj.category)
	
    context={
        'object':obj,
        'categori':item6
    }
    return render(request,'shop/product2.html',context)

def farm_market(request,slug):
    obj= Item.objects.filter(saler=str(slug))
    orders= Order.objects.get(saler=slug)
	
    context={
        'object':obj
    }
    return render(request,'shop/mymarket2.html',context)


class farmDetailView(ListView):
    model = Item
    paginate_by = 12
    #ordering = ['saler']
    
    template_name = "mymarket2.html"
    #item2=Item.objects.filter(saler=1)
    object_list=Item.objects.all()
    
    def get(self, request, *args, **kwargs):
        #object_list=Item.objects.filter(saler=self.kwargs ['slug'])
        context = locals()
        #context['item2'] = self.item2
        context['object_list'] = self.object_list
        return render_to_response(self.template_name, context, RequestContext(request))
    
    


class cowView(ListView):
    model = Item
    paginate_by = 12
    template_name = "mymarket2.html"
    item2=Item.objects.filter(category='Cows')
    
    def get(self, request, *args, **kwargs):
        context = locals()
        context['item2'] = self.item2
        
        return render_to_response(self.template_name, context, RequestContext(request))

class goatView(ListView):
    model = Item
    paginate_by = 12
    template_name = "mymarket2.html"
    item2=Item.objects.filter(category='Goats')
    
    def get(self, request, *args, **kwargs):
        context = locals()
        context['item2'] = self.item2
        
        return render_to_response(self.template_name, context, RequestContext(request))

class sheepView(ListView):
    model = Item
    paginate_by = 12
    template_name = "mymarket2.html"
    item2=Item.objects.filter(category='Cows')
    
    def get(self, request, *args, **kwargs):
        context = locals()
        context['item2'] = self.item2
        
        return render_to_response(self.template_name, context, RequestContext(request))

class chickenView(ListView):
    model = Item
    paginate_by = 12
    template_name = "mymarket2.html"
    item2=Item.objects.filter(category='Chicken')
    
    def get(self, request, *args, **kwargs):
        context = locals()
        context['item2'] = self.item2
        
        return render_to_response(self.template_name, context, RequestContext(request))

class ducksView(ListView):
    model = Item
    paginate_by = 12
    template_name = "mymarket2.html"
    item2=Item.objects.filter(category='Ducks')
    
    def get(self, request, *args, **kwargs):
        context = locals()
        context['item2'] = self.item2
        
        return render_to_response(self.template_name, context, RequestContext(request))

class pigsView(ListView):
    model = Item
    paginate_by = 12
    template_name = "mymarket2.html"
    item2=Item.objects.filter(category='Pigs')
    
    def get(self, request, *args, **kwargs):
        context = locals()
        context['item2'] = self.item2
        
        return render_to_response(self.template_name, context, RequestContext(request))

class rabbitsView(ListView):
    model = Item
    paginate_by = 12
    template_name = "mymarket2.html"
    item2=Item.objects.filter(category='Rabits')
    
    def get(self, request, *args, **kwargs):
        context = locals()
        context['item2'] = self.item2
        
        return render_to_response(self.template_name, context, RequestContext(request))

class dovesView(ListView):
    model = Item
    paginate_by = 12
    template_name = "mymarket2.html"
    item2=Item.objects.filter(category='Doves')
    
    def get(self, request, *args, **kwargs):
        context = locals()
        context['item2'] = self.item2
        
        return render_to_response(self.template_name, context, RequestContext(request))


def mymarket(request):
	return render(request,'shop/mymarket.html')

def error1(request):
	return render(request,'shop/error1.html')

def product_upload(request):
	return render(request,'shop/product_upload.html')


class HomeView(ListView):
    model = Item
    #paginate_by = 10
    template_name = "home.html"

class MarketView(ListView):
    model = Item
    paginate_by = 12
    template_name = "mymarket.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = "product2.html"

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            print(order)
            queryset2 = Order.objects.get(user=self.request.user,ordered=False)
           
            for order_item in order.items.all():
                order_saler=order_item.item.saler
                queryset2 = OrderItem.objects.filter(user=self.request.user, saler=order_saler,ordered=False)
                print(order_item,order_item.item, order_item.user, order_item.item.saler,order_item.quantity)
                
                order_item_name=order_item.item.title
                #print(order_item, 'sold by',order_saler,'--',order_item_name,order_item.saler)
               
            
            
            shipping_price=5000
            amount= order.get_total() + shipping_price

            print(amount)
            print(order.order_id)
            context = {
                'object': order,
                'shipping_price':shipping_price,
                'amount':amount
            }
            return render(self.request, 'cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")

class OrderSummaryView_farmer(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            farmers = Farmer.objects.get(user=self.request.user)
            print(farmers,'ttttt')

            #queryset2 = OrderItem2.objects.filter(user=request.user,ordered=True)
            order = OrderItem2.objects.filter(saler=farmers,ordered=True)
            print(order)
            
            #print(order_item, 'sold by',order_saler,'--',order_item_name,order_item.saler)
               
            
            
            shipping_price=5000
            amount= order.get_total() + shipping_price

            print(amount)
            print(order.order_id)
            context = {
                'object': order,
                'shipping_price':shipping_price,
                'amount':amount
            }
            return render(self.request, 'farmer.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")
def add(request):
    try:
        for order1 in order.items.all():
            order2 = OrderItem.objects.get( saler=order1.item.saler)
            print(order2)
                
                
    except ValueError:
        print('fail') 

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, id=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item.quantity += 1
            order_item.saler=item.saler
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("shop:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("shop:product",slug=slug)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("shop:product",slug=slug)

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, id=slug)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_qs2 = OrderItem.objects.filter(user=request.user)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item= OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "The product was succefully removed from your cart.")
            return redirect("shop:product",slug=slug)
            
            
        else:
            messages.info(request, "Your order doesnot contain this item.")
            return redirect("shop:product",slug=slug)
            
            

    else:
            messages.info(request, "You donot have an order.")
            return redirect("shop:product",slug=slug)
            

@login_required
def remove_single_item_from_cart2(request, slug):
    item = get_object_or_404(Item, slug= slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).ueryset2exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.quantity -= 1
            order_item.save()
    
            messages.info(request, "This item quantity was updated.")
            return redirect("shop:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("shop:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("shop:product", slug=slug)
            
            
@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item= OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                messages.info(request, "The product was succefully removed from your cart.")
                return redirect("shop:order-summary")
            
            
        else:
            messages.info(request, "Your order doesnot contain this item.")
            return redirect("shop:product",slug=slug)
            
            

    else:
            messages.info(request, "You donot have an order.")
            return redirect("shop:product",slug=slug)
            


def report_view(request):
    order = Order.objects.get(user=request.user, ordered=False)
    address = Address.objects.get(user=request.user)
    shipping_price=5000
    amount= order.get_total() + shipping_price
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    order_detail=['Order Date', 'Order No.','Payment Type','shipping Fee','Amount','Name','Phone No.', 'Email','Delivery Address']
    address_to =str(address.shipping_address)+','+str(address.shipping_village)+','+str(address.shipping_city)+','+str(address.country)
    customer_detail=[str(order.ordered_date),str(order.order_id),str(address.payment_option),str(shipping_price),str(amount),str(request.user.username),str(address.customer_phone), str(request.user.email),str(address_to)]
    p.drawString(30,820, "www.wolm.com")
    p.drawString(30,800, "contact us:+256702346241")
    p.drawString(440,820, "Plot 47 Hospital Road")
    p.drawString(440,800, "Arua,Uganda")
    
    # 5) Draw a image
    image = 'shop/static/shop/images/logo.PNG'
    p.drawInlineImage(image, 220,730)
    p.drawString(140, 710, "Thank You for Shopping with us. Hope you enjoy Your Order.")
    p.drawString(140, 690, "Incase of any concerns please contact us: +256702346241")
    p.drawString(240, 430, "Package Content")
    
    #order_detail
    x=70
    y=660
    
    for detail in order_detail:
        y -=20
        p.drawString(x, y, detail)
        
    x2=280
    y2=660
    for detail in customer_detail:
        y2 -=20
        p.drawString(x2, y2, detail)

    data = [
    ['Item Title', 'Unit Price', 'quantity', 'Total Item Price' ],
    
    ]
    total=[' Order Total + Shipping', ' ', ' ',amount ]
    for order_item in order.items.all():
        lista=[]

        lista.append(order_item.item.title) 
        lista.append(order_item.item.price)
        lista.append(order_item.quantity)
        lista.append(order_item.get_total_item_price())
        data.append(lista)

    data.append(total)



    

    width = 500
    height = 200
    x = 90
    y = 330
    f = Table(data)
    style = TableStyle([

    ('BACKGROUND', (0,0), (3,0), colors.green),
    ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),

    ('ALIGN',(0,0),(-1,-1),'CENTER'),

    ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 12),

    ('BOTTOMPADDING', (0,0), (-1,0), 12),

    ('BACKGROUND',(0,1),(-1,-1),colors.beige),
    ])
    f.setStyle(style)
    # 2) Alternate backgroud color
    rowNumb = len(data)
    for i in range(1, rowNumb):
        if i % 2 == 0:
            bc = colors.burlywood
        else:
            bc = colors.beige
        
        ts = TableStyle(
            [('BACKGROUND', (0,i),(-1,i), bc)]
        )
        f.setStyle(ts)


    f.wrapOn(p, width, height)
    f.drawOn(p, x, y)
    #frame = Frame(inch, inch, 10*inch, 11*inch, showBoundary=1)
    #frame.drawBoundary(p)

    
    

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(1)
    # Your Account Sid and Auth Token from twilio.com/user/account
    try:
        account_sid = "ACd1ab94afd548f8d02497399aa7185930"
        auth_token  = "f90d4d12e0c5b981e3567dac86b68bc3"
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body="""Hello {}!. Thank you for shopping with us.
            You purchased products worth UGX {},details have been sent to your Email. 
            Your products will be delivered to you in a weeks time.
            For any Questions contact us on +256702346241.
            www.wolm.com.
            Westnile Online Livestock Market.""".format(request.user.username,amount),
            
            from_="+17542601075",
            to="+256702346241"
            )
        print(message.sid)
        return FileResponse(buffer, as_attachment=True, filename='Invoice.pdf')
    except ConnectionError:
        messages.info(request, "sorry, your internet connection seems to be down. ")

    


def sms_notification(request):
    # Download the Python helper library from twilio.com/docs/python/install 


    # Your Account Sid and Auth Token from twilio.com/user/account
    account_sid = "ACdffe66ee2aba9a9b2922d5f99a923fcd"
    auth_token  = "53bc6bdf969a83c1a19ca42f82bc4666"
    client = TwilioRestClient(account_sid, auth_token)

    message = client.messages.create(
        body="Jenny please?! I love you <3",
        to="+256702346241",
        from_="+14158141829",
        media_url="http://www.example.com/hearts.png")
    print(message.sid)

def withdraw_request(request):
    # Your Account Sid and Auth Token from twilio.com/user/account
    account_sid = "ACdffe66ee2aba9a9b2922d5f99a923fcd"
    auth_token  = "53bc6bdf969a83c1a19ca42f82bc4666"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="""User {} a farm saler on wolm requests a  withdraw  and awaits your approval.
        For any Questions contact us on +256702346241.
        www.wolm.com. Westnile Online Livestock Market.""".format(request.user.username),
                
        from_="+15162520489",
        to="+256702346241"
        )
    messages.info(request, "Your request to withdraw has been successfully sent to the administrator for approoval as soon as possible.You will be notified once approved.")
    return redirect("shop:post_product")