from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Item, Message, Transaction, UserProfile

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
    owner = UserSerializer(read_only=True)  # show in response, not required in input

    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ['owner', 'posted_at']  # prevents POST issues

# ─── Message Serializer ───
class MessageSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = UserProfile
        fields = ['total_points', 'badge_level']
