import unittest

from commander import Commander


class TestCommander(unittest.TestCase):

    def setUp(self):
        self.commander = Commander()

    def tearDown(self):
        del self.commander
    

    def test_reader_creation(self):
        self.commander.process("create reader SomeName")
        self.assertEqual(self.commander.state.users[0].name, "SomeName")
    
    def test_writer_creation(self):
        self.commander.process("create writer SomeName")
        self.assertEqual(self.commander.state.users[0].name, "SomeName")

    def test_publisher_creation(self):
        self.commander.process("create publisher SomeName")
        self.assertEqual(self.commander.state.users[0].name, "SomeName")


if __name__ == '__main__':
    unittest.main()
    