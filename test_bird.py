import unittest
from unittest.mock import DEFAULT, MagicMock, patch

import game_framework
import game_world
from bird import Bird
from bird_flock import BirdFlock
import play_mode


class BirdTests(unittest.TestCase):
    def setUp(self):
        self.previous_frame_time = game_framework.frame_time
        game_framework.frame_time = 0
        Bird.image = None

    def tearDown(self):
        game_framework.frame_time = self.previous_frame_time
        Bird.image = None

    def test_sprite_sheet_has_fourteen_frames(self):
        self.assertEqual(len(Bird.frame_rects), 14)

    @patch('bird.get_canvas_width', return_value=1600)
    @patch('bird.load_image')
    def test_update_advances_animation_and_wraps_at_edge(
            self, load_image, get_canvas_width):
        game_framework.frame_time = 1
        bird = Bird(1600, 300, direction=1, speed=100, frame=13)

        bird.update()

        self.assertEqual(bird.frame, 11)
        self.assertEqual(bird.x, -60)

    @patch('bird.load_image')
    def test_left_facing_bird_is_flipped_horizontally(self, load_image):
        bird = Bird(100, 300, direction=-1)
        bird.image = MagicMock()

        bird.draw()

        self.assertEqual(bird.image.clip_composite_draw.call_args.args[5], 'h')

    @patch('bird.load_image')
    @patch('bird_flock.get_canvas_width', return_value=1600)
    def test_flock_contains_ten_varied_birds(self, get_canvas_width,
                                              load_image):
        flock = BirdFlock()

        self.assertEqual(len(flock.birds), 10)
        self.assertEqual(
            {bird.direction for bird in flock.birds}, {-1, 1}
        )
        self.assertGreater(len({bird.speed for bird in flock.birds}), 1)
        self.assertEqual(
            len({bird.frame for bird in flock.birds}), 10
        )


class PlayModeTests(unittest.TestCase):
    def setUp(self):
        game_world.clear()

    def tearDown(self):
        play_mode.finish()

    def test_init_registers_bird_flock_with_existing_objects(self):
        with patch.multiple(
                play_mode, Boy=DEFAULT, BirdFlock=DEFAULT, Grass=DEFAULT
        ) as objects:
            play_mode.init()

            self.assertIn(objects['Boy'].return_value, game_world.world[1])
            self.assertIn(
                objects['BirdFlock'].return_value, game_world.world[1]
            )
            self.assertIn(objects['Grass'].return_value, game_world.world[0])


if __name__ == '__main__':
    unittest.main()
