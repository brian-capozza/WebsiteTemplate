"""
admin.py

Custom admin site using Django OTP (TOTP) for two-factor authentication.

This module defines an OTP-enabled admin interface to enhance security for the
Django admin backend. It uses the django-otp library with TOTP (Time-based One-Time Passwords).

The admin site can be imported into the project and used in place of the default `admin.site`.

Includes:
- A custom `OTPAdmin` class extending `OTPAdminSite`
- Registration of TOTPDevice with TOTPDeviceAdmin for managing user devices
"""

from django.contrib import admin
from django_otp.admin import OTPAdminSite
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin

from WebsiteTemplate.settings import TOTP_ADMIN


class OTPAdmin(OTPAdminSite):
    """
    Custom admin site that enforces OTP verification for admin users.

    This is a subclass of `OTPAdminSite`, provided by `django-otp`, which wraps the default
    Django admin and requires users to complete two-factor authentication to access it.
    """
    pass


# Instance of the OTP-enabled admin site, used in place of Django's default `admin.site`
admin_site = OTPAdmin(name='OTPAdmin')
# Register TOTP devices so they can be managed through the admin interface
admin_site.register(TOTPDevice, TOTPDeviceAdmin)
