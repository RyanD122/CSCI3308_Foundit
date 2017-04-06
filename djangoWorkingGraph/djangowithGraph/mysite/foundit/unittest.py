import unittest
import re
import views
from django.tests import TestCase, Client

class MyTests(TestCase):
    def test_forms(self):
        response = self.client.get("/my/form/"{'something':'something')
        self.assertFormError(response, 'form', 'something', 'This field is required.')
