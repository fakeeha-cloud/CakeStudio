# Generated by Django 5.0.6 on 2024-09-08 07:00

import django.core.validators
import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('description', models.CharField(max_length=500)),
                ('image', models.ImageField(default='/cake_images/default.png', upload_to='cake_images')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Flavour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shape',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Weight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='CakeVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('cake_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='varients', to='myapp.cake')),
                ('flavour_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.flavour')),
                ('shape_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.shape')),
                ('weight_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.weight')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='basket', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)])),
                ('is_order_placed', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('cake_variant_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.cakevariant')),
                ('cart_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basket_items', to='myapp.cart')),
                ('flavour_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.flavour')),
                ('shape_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.shape')),
                ('tag_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.tag')),
                ('weight_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.weight')),
            ],
        ),
        migrations.CreateModel(
            name='MyOrders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('house_name', models.CharField(max_length=500)),
                ('place', models.CharField(max_length=200)),
                ('pincode', models.CharField(max_length=6)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='IN')),
                ('payment_method', models.CharField(choices=[('cash', 'cash'), ('upi', 'upi')], default='cash', max_length=200)),
                ('order_id', models.CharField(max_length=200, null=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('cart_item_object', models.ManyToManyField(to='myapp.cartitems')),
                ('user_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('rating', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('cake_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cake_reviews', to='myapp.cake')),
                ('user_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='cake',
            name='tag_objects',
            field=models.ManyToManyField(to='myapp.tag'),
        ),
    ]
