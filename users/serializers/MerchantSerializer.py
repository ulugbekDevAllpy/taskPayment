from rest_framework import serializers

from users.models.models import Merchant, MerchantCategory


class MerchantSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=MerchantCategory.objects.all())  # Use PrimaryKeyRelatedField for category

    class Meta:
        model = Merchant
        fields = ['id', 'name', 'category']

    def create(self, validated_data):
        merchant = Merchant.objects.create(**validated_data)
        return merchant