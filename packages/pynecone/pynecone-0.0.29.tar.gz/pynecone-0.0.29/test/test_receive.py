import unittest
import os
import argparse

from pynecone import ReceiveCommand

import dotenv
found_dotenv = dotenv.find_dotenv(usecwd=True)

if found_dotenv:
    dotenv.load_dotenv(found_dotenv)


class ReceiveCommandTestCase(unittest.TestCase):

    def setUp(self):
        self.parser = argparse.ArgumentParser(prog='test')
        ReceiveCommand().add_arguments(self.parser)

    def test_something1(self):
        return
        parsed = self.parser.parse_args(['--something', 'test', '--blah', 'kiki'])
        self.assertEqual(parsed.something, 'test')

    def test_something(self):

        path = os.getcwd() + '\\test\\receive_scripts.py'
        args = self.parser.parse_args([path, 'test_handle'])

        res = ReceiveCommand().run(args)

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
