from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model, CharField, FloatField, ForeignKey, CASCADE, DateTimeField, ImageField

from root import settings


# Create your models here.
User = get_user_model()

class Category(Model):
    name = CharField(max_length=255)

    # mana shu modelni ko'plikda va birlikda qanday chiqishligi admin panelda
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(Model):
    class Meta:
        managed = False
        db_table = ("apps_product")
    name = CharField(max_length=255)
    description = CharField(max_length=2555)
    price = FloatField()
    category = ForeignKey(to='apps.Category', on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    father = models.ForeignKey(
        "self", related_name="children", null=True, blank=True, on_delete=models.SET_NULL
    )
    image = ImageField(upload_to='media', null=True, blank=True)
    is_unique = models.BooleanField(default=True)

    added_by = models.ForeignKey(User,
                                 null=True, blank=True, on_delete=models.SET_NULL)


    # mana shunday biror bir metod yozib uni admin.py da list_desplay ga berib yuborishimiz mumkin
    def name_count(self, ):
        return self.name.count('e')


class ProductProxy(Product):
    class Meta:
        proxy = True

