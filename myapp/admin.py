from django.contrib import admin

# Register your models here.
from myapp.models import Tag,Shape,Flavour,Weight,Cake,CakeVariant

#register Tag model with admin
admin.site.register(Tag)
admin.site.register(Shape)
admin.site.register(Flavour)
admin.site.register(Weight)



class CakeVarientInline(admin.TabularInline):
    model=CakeVariant
    extra=2
   

class CakeAdmin(admin.ModelAdmin):

    inlines = [CakeVarientInline]


admin.site.register(Cake,CakeAdmin)