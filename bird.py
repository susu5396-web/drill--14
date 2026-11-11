import game_framework
from pico2d import load_image


class Bird:
    FRAMES_PER_SECOND = 12
    image = None
    image_width = 918
    image_height = 506
    frame_width = 185
    frame_height = 169
    frame_rects = tuple(
        (
            column * 183,
            image_height - (row_top + frame_height),
            min(frame_width, image_width - column * 183),
            frame_height,
        )
        for row_top, frame_count in ((0, 5), (168, 5), (337, 4))
        for column in range(frame_count)
    )

    def __init__(self, x, y):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = x, y
        self.frame = 0

    def update(self):
        self.frame = (
            self.frame + self.FRAMES_PER_SECOND * game_framework.frame_time
        ) % len(self.frame_rects)

    def draw(self):
        left, bottom, width, height = self.frame_rects[int(self.frame)]
        self.image.clip_draw(
            left, bottom, width, height, self.x, self.y, 120, 110
        )
