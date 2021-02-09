from mainapp.services import ModelManager, BackpackManager, OrderManager, MaterialManager
from mainapp.services import OrderDetailManager, UserManager, TypeManager, ManufacturerManager
from django.contrib.auth.models import User


class Builder():

    def product(self): pass


class TypeBuilder(Builder):
    
    def __init__(self):
        self.reset()

    def reset(self):
        self._type_name = None

    @property
    def product(self):
        if not self._type_name:
            self._type_name = 't_name'
        product = TypeManager(self._type_name) 
        self.reset()
        return product.object

    def setup(self, type_name):
        if isinstance(type_name, str):
            self._type_name = type_name

    @property
    def type_name(self):
        return self._type_name

    @type_name.setter
    def type_name(self, name):
        if isinstance(name, str):
            self._type_name = name


class ManufacturerBuilder(Builder):
    
    def __init__(self):
        self.reset()

    def reset(self):
        self._name = None
        self._info = None
        self._country = None
    
    @property
    def product(self):
        if not self._name:
            self._name = 'novatour'
        if not self._info:
            self._info = 'info'
        if not self._country:
            self._country = 'Russia'
        product = ManufacturerManager(self._name, self._info, self._country)
        self.reset()
        return product.object

    def setup(self, name=None, info=None, country=None):
        if isinstance(name, str):
            self._name = name
        if isinstance(info, str):
            self._info = info
        if isinstance(country, str):
            self._country = country


class MaterialBuilder(Builder):

    def __init__(self):
        self.reset()

    def reset(self):
        self._name = None
        self._is_waterproof = None
        self._density = None

    @property
    def product(self):
        if not self._name:
            self._name = 'oxford'
        if not self._is_waterproof:
            self._is_waterproof = True
        if not self._density:
            self._density = 300
        product = MaterialManager(self._name, self._is_waterproof, self._density)
        self.reset()
        return product.object

    def setup(self, name=None, is_waterproof=None, density=None):
        if isinstance(name, str):
            self._name = name
        if isisinstance(is_waterproof, bool):
            self._is_waterproof = is_waterproof
        if isinstance(density, (int, double)):
            self._density = density


class UserBuilder(Builder):
    
    def __init__(self):
        self.reset()

    def reset(self):
        self._login = None
        self._email = None
        self._password = None

    @property
    def product(self):
        if not self._login:
            self._login = 'login'
        if not self._email:
            self._email = 'email@mail.ru'
        if not self._password:
            self._password = 'pA$$w0rd'
        product = User.objects.create_user(self._login, self._email, self._password)
        self.reset()
        return product

    def setup(self, login=None, email=None, password=None):
        if isinstance(login, str):
            self._login = login
        if isinstance(email, str):
            self._email = email
        if isinstance(password, str):
            self._password = password


class OrderBuilder(Builder):

    def __init__(self):
        self.reset()

    def reset(self):
        self._buyer = None
        self._total = None
        self._product = None

    @property
    def product(self):
        if not self._total:
            self._total = 0
        if not self._buyer:
            builder = UserBuilder()
            self._buyer = builder.product
        product = OrderManager(self._buyer, self._total)
        self.reset()
        return product.object

    def build_buyer(self, login, email, password):
        builder = UserBuilder()
        builder.setup(login, email, password)
        self._buyer = builder.product

    @property
    def buyer(self):
        return self._buyer

    @buyer.setter
    def buyer(self, user):
        if isinstance(user, User):
            self._buyer = user

    @property
    def total(self, total):
        return total

    @total.setter
    def total(self, total):
        if isinstance(total, (int, float)):
            self._total = total


class BackpackBuilder(Builder):
    
    def __init__(self):
        self.reset()

    def reset(self):
        self._title = None
        self._info = None
        self._price = None
        self._size = None
        self._number = None
        self._color = None
        self._manufacturer = None
        self._type = None
        self._material = None

    @property
    def product(self):
        if not self._title:
            self._title = 'title'
        if not self._info:
            self._info = 'info'
        if not self._price:
            self._price = 100
        if not self._size:
            self._size = 50
        if not self._number:
            self._number = 100
        if not self._color:
            self._color = 'b'
        if not self._manufacturer:
            self._manufacturer = self.build_manufacturer()
        product = BackpackManager(
            self._title, self._info, self._price, self._size, self._number, self._color, self._manufacturer,
            )
        # todo не могу добавить type=self._type, material=self._material, потому что
        # в init ModelManager нет **kwargs. Чтобы его добавить надо поменять порядок
        # аргументов в init ModelManager
        self.reset()
        return product.object

    def setup(self, title=None, info=None, price=None, size=None, number=None, color=None):
        if isinstance(title, str):
            self._title = title
        if isinstance(info, str):
            self._info = info
        if isinstance(price, (int, float)):
            self._price = price 
        if isinstance(size, (int, float)):
            self._size = size 
        if isinstance(number, (int, float)):
            self._number = number
        if isinstance(color, str):
            self._color = color

    def build_manufacturer(self, name=None, info=None, country=None):
        builder = ManufacturerBuilder()
        builder.setup(name, info, country)
        self._manufacturer = builder.product

    def build_type(self, type_name=None):
        builder = TypeBuilder()
        builder.setup(type_name)
        self._type = builder.product

    def build_material(self, name=None, is_waterproof=None, density=None):
        builder = MaterialBuilder()
        builder.setup(name, is_waterproof, density)
        self._material = builder.product


class OrderDetailBuilder(Builder):

    def __init__(self):
        self.reset()

    def reset(self):
        self._order = None
        self._backpack = None
        self._number = None
        self._total = None

    @property
    def product(self):
        if not self._order:
            builder = OrderBuilder()
            self._order = builder.product
        if not self._backpack:
            builder = BackpackBuilder()
            self._backpack = builder.product
        if not self._numbere:
            self._number = 10
        if not self._total:
            self._total = 100
        product = OrderDetailManager(self._order, self._backpack, self._number, self._total)
        self.reset()
        return product.object

    def setup(self, number=None, total=None):
        if isinstance(number, (int, float)):
            self._number = number
        if isinstance(total, (int, float)):
            self._total = total

    def build_order(self, login=None, email=None, password=None):
        buider = OrderBuilder()
        builder.setup(login, email, password)
        return builder.product

    def build_backpack(
        self,
        manufacturer_name=None, manufacturer_info=None, manufacturer_country=None, 
        type_name=None, 
        material_name=None, material_is_waterproof=None, material_density=None, 
        title=None, info=None, price=None, size=None, number=None, color=None
        ):
        builder = BackpackBuilder()
        builder.build_manufacturer(manufacturer_name, manufacturer_info, manufacturer_country)
        builder.build_material(material_name, material_is_waterproof, material_density)
        builder.build_type(type_name)
        builder.setup(title, info, price, size, number, color)
        return builder.product