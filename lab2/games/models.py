from django.db import models
from django.contrib.auth.models import User
from django.core import validators
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)

    def __str__(self):
        return self.username
    
class Game_list(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField('Название', max_length=50)
    anounce = models.CharField('Анонс', max_length=250, validators=[validators.MinLengthValidator(10)])
    discription = models.TextField('Описание')
    date = models.DateTimeField('Дата')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Ganre = models.BooleanField("ММО", default=False)
    GanreTwo = models.BooleanField("Стратегия", default=False)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, default=0.00)

    def is_purchased(self, user):
        return Purchase.objects.filter(user=user, game=self).exists()
    
    def is_purchased_by_current_user(self):
        return Purchase.objects.filter(user=self.user, game=self).exists()

    def get_absolute_url(self):
        return f'/games/{self.id}'

    def get_purchase_count(self):
        return self.purchase_set.count()
    
    def get_price(self):
        return self.price

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры' 

class UserBalance(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    balance = models.DecimalField('Баланс', max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Баланс пользователя {self.user.username}"

    def increase_balance(self, amount):
        self.balance += amount
        self.save()

    def decrease_balance(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True  # Возвращает True, если покупка успешно выполнена
        else:
            return False  # Возвращает False, если недостаточно средств

@receiver(post_save, sender=get_user_model())
def create_user_balance(sender, instance, created, **kwargs):
    if created:
        UserBalance.objects.create(user=instance)


class Purchase(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game = models.ForeignKey(Game_list, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game')  # Определяет уникальность комбинации пользователя и игры
