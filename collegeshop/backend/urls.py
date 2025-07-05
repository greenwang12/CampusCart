from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    ItemViewSet, MessageViewSet, TransactionViewSet,
    RegisterView, UserProfileView
)

router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
