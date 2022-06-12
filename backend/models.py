from django.db import models
from django.contrib.auth.models import User


class StrBoost(models.Model):
    level = models.IntegerField(default=0)
    name = models.TextField(default='Имя буста')
    description = models.TextField(default='Описание буста')
    price = models.JSONField(default=dict([(0, 10), (1, 100), (2, 1000), (3, -1)]))
    buyable = models.BooleanField(default=False)
    cur_price = models.IntegerField(default=10)
    powers = models.JSONField(default=dict([(0, 0), (1, 1), (2, 5), (3, 10)]))
    cur_power = models.IntegerField(default=0)
    level_names = models.JSONField(default=dict([(0, 'ноль'), (1, 'один'), (2, 'два'), (3, 'три')]))
    cur_level_name = models.TextField(default='ноль')

    def get_prices(self):
        return list(dict(self.price).values())[:3]

    def update(self, data):
        self.level = data['level']
        self.buyable = data['buyable']
        self.cur_price = data['cur_price']
        self.cur_power = data['cur_power']
        self.save()


class IntBoost(models.Model):
    level = models.IntegerField(default=0)
    name = models.TextField(default='Имя буста')
    description = models.TextField(default='Описание буста')
    price = models.JSONField(default=dict([(0, 10), (1, 100), (2, 1000), (3, -1)]))
    buyable = models.BooleanField(default=False)
    cur_price = models.IntegerField(default=10)
    auto_click_intervals = models.JSONField(default=dict([(0, -1), (1, 10000), (2, 5000), (3, 1000)]))
    cur_interval = models.IntegerField(default=-1)
    level_names = models.JSONField(default=dict([(0, 'ноль'), (1, 'один'), (2, 'два'), (3, 'три')]))
    cur_level_name = models.TextField(default='ноль')

    def update(self, data):
        self.level = data['level']
        self.buyable = data['buyable']
        self.cur_price = data['cur_price']
        self.cur_interval = data['cur_interval']
        self.save()


class Core(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    click_power = models.IntegerField(default=1)
    str_boosts = models.ManyToManyField(StrBoost)
    int_boosts = models.ManyToManyField(IntBoost)

    def update(self, data):
        self.coins = data['coins']
        self.click_power = data['click_power']
        str_boosts_data = data['str_boosts']
        for str_boost in str_boosts_data:
            boost = self.str_boosts.get(id=str_boost['id'])
            boost.update(str_boost)
        int_boosts_data = data['int_boosts']
        for int_boost in int_boosts_data:
            boost = self.int_boosts.get(id=int_boost['id'])
            boost.update(int_boost)
        self.save()

    def get_all_str_boost(self):
        return self.str_boosts.all()

    def get_all_int_boost(self):
        return self.int_boosts.all()
