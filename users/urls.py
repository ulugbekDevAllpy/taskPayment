from django.urls import path
from graphene_django.views import GraphQLView
from rest_framework.routers import DefaultRouter

from users.views import PhoneVerificationView, VerifyCodeView, AddCard, MerchantCategoryView, \
    TransactionView, MerchantView, GetCard, DeleteCard

urlpatterns = [
    #RESTAPI
    path('api/verify-phone/', PhoneVerificationView.as_view(), name='verify_phone'),
    path('api/verify-code/', VerifyCodeView.as_view(), name='verify_code'),
    path('api/add-card/', AddCard.as_view(), name='add_card'),
    path('api/cards/', GetCard.as_view(), name='get_card'),
    path('api/cards/<int:card_id>/', DeleteCard.as_view(), name='delete_card'),

    #Merchant
    path('api/merchant-categories/', MerchantCategoryView.as_view(), name='merchant_category'),
    path('api/merchants/', MerchantView.as_view(), name='merchant'),
    path('api/transactions/', TransactionView.as_view(), name='transaction'),

    #GraphQLView
    path('graphql/', GraphQLView.as_view(graphiql=True)),

]