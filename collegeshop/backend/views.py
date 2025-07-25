from rest_framework import viewsets, generics, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import (
    Item, Message, Transaction, UserProfile,
    Cart, CartItem, Wishlist, WishlistItem, GiftCard, GiftCardTransaction
)
from .serializers import (
    ItemSerializer, MessageSerializer, TransactionSerializer,
    RegisterSerializer, UserProfileSerializer,
    CartSerializer, CartItemSerializer,
    WishlistSerializer, WishlistItemSerializer,
    GiftCardSerializer, GiftCardTransactionSerializer
)
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response

# Item ViewSet
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Item.objects.all().order_by('-posted_at')
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__iexact=category)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Message ViewSet
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-timestamp')
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter messages by logged-in user
        user = self.request.user
        return Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)

# Transaction ViewSet
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

# User Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# User Profile View
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)
    
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def checkout(self, request):
        # Your checkout logic here
        return Response({'status': 'checkout completed'})

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

class WishlistItemViewSet(viewsets.ModelViewSet):
    queryset = WishlistItem.objects.all()
    serializer_class = WishlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class GiftCardViewSet(viewsets.ModelViewSet):
    queryset = GiftCard.objects.all()
    serializer_class = GiftCardSerializer
    permission_classes = [permissions.IsAuthenticated]

class GiftCardTransactionViewSet(viewsets.ModelViewSet):
    queryset = GiftCardTransaction.objects.all()
    serializer_class = GiftCardTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

# API Home Page
def api_home(request):
    return HttpResponse("""
        <html>
            <head>
                <title>Co API</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background: #f4f4f4;
                        color: #333;
                        padding: 40px;
                        text-align: center;
                    }
                    h1 {
                        color: #1c87c9;
                        margin-bottom: 10px;
                    }
                    p {
                        font-size: 18px;
                        margin-bottom: 20px;
                    }
                    ul {
                        list-style: none;
                        padding: 0;
                    }
                    li {
                        margin: 10px 0;
                    }
                    a {
                        text-decoration: none;
                        color: #0077cc;
                        font-weight: bold;
                    }
                    a:hover {
                        color: #005999;
                    }
                </style>
            </head>
            <body>
                <h1>🎉 CampusCart API</h1>
                <p>Welcome to the backend! Use the links below to access available API endpoints:</p>
                <ul>
                   <li><a href="/api/register/">Register</a></li>
                   <li><a href="/api/token/">Login (JWT Token)</a></li>
                   <li><a href="/api/token/refresh/">Refresh Token</a></li>
                   <li><a href="/api/profile/">User Profile</a></li>
                   <li><a href="/api/items/">Item Listings</a></li>
                   <li><a href="/api/messages/">Messages</a></li>
                   <li><a href="/api/transactions/">Transactions</a></li>
                   <li><a href="/api/carts/">Carts</a></li>
                   <li><a href="/api/cart-items/">Cart Items</a></li>
                   <li><a href="/api/wishlists/">Wishlists</a></li>
                   <li><a href="/api/wishlist-items/">Wishlist Items</a></li>
                   <li><a href="/api/giftcards/">Gift Cards</a></li>
                   <li><a href="/api/giftcard-transactions/">Gift Card Transactions</a></li>
                   <li><a href="/admin/">Admin Panel</a></li>
            </ul>
            </body>
        </html>
    """)
