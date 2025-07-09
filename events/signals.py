from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Event, Participant

@receiver(m2m_changed, sender=Participant.events.through)
def send_rsvp_confirmation_email(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        for event_id in pk_set:
            try:
                event = Event.objects.get(pk=event_id)
                send_mail(
                    subject='RSVP Confirmation',
                    message=f'Thank you {instance.name} for RSVPing to {event.name}!',
                    from_email='rahmanmdatiar75@gmail.com',
                    recipient_list=[instance.email],
                    fail_silently=False,
                )
            except Event.DoesNotExist:
                pass
