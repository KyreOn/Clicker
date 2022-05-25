from rest_framework import serializers
from .models import Core, StrBoost, IntBoost


class StrBoostSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrBoost
        fields = '__all__'


class IntBoostSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntBoost
        fields = '__all__'


class CoreSerializer(serializers.ModelSerializer):
    str_boost = StrBoostSerializer()
    int_boost = IntBoostSerializer()
    class Meta:
        model = Core
        fields = ['coins', 'click_power', 'str_boost', 'int_boost', 'auto_click_interval']





