import thelca.http
import unittest

class TestHTTP(unittest.TestCase):

    def test_versions(self):
        self.assertEqual('TheElectricCat/0', thelca.http.Handler.server_version)
        self.assertEqual('X', thelca.http.Handler.sys_version)

if __name__ == '__main__':
    unittest.main()
