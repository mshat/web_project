from rest_framework import serializers
from .models import Backpack


class BackpackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backpack
        fields = '__all__'


class BackpacksListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backpack
        fields = ('title', 'number')


class BackpackDetailSerializer(serializers.ModelSerializer):
    #todo 2 строчки ниже сделаны для примера, позже удалить
    #price = serializers.HiddenField(default=serializers.CurrentUserDefault)
    price = serializers.HiddenField(default=1000)

    class Meta:
        model = Backpack
        fields = '__all__'
