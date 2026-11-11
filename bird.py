import game_framework
from pico2d import get_canvas_width, load_image


IMAGE_WIDTH = 918
IMAGE_HEIGHT = 506
FRAME_WIDTH = 185
FRAME_HEIGHT = 169
FRAME_RECTS = tuple(
    (
        column * 183,
        IMAGE_HEIGHT - (row_top + FRAME_HEIGHT),
        min(FRAME_WIDTH, IMAGE_WIDTH - column * 183),
        FRAME_HEIGHT,
    )
    for row_top, frame_count in ((0, 5), (168, 5), (337, 4))
    for column in range(frame_count)
)


class Bird:
    FRAMES_PER_SECOND = 12
    image = None
    frame_rects = FRAME_RECTS

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
