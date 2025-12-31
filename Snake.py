from pynput import keyboard
import os
import time
import random  # for random fruit placement

# --- Game configuration and state ---
size = 10                 # Board is size x size
xhead = 5                 # Snake head X position
yhead = 5                 # Snake head Y position
fruit_pos = []            # List holding the current fruit position as (x, y)
x_snake = []              # Snake body X positions (queue-like: head tail management)
y_snake = []              # Snake body Y positions

last_key = None           # Last key pressed (raw from pynput)
current_direction = None  # Current movement direction: 'up'/'down'/'left'/'right'
running = True            # Main loop flag


def clear():
    """Clear the console screen (cross-platform)."""
    os.system('cls' if os.name == 'nt' else 'clear')


def spawn_fruit():
    """
    Place a fruit at a random free position (not on the head or body).
    Ensures the fruit does not spawn on the snake positions.
    """
    global fruit_pos
    while True:
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        # Make sure the cell is not occupied by the head or the body
        if (x, y) != (xhead, yhead) and (x, y) not in zip(x_snake, y_snake):
            fruit_pos = [(x, y)]
            break


def display():
    """
    Render the board to the console.
    Symbols:
      - "□" for the head and body
      - "@" for the fruit
      - "■" for empty cells
    """
    snake_positions = {(x_snake[i], y_snake[i]) for i in range(len(x_snake))}
    for iy in range(size):
        line_chars = []
        for ix in range(size):
            if ix == xhead and iy == yhead:
                line_chars.append("□")  # head
            elif (ix, iy) in snake_positions:
                line_chars.append("□")  # body
            elif (ix, iy) in fruit_pos:
                line_chars.append("@")  # fruit
            else:
                line_chars.append("■")  # empty
        print(" ".join(line_chars))


def move_head():
    """
    Update the snake's direction based on the last key, move the head,
    shift the body accordingly, handle fruit consumption, and detect collisions.

    Returns:
        bool: True to continue the game loop, False to end (collision or ESC).
    """
    global xhead, yhead, last_key, current_direction, x_snake, y_snake

    new_direction = None

    # Read and normalize input into a direction if available
    if last_key is not None:
        try:
            ch = last_key.char.lower()
            if ch == 'w':
                new_direction = 'up'
            elif ch == 's':
                new_direction = 'down'
            elif ch == 'a':
                new_direction = 'left'
            elif ch == 'd':
                new_direction = 'right'
        except AttributeError:
            # Arrow keys / special keys
            if last_key == keyboard.Key.up:
                new_direction = 'up'
            elif last_key == keyboard.Key.down:
                new_direction = 'down'
            elif last_key == keyboard.Key.left:
                new_direction = 'left'
            elif last_key == keyboard.Key.right:
                new_direction = 'right'
            elif last_key == keyboard.Key.esc:
                return False  # ESC ends the game

        # Prevent immediate reversal into the snake's body
        opposites = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
        if new_direction and (current_direction is None or new_direction != opposites.get(current_direction)):
            current_direction = new_direction

        # Consume the key
        last_key = None

    # If no direction yet, keep waiting (no movement)
    if current_direction is None:
        return True

    # Compute next head position based on current direction
    nx, ny = xhead, yhead
    if current_direction == 'up':
        ny -= 1
    elif current_direction == 'down':
        ny += 1
    elif current_direction == 'left':
        nx -= 1
    elif current_direction == 'right':
        nx += 1

    # Wall collision: end game if out of bounds
    if nx < 0 or nx >= size or ny < 0 or ny >= size:
        return False

    # --- Body movement ---
    xqueue = yqueue = None
    if len(x_snake) > 0:
        # Save last tail to re-attach if fruit is eaten
        xqueue = x_snake[-1]
        yqueue = y_snake[-1]

        # Move the segments forward: drop tail, push current head as first segment
        x_snake.pop()
        y_snake.pop()
        x_snake.insert(0, xhead)
        y_snake.insert(0, yhead)

    # --- Fruit consumption ---
    if (nx, ny) in fruit_pos:
        if xqueue is not None and yqueue is not None:
            # Grow by restoring the dropped tail (classic snake growth)
            x_snake.append(xqueue)
            y_snake.append(yqueue)
        else:
            # If there was no body yet, start it by adding the previous head
            x_snake.append(xhead)
            y_snake.append(yhead)
        spawn_fruit()  # place a new fruit

    # Commit new head position
    xhead, yhead = nx, ny

    # Self-collision check
    snake_positions = set(zip(x_snake, y_snake))
    if (xhead, yhead) in snake_positions:
        return False

    return True


def on_press(key):
    """Keyboard callback: store the last pressed key for processing."""
    global last_key
    last_key = key


# --- Game setup ---
spawn_fruit()

listener = keyboard.Listener(on_press=on_press)
listener.start()

try:
    while listener.is_alive() and running:
        clear()
        if not move_head():
            running = False
            listener.stop()
            input("game over! Enter pour quitter")
            break

        display()
        time.sleep(0.5)
finally:
    if listener.is_alive():
        listener.stop()
