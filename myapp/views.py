from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import View,FormView,TemplateView,ListView,CreateView,UpdateView
from myapp.forms import SignUpForm,SignInForm,QunatityForm,CheckOutForm,ReviewForm,SearchForm
from django.contrib.auth import authenticate,login,logout
from myapp.models import Tag,Cake,CakeVariant,CartItems,MyOrders,Reviews,WishList
from django.db.models import Min
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from myapp.decoroters import signin_required
from twilio.rest import Client
from decouple import config
from django.db.models import Q
from django.contrib import messages
import random
# Create your views here.

account_sid = config('account_sid') 
auth_token = config('auth_token')

def sent_sms(user_phone,message):                  

    client = Client(account_sid, auth_token)                              
                                                                               
    sms = client.messages.create(
                                    from_='+18645280831',
                                    body=message,
                                    to=user_phone
                                    )
    
    print(sms.sid)

def generate_otp(length=6):
    
    return ''.join([str(random.randint(0, 9)) for i in range(length)])
   

#view for registration
#url-lh:8000/register
class SignUpView(FormView):
    template_name='store/signup.html'
    form_class=SignUpForm

    def post(self,request,*args,**kwargs):
        form_instance=SignUpForm(request.POST)

        if form_instance.is_valid():

            otp = generate_otp(6)

            request.session['otp'] = otp

            messages.success(request,f"Your OTP is: {otp}")

            return redirect('verify_otp')
        
        else:
            form_instance = SignUpForm()   
            
           
        return render(request,'store/signup.html',{'form':form_instance})
    
   
class verifyOtpView(View):
    def post(self,request,*args,**kwargs):

        entered_otp = request.POST.get('otp')
        saved_otp = request.session.get('otp')

        if entered_otp == saved_otp:
            messages.success(request, "OTP verified successfully!")

        else:
            messages.error(request, "Invalid OTP, please try again.")

        return render(request, 'otp.html')





#login View
#url-lh:8000
class SignInView(FormView):
    template_name='store/signin.html'
    form_class=SignInForm

    def post(self,request,*args,**kwargs):

        form_instance=SignInForm(request.POST)

        if form_instance.is_valid():
            data=form_instance.cleaned_data
            user_obj=authenticate(request,**data)

            if user_obj:
                login(request,user_obj)
                messages.success(request,'Successfully  Login !  ')
                return redirect('index')
            
        messages.error(request,'Login Failure!')    
        return render(request,'store/signin.html',{'form':form_instance})
    
#index view
#url-lh:8000/index/
@method_decorator(signin_required,name='dispatch')
class IndexView(View):
    template_name='store/index.html'

    def get(self,request,*args,**kwargs):
        qs=Tag.objects.all()
        return render(request,self.template_name,{'tags':qs})


#view for display cakes
#url-lh:8000/cake/<int:pk>/list/
@method_decorator(signin_required,name='dispatch')
class CakeListView(View):
    def get(self,request,*args,**kwargs):

        id=kwargs.get('pk')

        qs=Cake.objects.filter(tag_objects=id)

        # print('tag:',id)
      
        return render(request,'store/cake_list.html',{'cakes':qs})
    
#view for display cakes Variants
#url-lh:8000/cake/<int:pk>/variants/
@method_decorator(signin_required,name='dispatch')
class CakeVaraintsView(View):
    def get(self,request,*args,**kwargs):
        
        id=kwargs.get('pk')
        
        print('cake..:',id)

        cake_obj=Cake.objects.get(id=id)

        qs=CakeVariant.objects.filter(cake_object=id)
    
        return render(request,'store/cake_variants.html',{'variants':qs,'cake':cake_obj})

#view for display cakes Variant detail
#url-lh:8000/cake/<int:pk1>/variant/<int:pk2>/detail/
@method_decorator(signin_required,name='dispatch') 
class CakeVariantDetailView(View):
    def get(self,request,*args,**kwargs):
        v_id=kwargs.get('pk1')
        c_id=kwargs.get('pk2')
     
        cake_variant_object=CakeVariant.objects.get(id=v_id)
        cake_object=Cake.objects.get(id=c_id)

        return render(request,'store/cake_variants.html',{'variant':cake_variant_object,'cake':cake_object})
 
#view for add to wishlist
#url-lh:8000/cake/<int:pk>/wishlist/add
@method_decorator(signin_required,name='dispatch')  
class AddToWishListView(View):
    def get(self,request,*args,**kwargs):

        cake_id=kwargs.get('pk')

        cake_obj=Cake.objects.get(id=cake_id)

        WishList.objects.create(
                                    user_object=request.user,
                                    cake_object=cake_obj
                                )
        return redirect('mywishlist')

