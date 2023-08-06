# python import - http://docs.python.org/library/unittest.html
import unittest
from datetime import date
from io import StringIO

from nose.tools import assert_is_not_none, assert_equal

from cfonb import StatementReader
from cfonb.writer.statement import Statement, number_format


class TestStatement(unittest.TestCase):

    def test_render_parse_cfonb(self):
        content = Statement().header('20002', '90005', 'EUR', '01711467640', date(2011, 10, 14), 12345.67)\
                             .add('20002', '1234567', '90005', 'EUR', '01711467640', date(2011, 10, 14), 'label 1', 1234.56, 'reference1')\
                             .add('20002', '1234567', '90005', 'EUR', '01711467640', date(2011, 10, 13), 'label 2', 123.45, 'reference2')\
                             .render()
        print('content: {}'.format(content))
        reader = StatementReader()
        result = reader.parse(StringIO(content))
        for account in result:
            assert_is_not_none(account.account_nb)
            assert_equal(account.header.get('account_nb'), '01711467640')
            assert_equal(account.header.get('currency_code'), 'EUR')
            assert_equal(account.header.get('nb_of_dec'), '2')
            assert_equal(account.header.get('bank_code'), '20002')

    def test_number_format(self):
        assert_equal(number_format(123), '12C')
        assert_equal(number_format(123.45), '1234E')
        assert_equal(number_format(-123.45), '1234N')
        assert_equal(number_format(-12340), '1234}')
        assert_equal(number_format(12340), '1234{')
        assert_equal(number_format(None), '')
        assert_equal(number_format(''), '')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestStatement('test_parse_cfonb'))
    suite.addTest(TestStatement('test_number_format'))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=1).run(suite())
