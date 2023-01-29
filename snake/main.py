import turtle
import time
import tkinter
import random
import heapq
from math import sqrt

delay = 0.1
score = 0
control = "human"
ai_mode = "basic"

# Set up the screen
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("green")
wn.setup(width=600, height=640)
wn.tracer(0) # turns off screen updates

class TurtleShape:
    def __init__(self, color, shape, x, y):
        self.color = color
        self.shape = shape
        self.x = x
        self.y = y
        self.speed = 0

        self.pen = turtle.Turtle()
        self.pen.color(color)
        self.pen.shape(shape)
        self.pen.speed(self.speed)
        self.pen.penup()
        self.pen.goto(x, y)

class Snake(TurtleShape):
    def __init__(self, color, shape, x, y):
        super().__init__(color, shape, x, y)
        self.direction = "stop"

    def hideturtle(self):
        self.pen.hideturtle()

class Food(TurtleShape):
    pass

# Snake head
head = Snake("black", "square", 0, 0)

# Snake food
food = Food("red", "circle", 0, 100)

segments = []

# Functions
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

# Functions to determine the next move direction for the AI player
def ai_move_basic(head, food, segments):
    # Get the current position of the head
    x_head, y_head = head.pen.position()
    # Get the current position of the food
    x_food, y_food = food.pen.position()
    # Get the current direction of the snake
    current_direction = head.direction

    # Create a list to store the possible next moves
    possible_moves = ["up", "down", "left", "right"]
    # Remove the opposite direction of the current direction from the list of possible moves
    if current_direction == "up":
        possible_moves.remove("down")
    elif current_direction == "down":
        possible_moves.remove("up")
    elif current_direction == "left":
        possible_moves.remove("right")
    elif current_direction == "right":
        possible_moves.remove("left")

    # Create a set to store the positions of the snake's segments
    segment_positions = set()
    for segment in segments:
        x_segment, y_segment = segment.pen.position()
        segment_positions.add((x_segment, y_segment))

    # Remove any moves that would cause the snake to crash into its own segments or go out of the boundaries
    for move in possible_moves[:]:
        x, y = x_head, y_head
        if move == "up":
            y += 20
        elif move == "down":
            y -= 20
        elif move == "left":
            x -= 20
        elif move == "right":
            x += 20
        if (x, y) in segment_positions or x < -280 or x > 280 or y < -280 or y > 280:
            possible_moves.remove(move) if move in possible_moves else None

    # If there are no possible moves, return None
    if not possible_moves:
        return None

    # Determine the best move based on the distance from the food
    best_move = None
    min_distance = float("inf")
    for move in possible_moves:
        x, y = x_head, y_head
        if move == "up":
            y += 20
        elif move == "down":
            y -= 20
        elif move == "left":
            x -= 20
        elif move == "right":
            x += 20
        distance = sqrt((x - x_food)**2 + (y - y_food)**2)
        if distance < min_distance:
            min_distance = distance
            best_move = move

    head.direction = best_move

