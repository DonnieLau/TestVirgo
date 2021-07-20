import unittest
from Myapp.HTMLRunner import HTMLTestRunner


class Test(unittest.TestCase):

    def test_01(self):
        print("第一步")


def run(case_id, case_name):
    suit = unittest.makeSuite(Test)
    filename = 'Myapp/templates/reports/%s.html' % case_id
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(fp, title='TestVirgo平台测试报告：%s' % case_name, description='用例描述')
    runner.run(suit)
