# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your models here.
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver


class Bucketlist(models.Model):
    """This class represents the bucketlist model."""
    name = models.CharField(max_length=255, blank=False, unique=True)
    owner = models.ForeignKey('auth.User',
                              on_delete=models.CASCADE,
                              related_name='bucketlists')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    @property
    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
