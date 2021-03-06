# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import Bucketlist
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class ViewTestCase(TestCase):
    """Test suite for api views."""

    def setUp(self):
        user = User.objects.create_user('testuser')
        self.client = APIClient()
        self.client.force_authenticate(user)
        self.bucketlist_data = {'name': 'Go to Ibiza', 'owner': user.id}
        self.response = self.client.post(
            reverse('create'),
            self.bucketlist_data,
            format="json")

    def test_api_can_create_a_bucketlist(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_update_bucketlist(self):
        bucketlist = Bucketlist.objects.get()
        change_bucketlist = {'name': 'Something new'}
        res = self.client.put(
            reverse('details', kwargs={'pk': bucketlist.id}),
            change_bucketlist, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_get_a_bucket_list(self):
        bucketlist = Bucketlist.objects.get()
        res = self.client.get(
            reverse('details', kwargs={'pk': bucketlist.id}),
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_bucketlist(self):
        bucketlist = Bucketlist.objects.get()
        response = self.client.delete(
            reverse('details', kwargs={'pk': bucketlist.id}),
            format='json',
            follow=True)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)


class ModelTestCase(TestCase):
    """This class defines the test suite for the bucketlist model."""

    def setUp(self):
        """Define the test client and other test variables."""
        user = User.objects.create_user('testuser')
        self.bucketlist_name = "Write world class code"
        self.bucketlist = Bucketlist(name=self.bucketlist_name, owner=user)

    def test_model_can_create_a_bucketlist(self):
        """Test the bucketlist model can create a bucketlist."""
        old_count = Bucketlist.objects.count()
        self.bucketlist.save()
        new_count = Bucketlist.objects.count()
        self.assertNotEqual(old_count, new_count)