from special import Special
import pyxel
import time

class Coin(Special):
    def __init__(self, pos: list):
        """Since we are inheriting the Special class, call its __init__, passing as parameters its position and the sprite of a coin"""
        super().__init__(pos, (0, 48, 120, 16, 16))

    def check(self, points: int, coin_counter: int, x: int, y: int, big: bool, sprite: tuple):
        """
            In this method we add the points and display them in the screen. To do this, we call this method from the update of Board and return it the new (if changed)
            points and coin counter. We also return it if is Super Mario just so we can simplify the algorithm with a simple loop. (use it for Coin and Mushroom)
            @param points: the points of the game in the moment (score)
            @param coin_counter: the coin counter in the moment
            @x: as said before, we do not need this parameter here, but we put it so we can simplify the algorith with a simple loop. It would be the x of Mario
            @y: as said before, we do not need this parameter here, but we put it so we can simplify the algorith with a simple loop. It would be the y of Mario
            @big: as said before, we do not need this parameter here, but we put it so we can simplify the algorith with a simple loop. It is if Mario is Super or not 
            @sprite: as said before, we do not need this parameter here, but we put it so we can simplify the algorith with a simple loop. It would be the sprite of Mario
        """
        if self.active:
            # If the coin is activated and 1 second has not passed
            if time.time()-self.init_time < 1:
                # Set the coin's sprite (so it appears)
                self.sprite = (0, 48, 120, 16, 16)
                # Draw the points got for getting the coin
                pyxel.text(self.pos[0]+3, self.pos[1]-8, "200", 7)
                # Add the points and the coin to the coin counter
                points, coin_counter = self.add_points(points, coin_counter)
            else:
                self.active = False
        else:
            # Set the sprite to be the background sprite if the coin is not active
            self.sprite = (0, 0, 0, 16, 16)

        return points, coin_counter, big
        

    def add_points(self, points: int, coin_counter: int):
        """
            This method helps add the points by returning the new points and coin counter once
            @param points: the points of the game
            @param coin_counter: the coin counter
        """
        if not self.added:
            points += 200
            coin_counter += 1
            self.added = True
        
        return points, coin_counter

