from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class Tag(models.Model):

    title=models.CharField(max_length=300,unique=True)

    image=models.ImageField(upload_to='tag_images',default='/tag_images/default.png')

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title
    


from django.db.models import Min
class Cake(models.Model):

    name=models.CharField(max_length=300)

    description=models.TextField()

    image=models.ImageField(upload_to="cake_images",default="/cake_images/default.png")

    tag_objects=models.ManyToManyField(Tag)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    @property
    def cake_variant(self):

        return self.varients.order_by('price').first()
    

    def __str__(self) -> str:
        return self.name


class Shape(models.Model):

    title=models.CharField(max_length=100,unique=True)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title
    


class Flavour(models.Model):

    name=models.CharField(max_length=100,unique=True)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name
    


class Weight(models.Model):

    title=models.CharField(max_length=100,unique=True)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title
    

class CakeVariant(models.Model):

    cake_object=models.ForeignKey(Cake,on_delete=models.CASCADE,related_name='varients') 

    weight_object=models.ForeignKey(Weight,on_delete=models.CASCADE)

    shape_object=models.ForeignKey(Shape,on_delete=models.CASCADE)

    flavour_object=models.ForeignKey(Flavour,on_delete=models.CASCADE)

    price=models.PositiveIntegerField()

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)


class Cart(models.Model):

    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="basket")

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)


class CartItems(models.Model):

    cart_object=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="basket_items")

    cake_variant_object=models.ForeignKey(CakeVariant,on_delete=models.CASCADE)

    tag_object=models.ForeignKey(Tag,on_delete=models.CASCADE)

    shape_object=models.ForeignKey(Shape,on_delete=models.CASCADE)

    flavour_object=models.ForeignKey(Flavour,on_delete=models.CASCADE)

    weight_object=models.ForeignKey(Weight,on_delete=models.CASCADE)

    quantity=models.PositiveIntegerField(default=1,validators=[MinValueValidator(1),MaxValueValidator(20)])

    is_order_placed=models.BooleanField(default=False)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)


class MyOrders(models.Model):

    user_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name="orders")

    cart_item_object=models.ManyToManyField(CartItems)

    house_name=models.CharField(max_length=500)

    place=models.CharField(max_length=200)

    pincode=models.CharField(max_length=6)

    phone=PhoneNumberField(region='IN')

    payment_options=(
        ("cash","cash"),
        ("upi","upi"),
    )

    payment_method=models.CharField(max_length=200,choices=payment_options,default="cash")

    order_id=models.CharField(max_length=200,null=True)

    is_paid=models.BooleanField(default=False)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)



class Reviews(models.Model):
    cake_object=models.ForeignKey(Cake,on_delete=models.CASCADE,related_name='cake_reviews')

    user_object=models.ForeignKey(User,on_delete=models.CASCADE)

    comment=models.TextField()

    rating=models.PositiveIntegerField(default=1,validators=[MinValueValidator(1),MaxValueValidator(5)])

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

#signals
#creating basket for a user

from django.db.models.signals import post_save
def create_basket(sender,instance,created,*args,**kwargs):
    if created:
        Cart.objects.create(owner=instance)
post_save.connect(sender=User,receiver=create_basket)