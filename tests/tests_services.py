import os
import django
import sys
sys.path.append('D:\git\shop2\onlineshop')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

import unittest
from unittest.mock import Mock, patch
from django.shortcuts import get_object_or_404
from django.test import SimpleTestCase, TestCase

from mainapp.services import ModelManager, BackpackManager, OrderManager, OrderDetailManager, UserManager, TypeManager
from mainapp.models import Type, Backpack, Manufacturer, Material, Order, OrderDetail
from mainapp.const import ORDER_STATUS, COLORS
from data_builders import TypeBuilder, ManufacturerBuilder, MaterialBuilder, UserBuilder, OrderBuilder, BackpackBuilder


class ModelManagerTests(TestCase):
    '''
    Тестирует абстрактный класс-обертку для работы с моделью. 
    '''
    def setUp(self):
        self.mocked_model = Mock()
        self.test_args = [1, '2', True]

    def test_constructor_create(self):
        """
        Создается ли экземпляр модели при инициализации экземпляра ModelManager?
        Лондонский стиль.
        """
        model_manager = ModelManager(self.mocked_model, *self.test_args)
        self.mocked_model.objects.create_object.assert_called_with(*self.test_args)
    
    #@unittest.skip('Почему-то не работает :с')
    @patch('django.shortcuts.get_object_or_404')
    def test_constructor_get_by_id(self, get_object_mock):
        """
        Инициализируется ли экземпляр ModelManager через готовый объект?
        Лондонский стиль. Проверяю, вызвалась ли функция, возвращающая объект из БД
        для инициализации нового экземпляра.
        """
        #model_manager = ModelManager(self.mocked_model, *self.test_args)
        model_manager = ModelManager(Type, 'name')
        model_manager2 = ModelManager(Type, id=model_manager.id)
        get_object_mock.assert_called_with(self.mocked_model, 1)

    def test_constructor_get_by_id_classic(self):
        """
        Инициализируется ли экземпляр ModelManager через объект из бд по id?
        """
        model_manager1 = ModelManager(Type, 'name')
        model_manager2 = ModelManager(Type, id=model_manager1.id)
        self.assertEqual(model_manager2.object, model_manager1.object)  
    
    def test_constructor_get_by_other_object(self):
        """
        Инициализируется ли экземпляр ModelManager через готовый объект, передаваемый в качестве аргумента?
        """
        other_object_mock = Type()
        model_manager = ModelManager(Type, *self.test_args, object=other_object_mock)
        self.assertEqual(model_manager.object, other_object_mock)  

    def test_constructor_get_by_wrong_other_object(self):
        """
        Поднимется ли ошибка при попытке инициалализации ModelManager через готовый объект неправильного типа?
        """
        other_object_mock = Mock()
        self.assertRaises(TypeError, ModelManager, Type, *self.test_args, object=other_object_mock)

    def test_property_getter_model(self):
        """
        Проверяет свойство model
        """
        model_manager = ModelManager(self.mocked_model, *self.test_args)
        self.assertEqual(model_manager.model, self.mocked_model)

    def test_property_getter_object(self):
        """
        Проверяет свойство object
        """
        other_object_mock = Type()
        model_manager = ModelManager(Type, *self.test_args, object=other_object_mock)
        self.assertEqual(model_manager.object, other_object_mock)

    def test_property_setter_object(self):
        """
        Проверяет свойство object
        """
        type_args = 'type_name'
        model_manager = ModelManager(Type, type_args)
        other_object_mock = Mock()
        model_manager.object = other_object_mock
        self.assertEqual(model_manager.object, other_object_mock)

    def test_delete_object(self):
        """
        Проверяет удаление объекта (записи в бд)
        """
        model_manager = ModelManager(self.mocked_model, *self.test_args)
        other_object_mock = Mock(name='object_to_delete')
        model_manager.object = other_object_mock
        model_manager.delete_object()
        other_object_mock.delete.assert_called_with()
        

class BackpackManagerTests(TestCase):
    '''
    Тестирует класс-обертку для работы с моделью Backpack
    '''
    def setUp(self):
        builder = ManufacturerBuilder()
        manufacturer = builder.product
        self.test_args = {
            'title': 'title', 
            'info': 'info', 
            'price': 100,
            'size': 10, 
            'number': 10, 
            'color': COLORS[0][0], 
            'manufacturer': manufacturer
            }

    def test_property_getter_price(self):
        """
        Проверяет свойство price
        """
        test_price = 20
        self.test_args['price'] = test_price
        manager = BackpackManager(*self.test_args.values())
        self.assertEqual(manager.price, test_price)

    def test_property_getter_number(self):
        """
        Проверяет свойство number
        """
        test_number = 20
        self.test_args['number'] = test_number
        manager = BackpackManager(*self.test_args.values())
        self.assertEqual(manager.number, test_number)
    
    def test_property_setter_number(self):
        """
        Проверяет свойство number
        """
        test_number = 20
        manager = BackpackManager(*self.test_args.values())
        manager.number = test_number
        self.assertEqual(manager.number, test_number)


class OrderManagerTests(TestCase):
    '''
    Тестирует класс-обертку для работы с моделью Order
    '''
    def setUp(self):
        builder = UserBuilder()
        buyer = builder.product
        self.test_args = {
            'buyer': buyer, 
            'total': 12345, 
            }

    def test_property_getter_total(self):
        """
        Проверяет свойство total
        """
        test_total = 30
        self.test_args['total'] = test_total
        manager = OrderManager(*self.test_args.values())
        self.assertEqual(manager.total, test_total)

    def test_property_setter_total(self):
        """
        Проверяет свойство total
        """
        test_total = 30
        manager = OrderManager(*self.test_args.values())
        manager.total = test_total
        self.assertEqual(manager.total, test_total)
    
    def test_property_getter_status(self):
        """
        Проверяет свойство status. Для нового объекта статус должен быть 'c'.
        """
        manager = OrderManager(*self.test_args.values())
        self.assertEqual(manager.status, 'c')

    def test_property_setter_status(self):
        """
        Проверяет свойство status
        """
        manager = OrderManager(*self.test_args.values())
        test_status = ORDER_STATUS[1][0]
        manager.status = test_status
        self.assertEqual(manager.status, test_status)


class OrderDetailManagerTests(TestCase):
    '''
    Тестирует класс-обертку для работы с моделью OrderDetail
    '''
    def setUp(self):
        order_builder = OrderBuilder()
        order = order_builder.product
        builder = BackpackBuilder()
        backpack = builder.product
        self.test_args = {
            'order': order, 
            'backpack': backpack, 
            'number': 10, 
            'total': 1234,
            }

    def test_property_getter_total(self):
        """
        Проверяет свойство total
        """
        test_total = 30
        self.test_args['total'] = test_total
        manager = OrderDetailManager(*self.test_args.values())
        self.assertEqual(manager.total, test_total)
    
    def test_property_getter_ordered(self):
        """
        Проверяет свойство ordered. Для нового объекта свойство должно быть False
        """
        manager = OrderDetailManager(*self.test_args.values())
        self.assertEqual(manager.ordered, False)
    
    def test_property_setter_ordered(self):
        """
        Проверяет свойство ordered
        """
        manager = OrderDetailManager(*self.test_args.values())
        manager.ordered = True
        self.assertEqual(manager.ordered, True)


if __name__ == "__main__":
    unittest.main()
