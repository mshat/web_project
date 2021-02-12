from django.shortcuts import get_object_or_404
from .models import Type, Backpack, Manufacturer, Material, Order, OrderDetail
from .const import ORDER_STATUS
from .forms import CartAddBackpackForm, RegistrationForm, TypeCreateForm
from django.contrib.auth.models import User


class ModelManager:
    """
    Абстрактный класс-обертка для работы с моделью. 
    """
    def __init__(self, model, *args, id=None, object=None):
        """
        Создает объект модели, если id==None. Иначе инициализирует объект модели по id или object
        """
        self._model = model
        if id:
            self._object = get_object_or_404(model, id=id)
            if not self._object:
                raise Exception('Object with id %d not found' % id)
        elif object:
            if isinstance(object, model):
                self._object = object
                self._object.save()
            else:
                raise TypeError('odject is not instance of model')
        elif args:
            try:
                self._object = self._model.objects.create_object(*args)
            except AttributeError as e:
                raise AttributeError(e)


    @property
    def model(self):
        return self._model

    @property
    def object(self):
        return self._object

    @object.setter
    def object(self, object):
        self._object = object

    def delete_object(self):
        self._object.delete()

    @property
    def id(self):
        return self._object.id


class BackpackManager(ModelManager):
    def __init__(self, *args, id=None, object=None):
        super().__init__(Backpack, *args, id=id, object=object)
    
    @property
    def price(self):
        return self._object.price

    @property
    def number(self):
        return self._object.number
    
    @number.setter
    def number(self, value):
        self._object.number = value
        self._object.save()


class OrderManager(ModelManager):
    def __init__(self, *args, id=None, object=None):
        super().__init__(Order, *args, id=id, object=object)

    @property
    def total(self):
        return self._object.total

    @total.setter
    def total(self, value):
        if isinstance(value, int):
            self._object.total = value
            self._object.save()
    
    @property
    def status(self):
        return self._object.status

    @status.setter
    def status(self, value):
        values = [c[0] for c in ORDER_STATUS]
        if value in values:
            self._object.status = value
            self._object.save()


class OrderDetailManager(ModelManager):
    def __init__(self, *args, id=None, object=None):
        super().__init__(OrderDetail, *args, id=id, object=object)

    @property
    def total(self):
        return self._object.total

    @property
    def ordered(self):
        return self._object.ordered

    @ordered.setter
    def ordered(self, value):
        if isinstance(value, bool):
            self._object.ordered = value
            self._object.save()


class UserManager(ModelManager):
    def __init__(self, *args, id=None, object=None):
        super().__init__(OrderDetail, *args, id=id, object=object)


class TypeManager(ModelManager):
    def __init__(self, *args, id=None, object=None):
        super().__init__(Type, *args, id=id, object=object)


class ManufacturerManager(ModelManager):
    def __init__(self, *args, id=None, object=None):
        super().__init__(Manufacturer, *args, id=id, object=object)


class MaterialManager(ModelManager):
    def __init__(self, *args, id=None, object=None):
        super().__init__(Material, *args, id=id, object=object)


#todo переделать в объектный стиль функции ниже
def add_item(request, pk, func, arg):
    """
    Добавляет Item в корзину. func принимает with_form или with_serializer в зависимости от того, откуда пришел
    запрос на добавление итема. В arg передается, соответственно, request или serializer
    """
    buyer = request.user
    order_objects = Order.objects.filter(buyer=buyer).filter(status='c')
    if order_objects:
        order_object = order_objects[0]
    else:
        raise Exception('Orders from this user do not exist in the table')
    order = OrderManager(object=order_object)
    backpack = BackpackManager(id=pk)
    func(arg, backpack, order)


def with_form(request, backpack, order):
    form = CartAddBackpackForm([(i, str(i)) for i in range(1, backpack.number + 1)], request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        ordered_products_number = cd['number']
        total = ordered_products_number * backpack.price
        OrderDetailManager(order.object, backpack.object, ordered_products_number, total)
        order.total += total
        backpack.number -= ordered_products_number


def with_serializer(serializer, backpack, order):
    number = serializer.data.get('number')
    total = number * backpack.price
    OrderDetailManager(order.object, backpack.object, number, total)
    order.total += total
    backpack.number -= number


def create_default_order(buyer):
    OrderManager(buyer, 0)


def create_user(username, password, email=''):
    user = User.objects.create_user(username, email, password)
    create_default_order(user)


def delete_order(request, pk):
    order = OrderManager(id=pk)
    if order:
        buyer = order.object.buyer
        order_details = OrderDetail.objects.filter(order=order.object)
        for item in order_details:
            BackpackManager(object=item.backpack).number += item.number
            OrderDetailManager(object=item).delete_object()
        order.delete_object()
    if len(Order.objects.filter(buyer=buyer)) == 0:
        create_default_order(buyer)


def order(buyer):
    """
    Говнокод. Из спика всех order_details собирается корзина данного покупателя и создается заказ.
    """
    order_details = OrderDetail.objects.filter(order__buyer=buyer).filter(ordered=False)
    if order_details:
        this_order = OrderManager(object=order_details[0].order)
        this_order.status = 'o'
        create_default_order(buyer)
        for item in order_details:
            OrderDetailManager(object=item).ordered = True


