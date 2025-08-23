# remainder/tasks.py

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
import datetime

from .models import Contact, User

@shared_task
def send_birthday_reminders():
    """
    Celery periodic task to check for upcoming birthdays and send emails.
    """
    today = timezone.localdate()

    # Find contacts with birthdays either today or tomorrow
    contacts_with_birthday_today = Contact.objects.filter(
        date_of_birth__month=today.month,
        date_of_birth__day=today.day,
    )

    tomorrow = today + datetime.timedelta(days=1)
    contacts_with_birthday_tomorrow = Contact.objects.filter(
        date_of_birth__month=tomorrow.month,
        date_of_birth__day=tomorrow.day,
        user__notification_preference='one_day_before', # Check for users with the preference
    )
    
    # Combine the two querysets
    contacts_to_remind = list(contacts_with_birthday_today) + list(contacts_with_birthday_tomorrow)

    for contact in contacts_to_remind:
        user = contact.user
        
        # Build the email context to pass to the template
        context = {
            'contact_name': contact.name,
            'user_name': user.first_name,
        }

        subject = f"Don't Forget! It's {contact.name}'s Birthday!"
        
        # Render the HTML template
        html_message = render_to_string('email_template.html', context)
        
        # We also create a plain text version for compatibility
        plain_message = f"Hey {user.first_name},\n\nJust a friendly reminder: it's {contact.name}'s birthday today! Don't forget to send them a message and make their day special."

        send_mail(
            subject=subject,
            message=plain_message, # This is the plain text fallback
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"Sent HTML reminder for {contact.name} to {user.email}")
