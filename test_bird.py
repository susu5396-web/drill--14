import unittest
from unittest.mock import patch

import game_framework
from bird import Bird
from bird_flock import BirdFlock


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


if __name__ == '__main__':
    unittest.main()
