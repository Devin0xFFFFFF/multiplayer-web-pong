import unittest

from ....src.game.game_core.actor import Actor


class ActorTest(unittest.TestCase):
    def test_create_valid_actor(self):
        actor = Actor("id", 50, 50)

        self.assertEqual("id", actor.ID)
        self.assertEqual(True, actor.visible)
        self.assertEqual(10, actor.collisionBuffer)
        self.assertEqual(0, actor.x)
        self.assertEqual(0, actor.y)
        self.assertEqual(50, actor.width)
        self.assertEqual(50, actor.height)
        self.assertEqual(0, actor.rotation)

    def test_invalid_actor(self):
        self.failUnlessRaises(TypeError, Actor, None)
        self.failUnlessRaises(TypeError, Actor, 0)
        self.failUnlessRaises(TypeError, Actor, "id", 50, "hi")
        self.failUnlessRaises(TypeError, Actor, "id", 7.35, 3)

    def test_get_actor_state(self):
        actor = Actor("id", 50, 50)
        state = actor.get_state()

        self.assertEqual(actor.visible, state[0])
        self.assertEqual(actor.x, state[1])
        self.assertEqual(actor.y, state[2])
        self.assertEqual(actor.width, state[3])
        self.assertEqual(actor.height, state[4])
        self.assertEqual(actor.rotation, state[5])

    def test_set_position_or_rotation(self):
        actor = Actor("id", 50, 50)

        actor.set_position(10, 10)
        self.assertEqual(10, actor.x)
        self.assertEqual(10, actor.y)

        actor.set_position(0.8, 30)
        self.assertEqual(0, actor.x)

        actor.set_position(5, 15.2)
        self.assertEqual(15, actor.y)

        self.failUnlessRaises(TypeError, actor.set_position, 0, None)
        self.failUnlessRaises(TypeError, actor.set_position, "hi", 0)

        actor.set_rotation(100)
        self.assertEqual(100, actor.rotation)

        self.failUnlessRaises(TypeError, actor.set_rotation, None)

        # beyond 365
        actor.set_rotation(365)
        self.assertEqual(5, actor.rotation)

        # negative

        actor.set_rotation(-90)
        self.assertEqual(270, actor.rotation)

if __name__ == '__main__':
    unittest.main()
