# Group#: B41
# Student Names: Gyan Edbert Zesiro, Ryan Edric Nashota

"""
    This program implements a variety of the snake
    game (https://en.wikipedia.org/wiki/Snake_(video_game_genre))
"""

import threading
import queue        #the thread-safe queue from Python standard library

from tkinter import Tk, Canvas, Button
import random, time


class Gui():
    """
        This class takes care of the game's graphic user interface (gui)
        creation and termination.
    """
    def __init__(self):
        """
            The initializer instantiates the main window and
            creates the starting icons for the snake and the prey,
            and displays the initial gamer score.
        """
        #some GUI constants
        scoreTextXLocation = 60
        scoreTextYLocation = 15
        textColour = "white"
        #instantiate and create gui
        self.root = Tk()
        self.canvas = Canvas(self.root, width = WINDOW_WIDTH,
            height = WINDOW_HEIGHT, bg = BACKGROUND_COLOUR)
        self.canvas.pack()
        #create starting game icons for snake and the prey
        self.snakeIcon = self.canvas.create_line(
            (0, 0), (0, 0), fill=ICON_COLOUR, width=SNAKE_ICON_WIDTH)
        self.preyIcon = self.canvas.create_rectangle(
            0, 0, 0, 0, fill=ICON_COLOUR, outline=ICON_COLOUR)
        #display starting score of 0
        self.score = self.canvas.create_text(
            scoreTextXLocation, scoreTextYLocation, fill=textColour,
            text='Your Score: 0', font=("Helvetica","11","bold"))
        #binding the arrow keys to be able to control the snake
        for key in ("Left", "Right", "Up", "Down"):
            self.root.bind(f"<Key-{key}>", game.whenAnArrowKeyIsPressed)

    def gameOver(self):
        """
            This method is used at the end to display a
            game over button.
        """
        gameOverButton = Button(self.canvas, text="Game Over!",
            height = 3, width = 10, font=("Helvetica","14","bold"),
            command=self.root.destroy)
        self.canvas.create_window(200, 100, anchor="nw", window=gameOverButton)


class QueueHandler():
    """
        This class implements the queue handler for the game.
    """
    def __init__(self):
        self.queue = gameQueue
        self.gui = gui
        self.queueHandler()

    def queueHandler(self):
        '''
            This method handles the queue by constantly retrieving
            tasks from it and accordingly taking the corresponding
            action.
            A task could be: game_over, move, prey, score.
            Each item in the queue is a dictionary whose key is
            the task type (for example, "move") and its value is
            the corresponding task value.
            If the queue.empty exception happens, it schedules
            to call itself after a short delay.
        '''
        try:
            while True:
                task = self.queue.get_nowait()
                if "game_over" in task:
                    gui.gameOver()
                elif "move" in task:
                    points = [x for point in task["move"] for x in point]
                    gui.canvas.coords(gui.snakeIcon, *points)
                elif "prey" in task:
                    gui.canvas.coords(gui.preyIcon, *task["prey"])
                elif "score" in task:
                    gui.canvas.itemconfigure(
                        gui.score, text=f"Your Score: {task['score']}")
                self.queue.task_done()
        except queue.Empty:
            gui.root.after(100, self.queueHandler)


