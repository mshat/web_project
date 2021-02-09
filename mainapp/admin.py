from django.contrib import admin

from .models import Backpack, Type, Manufacturer, Material, Order, OrderDetail, IndexImage
#for model in (Backpack, Type, Manufacturer, Material):
#    admin.site.register(model)

admin.site.register(Type)

# Register the Admin classes for models using the decorator

@admin.register(Backpack)
class BackpackAdmin(admin.ModelAdmin):
    list_display = ('title', 'manufacturer', 'price', 'display_type')

@admin.register(Manufacturer) 
class ManufacturerAdmin(admin.ModelAdmin):
    list_filter = ('country',)

@admin.register(Material) 
class MaterialAdmin(admin.ModelAdmin):
    pass

@admin.register(Order) 
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(OrderDetail) 
class OrderDetailAdmin(admin.ModelAdmin):
    pass

@admin.register(IndexImage) 
class IndexAdmin(admin.ModelAdmin):
    pass

