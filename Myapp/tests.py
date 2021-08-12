from django.test import TestCase

# Create your tests here.
import uuid

a = str(uuid.uuid1())
print(a.replace('-', ''))
