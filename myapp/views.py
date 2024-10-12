from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import View,FormView,TemplateView,ListView,CreateView,UpdateView
from myapp.forms import SignUpForm,SignInForm,QunatityForm,CheckOutForm,ReviewForm
from django.contrib.auth import authenticate,login,logout
from myapp.models import Tag,Cake,CakeVariant,CartItems,MyOrders,Reviews
from django.db.models import Min
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from myapp.decoroters import signin_required
from twilio.rest import Client
from decouple import config
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



#view for registration
#url-lh:8000/register
class SignUpView(FormView):
    template_name='store/signup.html'
    form_class=SignUpForm

    def post(self,request,*args,**kwargs):
        form_instance=SignUpForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('sign-in')
        else:
            return render(request,'store/signup.html',{'form':form_instance})
        
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
                return redirect('index')
            
        return render(request,'store/signin.html')
    
#index view
#url-lh:8000/index/
@method_decorator(signin_required,name='dispatch')
class IndexView(View):
    template_name='store/index.html'

    def get(self,request,*args,**kwargs):
        qs=Tag.objects.all()
        return render(request,self.template_name,{'tags':qs})


#display cakes
#url-lh:8000/cake/<int:pk>/list/
@method_decorator(signin_required,name='dispatch')
class CakeListView(View):
    def get(self,request,*args,**kwargs):

        id=kwargs.get('pk')

        qs=Cake.objects.filter(tag_objects=id)

        # print('tag:',id)
      
        return render(request,'store/cake_list.html',{'cakes':qs,'tag_id':id})

@method_decorator(signin_required,name='dispatch')
class CakeVaraintsView(View):
    def get(self,request,*args,**kwargs):
        
        id=kwargs.get('pk')
        
        tag_id=kwargs.get('pk1')

        # print('tag..:',tag_id)

        cake_obj=Cake.objects.get(id=id)

        qs=CakeVariant.objects.filter(cake_object=id)
    
        return render(request,'store/cake_variants.html',{'variants':qs,'cake':cake_obj,'tag_id':tag_id})

@method_decorator(signin_required,name='dispatch') 
class CakeVariantDetailView(View):
    def get(self,request,*args,**kwargs):
        v_id=kwargs.get('pk1')
        c_id=kwargs.get('pk2')
        tag_id=kwargs.get('pk')

        # print('tag..:',tag_id)
      
        cake_variant_object=CakeVariant.objects.get(id=v_id)
        cake_object=Cake.objects.get(id=c_id)

        return render(request,'store/cake_variants.html',{'variant':cake_variant_object,'cake':cake_object,'tag_id':tag_id})

@method_decorator(signin_required,name='dispatch')
class AddToCartView(View):
    def get(self,request,*args,**kwargs):
        v_id=kwargs.get('pk')

        tag_id=kwargs.get('pk1')

        # print('tag..:',tag_id)
        
        variant_object=CakeVariant.objects.get(id=v_id)

        tag_obj=Tag.objects.get(id=tag_id)
  

        CartItems.objects.create(
                                    cart_object=request.user.basket,

                                    cake_variant_object=variant_object,

                                    tag_object=tag_obj,

                                    shape_object=variant_object.shape_object,
                                    
                                    flavour_object=variant_object.flavour_object,

                                    weight_object=variant_object.weight_object,

                                    updated_price=variant_object.price                    

                                )
        return redirect('index')


#view for cart list
#url:lh:8000/cart/summary
@method_decorator(signin_required,name='dispatch')
class MyCartView(View):
    def get(self,request,*args,**kwargs):

        form_instance=QunatityForm()

        cart_items=request.user.basket.basket_items.filter(is_order_placed=False)

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

            cart_obj.quantity = current_quantity + 1
       
        elif update_type == 'decrease':

            cart_obj.quantity = current_quantity - 1


        cart_obj.updated_price=current_price * cart_obj.quantity
            
        cart_obj.save()
            

        return redirect('mycart')



KEY_SECRET=config('KEY_SECRET')
KEY_ID=config('KEY_ID')

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


@method_decorator(signin_required,name='dispatch')     
class OrderPlacedView(View):

    def get(self,request,*args,**kwargs):

        return render(request,'store/order_placed.html')


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

@method_decorator(signin_required,name='dispatch')
class MyOrderSummaryView(View):
    def get(self,request,*args,**kwargs):

        qs=MyOrders.objects.filter(user_object=request.user,is_paid=True).order_by('-created_date')

        return render(request,'store/order_summary.html',{'orders':qs})

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

@method_decorator(signin_required,name='dispatch')
class AboutUsView(TemplateView):

    template_name = 'store/about_us.html'

@method_decorator(signin_required,name='dispatch')
class ContactUsView(TemplateView):
    template_name = 'store/contact_us.html'


@method_decorator(signin_required,name='dispatch')
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('sign-in')
    


    
    