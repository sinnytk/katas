from django.db import models
from django.db.models.functions import Concat
from datetime import date, timedelta


class PersonQuerySet(models.QuerySet):
    def with_extra_fields(self):
        return self.annotate(
            full_name=Concat("first_name", models.Value(" "), "last_name")
        )

    def experienced(self):
        return self.filter(join_date__lt=date.today() - timedelta(days=1000))

    def number_of_unique_last_names(self):
        return self.aggregate(count=models.Count("last_name", distinct=True)["count"])

    def active(self):
        """Users with >=5 orders in the last 30 days"""
        days_ago_30 = date.today() - timedelta(days=30)
        return self.annotate(
            order_count=models.Count(
                "order", filter=models.Q(order__sale_date__gte=days_ago_30)
            ),  # get number of orders made in the past 30 days
        ).filter(order_count__gte=5)