#view for listing  wishlist items
#url-lh:8000/wishlist/summary/  
@method_decorator(signin_required,name='dispatch')
class MyWishlistView(View):

    def get(self,request,*args,**kwargs):

        wishlist_items=WishList.objects.filter(user_object=request.user)

        return render(request,'store/wishlist.html',{'wishitems':wishlist_items})  

#view for remove  wishlist items
#url-lh:8000/wishlist/item/<int:pk>/remove/    
@method_decorator(signin_required,name='dispatch')
class WishlistItemDeleteView(View):
    def get(self,request,*args,**kwargs):

        wi_id=kwargs.get('pk')

        WishList.objects.get(id=wi_id).delete()

        return redirect('mywishlist')

#view for add to  cart
#url-lh:8000/cake/<int:pk>/cart/add
@method_decorator(signin_required,name='dispatch')
class AddToCartView(View):
    def get(self,request,*args,**kwargs):
        v_id=kwargs.get('pk')

        # print('tag..:',tag_id)
        
        variant_object=CakeVariant.objects.get(id=v_id)

        # tag_obj=Tag.objects.get(id=tag_id)
  

        CartItems.objects.create(
                                    cart_object=request.user.basket,

                                    cake_variant_object=variant_object,

                                    updated_price=variant_object.price                    

                                )
        return redirect('index')


#view for listing cart items
#url:lh:8000/cart/summary
@method_decorator(signin_required,name='dispatch')
class MyCartView(View):
    def get(self,request,*args,**kwargs):

        form_instance=QunatityForm()

        cart_items=request.user.basket.basket_items.filter(is_order_placed=False).order_by('-created_date')

        total_items=cart_items.count()

        total_amount=request.user.basket.total_amount 

        return render(request,'store/cart_summary.html',{'cartitems':cart_items,'total_items':total_items,'total_amount':total_amount,'form':form_instance})
    
  
#view for remove cart items
#url-lh:8000/cart/item/<int:pk>/remove
@method_decorator(signin_required,name='dispatch')
class CartItemDeleteView(View):
    def get(self,request,*args,**kwargs):

        id=kwargs.get('pk')

        CartItems.objects.get(id=id).delete()

        return redirect('mycart')


#view for update quantity and curresponding price in cart
#url-lh:8000/cart/item/<int:pk>/update 
@method_decorator(signin_required,name='dispatch')  
class QuantityUpdateView(FormView):
      
    def post(self,request,*args,**kwargs):

        cart_id=kwargs.get('pk')

        cart_obj=CartItems.objects.get(id=cart_id)

        cakevar_obj=CakeVariant.objects.get(id=cart_obj.cake_variant_object_id)
   
        update_type = request.POST.get('update')  #+ = increase

        current_quantity = cart_obj.quantity      #1

        current_price=cart_obj.cake_variant_object.price
        
        if update_type == 'increase':

            if current_quantity < 5:

                cart_obj.quantity = current_quantity + 1
       
        elif update_type == 'decrease':

            if current_quantity > 1:

                cart_obj.quantity = current_quantity - 1


        cart_obj.updated_price=current_price * cart_obj.quantity
            
        cart_obj.save()
            

        return redirect('mycart')



KEY_SECRET=config('KEY_SECRET')
KEY_ID=config('KEY_ID')
#view for payment
#url-lh:8000/payment/
import razorpay
@method_decorator(signin_required,name='dispatch')                              
class PaymentView(FormView):

    template_name='store/checkout.html'

    form_class= CheckOutForm

    def post(self,request,*args,**kwargs):

        form_instance=CheckOutForm(request.POST)

        if form_instance.is_valid():

            payment_method = form_instance.cleaned_data['payment_method']
            print('printing....',payment_method)

            if payment_method == 'cash-on-delivery':
                form_instance.instance.user_object = request.user
                form_instance.instance.is_paid=True
                form_instance.instance.total=request.user.basket.total_amount
                form_instance.save()

                cart_items = self.request.user.basket.basket_items.filter(is_order_placed=False)
                

                for ci in cart_items:
                    form_instance.instance.cart_item_object.add(ci)
                    ci.is_order_placed = True
                    ci.save()
                form_instance.save()

                user_phone = '+919947115118'
                message = f"Thank you for your payment of Rs. {form_instance.instance.total}. Your order has been placed!"
                sent_sms(user_phone, message)

                return redirect('order-placed')
            
            elif payment_method == 'online-payment':

                client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))                                     #authentication to razorpay

                amount=self.request.user.basket.total_amount*100                                           #total amount in wishlist

                data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }

                payment = client.order.create(data=data)
  
                form_instance.instance.order_id=payment.get('id')
                form_instance.instance.user_object = request.user
                form_instance.instance.total=request.user.basket.total_amount
                form_instance.save()

                cart_items = self.request.user.basket.basket_items.filter(is_order_placed=False)

                for ci in cart_items:
                    form_instance.instance.cart_item_object.add(ci)
                    ci.is_order_placed = True
                    ci.save()
                form_instance.save()

                context={
                    'key':KEY_ID,
                    'amount':data.get('amount'),
                    'currency':data.get('currency'),
                    'order_id':payment.get('id')
                }

                return render(self.request,'store/payment.html',context)

            return redirect('index')
        else:
            return redirect('payment')

