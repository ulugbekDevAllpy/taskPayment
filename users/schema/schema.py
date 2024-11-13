import graphene
from graphene_django.types import DjangoObjectType
from users.models.models import Users, Cards, Merchant, Transaction, MerchantCategory


class UserType(DjangoObjectType):
    class Meta:
        model = Users
        fields = ("user_id", "phone_number", "first_name", "last_name", "verification_code")


class CardType(DjangoObjectType):
    class Meta:
        model = Cards
        fields = ("id", "user", "card_type", "bank_name", "balance")


class MerchantCategoryType(DjangoObjectType):
    class Meta:
        model = MerchantCategory
        fields = ("id", "name")


class MerchantType(DjangoObjectType):
    class Meta:
        model = Merchant
        fields = ("id", "name", "category")


class TransactionType(DjangoObjectType):
    class Meta:
        model = Transaction
        fields = ("id", "user", "merchant", "phone_number", "amount", "ip_address", "device_id", "card_id", "status", "created_at")


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    merchant_categories=graphene.List(MerchantCategoryType)
    merchants=graphene.List(MerchantType)
    user = graphene.Field(UserType, user_id=graphene.String())
    transactions = graphene.List(TransactionType)
    transaction = graphene.Field(TransactionType, transaction_id=graphene.Int())


    def resolve_users(self, info):
        return Users.objects.all()



    def resolve_merchant_categories(self,info):
        return  MerchantCategory.objects.all()

    def resolve_merchants(self, info):
        return Merchant.objects.all()

    def resolve_user(self, info, user_id):
        return Users.objects.get(user_id=user_id)


    def resolve_transactions(self, info):
        return Transaction.objects.all()


    def resolve_transaction(self, info, transaction_id):
        return Transaction.objects.get(id=transaction_id)


class CreateCard(graphene.Mutation):
    class Arguments:
        user_id = graphene.String()
        card_type = graphene.String()
        bank_name = graphene.String()
        balance = graphene.Decimal()

    card = graphene.Field(CardType)
    success = graphene.Boolean()

    def mutate(self, info, user_id, card_type, bank_name, balance):
        try:

            user = Users.objects.get(user_id=user_id)


            card = Cards.objects.create(
                user=user,
                card_type=card_type,
                bank_name=bank_name,
                balance=balance
            )


            return CreateCard(card=card, success=True)
        except Exception as e:

            return CreateCard(card=None, success=False)



class CreateTransaction(graphene.Mutation):
    class Arguments:
        user_id = graphene.String()
        merchant_id = graphene.Int()
        phone_number = graphene.String()
        amount = graphene.Decimal()
        ip_address = graphene.String()
        device_id = graphene.String()
        card_id = graphene.Int()

    transaction = graphene.Field(TransactionType)
    success = graphene.Boolean()

    def mutate(self, info, user_id, merchant_id, phone_number, amount, ip_address, device_id, card_id):
        try:

            user = Users.objects.get(user_id=user_id)
            merchant = Merchant.objects.get(id=merchant_id)
            card = Cards.objects.get(id=card_id)


            transaction = Transaction.create_transaction(
                user=user,
                merchant=merchant,
                phone_number=phone_number,
                amount=amount,
                ip_address=ip_address,
                device_id=device_id,
                card_id=card
            )
            return CreateTransaction(transaction=transaction, success=True)
        except Exception as e:
            return CreateTransaction(transaction=None, success=False)

class Mutation(graphene.ObjectType):
    create_transaction = CreateTransaction.Field()
    create_card = CreateCard.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)