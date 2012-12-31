from django.utils import unittest

def suite():
   suite = unittest.TestLoader().loadTestsFromTestCase(MessageGeneratorTestCase)
   return suite
