import random
import uuid
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('telefon raqimini kiriting!!!!!/....')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser):

    user_id=models.UUIDField(default=uuid.uuid4(),unique=True)
    #+998990085903
    phone_number=models.CharField(max_length=13,blank=True,unique=True)
    first_name=models.CharField(max_length=255,blank=True)
    last_name=models.CharField(max_length=255)

    objects=UserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    # def generate_verification_code(self):
    #     self.verification_code = "123456"
    #     self.save()


    def __str__(self):
        return f"{self.user_id} {self.phone_number}"


class Cards(models.Model):
    user=models.ForeignKey(Users,related_name='cards',on_delete=models.CASCADE)
    card_type = models.CharField(max_length=10)
    bank_name = models.CharField(max_length=100)
    balance=models.DecimalField(max_digits=12, decimal_places=2)

    objects = models.Manager()

class MerchantCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Merchant(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(MerchantCategory, related_name='merchants', on_delete=models.CASCADE)


    def __str__(self):
        return self.name


class Transaction(models.Model):
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    ip_address = models.GenericIPAddressField()
    device_id = models.CharField(max_length=100)
    card_id = models.ForeignKey(Cards, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('success', 'Success'), ('failed', 'Failed')])
    created_at = models.DateTimeField(auto_now_add=True)  # Transaction yaratish vaqti

    def __str__(self):
        return f"Transaction {self.id} - {self.status}"

    @classmethod
    def create_transaction(cls, user, merchant, phone_number, amount, ip_address, device_id, card_id):


        if card_id.balance < amount:
            raise ValueError("Kartada pul yoq")


        card_id.balance -= amount
        card_id.save()

        transaction = cls.objects.create(
            user=user,
            merchant=merchant,
            phone_number=phone_number,
            amount=amount,
            ip_address=ip_address,
            device_id=device_id,
            status='success',
            card_id=card_id
        )
        return transaction