#view for order placed
#url-lh:8000/order/placed/
@method_decorator(signin_required,name='dispatch')     
class OrderPlacedView(View):

    def get(self,request,*args,**kwargs):

        return render(request,'store/order_placed.html')

#view for payment verification
#url-lh:8000/payment/verification/
from django.views.decorators.csrf import csrf_exempt 
@method_decorator(csrf_exempt,name='dispatch') 
@method_decorator(signin_required,name='dispatch') 
class PaymentVerificationView(View):
    def post(self,request,*args,**kwargs):

        client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

        myoder_obj=MyOrders.objects.get(order_id=request.POST.get('razorpay_order_id'))

        login(request,myoder_obj.user_object)

        try:
            client.utility.verify_payment_signature(request.POST)                     #checking payment verification (success or not)
            print("payment success!")
            order_id=request.POST.get('razorpay_order_id')                                #taking order id from rayzorpay reqst/this order_id is coming after payment success
            MyOrders.objects.filter(order_id=order_id).update(is_paid=True)           #updating is_paid =true of order which is payment success
            
            order_obj=request.user.orders

            cart_items=request.user.basket.basket_items.filter(is_order_placed=False)

            for ci in cart_items:
                ci.is_order_placed=True
                ci.save()

            user_phone = '+919947115118'
            message = f"Thank you for your payment. Your order has been placed!"
            sent_sms(user_phone, message)

        except:
            print('payment failed') 
              

        return redirect('order-placed')  

#view for order summary
#url-lh:8000/order/summary/
@method_decorator(signin_required,name='dispatch')
class MyOrderSummaryView(View):
    def get(self,request,*args,**kwargs):

        qs=MyOrders.objects.filter(user_object=request.user,is_paid=True).order_by('-created_date')

        return render(request,'store/order_summary.html',{'orders':qs})


#view for adding review
#url-lh:8000/cake/<int:pk>/review-add/
@method_decorator(signin_required,name='dispatch')
class ReviewView(CreateView):
    template_name='store/review.html'
    form_class=ReviewForm
    model=Reviews
    success_url=reverse_lazy('index')

    def form_valid(self, form):
        cart_id=self.kwargs.get('pk')      
        cart_obj=CartItems.objects.get(id=cart_id)      
        cake_obj=cart_obj.cake_variant_object.cake_object
        # print('printing....',cake_obj)

        form.instance.cake_object=cake_obj
        form.instance.user_object=self.request.user 

        return super().form_valid(form)

#view for about us
#url-lh:8000/about-us/
@method_decorator(signin_required,name='dispatch')
class AboutUsView(TemplateView):

    template_name = 'store/about_us.html'

#view for contact us
#url-lh:8000/contact-us/
@method_decorator(signin_required,name='dispatch')
class ContactUsView(TemplateView):
    template_name = 'store/contact_us.html'

#view for sign out
#url-lh:8000/signout/
@method_decorator(signin_required,name='dispatch')
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('sign-in')
    
#view for search
#url-lh:8000/search/
class SearchView(FormView):

    template_name='store/base.html'

    form_class = SearchForm

    def get(self,request,*args,**kwargs):

        query = self.request.GET.get('search')  # Get search term from request

        if query:

            qs=Cake.objects.filter(
                                         Q(name__icontains=query) | Q(description__icontains=query)
                                     ) 
            print('printingg...',qs)    
                                           
            return render(request,'store/search_list.html',{'cakes':qs})
        
        return redirect('index')
    