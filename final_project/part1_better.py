# Group#: B41
# Student Names: Gyan Edbert Zesiro, Ryan Edric Nashota

"""
    A polished snake game variant built for presentation and experimentation, because
    it's always fun to code a snake game.
"""

from tkinter import Tk, Canvas
import math
import random

TITLE = "Neon Orchard Snake"
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 552

BOARD_LEFT = 24
BOARD_TOP = 96
BOARD_COLS = 28
BOARD_ROWS = 18
CELL_SIZE = 24
BOARD_WIDTH = BOARD_COLS * CELL_SIZE
BOARD_HEIGHT = BOARD_ROWS * CELL_SIZE
BOARD_RIGHT = BOARD_LEFT + BOARD_WIDTH
BOARD_BOTTOM = BOARD_TOP + BOARD_HEIGHT

BACKGROUND_TOP = "#08111f"
BACKGROUND_BOTTOM = "#12233b"
PANEL_FILL = "#11213a"
PANEL_OUTLINE = "#2f4d78"
BOARD_CELL_DARK = "#0d2035"
BOARD_CELL_LIGHT = "#102641"
BOARD_GRID_DOT = "#203755"
BOARD_BORDER = "#5bc0be"

SNAKE_BODY_START = "#0f766e"
SNAKE_BODY_END = "#5eead4"
SNAKE_HEAD_FILL = "#99f6e4"
SNAKE_HEAD_OUTLINE = "#0f766e"
SNAKE_SHADOW = "#09111c"
PREY_RED = "#ef4444"
PREY_RED_DARK = "#b91c1c"
PREY_LEAF = "#4ade80"
PREY_STEM = "#854d0e"
TEXT_PRIMARY = "#f8fafc"
TEXT_SECONDARY = "#b6c6dd"
TEXT_ACCENT = "#fbbf24"
OVERLAY_FILL = "#07111f"

# The snake list is stored from tail to head, so the rightmost cell must be
# the last element if the opening direction is "Right".
INITIAL_SNAKE = [(2, 8), (3, 8), (4, 8), (5, 8), (6, 8)]
INITIAL_DIRECTION = "Right"
BASE_TICK_MS = 145
MIN_TICK_MS = 72
SPEED_STEP_MS = 4


def blend_colour(start: str, end: str, ratio: float) -> str:
    """Interpolate between two hex colours."""
    ratio = max(0.0, min(1.0, ratio))
    start_channels = [int(start[index:index + 2], 16) for index in (1, 3, 5)]
    end_channels = [int(end[index:index + 2], 16) for index in (1, 3, 5)]
    mixed = [
        round(start_channel + (end_channel - start_channel) * ratio)
        for start_channel, end_channel in zip(start_channels, end_channels)
    ]
    return "#{:02x}{:02x}{:02x}".format(*mixed)


