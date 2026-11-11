import game_framework
from pico2d import get_canvas_width, load_image


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

    def __init__(self, x, y, direction=1, speed=90, frame=0):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = x, y
        self.frame = frame % len(self.frame_rects)
        self.direction = direction
        self.speed = speed

    def update(self):
        self.frame = (
            self.frame + self.FRAMES_PER_SECOND * game_framework.frame_time
        ) % len(self.frame_rects)
        self.x += self.direction * self.speed * game_framework.frame_time
        canvas_width = get_canvas_width()
        if self.x < -60:
            self.x = canvas_width + 60
        elif self.x > canvas_width + 60:
            self.x = -60

    def draw(self):
        left, bottom, width, height = self.frame_rects[int(self.frame)]
        flip = '' if self.direction > 0 else 'h'
        self.image.clip_composite_draw(
            left, bottom, width, height, 0, flip,
            self.x, self.y, 120, 110
        )
