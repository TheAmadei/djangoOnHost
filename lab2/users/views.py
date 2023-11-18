from django.shortcuts import render
from games.models import Game_list, CustomUser
from django.contrib.auth.models import User

def user_records(request):
    records = Game_list.objects.filter(user=request.user)
    return render(request, 'users/users.html', {'records': records})

def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'users/users.html', {'users': users})

def listOfUserRecords(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    records = Game_list.objects.filter(user=user)
    return render(request, 'users/listOfUserRecord.html', {'user': user, 'records': records})
# Create your views here.
