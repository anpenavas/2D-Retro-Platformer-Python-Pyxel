import pyxel
from mario import Mario
from block import Block
from question_block import Question_Block
from normal_block import Normal_Block
from goomba import Goomba
from koopa import Koopa
import random
import time

class Board:
    def __init__(self):
        """This magic method is used to declare the attributes of the class."""

        self.over = False
        self.points = 0
        self.coin_counter = 0
        self.time = time.time()+400
        self.time_left = 0
        self.x = 0
        self.width = 256
        self.height = 256
        self.floor = 216
        self.mario = Mario(10, self.floor, True, 3)
        # self.enemies will contain all the enemies (as their according class)
        self.enemies = []

        # Set the standard blocks (the floor blocks, bushes, clouds and pipes)
        # Instead of having 1 class per block, we have 1 class in which we define all the blocks' positions in its pos attribute (position).
        self.f1blocks = Block(False, (0, 32, 104, 16, 16), [(16*i, 232) for i in range(200)])
        self.f2blocks = Block(False, (0, 32, 104, 16, 16), [(16*i, 248) for i in range(200)])
        # In the bushes and clouds we make this positions random.
        self.bush = Block(False, (0, 16, 88, 48, 16), [(i * random.randint(150, 200), self.floor) for i in range(10)])
        self.clouds = Block(False, (0, 16, 64, 48, 26), [(i * random.randint(100, 150), (random.randint(100, 225))) for i in range(15)])
        self.pipes = Block(True, (0, 32, 0, 32, 32), [(464, 200), (464+16*18, 200), (464+16*37, 200)])

        # Since the question and normal blocks are more "special" than the others (we can destroy them and the question block has an special object "inside"), we create one class per block, instead of having one object
        qblocks_pos = [(272, 168), (352, 168), (368, 104), (384, 168), (464+16*10, 168), (464+16*12, 168), (464+16*11, 104), (464+16*31, 168), (464+16*33, 104)]
        # self.qblocks will contain all the question blocks (as their according class)
        self.qblocks = []
        for i in range(len(qblocks_pos)):
            # We pass its position and a random number (used to define if the special object is a mushroom or a coin) as parameters
            self.qblocks.append(Question_Block(qblocks_pos[i], random.randint(1, 3)))

        nblocks_pos = [(336, 168), (368, 168), (400, 168), (464+16*9, 168), (464+16*11, 168), (464+16*13, 168), (464+16*30, 168), (464+16*32, 168), (464+16*32, 104), (464+16*34, 104)]
        # self.nblocks will contain all the normal blocks (bricks, breakeable) (as their according class)
        self.nblocks = []
        for i in range(len(nblocks_pos)):
            self.nblocks.append(Normal_Block(nblocks_pos[i]))

        # Now we define a list containing all the blocks that we have defined, just so we can simplify with loops later.
        self.objects = [self.f1blocks, self.f2blocks, self.bush, self.clouds, self.pipes]
        # Add the question and normal blocks to the list of objects by extending the lists
        self.objects.extend(self.nblocks)
        self.objects.extend(self.qblocks)


    def update(self):
        """
            This is one of the most important method. Here we will define all the logic of the game.
            This method's behaviour is like a while, since it is called every time in pyxel.run of main.py
        """
        # The time left will be the difference between the initial time (the time at the moment of the start plus 400 seconds) and the time at the moment
        self.time_left = self.time-time.time()
        # If the time runs out 
        if int(self.time_left) <= 0:
            # Reset the level and decrease one live or game over if no lives remaining
            self.reset()

        # Check Mario's collisions. We pass all the blocks as parameter so we can iterate through them in the method.
        self.mario.check_collision(self.objects)

        
        # Check every 2.99 sec
        if pyxel.frame_count%90 == 89:
            # We only want atmost 4 enemies in the screen. so we check self.enemies length.
            if len(self.enemies) < 4:
                prohibited = []
                # We check if any block is in the right side of the screen. If this condition is met, then we spawn the enemy in the right side of that block (outside the screen)
                # Iterate through every object (block)
                for i in range(len(self.objects)):
                    # We only want the blocks that we can touch
                    if self.objects[i].touchable: 
                        for x, y in self.objects[i].pos:
                            # If that block is in the floor (in this case, only the pipe); we will only spawn enemies on the floor
                            if y == 200:
                                # This inverval representes the "floor" of the block with some extra space in the left so enemies do not spawn inside the pipes
                                for j in range(-12, self.objects[i].sprite[3]+2):
                                    # If any point in the x of the block is equal to the width of the screen (256), then that block is in the right side of the screen
                                    if x+j == self.width:
                                        # We add the position of the block from the right to the list we created before.
                                        prohibited.append(x+self.objects[i].sprite[3])

                # Now we check the same but with the enemies that are already spawned
                for enemy in self.enemies:
                    for i in range(-12, abs(enemy.sprite[3])+2):
                        if enemy.x+i == self.width:
                            prohibited.append(enemy.x+abs(enemy.sprite[3]))

                # Get a random number to decide if we create a Goomba (25% probability) or a Koopa (75% probability)
                n = random.randint(1, 4)
                # If there is any block in the right side of the screen, create the enemy after it
                if len(prohibited) > 0:
                    if n == 1:
                        self.enemies.append(Koopa(prohibited[0]+2, self.floor-8))
                    else:
                        self.enemies.append(Goomba(prohibited[0]+2, self.floor))
                else:
                    # Simply create the enemy in the right side of the screen
                    if n == 1:
                        self.enemies.append(Koopa(256, self.floor-8))
                    else:
                        self.enemies.append(Goomba(256, self.floor))

        # We have the enemies' logic here. For that, we iterate through every enemy
        for enemy in self.enemies:
            if enemy.alive:
                # If the enemy is alive, we want to check its collisions to the objects and the other enemies
                enemy.check_collisions(self.objects, self.enemies)
                # and let the enemy move
                enemy.move()

                # If the enemy is too far away from the screen, remove it
                if enemy.x <= -128:
                    enemy.alive = False
                if enemy.x >= 256+128:
                    enemy.alive = False
                
                # Here we have the collision of the enemy with Mario
                # For that, we want to check if the x position of Mario is in any point of the x position of the enemy and the same with their y position
                # This interval represents the "floor" of the enemy. We start from -12 so we also get some width of Mario (unless, it would only start being True after Mario is in the same x position as the enemy)
                for j in range(-12, abs(enemy.sprite[3])):
                    # If the x position of Mario is in any point of the x position of the enemy
                    if self.mario.x == enemy.x+j:
                        # This interval represents the "wall" of the enemy. We add +1 because the range is excluded
                        for z in range(enemy.sprite[4]+1):
                            # If the bottom side of Mario is equal any point in the y position of the enemy
                            if self.mario.y+self.mario.sprite[4] == enemy.y+z:
                                # Reset hit_time of Mario if previously set. (the moment when Mario got hit in Super Mario)
                                if self.mario.hit_time != 0 and time.time()-self.mario.hit_time > 2:
                                    self.mario.hit_time = 0

                                # If the bottom side of Mario is exactly at the top of the enemy
                                if z == 0:
                                    # and the time has reset)
                                    if self.mario.hit_time == 0:
                                        # Kill the enemy, set time time when the enemy has died (to display the points' text) and add the points
                                        enemy.alive = False
                                        enemy.init_time = time.time()
                                        self.points += 100
                                else:
                                    # If Mario is not in the top of the enemy, lose a life and reset or go from Super Mario to Mario (normal)
                                    if self.mario.hit_time == 0:
                                        if self.mario.big:
                                            self.mario.big = False
                                            # Set the moment when Mario goes from Super Mario to Mario. We do this so we can set Mario "invicible" for 2 seconds after being hit in Super Mario
                                            self.mario.hit_time = time.time()
                                        else:
                                            self.reset()
            else:
                # If the enemy is dead, set its sprite to the background's sprite and remove it from the list of enemies
                enemy.sprite = (0, 0, 0, 16, 16)


        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        if pyxel.btn(pyxel.KEY_RIGHT):
            if not self.mario.touching_right:
                # If not touching anything from the right, move to the right and update the board and its elements
                self.mario.move(True, self.width)
                self.update_board()
        elif pyxel.btn(pyxel.KEY_LEFT):
            # If not touching anything from the left, move to the left
            if not self.mario.touching_left:
                self.mario.move(False, self.width)

        if pyxel.btn(pyxel.KEY_UP):
            # If not jumping nor falling, then jump
            if(not self.mario.jumping and not self.mario.falling):
                self.mario.jump()


    def draw(self):
        """
            This method is one of the most important method. It has the same behaviour as update
        """
        if not self.over:
            # If the game is not over, draw the background and every element of it
            # Draw the tilemap (this is only the background)
            pyxel.bltm(0, 0, 0, self.x, 65, self.width, self.height)
            
            # Draw every object/element of the game
            for i in range(len(self.objects)):
                if i == 3:
                    # Draw the clouds. They are in a different loop because we change the y position of the clouds
                    for x, y in self.clouds.pos:
                        pyxel.blt(x, self.floor-y, self.clouds.sprite[0], self.clouds.sprite[1], self.clouds.sprite[2], self.clouds.sprite[3], self.clouds.sprite[4], 12)
                else:
                    # Draw every other object/element (bushes, pipes, floor, normal and question blocks)
                    for x, y in self.objects[i].pos:
                        pyxel.blt(x, y, self.objects[i].sprite[0], self.objects[i].sprite[1], self.objects[i].sprite[2], self.objects[i].sprite[3], self.objects[i].sprite[4], 12)
                
            # Draw special objects. They are drawn from the start but they are "hidden" (their sprite is the background)
            for i in range(len(self.qblocks)):
                pyxel.blt(self.qblocks[i].special.pos[0], self.qblocks[i].special.pos[1], self.qblocks[i].special.sprite[0], self.qblocks[i].special.sprite[1], self.qblocks[i].special.sprite[2], self.qblocks[i].special.sprite[3], self.qblocks[i].special.sprite[4], 12)

            # Draw every enemy
            for enemy in self.enemies:
                # If the enemy is not alive, draw the points added and when they already disappeared from the screen, remove the enemy from the list
                if not enemy.alive:
                    set = enemy.draw_points()
                    if set:
                        self.enemies.remove(enemy)
                else:
                    pyxel.blt(enemy.x, enemy.y, enemy.sprite[0], enemy.sprite[1], enemy.sprite[2], enemy.sprite[3], enemy.sprite[4], 12)


            # Draw points, coins counter, time left and lives counter.
            pyxel.text(20, 10, "MARIO", 7)
            pyxel.text(20, 17, str(self.points).rjust(6, "0"), 7)

            pyxel.blt(63, 8, 0, 48, 120, 16, 16, 12)
            pyxel.text(80, 13, "x " + str(self.coin_counter), 7)

            pyxel.text(220, 10, "TIME", 7)
            pyxel.text(220, 17, str(int(self.time_left)), 7)

            pyxel.text(170, 10, "WORLD", 7)
            pyxel.text(173, 17, "1-1", 7)

            pyxel.blt(120, 12, 0, 50, 152, 12, 7, 12)
            pyxel.text(135, 13, "x " + str(self.mario.lives), 7)

            # Here we update the points and coins counter and set Super Mario if touching a Mushroom
            for i in range(len(self.qblocks)):
                self.points, self.coin_counter, self.mario.big = self.qblocks[i].special.check(self.points, self.coin_counter, self.mario.x, self.mario.y, self.mario.big, self.mario.sprite)

            # Draw Mario
            pyxel.blt(self.mario.x, self.mario.y, self.mario.sprite[0], self.mario.sprite[1], self.mario.sprite[2], self.mario.sprite[3], self.mario.sprite[4], 12)
        else:
            # Draw a black background with "GAME OVER" in the middle and with the final points if the game is over (no lives remaining)
            pyxel.cls(0)
            pyxel.text(115, 120, "GAME OVER", 7)
            pyxel.text(121, 130, str(self.points).rjust(6, "0"), 7)

    def update_board(self):
        """
            This method updates all the elements of the screen position
        """
        # If Mario is in the middle of the board, change the board x position. (remember that this function it's only called when Mario is moving to the right)
        if(self.width-self.mario.x <= self.width/2):
            self.x += 0.3
        
        # If Mario is in the middle of the board
        if(self.width-self.mario.x <= self.width/2):
                for i in range(len(self.objects)):
                    for j in range(len(self.objects[i].pos)):
                        # Update the position of each object/element
                        self.objects[i].pos[j] = self.update_pos(*self.objects[i].pos[j])

                # Update the position of every special object
                for i in range(len(self.qblocks)):
                    self.qblocks[i].special.pos[0], self.qblocks[i].special.pos[1] = self.update_pos(self.qblocks[i].special.pos[0], self.qblocks[i].special.pos[1])

                # If the map is moving, the movement of the enemies will cancel. Therefore, we have to also change the position of these.
                for enemy in self.enemies:
                    enemy.x, enemy.y = self.update_pos(enemy.x, enemy.y)


    def update_pos(self, x: int, y: int):
        """
            This method helps to change the x position of every element of the screen
            @param x: the x position of the element
            @param y: the y position of the element
            Returns the positions modified
        """
        x -= 2
        return x, y

    def reset(self):
        """
            This method resets the level and substacts one live to Mario if its number of lives after the reset is not zero
        """
        if self.mario.lives-1 != 0:
            # To reset, we just do the same as we did in the __init__, but skipping some attributes that stay constant (points, coin_counter)
            self.time = time.time()+400
            self.time_left = 0
            self.x = 0
            self.mario = Mario(10, self.floor, True, self.mario.lives-1)
            self.enemies = []

            self.f1blocks = Block(False, (0, 32, 104, 16, 16), [(16*i, 232) for i in range(200)])
            self.f2blocks = Block(False, (0, 32, 104, 16, 16), [(16*i, 248) for i in range(200)])
            self.bush = Block(False, (0, 16, 88, 48, 16), [(i * random.randint(150, 200), self.floor) for i in range(10)])
            self.clouds = Block(False, (0, 16, 64, 48, 26), [(i * random.randint(100, 150), (random.randint(100, 225))) for i in range(15)])
            self.pipes = Block(True, (0, 32, 0, 32, 32), [(464, 200)])

            qblocks_pos = [(272, 168), (352, 168), (368, 104), (384, 168)]
            self.qblocks = [None]*len(qblocks_pos)
            for i in range(len(qblocks_pos)):
                self.qblocks[i] = Question_Block(qblocks_pos[i], random.randint(1, 3))

            nblocks_pos = [(336, 168), (368, 168), (400, 168)]
            self.nblocks = [None]*len(nblocks_pos)
            for i in range(len(nblocks_pos)):
                self.nblocks[i] = Normal_Block(nblocks_pos[i])

            self.objects = [self.f1blocks, self.f2blocks, self.bush, self.clouds, self.pipes]
            self.objects.extend(self.nblocks)
            self.objects.extend(self.qblocks)
        else:
            # If not lives remaining, set the game to be over
            self.over = True