import turtle
import pygame  # Import the pygame library
import os

# Initialize pygame mixer
pygame.mixer.init()

# Set up the screen
wn = turtle.Screen()
wn.title("Breakout Game")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)  # Stops the window from updating automatically



# Load sound effects
hit_sound = pygame.mixer.Sound("ball-hit.wav")  # Replace with your sound effect file
brick_break_sound = pygame.mixer.Sound("crack.wav")  # Sound for breaking a brick
game_over_sound = pygame.mixer.Sound("game-over-160612.wav")


# Paddle
paddle = turtle.Turtle()
paddle.speed(0)
paddle.shape("square")
paddle.color("white")
paddle.shapesize(stretch_wid=1, stretch_len=5)
paddle.penup()
paddle.goto(0, -250)

# Ball
ball = turtle.Turtle()
ball.speed(40)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.175  # Ball movement in x direction
ball.dy = -0.175  # Ball movement in y direction

# Bricks
bricks = []

colors = ["red", "orange", "yellow", "green", "blue"]

for y in range(5):
    for x in range(-350, 400, 100):
        brick = turtle.Turtle()
        brick.speed(0)
        brick.shape("square")
        brick.color(colors[y % len(colors)])
        brick.shapesize(stretch_wid=1, stretch_len=4)
        brick.penup()
        brick.goto(x, 250 - y * 30)
        bricks.append(brick)

# Score
score = 0
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)
score_display.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))

# Paddle movement functions
def paddle_right():
    x = paddle.xcor()
    if x < 350:
        x += 60
    paddle.setx(x)

def paddle_left():
    x = paddle.xcor()
    if x > -350:
        x -= 60
    paddle.setx(x)

def move_paddle_with_mouse(x, y):
    if x > -350 and x < 350:
        paddle.setx(x)


# Keyboard bindings
wn.listen()
wn.onkey(paddle_right, "Right")
wn.onkey(paddle_left, "Left")

# Mouse binding
wn.onscreenclick(move_paddle_with_mouse)

# Main game loop
while True:
    wn.update()

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border checking
    if ball.xcor() > 390:
        ball.setx(390)
        ball.dx *= -1
        hit_sound.play()  # Play sound when the ball hits the wall

    if ball.xcor() < -390:
        ball.setx(-390)
        ball.dx *= -1
        hit_sound.play()  # Play sound when the ball hits the wall

    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1
        hit_sound.play()  # Play sound when the ball hits the wall

    # Paddle and ball collision
    if (ball.ycor() > -240 and ball.ycor() < -230) and (paddle.xcor() - 50 < ball.xcor() < paddle.xcor() + 50):
        ball.sety(-230)
        ball.dy *= -1
        hit_sound.play()  # Play sound when the ball hits the paddle

    # Brick and ball collision
    for brick in bricks:
        if brick.isvisible() and ball.distance(brick) < 50:
            ball.dy *= -1
            brick.hideturtle()
            bricks.remove(brick)
            brick_break_sound.play()  # Play sound when the brick is broken
            score += 10

            # Increase ball speed slightly
            ball.dx *= 1.05
            ball.dy *= 1.05

            score_display.clear()
            score_display.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))

    # Check for game over (when the ball hits the bottom of the screen)
    if ball.ycor() < -290:
        score_display.clear()
        score_display.goto(0, 0)
        score_display.write(f"GAME OVER! Final Score: {score}", align="center", font=("Courier", 36, "normal"))
        game_over_sound.play()
        break

    # Check for win (when all bricks are cleared)
    if not bricks:
        score_display.clear()
        score_display.goto(0, 0)
        score_display.write(f"YOU WIN! Final Score: {score}", align="center", font=("Courier", 36, "normal"))
        break

wn.mainloop()