class Game():
    '''
        This class implements most of the game functionalities.
    '''
    def __init__(self):
        """
           This initializer sets the initial snake coordinate list, movement
           direction, and arranges for the first prey to be created.
        """
        self.queue = gameQueue
        self.score = 0
        #starting length and location of the snake
        #note that it is a list of tuples, each being an
        # (x, y) tuple. Initially its size is 5 tuples.
        self.snakeCoordinates = [(495, 55), (485, 55), (475, 55),
                                 (465, 55), (455, 55)]
        #initial direction of the snake
        self.direction = "Left"
        self.gameNotOver = True
        self.preyCoordinates = (0, 0, 0, 0)
        self.preyCenter = (0, 0)
        self.createNewPrey()

    def superloop(self) -> None:
        """
            This method implements a main loop
            of the game. It constantly generates "move"
            tasks to cause the constant movement of the snake.
            Use the SPEED constant to set how often the move tasks
            are generated.
        """
        SPEED = GAME_SPEED     #speed of snake updates (sec)
        while self.gameNotOver:
            time.sleep(SPEED)
            self.move()

    def whenAnArrowKeyIsPressed(self, e) -> None:
        """
            This method is bound to the arrow keys
            and is called when one of those is clicked.
            It sets the movement direction based on
            the key that was pressed by the gamer.
            Use as is.
        """
        currentDirection = self.direction
        #ignore invalid keys
        if (currentDirection == "Left" and e.keysym == "Right" or
            currentDirection == "Right" and e.keysym == "Left" or
            currentDirection == "Up" and e.keysym == "Down" or
            currentDirection == "Down" and e.keysym == "Up"):
            return
        self.direction = e.keysym

    def move(self) -> None:
        """
            This method implements what is needed to be done
            for the movement of the snake.
            It generates a new snake coordinate.
            If based on this new movement, the prey has been
            captured, it adds a task to the queue for the updated
            score and also creates a new prey.
            It also calls a corresponding method to check if
            the game should be over.
            The snake coordinates list (representing its length
            and position) should be correctly updated.
        """
        NewSnakeCoordinates = self.calculateNewCoordinates()
        halfSnakeWidth = SNAKE_ICON_WIDTH / 2
        headRectangle = (
            NewSnakeCoordinates[0] - halfSnakeWidth,
            NewSnakeCoordinates[1] - halfSnakeWidth,
            NewSnakeCoordinates[0] + halfSnakeWidth,
            NewSnakeCoordinates[1] + halfSnakeWidth,
        )
        preyCaptured = not (
            headRectangle[2] < self.preyCoordinates[0] or
            headRectangle[0] > self.preyCoordinates[2] or
            headRectangle[3] < self.preyCoordinates[1] or
            headRectangle[1] > self.preyCoordinates[3]
        )
        updatedSnakeCoordinates = [*self.snakeCoordinates, NewSnakeCoordinates]

        if preyCaptured:
            self.snakeCoordinates = updatedSnakeCoordinates
            self.score += 1
            self.queue.put({"score": self.score})
            self.createNewPrey()
        else:
            self.snakeCoordinates = updatedSnakeCoordinates[1:]

        self.queue.put({"move": self.snakeCoordinates})
        self.isGameOver(NewSnakeCoordinates)

    def calculateNewCoordinates(self) -> tuple:
        """
            This method calculates and returns the new
            coordinates to be added to the snake
            coordinates list based on the movement
            direction and the current coordinate of
            head of the snake.
            It is used by the move() method.
        """
        lastX, lastY = self.snakeCoordinates[-1]
        stepSize = SNAKE_STEP
        if len(self.snakeCoordinates) > 1:
            previousX, previousY = self.snakeCoordinates[-2]
            stepSize = abs(lastX - previousX) or abs(lastY - previousY) or SNAKE_STEP

        if self.direction == "Left":
            return (lastX - stepSize, lastY)
        if self.direction == "Right":
            return (lastX + stepSize, lastY)
        if self.direction == "Up":
            return (lastX, lastY - stepSize)
        return (lastX, lastY + stepSize)

    def isGameOver(self, snakeCoordinates) -> None:
        """
            This method checks if the game is over by
            checking if now the snake has passed any wall
            or if it has bit itself.
            If that is the case, it updates the gameNotOver
            field and also adds a "game_over" task to the queue.
        """
        x, y = snakeCoordinates
        halfSnakeWidth = SNAKE_ICON_WIDTH / 2
        headRectangle = (
            x - halfSnakeWidth,
            y - halfSnakeWidth,
            x + halfSnakeWidth,
            y + halfSnakeWidth,
        )
        wallWasHit = (
            headRectangle[0] < 0 or
            headRectangle[1] < 0 or
            headRectangle[2] > WINDOW_WIDTH or
            headRectangle[3] > WINDOW_HEIGHT
        )

        # A visible-overlap test is too aggressive here because the snake line
        # is wider than the movement step. Turning up or down would therefore
        # overlap the neck visually and end the game immediately. Instead, treat
        # a self-hit as the head moving onto any already occupied body point.
        snakeBitItself = snakeCoordinates in self.snakeCoordinates[:-1]

        if wallWasHit or snakeBitItself:
            self.gameNotOver = False
            self.queue.put({"game_over": True})

    def createNewPrey(self) -> None:
        """
            This methods picks an x and a y randomly as the coordinate
            of the new prey and uses that to calculate the
            coordinates (x - 5, y - 5, x + 5, y + 5). [you need to replace 5 with a constant]
            It then adds a "prey" task to the queue with the calculated
            rectangle coordinates as its value. This is used by the
            queue handler to represent the new prey.
            To make playing the game easier, set the x and y to be THRESHOLD
            away from the walls.
        """
        THRESHOLD = PREY_SPAWN_THRESHOLD   #sets how close prey can be to borders
        halfPreyWidth = PREY_ICON_WIDTH / 2
        minimumX = THRESHOLD + PREY_ICON_WIDTH
        maximumX = WINDOW_WIDTH - THRESHOLD - PREY_ICON_WIDTH
        minimumY = THRESHOLD + PREY_ICON_WIDTH
        maximumY = WINDOW_HEIGHT - THRESHOLD - PREY_ICON_WIDTH
        candidatePreyCoordinates = []

        for preyX in range(minimumX, maximumX + 1, SNAKE_STEP):
            for preyY in range(minimumY, maximumY + 1, SNAKE_STEP):
                rectangleCoordinates = (
                    preyX - halfPreyWidth,
                    preyY - halfPreyWidth,
                    preyX + halfPreyWidth,
                    preyY + halfPreyWidth,
                )
                overlapsScore = not (
                    rectangleCoordinates[2] < SCORE_SAFE_ZONE[0] or
                    rectangleCoordinates[0] > SCORE_SAFE_ZONE[2] or
                    rectangleCoordinates[3] < SCORE_SAFE_ZONE[1] or
                    rectangleCoordinates[1] > SCORE_SAFE_ZONE[3]
                )
                if overlapsScore:
                    continue

                overlapsSnake = False
                for segmentStart, segmentEnd in zip(
                        self.snakeCoordinates[:-1], self.snakeCoordinates[1:]):
                    segmentRectangle = (
                        min(segmentStart[0], segmentEnd[0]) - SNAKE_ICON_WIDTH / 2,
                        min(segmentStart[1], segmentEnd[1]) - SNAKE_ICON_WIDTH / 2,
                        max(segmentStart[0], segmentEnd[0]) + SNAKE_ICON_WIDTH / 2,
                        max(segmentStart[1], segmentEnd[1]) + SNAKE_ICON_WIDTH / 2,
                    )
                    overlapsSnake = not (
                        rectangleCoordinates[2] < segmentRectangle[0] or
                        rectangleCoordinates[0] > segmentRectangle[2] or
                        rectangleCoordinates[3] < segmentRectangle[1] or
                        rectangleCoordinates[1] > segmentRectangle[3]
                    )
                    if overlapsSnake:
                        break

                if not overlapsSnake:
                    candidatePreyCoordinates.append((preyX, preyY, rectangleCoordinates))

        if not candidatePreyCoordinates:
            self.gameNotOver = False
            self.queue.put({"game_over": True})
            return

        preyX, preyY, rectangleCoordinates = random.choice(candidatePreyCoordinates)
        self.preyCenter = (preyX, preyY)
        self.preyCoordinates = rectangleCoordinates
        self.queue.put({"prey": rectangleCoordinates})


if __name__ == "__main__":
    #some constants for our GUI
    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 300
    SNAKE_ICON_WIDTH = 15
    PREY_ICON_WIDTH = 10
    SNAKE_STEP = 10
    PREY_SPAWN_THRESHOLD = 15
    GAME_SPEED = 0.15
    SCORE_SAFE_ZONE = (0, 0, 130, 30)

    BACKGROUND_COLOUR = "green"   #you may change this colour if you wish
    ICON_COLOUR = "yellow"        #you may change this colour if you wish

    gameQueue = queue.Queue()     #instantiate a queue object using python's queue class

    game = Game()        #instantiate the game object

    gui = Gui()    #instantiate the game user interface

    QueueHandler()  #instantiate the queue handler

    #start a thread with the main loop of the game
    threading.Thread(target = game.superloop, daemon=True).start()

    #start the GUI's own event loop
    gui.root.mainloop()
