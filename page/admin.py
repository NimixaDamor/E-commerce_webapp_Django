from django.contrib import admin
from .models import Product,AddItem,Contact,Category,Checkout,OrderDetail

class AdminProduct(admin.ModelAdmin):
    list_display = ['name','price','category']


@admin.action(description='Accept selected orders')
def accept_orders(modeladmin, request, queryset):
    queryset.update(status='Accepted')

@admin.action(description='Reject selected orders')
def reject_orders(modeladmin, request, queryset):
    queryset.update(status='Cancel')


class AdminOrder(admin.ModelAdmin):
    list_display = ['id','user','product_name','total','quantity','status','order_date']
    actions = [accept_orders, reject_orders]




admin.site.register(Product,AdminProduct)
admin.site.register(AddItem)
admin.site.register(Contact)
admin.site.register(Category)
admin.site.register(Checkout)

admin.site.register(OrderDetail,AdminOrder)



# nimixa11 :123

