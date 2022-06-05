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


class IntBoost(models.Model):
    level = models.IntegerField(default=0)
    name = models.TextField(default='Имя буста')
    description = models.TextField(default='Описание буста')
    price = models.JSONField(default=dict([(0, 10), (1, 100), (2, 1000), (3, -1)]))
    buyable = models.BooleanField(default=False)
    cur_price = models.IntegerField(default=10)

    auto_click_intervals = models.JSONField(default=dict([(0, -1), (1, 10000), (2, 5000), (3, 1000)]))
    cur_interval = models.IntegerField(default=-1)

class Core(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    click_power = models.IntegerField(default=1)
    str_boosts = models.ManyToManyField(StrBoost)
    int_boosts = models.ManyToManyField(IntBoost)

    def click(self):
        self.coins += self.click_power
        self.check_for_buyable()
        return self

    def str_upgrade(self, boost_id):
        boost = self.str_boosts.get(id=boost_id)
        self.coins -= boost.cur_price
        boost.level += 1
        boost.cur_power = boost.powers[str(boost.level)]
        boost.cur_price = boost.price[str(boost.level)]
        self.click_power += boost.cur_power
        boost.save()
        self.check_for_buyable()

    def int_upgrade(self, boost_id):
        boost = self.int_boosts.get(id=boost_id)
        self.coins -= boost.cur_price
        boost.level += 1
        boost.cur_price = boost.price[str(boost.level)]
        boost.cur_interval = boost.auto_click_intervals[str(boost.level)]
        boost.save()
        self.check_for_buyable()

    def check_for_buyable(self):
        for boost in self.str_boosts.all():
            boost.buyable = self.coins >= boost.cur_price and not boost.cur_price == -1
            boost.save()
        for boost in self.int_boosts.all():
            boost.buyable = self.coins >= boost.cur_price and not boost.cur_price == -1
            boost.save()

    def get_all_str_boost(self):
        return self.str_boosts.all()

    def get_all_int_boost(self):
        return self.int_boosts.all()