class BetterSnakeGame:
    """A more polished snake game presentation using custom Canvas artwork."""

    def __init__(self):
        self.root = Tk()
        self.root.title(TITLE)
        self.root.resizable(False, False)
        self.root.configure(bg=BACKGROUND_TOP)

        self.canvas = Canvas(
            self.root,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            bg=BACKGROUND_TOP,
            highlightthickness=0
        )
        self.canvas.pack()

        self.score_value = None
        self.best_value = None
        self.state_value = None

        self.frame_index = 0
        self.best_score = 0
        self.victory = False

        self.root.bind("<Key>", self.when_key_is_pressed)
        self.root.bind("<Escape>", lambda _event: self.root.destroy())

        self.draw_static_scene()
        self.reset_game()
        self.root.after(self.current_tick_ms(), self.tick)

    def draw_static_scene(self) -> None:
        """Draw the background, the board, and the fixed HUD panels."""
        for row in range(WINDOW_HEIGHT):
            fill = blend_colour(
                BACKGROUND_TOP,
                BACKGROUND_BOTTOM,
                row / max(1, WINDOW_HEIGHT - 1)
            )
            self.canvas.create_line(0, row, WINDOW_WIDTH, row, fill=fill)

        self.canvas.create_rectangle(
            18, 18, WINDOW_WIDTH - 18, 74,
            fill=PANEL_FILL, outline=PANEL_OUTLINE, width=2
        )
        self.canvas.create_text(
            42, 38,
            text=TITLE,
            anchor="w",
            fill=TEXT_PRIMARY,
            font=("Georgia", 21, "bold")
        )
        self.canvas.create_text(
            44, 63,
            text="Arrow keys move. Press P to pause, R to restart, Esc to quit.",
            anchor="w",
            fill=TEXT_SECONDARY,
            font=("Segoe UI", 10, "normal")
        )

        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLS):
                x1 = BOARD_LEFT + column * CELL_SIZE
                y1 = BOARD_TOP + row * CELL_SIZE
                fill = BOARD_CELL_LIGHT if (row + column) % 2 == 0 else BOARD_CELL_DARK
                self.canvas.create_rectangle(
                    x1, y1, x1 + CELL_SIZE, y1 + CELL_SIZE,
                    fill=fill, outline=""
                )
                self.canvas.create_oval(
                    x1 + CELL_SIZE / 2 - 1,
                    y1 + CELL_SIZE / 2 - 1,
                    x1 + CELL_SIZE / 2 + 1,
                    y1 + CELL_SIZE / 2 + 1,
                    fill=BOARD_GRID_DOT,
                    outline=""
                )

        self.canvas.create_rectangle(
            BOARD_LEFT, BOARD_TOP, BOARD_RIGHT, BOARD_BOTTOM,
            outline=BOARD_BORDER, width=3
        )
        self.canvas.create_rectangle(
            BOARD_LEFT + 4, BOARD_TOP + 4, BOARD_RIGHT - 4, BOARD_BOTTOM - 4,
            outline="#173555", width=1
        )

        self.canvas.create_text(
            BOARD_LEFT, 84,
            text="Score",
            anchor="w",
            fill=TEXT_SECONDARY,
            font=("Segoe UI", 10, "bold")
        )
        self.score_value = self.canvas.create_text(
            BOARD_LEFT + 48, 84,
            text="0",
            anchor="w",
            fill=TEXT_ACCENT,
            font=("Segoe UI", 14, "bold")
        )
        self.canvas.create_text(
            BOARD_LEFT + 120, 84,
            text="Best",
            anchor="w",
            fill=TEXT_SECONDARY,
            font=("Segoe UI", 10, "bold")
        )
        self.best_value = self.canvas.create_text(
            BOARD_LEFT + 158, 84,
            text="0",
            anchor="w",
            fill="#93c5fd",
            font=("Segoe UI", 14, "bold")
        )
        self.state_value = self.canvas.create_text(
            BOARD_RIGHT, 84,
            text="Status: Ready",
            anchor="e",
            fill=TEXT_SECONDARY,
            font=("Segoe UI", 11, "bold")
        )

    def reset_game(self) -> None:
        """Reset the model to a fresh game state."""
        self.score = 0
        self.direction = INITIAL_DIRECTION
        self.pending_direction = INITIAL_DIRECTION
        self.snake = list(INITIAL_SNAKE)
        self.paused = False
        self.game_over = False
        self.victory = False
        self.frame_index = 0
        self.prey = self.choose_prey_location()
        self.draw_dynamic_scene()

    def choose_prey_location(self):
        """Select a random free cell for the prey."""
        free_cells = [
            (column, row)
            for row in range(BOARD_ROWS)
            for column in range(BOARD_COLS)
            if (column, row) not in self.snake
        ]
        return random.choice(free_cells) if free_cells else None

    def current_tick_ms(self) -> int:
        """Speed up slightly as the score increases."""
        return max(MIN_TICK_MS, BASE_TICK_MS - min(self.score, 12) * SPEED_STEP_MS)

    def when_key_is_pressed(self, event) -> None:
        """Handle movement, pause, and restart keys."""
        key = event.keysym
        if key.lower() == "r":
            self.reset_game()
            return
        if key.lower() == "p" and not self.game_over:
            self.paused = not self.paused
            self.draw_dynamic_scene()
            return

        valid_directions = {"Left", "Right", "Up", "Down"}
        if key not in valid_directions or self.game_over:
            return

        opposite_directions = {
            ("Left", "Right"),
            ("Right", "Left"),
            ("Up", "Down"),
            ("Down", "Up"),
        }
        comparison_direction = self.pending_direction
        if (comparison_direction, key) in opposite_directions:
            return
        self.pending_direction = key

    def next_head(self):
        """Return the next head cell based on the active direction."""
        head_x, head_y = self.snake[-1]
        if self.direction == "Left":
            return (head_x - 1, head_y)
        if self.direction == "Right":
            return (head_x + 1, head_y)
        if self.direction == "Up":
            return (head_x, head_y - 1)
        return (head_x, head_y + 1)

    def hits_wall(self, cell) -> bool:
        """Check whether a cell is outside the board."""
        column, row = cell
        return (
            column < 0 or row < 0 or
            column >= BOARD_COLS or row >= BOARD_ROWS
        )

    def hits_body(self, cell) -> bool:
        """Check whether the snake runs into its own body."""
        return cell in self.snake[1:]

    def tick(self) -> None:
        """Advance the game by one step and schedule the next frame."""
        if not self.game_over and not self.paused:
            self.direction = self.pending_direction
            next_head = self.next_head()

            if self.hits_wall(next_head) or self.hits_body(next_head):
                self.game_over = True
                self.best_score = max(self.best_score, self.score)
            else:
                self.snake.append(next_head)
                if next_head == self.prey:
                    self.score += 1
                    self.best_score = max(self.best_score, self.score)
                    self.prey = self.choose_prey_location()
                    if self.prey is None:
                        self.game_over = True
                        self.victory = True
                else:
                    self.snake.pop(0)
                self.frame_index += 1

        self.draw_dynamic_scene()
        self.root.after(self.current_tick_ms(), self.tick)

    def cell_bounds(self, cell, inset: float = 0.0):
        """Convert a board cell into pixel bounds."""
        column, row = cell
        x1 = BOARD_LEFT + column * CELL_SIZE + inset
        y1 = BOARD_TOP + row * CELL_SIZE + inset
        x2 = x1 + CELL_SIZE - inset * 2
        y2 = y1 + CELL_SIZE - inset * 2
        return (x1, y1, x2, y2)

    def cell_center(self, cell):
        """Return the pixel center for a board cell."""
        x1, y1, x2, y2 = self.cell_bounds(cell)
        return ((x1 + x2) / 2, (y1 + y2) / 2)

    def draw_dynamic_scene(self) -> None:
        """Redraw the animated game elements."""
        self.canvas.delete("dynamic")

        self.canvas.itemconfigure(self.score_value, text=str(self.score))
        self.canvas.itemconfigure(self.best_value, text=str(self.best_score))

        if self.game_over:
            status = "Status: Victory" if self.victory else "Status: Game Over"
        elif self.paused:
            status = "Status: Paused"
        else:
            status = "Status: Running"
        self.canvas.itemconfigure(self.state_value, text=status)

        if self.prey is not None:
            self.draw_prey()
        self.draw_snake()

        if self.paused and not self.game_over:
            self.draw_banner("Paused", "Press P to continue")
        if self.game_over:
            title = "You Win" if self.victory else "Game Over"
            subtitle = f"Score: {self.score}   Best: {self.best_score}"
            self.draw_banner(title, subtitle + "   Press R to restart")

    def draw_prey(self) -> None:
        """Draw an apple-like prey with a small pulse animation."""
        pulse = 1.0 + 0.05 * math.sin(self.frame_index * 0.45)
        center_x, center_y = self.cell_center(self.prey)
        radius = CELL_SIZE * 0.28 * pulse

        self.canvas.create_oval(
            center_x - radius - 5,
            center_y - radius + 3,
            center_x + radius + 5,
            center_y + radius + 10,
            fill="#22060a",
            outline="",
            tags="dynamic"
        )
        self.canvas.create_oval(
            center_x - radius - 2,
            center_y - radius,
            center_x + radius - 2,
            center_y + radius + 1,
            fill=PREY_RED,
            outline="",
            tags="dynamic"
        )
        self.canvas.create_oval(
            center_x - radius + 2,
            center_y - radius - 1,
            center_x + radius + 2,
            center_y + radius,
            fill=PREY_RED_DARK,
            outline="",
            tags="dynamic"
        )
        self.canvas.create_line(
            center_x, center_y - radius - 4,
            center_x + 1, center_y - radius - 12,
            fill=PREY_STEM,
            width=3,
            capstyle="round",
            tags="dynamic"
        )
        self.canvas.create_polygon(
            center_x + 2, center_y - radius - 8,
            center_x + 12, center_y - radius - 14,
            center_x + 9, center_y - radius - 3,
            fill=PREY_LEAF,
            outline="",
            tags="dynamic"
        )
        self.canvas.create_oval(
            center_x - radius * 0.5,
            center_y - radius * 0.6,
            center_x - radius * 0.1,
            center_y - radius * 0.2,
            fill="#fecaca",
            outline="",
            tags="dynamic"
        )

    def draw_snake(self) -> None:
        """Draw the snake with a smooth body line and a detailed head."""
        if len(self.snake) > 1:
            points = [coordinate for cell in self.snake for coordinate in self.cell_center(cell)]
            self.canvas.create_line(
                *points,
                fill=SNAKE_SHADOW,
                width=CELL_SIZE * 0.88,
                capstyle="round",
                joinstyle="round",
                smooth=True,
                splinesteps=12,
                tags="dynamic"
            )
            self.canvas.create_line(
                *points,
                fill="#1f8f83",
                width=CELL_SIZE * 0.7,
                capstyle="round",
                joinstyle="round",
                smooth=True,
                splinesteps=12,
                tags="dynamic"
            )

        body_length = max(1, len(self.snake) - 1)
        for index, cell in enumerate(self.snake[:-1]):
            shade = blend_colour(
                SNAKE_BODY_START,
                SNAKE_BODY_END,
                index / body_length
            )
            x1, y1, x2, y2 = self.cell_bounds(cell, inset=5)
            self.canvas.create_oval(
                x1 + 1, y1 + 2, x2 + 1, y2 + 2,
                fill="#07131d",
                outline="",
                tags="dynamic"
            )
            self.canvas.create_oval(
                x1, y1, x2, y2,
                fill=shade,
                outline="",
                tags="dynamic"
            )
            self.canvas.create_oval(
                x1 + 4, y1 + 4, x1 + 8, y1 + 8,
                fill="#d1fae5",
                outline="",
                tags="dynamic"
            )

        self.draw_head()

    def draw_head(self) -> None:
        """Draw the snake head, eyes, and a small tongue."""
        head = self.snake[-1]
        x1, y1, x2, y2 = self.cell_bounds(head, inset=3)
        center_x, center_y = self.cell_center(head)

        self.canvas.create_oval(
            x1 + 2, y1 + 3, x2 + 2, y2 + 3,
            fill="#06121c",
            outline="",
            tags="dynamic"
        )
        self.canvas.create_oval(
            x1, y1, x2, y2,
            fill=SNAKE_HEAD_FILL,
            outline=SNAKE_HEAD_OUTLINE,
            width=2,
            tags="dynamic"
        )

        eye_offsets = {
            "Left": [(-5, -4), (-5, 4)],
            "Right": [(5, -4), (5, 4)],
            "Up": [(-4, -5), (4, -5)],
            "Down": [(-4, 5), (4, 5)],
        }
        pupil_shift = {
            "Left": (-1.5, 0),
            "Right": (1.5, 0),
            "Up": (0, -1.5),
            "Down": (0, 1.5),
        }
        for offset_x, offset_y in eye_offsets[self.direction]:
            eye_x = center_x + offset_x
            eye_y = center_y + offset_y
            self.canvas.create_oval(
                eye_x - 3, eye_y - 3, eye_x + 3, eye_y + 3,
                fill="white", outline="", tags="dynamic"
            )
            shift_x, shift_y = pupil_shift[self.direction]
            self.canvas.create_oval(
                eye_x - 1.4 + shift_x,
                eye_y - 1.4 + shift_y,
                eye_x + 1.4 + shift_x,
                eye_y + 1.4 + shift_y,
                fill="#0f172a",
                outline="",
                tags="dynamic"
            )

        tongue = {
            "Left": ((x1 - 5, center_y), (x1 - 10, center_y - 3), (x1 - 10, center_y + 3)),
            "Right": ((x2 + 5, center_y), (x2 + 10, center_y - 3), (x2 + 10, center_y + 3)),
            "Up": ((center_x, y1 - 5), (center_x - 3, y1 - 10), (center_x + 3, y1 - 10)),
            "Down": ((center_x, y2 + 5), (center_x - 3, y2 + 10), (center_x + 3, y2 + 10)),
        }
        tongue_root, tongue_a, tongue_b = tongue[self.direction]
        self.canvas.create_line(
            *tongue_root, *tongue_a,
            fill="#fb7185",
            width=2,
            capstyle="round",
            tags="dynamic"
        )
        self.canvas.create_line(
            *tongue_root, *tongue_b,
            fill="#fb7185",
            width=2,
            capstyle="round",
            tags="dynamic"
        )

    def draw_banner(self, title: str, subtitle: str) -> None:
        """Draw a centered overlay banner."""
        panel_width = 360
        panel_height = 118
        left = (WINDOW_WIDTH - panel_width) / 2
        top = (WINDOW_HEIGHT - panel_height) / 2
        right = left + panel_width
        bottom = top + panel_height

        self.canvas.create_rectangle(
            BOARD_LEFT, BOARD_TOP, BOARD_RIGHT, BOARD_BOTTOM,
            fill=OVERLAY_FILL,
            outline="",
            stipple="gray50",
            tags="dynamic"
        )
        self.canvas.create_rectangle(
            left + 5, top + 6, right + 5, bottom + 6,
            fill="#04101b",
            outline="",
            tags="dynamic"
        )
        self.canvas.create_rectangle(
            left, top, right, bottom,
            fill=PANEL_FILL,
            outline=TEXT_ACCENT,
            width=2,
            tags="dynamic"
        )
        self.canvas.create_text(
            WINDOW_WIDTH / 2, top + 38,
            text=title,
            fill=TEXT_PRIMARY,
            font=("Georgia", 24, "bold"),
            tags="dynamic"
        )
        self.canvas.create_text(
            WINDOW_WIDTH / 2, top + 78,
            text=subtitle,
            fill=TEXT_SECONDARY,
            font=("Segoe UI", 11, "bold"),
            tags="dynamic"
        )

    def run(self) -> None:
        """Start the Tkinter event loop."""
        self.root.mainloop()


if __name__ == "__main__":
    BetterSnakeGame().run()
