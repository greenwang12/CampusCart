# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Item, Message, Transaction, UserProfile, Cart, CartItem, Wishlist, WishlistItem, GiftCard, GiftCardTransaction

# ─── User Serializer ───
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# ─── Registration Serializer ───
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

# ─── Item Serializer ───
class ItemSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ['owner', 'posted_at']

    def validate_price(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cartitem_set', many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'user', 'items']

class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = '__all__'

class WishlistSerializer(serializers.ModelSerializer):
    items = WishlistItemSerializer(source='wishlistitem_set', many=True, read_only=True)
    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'items']
        # serializers.py

class GiftCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftCard
        fields = '__all__'

class GiftCardTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftCardTransaction
        fields = '__all__'

# ─── Message Serializer ───
class MessageSerializer(serializers.ModelSerializer):
    receiver = serializers.SlugRelatedField(
        slug_field='username',  # This ensures we're matching by the username
        queryset=User.objects.all(),  # Queryset to look up the User model
        required=True  # Optional: make sure the receiver is always provided
    )
    sender = serializers.ReadOnlyField(source='sender.username')  # We get the sender username automatically
 
    class Meta:
        model = Message
        fields = '__all__'


# ─── Transaction Serializer ───
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

# ─── User Profile Serializer ───
class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'total_points', 'badge_level']
