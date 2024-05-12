from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=50, verbose_name='телефон', **NULLABLE)
    city = models.CharField(max_length=100, verbose_name='город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Pay(models.Model):
    PAYMENT_METHOD = [
        ('1', 'наличные'),
        ('2', 'банковский перевод')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    pay_date = models.DateField(auto_now_add=True, verbose_name='дата платежа')
    paid_course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name='оплаченный курс', **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, verbose_name='оплаченный урок', **NULLABLE)
    payment_amount = models.FloatField(verbose_name='сумма платежа')
    payment_method = models.CharField(choices=PAYMENT_METHOD, verbose_name='способ оплаты')

    def __str__(self):
        if self.paid_course:
            return f'{self.pay_date} - {self.paid_course} - {self.payment_amount} руб.'
        return f'{self.pay_date} - {self.paid_lesson} - {self.payment_amount} руб.'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
