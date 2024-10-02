from django.shortcuts import render,redirect
from django.views.generic import View,FormView,TemplateView,ListView
from myapp.forms import SignUpForm,SignInForm
from django.contrib.auth import authenticate,login,logout
from myapp.models import Tag,Cake,CakeVariant,CartItems
from django.db.models import Min
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

        print('tag..:',tag_id)
        
        variant_object=CakeVariant.objects.get(id=v_id)

        tag_obj=Tag.objects.get(id=tag_id)

        shape=variant_object.shape_object



        print('shape name:',shape)

  

        CartItems.objects.create(
                                    cart_object=request.user.basket,

                                    cake_variant_object=variant_object,

                                    tag_object=tag_obj,

                                    shape_object=variant_object.shape_object,
                                    
                                    flavour_object=variant_object.flavour_object,

                                    weight_object=variant_object.weight_object                     

                                )
        return redirect('index')

#view for cart list
#url:lh:8000/cart/summary
class MyCartView(View):
    def get(self,request,*args,**kwargs):

        cart_items=request.user.basket.basket_items.filter(is_order_placed=False)

        return render(request,'store/cart_summary.html',{'cartitems':cart_items})
