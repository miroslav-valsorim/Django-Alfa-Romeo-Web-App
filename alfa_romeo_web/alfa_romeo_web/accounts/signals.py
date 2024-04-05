from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from alfa_romeo_web import settings
from alfa_romeo_web.accounts.models import Profile

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def user_created(sender, instance, created, **kwargs):
    # created = False, when update
    # create = True, when create
    if created:
        # Eager save
        Profile.objects.create(user=instance)
        send_successful_registration_email(instance)


def send_successful_registration_email(instance):
    email_content = render_to_string('email/successful_registration.html', {
        'user': instance,
    })

    send_mail(
        subject='Welcome to Alfa Romeo Django Web Project!',
        message=strip_tags(email_content),
        html_message=email_content,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=(instance.email,),
    )