def ai_move_pathfinder(head, food, segments):

    def manhattan_distance(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # Get the current position of the head
    x_head, y_head = head.pen.position()
    # Get the current position of the food
    x_food, y_food = food.pen.position()

    # Create a set to store the positions of the snake's segments
    segment_positions = set()
    for segment in segments:
        x_segment, y_segment = segment.pen.position()
        segment_positions.add((x_segment, y_segment))

    # Create a valid path by pretending the food is not under the snake
    while (x_food, y_food) in segment_positions:
        x_food = round(random.randint(-280, 280) / 20) * 20
        y_food = round(random.randint(-280, 280) / 20) * 20

    # Create a set to store the visited positions
    visited_positions = set()

    # Create a priority queue to store the possible next moves
    heap = []
    heapq.heappush(heap, (0, 0, head.direction, x_head, y_head))
    came_from = {}
    came_from_direction = {(x_head, y_head): head.direction}
    cost_so_far = {}
    came_from[(x_head, y_head)] = None
    came_from_direction[(x_head, y_head)] = None
    cost_so_far[(x_head, y_head)] = 0

    while heap:
        current = heapq.heappop(heap)[3:]

        # If the current position is the food, reconstruct the path
        if current == (x_food, y_food):
            break

        # Mark the current position as visited
        visited_positions.add(current)

        # Get the possible next moves
        x, y = current
        possible_moves = [("up", (x, y+20)), ("down", (x, y-20)), ("left", (x-20, y)), ("right", (x+20, y))]

        for move, pos in possible_moves:
            if pos[0] < -280 or pos[0] > 280 or pos[1] < -280 or pos[1] > 280:
                continue
            if pos in segment_positions:
                continue
            if pos in visited_positions:
                continue
            new_cost = cost_so_far[(x, y)] + 1
            if pos not in cost_so_far or new_cost < cost_so_far[pos]:
                cost_so_far[pos] = new_cost
                priority = new_cost + manhattan_distance(pos, (x_food, y_food))
                heapq.heappush(heap, (priority, new_cost, move, pos[0], pos[1]))
                came_from[pos] = (x, y)
                came_from_direction[pos] = move
    path = []
    current = (x_food, y_food)
    while current != (x_head, y_head):
        try:
            path.append((current, came_from_direction[current]))
            current = came_from[current]
        except KeyError:
            break
    path.reverse()
    try:
        head.direction = path[0][1]
    except IndexError:
        print("AI couldn't find a valid path")
        return

def move():
    if head.direction == "up":
        y = head.pen.ycor()
        head.pen.sety(y + 20)

    if head.direction == "down":
        y = head.pen.ycor()
        head.pen.sety(y - 20)

    if head.direction == "left":
        x = head.pen.xcor()
        head.pen.setx(x - 20)

    if head.direction == "right":
        x = head.pen.xcor()
        head.pen.setx(x + 20)

# Add a button for switching between human and AI control
def switch_control():
    global control
    if control == "human":
        control = "AI"
        button.config(text="Switch to Human Control")
    else:
        control = "human"
        button.config(text="Switch to AI Control")

# Add a button for switching between AI modes
def switch_ai_mode():
    global ai_mode
    if ai_mode == "basic":
        ai_mode = "pathfinder"
        button2.config(text="Switch to basic AI")
    else:
        ai_mode = "basic"
        button2.config(text="Switch to Pathfinder AI")

# Keyboard bindings
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")

# Add a score tracker
score_tracker = turtle.Turtle()
score_tracker.speed(0)
score_tracker.color("white")
score_tracker.penup()
score_tracker.hideturtle()
score_tracker.goto(260, 280)
score_tracker.write("Score: 0", align="right", font=("Courier", 14, "normal"))

button = tkinter.Button(text="Switch to AI Control", command=switch_control)
button.pack(side="left")
button2 = tkinter.Button(text="Switch to Pathfinder AI", command=switch_ai_mode)
button2.pack(side="left")

# Function to update the score
def update_score(food_caught):
    global score
    score += food_caught
    score_tracker.clear()
    score_tracker.write("Score: {}".format(score), align="right", font=("Courier", 14, "normal"))

# Add a game_over function
def game_over():
    global delay
    score_tracker.goto(0, 0)
    score_tracker.color("red")
    score_tracker.write("Game Over!", align="center", font=("Courier", 24, "normal"))
    time.sleep(3)
    score_tracker.clear()
    score_tracker.goto(260, 280)
    score_tracker.color("white")
    update_score(-score)
    head.pen.goto(0, 0)
    head.direction = "stop"
    for segment in segments:
        segment.hideturtle()
    segments.clear()
    delay = 0.1

while True:
    wn.update()
    try:
        # Check for a collision with the border
        if head.pen.xcor() > 290 or head.pen.xcor() < -290 or head.pen.ycor() > 290 or head.pen.ycor() < -290:
            game_over()

        # Check for a collision with the food
        if head.pen.distance(food.pen) < 20:
            # Move the food to a random spot
            x = round(random.randint(-260, 260) / 20) * 20
            y = round(random.randint(-260, 260) / 20) * 20
            food.pen.goto(x, y)

            # Add a segment
            new_segment = Snake("grey", "square", 0, 0)
            segments.append(new_segment)

            # Shorten the delay
            delay /= 1.05

            # Update the score
            update_score(1)
        
        # Move the end segments first in reverse order
        for index in range(len(segments)-1, 0, -1):
            x = segments[index-1].pen.xcor()
            y = segments[index-1].pen.ycor()
            segments[index].pen.goto(x, y)

        # Move segment 0 to where the head is
        if len(segments) > 0:
            x = head.pen.xcor()
            y = head.pen.ycor()
            segments[0].pen.goto(x, y)

        if control == "AI":
            if ai_mode == "pathfinder":
                ai_move_pathfinder(head, food, segments)
            else:
                ai_move_basic(head, food, segments)

        move()    

        # Check for head collision with the body segments
        for segment in segments:
            if segment.pen.distance(head.pen) < 20:
                game_over()

        time.sleep(delay)

    except Exception as e:
        raise e
