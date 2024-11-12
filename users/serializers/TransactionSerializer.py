from rest_framework import serializers

from users.models import Transaction, Users, Cards


class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
    card_id = serializers.PrimaryKeyRelatedField(queryset=Cards.objects.all(), required=True)

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'merchant', 'phone_number', 'amount', 'ip_address', 'device_id', 'created_at', 'card_id']

    def create(self, validated_data):
        return Transaction.create_transaction(**validated_data)