from rest_framework import serializers

from users.models.models import Users


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['user_id', 'phone_number']

class PhoneVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13)

class VerifyCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13)
    verification_code = serializers.CharField(max_length=6)
    # first_name = serializers.CharField(max_length=255)
    # last_name = serializers.CharField(max_length=255)