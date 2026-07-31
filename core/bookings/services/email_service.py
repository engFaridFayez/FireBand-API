from django.conf import settings
from django.core.mail import EmailMultiAlternatives

def send_booking_email(booking):
    subject = f"New Booking🥳🎫✅ - {booking.full_name}"

    body = f"""
A new booking has been submitted.

Customer Information
--------------------
Name: {booking.full_name}
Phone: {booking.phone}
Email: {booking.email}

Event Information
-----------------
Date: {booking.event_date}
Time: {booking.event_time}
Location: {booking.location}

Booking Details
---------------
Category: {booking.category.name}
Sub Category: {booking.sub_category.name}
Duration: {booking.duration.title}
Members: {booking.team_members}

Custom Sub Category:
{booking.custom_sub_category or "-"}

Notes:
{booking.notes or "-"}
"""

    message = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=[settings.EMAIL_HOST_USER],
    )

    message.send()