# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import unittest

# Create your tests here.
# 单元测试
def sumF(x,b):
    return x + b

class Testsum(unittest.TestCase):
    def test_int(self):
        self.assertEqual(sumF(1,3),5)

if __name__ == '__main__':
    unittest.main()