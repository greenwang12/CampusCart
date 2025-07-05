from django.contrib import admin
from .models import Item, Message, Transaction, UserProfile

admin.site.register(Item)
admin.site.register(Message)
admin.site.register(Transaction)
admin.site.register(UserProfile)
