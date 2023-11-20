from django.db.models import Manager

class OrderManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)