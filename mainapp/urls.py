from django.urls import path
from . import views
from . import services
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.Index.as_view, name='index'),

    url(r'^backpacks/$', views.BackpackListView.as_view(), name='backpacks'),
    url(r'^backpack/(?P<pk>\d+)$', views.BackpackDetailView.as_view(), name='backpack_detail'),
    url(r'^backpacks/create/$', views.BackpackCreate.as_view(), name='backpack_create'),
    url(r'^backpack/(?P<pk>\d+)/update/$', views.BackpackUpdate.as_view(), name='backpack_update'),
    url(r'^backpack/(?P<pk>\d+)/delete/$', views.BackpackDelete.as_view(), name='backpack_delete'),

    url(r'^manufacturers/$', views.ManufacturerListView.as_view(), name='manufacturers'),
    url(r'^manufacturer/(?P<pk>\d+)$', views.ManufacturerDetailView.as_view(), name='manufacturer_detail'),
    url(r'^manufacturers/create/$', views.ManufacturerCreate.as_view(), name='manufacturer_create'),
    url(r'^manufacturer/(?P<pk>\d+)/update/$', views.ManufacturerUpdate.as_view(), name='manufacturer_update'),
    url(r'^manufacturer/(?P<pk>\d+)/delete/$', views.ManufacturerDelete.as_view(), name='manufacturer_delete'),

    url(r'^types/$', views.TypeListView.as_view(), name='types'),
    url(r'^type/(?P<pk>\d+)$', views.TypeDetailView.as_view(), name='type_detail'),
    url(r'^type/create/$', views.TypeCreateView.as_view(), name='type_create'),
    url(r'^type/(?P<pk>\d+)/update/$', views.TypeUpdate.as_view(), name='type_update'),
    url(r'^type/(?P<pk>\d+)/delete/$', views.TypeDelete.as_view(), name='type_delete'),

    url(r'^materials/$', views.MaterialListView.as_view(), name='materials'),
    url(r'^material/(?P<pk>\d+)$', views.MaterialDetailView.as_view(), name='material_detail'),
    url(r'^material/create/$', views.MaterialCreateView.as_view(), name='material_create'),
    url(r'^material/(?P<pk>\d+)/update/$', views.MaterialUpdate.as_view(), name='material_update'),
    url(r'^material/(?P<pk>\d+)/delete/$', views.MaterialDelete.as_view(), name='material_delete'),

    url(r'^orders/$', views.OrdersListView.as_view(), name='orders'),
    url(r'^order/(?P<pk>\d+)$', views.OrderDetailView.as_view(), name='order_detail'),

    url(r'^myorders/$', views.MyOrdersListView.as_view(), name='my_orders'),
    url(r'^myorder/(?P<pk>\d+)$', views.MyOrderDetailView.as_view(), name='my_order_detail'),
    url(r'^myorder/add/(?P<pk>\d+)/$', views.CartView.add_item, name='add_item'),
    url(r'^myorder/delete/(?P<pk>\d+)/$', views.CartView.delete_order, name='delete_order'),
    url(r'^myorder/pay/(?P<pk>\d+)/$', views.CartView.pay, name='pay'),

    url(r'^cart/$', views.OrderDetailListView.as_view(), name='orderdetails'),
    url(r'^cart/order$', views.CartView.order, name='order'),

    url(r'^registration/$', views.UserView.register, name='register'),
]

