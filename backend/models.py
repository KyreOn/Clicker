from django.db import models
from django.contrib.auth.models import User


class Boost(models.Model):
    level = models.IntegerField(default=0)
    price = models.IntegerField(default=10)
    buyable = models.BooleanField(default=False)


class StrBoost(Boost):
    pass


class IntBoost(Boost):
    pass


class Core(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    click_power = models.IntegerField(default=1)
    auto_click_interval = models.IntegerField(default=-1)
    str_boost = models.OneToOneField(StrBoost, null=True, on_delete=models.DO_NOTHING)
    int_boost = models.OneToOneField(IntBoost, null=True, on_delete=models.DO_NOTHING)

    def click(self):
        self.coins += self.click_power
        return self

    def str_upgrade(self):
        self.coins -= self.str_boost.price
        self.str_boost.level += 1
        self.str_boost.price = self.str_boost.price * 100
        self.click_power = 10 ** self.str_boost.level
        self.str_boost.save()

    def int_upgrade(self):
        self.coins -= self.int_boost.price
        self.int_boost.level += 1
        self.int_boost.price = self.int_boost.price * 100
        if self.int_boost.level == 0:
            self.auto_click_interval = 0
        if self.int_boost.level == 1:
            self.auto_click_interval = 10000
        if self.int_boost.level == 2:
            self.auto_click_interval = 5000
        if self.int_boost.level == 3:
            self.auto_click_interval = 1000
        self.click_power = 10 ** self.str_boost.level
        self.int_boost.save()

