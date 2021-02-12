from django.shortcuts import render
from .models import Type, Backpack, Manufacturer, Material, Order, OrderDetail, IndexImage
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import CartAddBackpackForm, RegistrationForm, TypeCreateForm
from django.views.decorators.http import require_POST
from . import services
from .services import BackpackManager, OrderDetailManager, OrderManager, UserManager, TypeManager
from django.contrib.auth.models import User, Group


class Index:
    def as_view(request):
        return render(
            request,
            'index.html',
        )


class BackpackListView(generic.ListView):
    model = Backpack

    def get_queryset(self):
        return Backpack.objects.order_by('title')

    paginate_by = 8


class BackpackDetailView(generic.DetailView):
    model = Backpack

    def get_context_data(self, **kwargs):
        context = super(BackpackDetailView, self).get_context_data(**kwargs)
        backpack_number_choices = [(i, str(i)) for i in range(1, context['backpack'].number + 1)]
        cart_backpack_form = CartAddBackpackForm(backpack_number_choices)
        context['cart_backpack_form'] = cart_backpack_form
        return context


class BackpackCreate(CreateView):
    model = Backpack
    fields = '__all__'
    #initial={'info':'',}


class BackpackUpdate(UpdateView):
    model = Backpack
    fields = '__all__'


class BackpackDelete(DeleteView):
    model = Backpack
    success_url = reverse_lazy('backpacks')


class TypeListView(generic.ListView):
    model = Type
    paginate_by = 8


class TypeDetailView(generic.DetailView):
    model = Type


class TypeCreateView(CreateView):
 
    def get(self, request, *args, **kwargs):
        context = {'form': TypeCreateForm()}
        return render(request, 'mainapp/type_form.html', context)

    def post(self, request, *args, **kwargs):
        form = TypeCreateForm(request.POST)
        if form.is_valid():
            type_name = form.cleaned_data['type']   
            type = TypeManager(type_name)
            return HttpResponseRedirect(reverse_lazy('types'))
        return render(request, 'mainapp/type_form.html', {'form': form})


class TypeUpdate(UpdateView):
    model = Type
    fields = '__all__'


class TypeDelete(DeleteView):
    model = Type
    success_url = reverse_lazy('types')


class MaterialListView(generic.ListView):
    model = Material
    paginate_by = 8


class MaterialDetailView(generic.DetailView):
    model = Material


class MaterialCreateView(CreateView):
    model = Material
    fields = '__all__'


class MaterialUpdate(UpdateView):
    model = Material
    fields = '__all__'


class MaterialDelete(DeleteView):
    model = Material
    success_url = reverse_lazy('materials')


class ManufacturerListView(generic.ListView):
    model = Manufacturer
    def get_queryset(self):
        return Manufacturer.objects.order_by('name')


class ManufacturerDetailView(generic.DetailView):
    model = Manufacturer
    paginate_by = 1


class ManufacturerCreate(CreateView):
    model = Manufacturer
    fields = '__all__'
    initial={'info':'',}


class ManufacturerUpdate(UpdateView):
    model = Manufacturer
    fields = '__all__'


class ManufacturerDelete(DeleteView):
    model = Manufacturer
    success_url = reverse_lazy('manufacturers')


class OrdersListView(LoginRequiredMixin, generic.ListView):
    model = Order
    paginate_by = 10
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.exclude(status='c').order_by('-id')
        else:
            return Order.objects.filter(buyer=self.request.user).exclude(status='c').order_by('-id')


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order

    def get_queryset(self):
        return Order.objects.order_by('-id')


class MyOrdersListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'mainapp/my_order_list.html'
    paginate_by = 10
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.exclude(status='c').order_by('-id')
        else:
            return Order.objects.filter(buyer=self.request.user).exclude(status='c').order_by('-id')


class MyOrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order
    template_name = 'mainapp/my_order_detail.html'

    def get_queryset(self):
        return Order.objects.order_by('-id')


class OrderDetailListView(LoginRequiredMixin, generic.ListView):
    """
    cart
    """
    model = OrderDetail

    def get_context_data(self, **kwargs):
        context = super(OrderDetailListView, self).get_context_data(**kwargs)
        total = 0
        for item in context['orderdetail_list']:
            total += item.total
        context['total'] = total
        return context

    def get_queryset(self):
        return OrderDetail.objects.filter(order__buyer=self.request.user).filter(ordered=False)


class CartView:

    def add_item(request, pk):
        services.add_item(request, pk, services.with_form, request)
        return HttpResponseRedirect('/catalog/cart/')

    @require_POST
    def order(request):
        buyer = request.user
        services.order(buyer)
        return HttpResponseRedirect('/catalog/myorders/')

    @require_POST
    def delete_order(request, pk):
        services.delete_order(request, pk)
        return HttpResponseRedirect('/catalog/myorders/')

    @require_POST
    def pay(request, pk):
        order = OrderManager(id=pk)
        if order:
            order.status = 'p'
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class UserView:

    def as_view(request):
        return render(
            request,
            'registration.html',
            context={},
        )

    def register(request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                login = form.cleaned_data['login']       
                password = form.cleaned_data['password']
                group = Group.objects.filter(name='Сustomer')
                services.create_user(username=login,
                                     email='',
                                     password=password
                                     )
                return HttpResponseRedirect('/accounts/login/')
        # If this is a GET (or any other method) create the default form.
        else:
            form = RegistrationForm(request.POST)

        return render(request, 'mainapp/registration.html', {'form': form})    