from django.shortcuts import get_object_or_404
from .models import Type, Backpack, Manufacturer, Material, Order, OrderDetail
from .const import ORDER_STATUS

class ModelManager():
    '''
    Абстрактный класс-обертка для работы с моделью. 
    '''
    def __init__(self, model, *args, id=None, object=None):
        '''
        Создает объект модели, если id==None. Иначе инициализирует объект модели по id или object
        '''
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
 