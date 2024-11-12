
from decimal import Decimal

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import Users, Cards, MerchantCategory, Merchant
from users.serializers.CardsSerializer import CardsSerializer, CreateCardSerializer
from users.serializers.MerchantCategorySerializer import MerchantCategorySerializer
from users.serializers.MerchantSerializer import MerchantSerializer
from users.serializers.TransactionSerializer import TransactionSerializer
from users.serializers.UserSerializer import PhoneVerificationSerializer, VerifyCodeSerializer


class PhoneVerificationView(APIView):
    def post(self, request):
        serializer = PhoneVerificationSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']


            user, created = Users.objects.get_or_create(phone_number=phone_number)




            return Response({
                'message': 'Success',
                'phone_number':phone_number
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(APIView):
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            verification_code = serializer.validated_data['verification_code']
            # first_name=serializer.validated_data['first_name'],
            # last_name=serializer.validated_data['last_name']
            try:
                user = Users.objects.get(phone_number=phone_number)
                if '123456' == verification_code:
                    refresh = RefreshToken.for_user(user)
                    user.save()
                    return Response({
                        'access_token': str(refresh.access_token),
                        'user': {
                            'user_id': user.user_id,
                            'phone_number': user.phone_number,

                        }
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Code error'}, status=status.HTTP_400_BAD_REQUEST)
            except Users.DoesNotExist:
                return Response({'messgae': f'user not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCard(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request):
        # print(f"Authenticated user: {request.user}")
        if request.user.is_authenticated:
            serialize = CreateCardSerializer(data=request.data)

            if serialize.is_valid():
                card_number = serialize.validated_data['card_number']
                bank_name=serialize.validated_data['bank_name']


                card_type = "HUMO" if card_number.startswith("8600") else "UZCARD"

                Cards.objects.create(
                    user=request.user,
                    card_type=card_type,
                    bank_name=bank_name,
                    balance=request.data.get('balance', 1000),
                )

                return Response({"message": "Card Add Success"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)



class GetCard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cards = Cards.objects.filter(user=user)
        serializer = CardsSerializer(cards, many=True)
        if len(cards) == 0:
            return Response({'message': 'Karta toplinmadi'})
        return Response(serializer.data)

class DeleteCard(APIView):

    permission_classes = [IsAuthenticated]
    def delete(self, request, card_id):
        if request.user.is_authenticated:
            try:
                card = Cards.objects.get(id=card_id, user=request.user)
                card.delete()
                return Response({"message": "Card deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
            except Cards.DoesNotExist:
                return Response({"detail": "Card not found or not owned by this user."},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)

class MerchantCategoryView(APIView):

    def get(self, request):
        categories = MerchantCategory.objects.all()
        serializer = MerchantCategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MerchantCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MerchantView(APIView):

    def get(self, request):
        merchants = Merchant.objects.all()
        serializer = MerchantSerializer(merchants, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MerchantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user


        phone_number = user.phone_number


        ip_address = request.META.get('REMOTE_ADDR')


        try:
            amount = Decimal(request.data.get('amount'))
        except (ValueError, TypeError):
            return Response({"detail": "Invalid amount format."}, status=status.HTTP_400_BAD_REQUEST)

        card_id = request.data.get('card_id')

        try:

            card = Cards.objects.get(id=card_id, user=user)
            merchant_id = request.data.get('merchant')
            merchant = Merchant.objects.get(id=merchant_id)


            if card.balance < amount:
                return Response({"message": ""}, status=status.HTTP_400_BAD_REQUEST)

        except Cards.DoesNotExist:
            return Response({"detail": "Karta topilmadi yoki foydalanuvchi kartasi emas."}, status=status.HTTP_400_BAD_REQUEST)
        except Merchant.DoesNotExist:
            return Response({"detail": "Merchant topilmadi."}, status=status.HTTP_400_BAD_REQUEST)


        data = request.data.copy()
        data['user'] = user.id
        data['phone_number'] = phone_number
        data['ip_address'] = ip_address
        data['card'] = card.id
        data['amount'] = amount

        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

