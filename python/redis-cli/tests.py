import unittest

import resp

class TestRespEncoding(unittest.TestCase):

    def test_simple_string(self):
        self.assertEqual(resp.encode('PING', True), '+PING\r\n')

    def test_error(self):
        self.assertEqual(resp.encode(ValueError('Unknown command')), '-Unknown command\r\n')

    def test_integer(self):
        self.assertEqual(resp.encode(23), ':23\r\n')

    def test_bulk_string(self):
        self.assertEqual(resp.encode('foobar'), '$6\r\nfoobar\r\n')

    def test_array(self):
       self.assertAlmostEqual(resp.encode([2,3]), '*2\r\n:2\r\n:3\r\n')

class TestRespDecoding(unittest.TestCase):

    def test_simple_string(self):
        self.assertEqual(resp.decode('+PING\r\n'), 'PING')

    def test_error(self):
        self.assertEqual(resp.decode('-Error 2\r\n'), 'Error 2')

    def test_integer(self):
        self.assertEqual(resp.decode( ':23\r\n'), 23)

    def test_bulk_string(self):
        self.assertEqual(resp.decode('$6\r\nfoobar\r\n'), 'foobar')

    def test_array(self):
        self.assertEqual(resp.decode('*2\r\n:2\r\n:3\r\n'), [2, 3])


if __name__ == '__main__':
    unittest.main()
