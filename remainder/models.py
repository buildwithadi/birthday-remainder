from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

NOTIFICATION_PREFERENCE_CHOICES = [
    ('same_day', 'Same day'),
    ('one_day_before', 'One day before'),
    ('two_days_before', 'Two days before'),
]

# Create your models here.
class User(AbstractUser):
    notification_preference = models.CharField(
        max_length=50,
        choices=NOTIFICATION_PREFERENCE_CHOICES,
        default='same_day', # Set a default value
        verbose_name="Notification Preference"
    )

    def __str__(self):
        return self.username
    
class Contact(models.Model):
    user = models.ForeignKey(
        to = settings.AUTH_USER_MODEL,  # connected to
        on_delete = models.CASCADE,     # to avoid orphan rows
        related_name='contacts',        # related table(shortname)
    )
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.name} for {self.user.username}"
    
class EmailReminder(models.Model):
    contact = models.ForeignKey(
        to = 'Contact',             # connected to
        on_delete = models.CASCADE, # to avoid orphan rows
        related_name = 'reminders'  # related table(shortname)
    )

    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Remainder for {self.contact.name}"