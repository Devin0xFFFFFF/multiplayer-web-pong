import unittest

from ....src.game.game_core.command import Command

from ....src.game.game_core.actor import Actor


class CommandTest(unittest.TestCase):
    def test_create_command(self):
        command = Command(b'id', "set_position", [0, 0])

        self.assertEqual(command.targetID, b'id')
        self.assertEqual(command.action, "set_position")
        self.assertListEqual([0, 0], command.args)

        self.failUnlessRaises(TypeError, Command, "id", "set_position", [0, 0])

    def test_serialize_command(self):
        command = Command(b'id', "set_position", [0, 0])

        data = command.serialize()

        self.assertIsNotNone(data)
        self.assertIsInstance(data, list)
        self.assertEqual(3, len(data))

        self.assertEqual(b'id', data[0])
        self.assertEqual("set_position", data[1])
        self.assertEqual([0, 0], data[2])

    def test_invalid_commands(self):
        self.failUnlessRaises(TypeError, Command, None, "set_position", [0, 0])

        self.failUnlessRaises(TypeError, Command, b'id', None, [0, 0])

        self.failUnlessRaises(TypeError, Command, b'id', "set_position", None)

    def test_command_execution(self):
        target = Actor(b'actor1')
        target2 = Actor(b'actor2')
        target3 = object()

        cmd1 = Command(b'actor1', "set_position", [100, 100])

        cmd1.execute(target)
        self.assertEqual(100, target.x)
        self.assertEqual(100, target.y)

        self.failUnlessRaises(AttributeError, cmd1.execute, None)
        self.failUnlessRaises(NameError, cmd1.execute, target2)
        self.failUnlessRaises(AttributeError, cmd1.execute, target3)


if __name__ == '__main__':
    unittest.main()
