from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    contract = models.CharField("Номер договора", max_length=200)
    item = models.CharField("Вещь", max_length=200)
    client = models.CharField("Клиент", max_length=200)
    phone = models.CharField("Телефон", max_length=200)
    branch = models.CharField("Филиал", max_length=200)
    service = models.CharField("Вид услуги", max_length=200)
    price = models.DecimalField("Стоимость услуги, руб.", max_digits=10, decimal_places=2)
    urgency = models.DecimalField("Надбавка за срочность, %", max_digits=10, decimal_places=2)
    complexity = models.DecimalField("Надбавка за сложность, %", max_digits=10, decimal_places=2)
    discount = models.DecimalField("Скидка, %", max_digits=10, decimal_places=2)
    receive_date = models.DateField("Дата приема")
    return_date = models.DateField("Дата возврата")
    text = models.TextField("Примечание")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор записи")
    created_date = models.DateField("Дата создания записи", auto_now_add=True)

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return "%s: %s" % (self.contract, self.item)

    def get_excerpt(self):
        return self.text[:140] + "..." if len(self.text) > 140 else self.text

    def get_cost(self):
        # к оплате: стоимость услуги с надбавками за срочность и сложность и со скидкой
        markup = 100 + self.urgency + self.complexity
        return round(self.price * markup / 100 * (100 - self.discount) / 100, 2)
