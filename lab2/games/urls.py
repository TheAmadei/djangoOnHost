from django.urls import path
from . import views
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path('', views.purchased_games, name='games'),
    path('create', views.create, name='create'),
    path('<int:pk>', views.GameDetailView.as_view(), name='game_detail'),
    path('<int:pk>/update', staff_member_required(views.GameUpdateView.as_view()), name='game-update'),
    path('<int:pk>/delete', staff_member_required(views.GameDeleteView.as_view()), name='game-delete'),
    path('purchase/<int:game_id>/', views.purchase_game, name='purchase_game'),

]
