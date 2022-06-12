from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import UserForm
from .models import Core, StrBoost, IntBoost
from .serializers import CoreSerializer

def base(request):
    return redirect('main')


def main(request):
    if request.user.is_authenticated:
        core = Core.objects.get(user=request.user)
    else:
        core = Core()
    return render(request, 'main.html', {'auth': request.user.is_authenticated, 'core': core})


class RegView(APIView):
    def get(self, request):
        form = UserForm()
        return render(request, 'reg.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            core = Core(user=user)
            core.save()
            sb1 = core.str_boosts.create(
                name='Сила',
                description='Закибербуленный, ты решил начать тренироваться. Из-за перекача, ты получаешь дополнительно 1/600/25000 кадуш за клик',
                level_names=dict([(0, 'Лалка'), (1, 'Сойжак'), (2, 'Гигачад'), (3, 'Босс качалки')]),
                cur_level_name='Лалка',
                powers=dict([(0, 0), (1, 1), (2, 600), (3, 25000)]),
                price=dict([(0, 10), (1, 20000), (2, 1500000), (3, -1)]),
                cur_price=10,
            )
            sb2 = core.str_boosts.create(
                name='Жирность',
                description='Ты жрешь так много фастфуда, что кнопки ломаются под весом твоих жирнющих пальцев-сосисок. Это дает тебе дополнительно 3/1250/50000 кадуш за клик',
                level_names=dict([(0, 'Нежить из дарксоулса'), (1, 'Дефолтнич'), (2, 'Пудж'), (3, 'Никокадо Авокадо')]),
                cur_level_name='Нежить из дарксоулса',
                powers=dict([(0, 0), (1, 3), (2, 1250), (3, 50000)]),
                price=dict([(0, 40), (1, 100000), (2, 17500000), (3, -1)]),
                cur_price=40,
            )
            sb3 = core.str_boosts.create(
                name='Ловкость',
                description='Ты настолько преисполнился в пути ниндзя, смотря аниме, что научился попадать в уязвимые места кнопки. Твоя техника позволяет тебе получать 5/3000/150000 дополнительных кадуш за клик',
                level_names=dict([(0, 'Криворукий'), (1, 'На скилле'), (2, 'Задрот-анимешник'), (3, 'Какаши')]),
                cur_level_name='Криворукий',
                powers=dict([(0, 0), (1, 5), (2, 3000), (3, 150000)]),
                price=dict([(0, 200), (1, 175000), (2, 80000000), (3, -1)]),
                cur_price=200,
            )
            sb4 = core.str_boosts.create(
                name='Работа',
                description='Мамка перестала давать тебе денег, поэтому ты устроился на работу. Твоя зарплата составляет 40/5000/250000 кадуш за клик',
                level_names=dict([(0, 'Каменщик без зарплаты'), (1, 'Местная пивнушка'), (2, 'МакДональдс'), (3, 'Погромист')]),
                cur_level_name='Каменьщик без зарплаты',
                powers=dict([(0, 0), (1, 40), (2, 5000), (3, 250000)]),
                price=dict([(0, 1500), (1, 400000), (2, 300000000), (3, -1)]),
                cur_price=1500,
            )
            sb5 = core.str_boosts.create(
                name='Дух',
                description='Развиваясь духовно, ты смог отделить от себя свою духовню оболочку заставить ее нажимать кнопку вместе с тобой. Она приносит 100/15000/500000 кадуш за клик',
                level_names=dict([(0, 'Облако от пердежа'), (1, 'Пар от вейпа'), (2, 'Твоя биполярка'), (3, 'Станд из жожи')]),
                cur_level_name='Облако от пердежа',
                powers=dict([(0, 0), (1, 100), (2, 15000), (3, 500000)]),
                price=dict([(0, 4500), (1, 900000), (2, 800000000), (3, -1)]),
                cur_price=4500,
            )
            ib1 = core.int_boosts.create(
                name='Интеллект',
                description='Благодаря своему нестандартному мышлению, ты понял как абузить систему и получать деньги из ничего. Кнопка нажимается сама по себе каждые 30/10/2 секунд',
                level_names=dict([(0, 'Очередняра'), (1, 'Умнич'), (2, 'Ге(ни)й'), (3, 'Высший разум')]),
                cur_level_name='Очередняра',
                auto_click_intervals=dict([(0, -1), (1, 30000), (2, 10000), (3, 2000)]),
                price=dict([(0, 150), (1, 600000), (2, 50000000), (3, -1)]),
                cur_price=150,
            )
            ib2 = core.int_boosts.create(
                name='Образование',
                description='Поняв, что ты не можешь сложить даже 2 и 2, ты решил поступить в образовательное учереждение, где научился разным лайфхакам, благодаря которым кнопка нажимается без твоей помощи каждые 20/10/1 секунд',
                level_names=dict([(0, 'Начальная школа'), (1, 'Шарага'), (2, 'Уник'), (3, 'УрФУ')]),
                cur_level_name='Начальная школа',
                auto_click_intervals=dict([(0, -1), (1, 20000), (2, 10000), (3, 1000)]),
                price=dict([(0, 1000), (1, 2500000), (2, 120000000), (3, -1)]),
                cur_price=1000,
            )
            ib3 = core.int_boosts.create(
                name='Хитрость',
                description='С помощью грубой силы и ума, ты смог заставить несколько школьников нажимать кнопку за себя. Они жмут кнопку каждые 20/5/1 секунд',
                level_names=dict([(0, 'Честный'), (1, 'Крысич'), (2, 'Мастер байтер'), (3, 'Кулко...Кукло...Куколд короче')]),
                cur_level_name='Честный',
                auto_click_intervals=dict([(0, -1), (1, 20000), (2, 5000), (3, 1000)]),
                price=dict([(0, 15000), (1, 5000000), (2, 175000000), (3, -1)]),
                cur_price=15000,
            )
            ib4 = core.int_boosts.create(
                name='Инвестиции',
                description='Ты так сильно устал работать на дядю, что решил уйти в инвестиции, чтобы получать пассивный доход. Твои грамотные вложения дают тебе кадуши каждые 15/5/0.5 секунд',
                level_names=dict([(0, 'А че это?'), (1, 'Хомячок'), (2, 'Пульсянин'), (3, 'Волк с Уолл-стрит')]),
                cur_level_name='А че это?',
                auto_click_intervals=dict([(0, -1), (1, 15000), (2, 5000), (3, 500)]),
                price=dict([(0, 50000), (1, 10000000), (2, 500000000), (3, -1)]),
                cur_price=50000,
            )
            ib5 = core.int_boosts.create(
                name='Фотосинтез',
                description='Твои долгие посиделки за компом превратили тебя в овоща. Однако теперь ты можешь превращать энергию Солнца в кадуши каждые 15/2/0.5 секунд',
                level_names=dict([(0, 'Человек в зелёнке'), (1, 'Зелёный слоник'), (2, 'Огурец'), (3, 'Подсолнух из растений против зомби')]),
                cur_level_name='Человек в зелёнке',
                auto_click_intervals=dict([(0, -1), (1, 15000), (2, 2000), (3, 500)]),
                price=dict([(0, 250000), (1, 30000000), (2, 1000000000), (3, -1)]),
                cur_price=250000,
            )

            sb1.save()
            sb2.save()
            sb3.save()
            sb4.save()
            sb5.save()
            ib1.save()
            ib2.save()
            ib3.save()
            ib4.save()
            ib5.save()
            return redirect('main')
        return render(request, 'reg.html', {'form': form})


class LoginView(APIView):
    form = UserForm()

    def get(self, request):
        return render(request, 'login.html', {'form': self.form})

    def post(self, request):
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('main')
        return render(request, 'login.html', {'form': self.form, 'invalid': True})


@login_required
def user_logout(request):
    logout(request)
    return redirect('main')


@api_view(['POST'])
def update(request):
    core = Core.objects.get(user=request.user)
    core.update(request.data['core'])
    core.save()
    return Response({'core': CoreSerializer(core).data})


@api_view(['GET'])
def get_core(request):
    core = Core.objects.get(user=request.user)
    return Response({'core': CoreSerializer(core).data})