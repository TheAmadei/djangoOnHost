from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Game_list, UserBalance, Purchase
from .forms import GamesForm, PurchaseForm
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import DetailView, UpdateView, DeleteView

def user_records(request):
    records = Game_list.objects.filter(user=request.user)
    return render(request, 'users/users.html', {'records': records})

@login_required
def purchase_game(request, game_id):
    game = get_object_or_404(Game_list, id=game_id)
    user = request.user

    # Проверяем, куплена ли уже игра
    if game.is_purchased(user):
        messages.error(request, 'Вы уже купили эту игру.')
        return redirect('games')

    # Получаем цену игры
    price = game.get_price()

    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            # Используем цену игры вместо введенной пользователем суммы
            amount = price

            # Проверяем, достаточно ли средств на балансе пользователя
            user_balance = UserBalance.objects.get(user=user)
            if user_balance.balance >= amount:
                # Уменьшаем баланс пользователя
                user_balance.decrease_balance(amount)

                # Создаем запись о покупке
                Purchase.objects.create(user=user, game=game)

                messages.success(request, 'Вы успешно купили игру!')
                return redirect('games')
            else:
                messages.error(request, 'Недостаточно средств на балансе.')
    else:
        # Используем initial для передачи цены в скрытое поле формы
        form = PurchaseForm(initial={'amount': price})

    return render(request, 'games/purchase_game.html', {'game': game, 'form': form})

@staff_member_required
def create(request):
    error = ''
    if request.method == 'POST':
        form = GamesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:home')
        else:
            error = 'Форма заполнена неправильно'

    form = GamesForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'games/create.html', data)

@login_required
def purchased_games(request):
    user = request.user
    purchased_games = Purchase.objects.filter(user=user).select_related('game')

    return render(request, 'games/games_home.html', {'purchased_games': purchased_games})

class GameDetailView(DetailView):
    model = Game_list
    template_name = 'games/details_view.html'
    context_object_name = 'game'

class GameUpdateView(UpdateView):
    model = Game_list
    template_name = 'games/create.html'
    form_class = GamesForm

class GameDeleteView(DeleteView):
    model = Game_list
    template_name = 'games/Delete.html'
    success_url = '/games/'


# Create your views here.   
