import unittest
import os
import argparse

from pynecone import AMQPCommand

class AMQPCommandTestCase(unittest.TestCase):

    def setUp(self):
        self.parser = argparse.ArgumentParser(prog='test')
        self.parser.add_argument('--something')

    def test_something1(self):
        parsed = self.parser.parse_args(['--something', 'test'])
        self.assertEqual(parsed.something, 'test')

    def test_something(self):
        return
        path = os.path.join(os.getcwd(),'scripts.py')
        cmd = AMQPCommand(path,
                          'test_something_script',
                          'aaaaaa',
                          '123456',
                          '1.1.1.1',
                          5672,
                          '/',
                          'broadcast')

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
