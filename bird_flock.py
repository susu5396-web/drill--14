from pico2d import get_canvas_width

from bird import Bird


class BirdFlock:
    BIRD_COUNT = 10
    HEIGHTS = (450, 390, 330, 270, 210)

    def __init__(self):
        canvas_width = get_canvas_width()
        margin = 100
        spacing = (canvas_width - margin * 2) / (self.BIRD_COUNT - 1)
        self.birds = [
            Bird(
                margin + spacing * index,
                self.HEIGHTS[index % len(self.HEIGHTS)],
                direction=1 if index % 2 == 0 else -1,
                speed=70 + (index % 4) * 12,
                frame=index * len(Bird.frame_rects) // self.BIRD_COUNT,
            )
            for index in range(self.BIRD_COUNT)
        ]

    def update(self):
        for bird in self.birds:
            bird.update()

    def draw(self):
        for bird in self.birds:
            bird.draw()
