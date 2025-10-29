from special import Special
import time
import pyxel

class Mushroom(Special):
    def __init__(self, pos: list):
        """Since we are inheriting the Special class, call its __init__, passing as parameters its position and the sprite of a mushroom"""
        super().__init__(pos, (0, 0, 32, 16, 16))
        self.toadd = False

    def check(self, points: int, coin_counter: int, x: int, y: int, big: bool, sprite: tuple):
        """
            In this method we add the points and display them in the screen. To do this, we call this method from the update of Board and return it the new (if changed)
            points, coin counter and if Mario is Super Mario.
            @param points: the points of the game in the moment (score)
            @param coin_counter: the coin counter in the moment
            @x: the x position of Mario
            @y: the y position of Mario
            @big: if Mario is Super or not 
            @sprite: the sprite of Mario
        """
        if self.active:
            # If the mushroom is activated, set its sprite (so it appears)
            self.sprite = (0, 0, 32, 16, 16)
            # If Mario touches the mushroom (the difference between the x of Mario and the x of the mushroom is less than the width of the mushroom and the same with the y position)
            if abs(self.pos[0]-x)<abs(sprite[3]) and abs(self.pos[1]-y)<sprite[4]:
                # Set initial time to be this exact moment and set that the mushroom's points are to be added
                self.init_time = time.time()
                self.active = False
                self.toadd = True
        else:
            # Make the mushroom disappear 
            self.sprite = (0, 0, 0, 16, 16)
            if self.toadd and time.time()-self.init_time<1:
                # If 1 seconds have not passed since the mushroom was set to be added, draw the points got and add them
                pyxel.text(self.pos[0]+3, self.pos[1]-8, "1000", 7)
                points, big = self.add_points(points), True
                    
        return points, coin_counter, big

    def add_points(self, points: int):
        """
            This method helps add the points by returning the new points
            @param points: the points of the game
        """
        if not self.added:
            points += 1000
            self.added = True
        
        return points