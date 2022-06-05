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
    str_boosts = StrBoostSerializer(source='get_all_str_boost', many=True)
    int_boosts = IntBoostSerializer(source='get_all_int_boost', many=True)
    class Meta:
        model = Core
        fields = ['coins', 'click_power', 'str_boosts', 'int_boosts']




