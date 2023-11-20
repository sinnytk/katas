from datetime import date
from django.db import models
from my_app.managers import OrderManager

from my_app.querysets import PersonQuerySet

class Person(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    join_date = models.DateField(default=date.today)
    
    objects = PersonQuerySet.as_manager()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

class Order(models.Model):
    seller = models.ForeignKey("Person", on_delete=models.CASCADE)
    sale_date = models.DateField(default=date.today)
    deleted = models.BooleanField(default=False)

    objects = OrderManager() # filters out deleted=True
    historical = models.Manager() # includes deleted=True as well