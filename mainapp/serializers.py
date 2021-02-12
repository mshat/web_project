from rest_framework import serializers
from .models import Backpack, Type, Manufacturer, Material, OrderDetail, Order


class DetailOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ('number', )


#ORDER
class OrdersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


#BACKPACK
class BackpackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backpack
        fields = '__all__'


class BackpacksListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backpack
        fields = '__all__'


class BackpackDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backpack
        fields = '__all__'


# class BackpackDetailSerializer(serializers.ModelSerializer):
#     id = serializers.HiddenField(default=1)
#
#     class Meta:
#         model = Backpack
#         fields = '__all__'


#TYPE
class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class TypesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class TypeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


#MANUFACTURER
class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'


class ManufacturersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'


class ManufacturerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'


#MATERIAL
class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class MaterialsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class MaterialDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'
