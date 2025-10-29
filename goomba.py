from enemy import Enemy
import time
import pyxel

class Goomba(Enemy):
    def __init__(self, x: int, y: int):
        """Since we are inheriting the Enemy class, call its __init__, passing as parameters its position and the sprite of a Goomba"""
        super().__init__(x, y, (0, 32, 48, 16, 16))

    def move(self):
        """
            This method makes Goomba move. This is called from the update of Board
        """
        if self.direction:
            # If facing right (direction == True), add 1 to the x position
            self.x += 1
        else:
            # If facing left (direction == False), substract 1 to the x position
            self.x -= 1

    def check_collisions(self, objects: tuple, enemies: list):
        """
            This method is used to check the collisions of Goomba with the blocks and with the other enemies
            @param objects: the tuple containing all the objects (blocks)
            @param enemies: the list containing all the enemies
        """
        # Set collisions with blocks
        for index in range(len(objects)):
            # Only get the predefined touchable blocks
            if objects[index].touchable:
                for x, y in objects[index].pos:
                    # Interval for the side ("wall") of the block.
                    for i in range(objects[index].sprite[4]):
                        # If Goomba's y position is in that interval
                        if self.y == y+i:
                            # Check when Goomba is in the left side of the block. -2 because we want some space. 
                            if self.x+self.sprite[3]-2 == x:
                                self.direction = not self.direction
                            # Check when Goomba is in the right side of the block. +2 because we want some space.
                            elif self.x == x+objects[index].sprite[3]+2:
                                self.direction = not self.direction

        # Set collisions with the enemies that are already spawned
        for enemy in enemies:
            # If the right side of Goomba is equal to the left side of any enemy
            if self.x+self.sprite[3] == enemy.x:
                # Change the direction of Goomba and the other enemy
                self.direction = not self.direction
                enemy.direction = not enemy.direction
            elif self.x == enemy.x+enemy.sprite[3]:
                # If the left side of Goomba is equal to the right side of any enemy
                # Change the direction of Goomba and the other enemy
                self.direction = not self.direction
                enemy.direction = not enemy.direction

                    

    def draw_points(self):
        """
            This method helps to draw the points awarded from killing the Goomba's
        """
        # If 1 seconds has not passed
        if time.time() - self.init_time < 1:
            # Draw the points
            pyxel.text(self.x+3, self.y-8, "100", 7)
        else:
            # Reset the attribute and return True (so we know when the points have stopped being displayed in the screen)
            self.init_time = 0
            return True
        return False