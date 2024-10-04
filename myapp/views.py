from django.shortcuts import render,redirect
from django.views.generic import View,FormView,TemplateView,ListView,CreateView
from myapp.forms import SignUpForm,SignInForm,QunatityForm,CheckOutForm
from django.contrib.auth import authenticate,login,logout
from myapp.models import Tag,Cake,CakeVariant,CartItems,MyOrders
from django.db.models import Min
from django.urls import reverse_lazy
# Create your views here.


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
                return redirect('sign-in')
            
        return render(request,'store/signin.html')
    
#index view
#url-lh:8000/index/

class IndexView(View):
    template_name='store/index.html'

    def get(self,request,*args,**kwargs):
        qs=Tag.objects.all()
        return render(request,self.template_name,{'tags':qs})


#display cakes
#url-lh:8000/cake/<int:pk>/list/
class CakeListView(View):
    def get(self,request,*args,**kwargs):

        id=kwargs.get('pk')

        qs=Cake.objects.filter(tag_objects=id)

        # print('tag:',id)
      
        return render(request,'store/cake_list.html',{'cakes':qs,'tag_id':id})


class CakeVaraintsView(View):
    def get(self,request,*args,**kwargs):
        
        id=kwargs.get('pk')
        
        tag_id=kwargs.get('pk1')

        # print('tag..:',tag_id)

        cake_obj=Cake.objects.get(id=id)

        qs=CakeVariant.objects.filter(cake_object=id)
        # cake_variant=CakeVariant.objects.get()
        return render(request,'store/cake_variants.html',{'variants':qs,'cake':cake_obj,'tag_id':tag_id})
    
class CakeVariantDetailView(View):
    def get(self,request,*args,**kwargs):
        v_id=kwargs.get('pk1')
        c_id=kwargs.get('pk2')
        tag_id=kwargs.get('pk')

        # print('tag..:',tag_id)
      
        cake_variant_object=CakeVariant.objects.get(id=v_id)
        cake_object=Cake.objects.get(id=c_id)

        return render(request,'store/cake_variants.html',{'variant':cake_variant_object,'cake':cake_object,'tag_id':tag_id})


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
class MyCartView(View):
    def get(self,request,*args,**kwargs):

        form_instance=QunatityForm()

        cart_items=request.user.basket.basket_items.filter(is_order_placed=False)

        total_items=cart_items.count()

        total_amount=request.user.basket.total_amount 

        return render(request,'store/cart_summary.html',{'cartitems':cart_items,'total_items':total_items,'total_amount':total_amount,'form':form_instance})
    
  


#view for remove cart items
#url-lh:8000/cart/item/<int:pk>/remove
class CartItemDeleteView(View):
    def get(self,request,*args,**kwargs):

        id=kwargs.get('pk')

        CartItems.objects.get(id=id).delete()

        return redirect('mycart')


#view for update quantity and curresponding price in cart
#url-lh:8000/cart/item/<int:pk>/update   
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



class CheckOutView(CreateView): 

    def get(self,request,*args,**kwargs):                                                   
        form_instance=CheckOutForm()                                    
        # qs=MyOrders.objects.filter(user_object=request.user)
        qs=request.user.orders.all()                                                                   # taking user address
        print('addr',qs)
        return render(request,'store/checkout.html',{'form':form_instance,'address':qs})

    def post(self,request,*args,**kwargs):

        form_instance=CheckOutForm(request.POST)
        if form_instance.is_valid():
            form_instance.instance.user_object=request.user
            form_instance.save()
            return redirect('checkout')
        else:
            return render(request,'store/checkout.html',{'form':form_instance})
         

   

KEY_SECRET="OYZL5YKQt1MltOuTFEhHVH3g"
KEY_ID="rzp_test_BP60rY1i9DQCEZ"

import razorpay                              
class PaymentView(View):

    def get(self,request,*args,**kwargs):

        #create order

        client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))                                     #authentication to razorpay

        amount=request.user.basket.total_amount*100                                           #total amount in wishlist

        data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }

        payment = client.order.create(data=data) 


        myorder_id=kwargs.get('pk')

        myorder_obj=MyOrders.objects.get(id=myorder_id)

        print('my order..',myorder_obj)

        myorder_obj.order_id=payment.get('id')

        myorder_obj.save() 

        # cart_items=request.user.basket.basket_items.filter(is_order_placed=False) 

        # print('cart item...',cart_items)

        # for ci in cart_items:

        #       myorder_obj.cart_item_object.add(ci.cake_variant_object)

        # myorder_obj.save() 

        context={
            'key':KEY_ID,
            'amount':data.get('amount'),
            'currency':data.get('currency'),
            'order_id':payment.get('id')
        }

        return render(request,'store/payment.html',context)         


class PaymentVerificationView(View):
     def post(self,request,*args,**kwargs): 
       
       print('print:sucesss')

       return render(request,'store/success.html')  







