from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    ItemViewSet, MessageViewSet, TransactionViewSet, RegisterView,
    UserProfileView, CartViewSet, CartItemViewSet,
    WishlistViewSet, WishlistItemViewSet,
    GiftCardViewSet, GiftCardTransactionViewSet,
    api_home 
)

# Register ViewSets with router
router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)
router.register(r'wishlists', WishlistViewSet)
router.register(r'wishlist-items', WishlistItemViewSet)
router.register(r'giftcards', GiftCardViewSet)
router.register(r'giftcard-transactions', GiftCardTransactionViewSet)

# ✅ NO extra "api/" prefix here!
urlpatterns = [
    path('', api_home, name='api-home'),  # now /api/
    path('', include(router.urls)),       # now /api/items/, etc.
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
