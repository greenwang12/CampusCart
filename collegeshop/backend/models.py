from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# ───── Item Model ─────

class Item(models.Model):
    CATEGORY_CHOICES = [
        ('books', 'Books'),
        ('electronics', 'Electronics'),
        ('stationery', 'Stationery'),
        ('sports', 'Sports'),
        ('others', 'Others'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='items/', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    available = models.BooleanField(default=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ───── Message Model ─────

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}"

# ───── Transaction Model ─────

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    points_earned = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.item.title}"

# ───── User Profile Model ─────

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)
    badge_level = models.CharField(max_length=50, default='Newbie')

    def add_points(self, points):
        self.total_points += points
        self.update_badge()
        self.save(update_fields=["total_points", "badge_level"])

    def update_badge(self):
        if self.total_points >= 100:
            self.badge_level = "Champion"
        elif self.total_points >= 50:
            self.badge_level = "Contributor"
        elif self.total_points >= 10:
            self.badge_level = "Sharer"
        else:
            self.badge_level = "Newbie"

    def __str__(self):
        return f"{self.user.username} ({self.total_points} pts, {self.badge_level})"

# ───── Signals ─────

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=Transaction)
def reward_on_transaction(sender, instance, created, **kwargs):
    if created and instance.completed:
        profile = UserProfile.objects.get(user=instance.user)
        profile.add_points(instance.points_earned or 10)
