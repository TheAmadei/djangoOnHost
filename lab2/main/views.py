from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from games.models import CustomUser, Game_list, Purchase, UserBalance
from django.http import HttpResponse
from django.contrib import messages
from .forms import PurchaseForm, RegistrationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, FormView

def index(request):
    records = Game_list.objects.order_by('-date')
    return render(request, 'main/index.html', {'records': records})

class register(FormView):
    form_class = RegistrationForm
    template_name = 'registration/register.html'
    success_url = '/accounts/login/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)  

@login_required
def profile(request):
    user = request.user
    user_balance = UserBalance.objects.get(user=user)
    context = {'user_balance': user_balance.balance}
    return render(request, 'main/profile.html', context)
# Create your views here.
