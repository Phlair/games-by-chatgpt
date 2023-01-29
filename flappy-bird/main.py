import turtle
import random
import time

# Set up the screen
wn = turtle.Screen()
wn.title("Flappy Bird")
wn.bgcolor("blue")
wn.setup(width=500, height=500)

default_sizer = 7

# Draw the bird
bird = turtle.Turtle()
bird.color("yellow")
bird.shape("circle")
bird.penup()
bird.speed(0)
bird.goto(0, 0)

# Draw the pipes
pipes = []
for i in range(2):
    pipe = turtle.Turtle()
    pipe.color("green")
    pipe.shape("square")
    pipe.shapesize(stretch_wid=20, stretch_len=3)
    pipe.penup()
    pipe.speed(0)
    pipe.goto(200 + i * 200, random.randint(-200, 200))
    pipes.append(pipe)

# Define the bird's movement
def bird_jump():
    bird.sety(bird.ycor() + 40)

# Add event listener for bird jumping
wn.listen()
wn.onkeypress(bird_jump, "space")

wn.update()

# Move the pipes
for pipe in pipes:
    pipe.setx(pipe.xcor() - 5)
    if pipe.xcor() < -200:
        pipe.goto(400, random.choice([-200, 200]))

time.sleep(0.2)

# Game loop
while True:
    wn.update()

    # Move the pipes
    for pipe in pipes:
        pipe.setx(pipe.xcor() - 5)
        if pipe.xcor() < -200:
            pipe.goto(400, random.choice([-200, 200]))

    bird.sety(bird.ycor() - 5)

    # # Check for collision with pipes
    for pipe in pipes:
        # Get bounding box of bird
        bird_x1, bird_y1, bird_x2, bird_y2 = (
            bird.xcor()-default_sizer, 
            bird.ycor()-default_sizer,
            bird.xcor()+default_sizer,
            bird.ycor()+default_sizer
        )
        # Get bounding box of pipe
        pipe_x1, pipe_y1, pipe_x2, pipe_y2 = (
            pipe.xcor()-(pipe.shapesize()[0]+default_sizer), 
            pipe.ycor()-(pipe.shapesize()[1]*22*3), 
            pipe.xcor()+(pipe.shapesize()[0]+default_sizer), 
            pipe.ycor()+(pipe.shapesize()[1]*22*3)
        )
        if (bird_x1 < pipe_x2 and bird_x2 > pipe_x1) and ((bird_y1 < pipe_y2 and bird_y2 > pipe_y1) or (bird_y1 > pipe_y2 and bird_y2 < pipe_y1)):
            # DEBUG: Draw bounding boxes
            turtle.penup()
            turtle.goto(bird_x1, bird_y1)
            turtle.pendown()
            turtle.goto(bird_x1, bird_y2)
            turtle.goto(bird_x2, bird_y2)
            turtle.goto(bird_x2, bird_y1)
            turtle.goto(bird_x1, bird_y1)
            turtle.penup()
            turtle.penup()
            turtle.goto(pipe_x1, pipe_y1)
            turtle.pendown()
            turtle.goto(pipe_x1, pipe_y2)
            turtle.goto(pipe_x2, pipe_y2)
            turtle.goto(pipe_x2, pipe_y1)
            turtle.goto(pipe_x1, pipe_y1)
            turtle.penup()

            print("Game Over")
            time.sleep(2)
            exit()

