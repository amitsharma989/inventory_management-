from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Item

class ItemTests(APITestCase):
    def setUp(self):
        self.item_data = {'name': 'Test Item', 'description': 'This is a test item.'}
        self.url = reverse('create_item')

    def test_create_item(self):
        response = self.client.post(self.url, self.item_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_item(self):
        item = Item.objects.create(**self.item_data)
        response = self.client.get(reverse('read_item', args=[item.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item(self):
        item = Item.objects.create(**self.item_data)
        update_data = {'name': 'Updated Item', 'description': 'This is an updated test item.'}
        response = self.client.put(reverse('update_item', args=[item.id]), update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_item(self):
        item = Item.objects.create(**self.item_data)
        response = self.client.delete(reverse('delete_item', args=[item.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
