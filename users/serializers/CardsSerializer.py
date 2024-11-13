from rest_framework import serializers

from users.models.models import Cards


class CardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cards
        fields = ['id', 'card_type', 'bank_name', 'balance', 'user']

class CreateCardSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=16)
    bank_name = serializers.CharField(max_length=16)