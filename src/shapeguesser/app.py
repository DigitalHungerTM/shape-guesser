from toga import App, Font, Window, Canvas, rgb
from toga.style import Pack
from typing import Any, List, NamedTuple
import logging
import math
import largestinteriorrectangle as lir
import numpy as np

logger = logging.Logger(name=__name__, level=logging.DEBUG)

class Point(NamedTuple):
    x: float
    y: float

class Rect(NamedTuple):
    x: float
    y: float
    width: float
    height: float

    @property
    def area(self) -> float:
        return self.width * self.height


def value_to_color(value: float):
    value = max(0.0, min(1.0, value))
    red = int(255 * (1 - value))
    green = int(255 * value)
    return rgb(red, green, 0)


class ShapeGuesser(App):
    main_window: Window
    canvas: Canvas
    last_point: Point
    path: List[Point]
    com: Point

    def reset(self):
        # clear the canvas
        self.canvas.root_state.drawing_actions.clear()
        self.canvas.redraw()

        self.last_point = Point(0, 0)

        self.path = list()

        self.com = Point(0, 0)

    def startup(self):
        self.canvas = Canvas(style=Pack(flex=1), on_press=self.on_press, on_release=self.on_release, on_drag=self.on_drag)

        self.reset()

        self.main_window = Window(title=self.formal_name)  # type: ignore
        self.main_window.content = self.canvas
        
        self.main_window.show()

    def on_press(self, widget: Canvas, x: int, y: int, **kwargs: Any):
        logger.info("Mouse Pressed")

        self.reset()

        self.last_point = Point(x, y)
    
    def on_drag(self, widget: Canvas, x: int, y: int, **kwargs: Any):
        self.canvas.begin_path()
        self.canvas.move_to(*self.last_point)
        self.canvas.line_to(x, y)
        self.canvas.stroke(color="black", line_width=3)


        # only record a point to path when it is at least one pixel away from the last
        if len(self.path) == 0:
            self.path.append(Point(x, y))
        else:
            diff_x = self.path[-1].x - x
            diff_y = self.path[-1].y - y
            dist = math.sqrt(diff_x**2 + diff_y**2)
            if dist > 1:
                self.path.append(Point(x, y))

        self.last_point = Point(x, y)

    def on_release(self, widget: Canvas, x: int, y: int, **kwargs: Any):
        if len(self.path) == 0:
            return

        self.score_square()

    def find_com(self):
        sum_x = 0
        sum_y = 0
        for point in self.path:
            sum_x += point.x
            sum_y += point.y
        
        avg_x = sum_x / len(self.path)
        avg_y = sum_y / len(self.path)

        self.com = Point(avg_x, avg_y)

    def find_inner_bounding_box(self):
        l: list[tuple[int, int]] = list(map(lambda p: (int(p.x), int(p.y)), self.path))
        np_path = np.array([l])
        rectangle = lir.lir(np_path)
        self.inner_bounding_box = Rect(*rectangle)

    def find_outer_bounding_box(self):
        x_s, y_s = zip(*self.path)
        min_x = min(x_s)
        max_x = max(x_s)
        min_y = min(y_s)
        max_y = max(y_s)

        height = max_y - min_y
        width = max_x - min_x

        self.outer_bounding_box = Rect(min_x, min_y, width, height)

    def score_square(self):
        self.find_com()
        self.find_inner_bounding_box()
        self.find_outer_bounding_box()

        big = self.outer_bounding_box.area
        small = self.inner_bounding_box.area

        score = small / big
        normalized_score = math.sqrt(small) / math.sqrt(big)

        self.draw_com()
        self.draw_bounding_boxes()

        font = Font(
            "FiraMono Nerd Font Mono",
            15,
            weight="REGULAR",
        )
        self.canvas.begin_path()
        self.canvas.fill_style = value_to_color(score)
        self.canvas.fill_text(f"Score:\t\t\t{score:.2f}", 10, 20, font=font)
        self.canvas.fill_style = value_to_color(normalized_score)
        self.canvas.fill_text(f"Normalized Score:\t{normalized_score:.2f}", 10, 40, font=font)


    def draw_com(self):
        self.canvas.begin_path()
        self.canvas.arc(*self.com, 3)
        self.canvas.fill(color="red")

    def draw_bounding_boxes(self):
        self.canvas.begin_path()
        self.canvas.rect(*self.inner_bounding_box)
        self.canvas.stroke(color="green", line_width=1)

        self.canvas.begin_path()
        self.canvas.rect(*self.outer_bounding_box)
        self.canvas.stroke(color="blue", line_width=1)


def main():
    return ShapeGuesser()
