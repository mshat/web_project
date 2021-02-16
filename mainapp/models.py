from django.db import models
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns
import uuid  # Required for unique order instances
from django.contrib.auth.models import User
from datetime import datetime
from .const import ORDER_STATUS, COLORS


class BackpackManager(models.Manager):
    """
    Менеджер используется для создания объекта модели: Order.objects.create_order_detail(*args)
    """

    def create_object(self, title, info, price, size, number, color, manufacturer, type=None, material=None):
        backpack = self.create(
            title=title, info=info, price=price, size=size, number=number, color=color, manufacturer=manufacturer
        )
        # type=type, material=material, #я не могу указывать эти аргументы, тк они many-to-many
        # todo эти аргументы можно добавлять в объект через .add
        return backpack


class Backpack(models.Model):
    title = models.CharField(max_length=200)
    info = models.TextField(max_length=2000, blank=True, null=True)
    manufacturer = models.ForeignKey('Manufacturer', null=True,
                                     on_delete=models.SET_NULL)  # , help_text="Select a manufacturer for this backpack")
    type = models.ManyToManyField('Type', blank=True, null=True, help_text="Select a type for this backpack")
    material = models.ManyToManyField('Material', blank=True, null=True,
                                      help_text="Select a materials for this backpack")
    price = models.IntegerField(help_text="Enter a price for this backpack")
    size = models.IntegerField(help_text="Enter a size for this backpack")
    number = models.IntegerField(default=0)

    color = models.CharField(max_length=1, choices=COLORS)

    objects = BackpackManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a particular backpack instance.
        """
        return reverse('backpack_detail', args=[str(self.id)])

    def display_type(self):
        """
        Creates a string for the type. This is required to display type in Admin.
        """
        return ', '.join([type.type for type in self.type.all()[:3]])

    display_type.short_description = 'Type'


class TypeManager(models.Manager):
    """
        Менеджер используется для создания объекта модели: Order.objects.create_order_detail(*args)
    """

    def create_object(self, type_name):
        type = self.create(type=type_name)
        return type


class Type(models.Model):
    """
    Model representing a backpack type (e.g. Tourism backpack, city backpack etc.).
    """
    type = models.CharField(max_length=200, help_text="Enter a type (e.g. Tourism backpack, city backpack etc.)")

    objects = TypeManager()

    def __str__(self):
        return self.type

    def get_absolute_url(self):
        """
       Returns the url to access a particular backpack instance.
       """
        return reverse('type_detail', args=[str(self.id)])


class ManufacturerManager(models.Manager):
    """
    Менеджер используется для создания объекта модели: Order.objects.create_order_detail(*args)
    """

    def create_object(self, name, info, country):
        manufacturer = self.create(name=name, info=info, country=country)
        return manufacturer


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    info = models.TextField(max_length=2000, blank=True, null=True)
    country = models.CharField(max_length=100)

    objects = ManufacturerManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
       Returns the url to access a particular backpack instance.
       """
        return reverse('manufacturer_detail', args=[str(self.id)])


class MaterialManager(models.Manager):
    """
        Менеджер используется для создания объекта модели: Order.objects.create_order_detail(*args)
    """

    def create_object(self, name, is_waterproof, density):
        object = self.create(name=name, is_waterproof=is_waterproof, density=density)
        return object


class Material(models.Model):
    name = models.CharField(max_length=100)
    isWaterproof = models.BooleanField()
    density = models.IntegerField(blank=True, null=True)

    objects = MaterialManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
       Returns the url to access a particular backpack instance.
       """
        return reverse('material_detail', args=[str(self.id)])


class OrderManager(models.Manager):
    """
        Менеджер используется для создания объекта модели: Order.objects.create_order_detail(*args)
    """

    def create_object(self, buyer, total):
        order = self.create(buyer=buyer, total=total)
        return order


class Order(models.Model):
    order_id = models.UUIDField(default=uuid.uuid4, help_text="Unique ID for this order")
    creation_date = models.DateField(default=datetime.now().date())
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.IntegerField()

    status = models.CharField(max_length=1, choices=ORDER_STATUS, default='c')

    objects = OrderManager()

    def __str__(self):
        return '{0}'.format(self.id)

    def get_absolute_url(self):
        return reverse('my_order_detail', args=[str(self.id)])

    def get_absolute_url_for_staff(self):
        return reverse('order_detail', args=[str(self.id)])


class OrderDetailManager(models.Manager):
    """
        Менеджер используется для создания объекта модели: OrderDetail.objects.create_order_detail(*args)
    """

    def create_object(self, order, backpack, number, total):
        order_detail = self.create(order=order, backpack=backpack, number=number, total=total)
        return order_detail


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    backpack = models.ForeignKey(Backpack, on_delete=models.SET_NULL, null=True)
    number = models.IntegerField()
    ordered = models.BooleanField(default=False)
    total = models.IntegerField(default=0)

    objects = OrderDetailManager()

    def __str__(self):
        if self.backpack:
            res = 'order item {0}'.format(self.backpack.title)
        else:
            res = 'order item'
        return res


class IndexImage(models.Model):
    home_image = models.ImageField()
