from rest_framework import serializers
from users.models.models import MerchantCategory


class MerchantCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantCategory
        fields = ['id', 'name', ]
