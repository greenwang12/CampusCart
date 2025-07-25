from django.contrib import admin
from .models import Item, Message, Transaction, UserProfile
from .models import Cart, CartItem
from .models import Wishlist, WishlistItem
from .models import GiftCard, GiftCardTransaction

admin.site.register(Item)
admin.site.register(Message)
admin.site.register(Transaction)
admin.site.register(UserProfile)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Wishlist)
admin.site.register(WishlistItem)
admin.site.register(GiftCard)
admin.site.register(GiftCardTransaction)
