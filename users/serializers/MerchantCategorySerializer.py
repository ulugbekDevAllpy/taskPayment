from rest_framework import serializers
from users.models import MerchantCategory, Merchant, Transaction

class MerchantCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantCategory
        fields = ['id', 'name', ]
