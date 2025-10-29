class Mario:
    def __init__(self, x: int, y: int, dir: bool, lives: int):
        """This magic method is used to declare the attributes of the class."""
        self.lives = lives
        self.x = x
        self.y = y
        # direction = True (facing right); direction = False (facing left)
        self.direction = dir
        self.sprite = (0, 0, 48, 16, 16)
        self.jumping = False
        # aux is the "floor to fall"
        self.aux = y
        self.falling = False
        self.touching_up = ()
        self.touching_down = ()
        self.touching_left = ()
        self.touching_right = ()
        self.big = False
        # hit_time is not used inside of the class but outside of it, in the board. We use it to make Mario invincible after getting hit being in Super Mario
        self.hit_time = 0

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x: int):
        if type(x) != int:
            raise TypeError("The initial x position must be an int")
        else:
            self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y: int):
        if type(y) != int:
            raise TypeError("The initial y position must be an integer")
        else:
            self.__y = y

    @property
    def dir(self):
        return self.__dir

    @dir.setter
    def dir(self, dir: bool):
        if type(dir) != bool:
            raise TypeError("The direction of Mario must be a boolean (True facing right, False facing left)")
        else:
            self.__dir = dir

    @property
    def lives(self):
        return self.__lives

    @lives.setter
    def lives(self, lives: int):
        if type(lives) != int:
            raise TypeError("The number of lives must be an integer")
        elif lives == 0:
            raise ValueError("The number of lives cannot be zero")
        else:
            self.__lives = lives


    def move(self, direction: bool, board_width: int):
        """
            This method handles the movement of Mario
        """
        # If direction is to the right (True) and Mario is not in the middle of the board, change its x position to the right and set that he is not touching anything from the left (since he moved)
        self.direction = direction
        if self.direction and board_width-self.x > board_width/2:
            self.x += 2
            self.touching_left = ()
        # If direction is to the left (False) and Mario is not in the left side of the board, change its x position to the left and set that he is not touching anything from the right (since he moved)
        elif not self.direction and board_width-self.x != board_width:
            self.x -= 2
            self.touching_right = ()

    def jump(self):
        """
            This method simply set self.jumping to True and changes the sprite. The jump logic is in check_collisions (we take advantage of this method because it is already being called from the update of the Board)
        """
        # Here, we set jumping to True. We do the logic of the jump in check_collision, which is called from the board's update
        self.jumping = True
        # Here, we set Mario's sprite to Mario's jumping sprite, according to its direction and if its normal Mario or Super Mario
        # If Mario is normal Mario
        if not self.big:
            if self.direction:
                # If Mario is looking to the right and normal Mario, set its according sprite
                self.sprite = (0, 48, 104, 16, 16)
            else:
                # If Mario is looking to the left and normal Mario, set its according sprite
                self.sprite = (0, 48, 104, -16, 16)
        else:  # If Mario is Super Mario
            if self.direction:
                # If Mario is looking to the right and Super Mario, set its according sprite
                self.sprite = (0, 32, 120, 16, 32)
            else:
                # If Mario is looking to the left and Super Mario, set its according sprite
                self.sprite = (0, 32, 120, -16, 32)

    
    def check_collision(self, objects):
        """
            This method handles the collisions of Mario
            @param objects: the tuple containing all the objects (blocks)
        """
        # Set collisions with blocks
        for index in range(len(objects)):
            # Only get the predefined touchable blocks
            if objects[index].touchable:
                for x, y in objects[index].pos:
                    # Interval for the base ("floor") of the block. It starts in a negative value so Mario can collide with the left side of it, and it ends with +2 so there is some space.
                    for i in range(-12, objects[index].sprite[3]+2):
                        # If Mario's x position is in that interval
                        if self.x == x+i:
                            # If Mario's y position is equal to the y position of the block but minus Mario's height (so we get when Mario is exactly above the block)
                            if self.y == y-self.sprite[4]:
                                # Set touching_up to be the position of the block (so we can after unset it checking the difference of the distance between Mario and the block position)
                                self.touching_up = (x, y)
                                # Set the floor to fall to be that block
                                self.aux = self.y
                            # If Mario's y position is equal to the y position of the block but plus its height (so we get exactly we Mario is under the block) 
                            elif self.y == y+objects[index].sprite[4] and not self.falling:
                                # Set touching_down to be the position of the block (so we can after unset it checking the difference of the distance between Mario and the block position)
                                self.touching_down = (x, y)
                    
                    # Interval for the side ("wall") of the block. It start from negative height of Mario so Mario can collide correctly with the upper side of the "wall"
                    for i in range(-self.sprite[4], objects[index].sprite[4]):
                        # If Mario's y position is in that interval
                        if self.y == y+i:
                            # Avoid when the y position is exactly when Mario is above the block (touching_up)
                            if i != -self.sprite[4]:
                                # Check when Mario's in the left side of the block. -2 because we want some space. Be aware that this value must be set accordingy to the start of the base interval (-12), so we don't leave a free space in which the player can go through the block
                                if self.x+self.sprite[3]-2 == x:
                                    # Set touching_right to be the position of the block (so we can after unset it checking the difference of the distance between Mario and the block position)
                                    self.touching_right = (x, y)
                                # Check when Mario's in the right side of the block. +2 because we want some space. Be aware that this value must be set accordingy to the end of the base interval (objects[index].sprite[3]+2), so we don't leave a free space in which the player can go through the block
                                elif self.x == x+objects[index].sprite[3]+2:
                                    # Set touching_left to be the position of the block (so we can after unset it checking the difference of the distance between Mario and the block position)
                                    self.touching_left = (x, y)
                    
                    # If Mario's right side is touching some block
                    if self.touching_right:
                        # Since Super Mario has a different height of normal Mario, we have to have 2 different conditionals
                        if self.big:
                            # Check if the difference between their positions is greater or equal than Mario's height (equal because we may find the situation in which it is equal when Mario is Super Mario and Mario gets stuck)
                            if abs(self.touching_right[1]-self.y)>=self.sprite[4]:
                                self.touching_right = ()
                        else:
                            if abs(self.touching_right[1]-self.y)>objects[index].sprite[4]:
                                self.touching_right = ()
                    # The same for Mario's left side (from the right)
                    elif self.touching_left:
                        if self.big:
                            if abs(self.touching_left[1]-self.y)>=self.sprite[4]:
                                self.touching_left = ()
                        else:
                            if abs(self.touching_left[1]-self.y)>objects[index].sprite[4]:
                                self.touching_left = ()

                    # If Mario is above of a block but the distance between his y position and the y position of the block is greater than 16 or if the distance between his x position and the x position of the block is greater or equal than the block's height (equal to avoid being stuck in the air if the block were in the middle of the screen), set that Mario is not touching any block from its upper side
                    if self.touching_up and (abs(self.touching_up[1]-self.y)>objects[index].sprite[4] or abs(self.touching_up[0]-self.x)>=objects[index].sprite[3]):
                        self.touching_up = ()
                    # The same for being under the block, but without the equal in the distance between the x positions because we cannot get stuck here.
                    elif self.touching_down and (abs(self.touching_down[1]-self.y)>objects[index].sprite[4] or abs(self.touching_down[0]-self.x)>objects[index].sprite[3]):
                        self.touching_down = ()

        if self.jumping:
            if not self.touching_down:
                # If jumping and not being under any block, increase the y position of Mario
                self.y -= 4
                # When the y position of Mario in this moment plus 76 (76 is the height of the jump, remember that + means going down since y=0 is on the top) if equal to the "floor to fall", then stop jumping and start falling
                if(self.aux == (self.y + 76)):
                    self.jumping = False
                    self.falling = True
            else:
                # If being under a block, fall
                self.jumping = False
                self.falling = True
        else:
            # If not jumping but nor in the floor nor being above a block, then fall (because Mario is in the air)
            if(self.y != self.aux and not self.touching_up):
                self.y += 4
                self.falling = True
            else:
                self.falling = False
                # When Mario is not in the air, set its sprite to the "normal" one: static Mario or static Super Mario
                if not self.big:
                    if self.direction:
                        self.sprite = (0, 0, 48, 16, 16)
                    else:
                        self.sprite = (0, 0, 48, -16, 16)
                else:
                    # If going from normal Mario to Super Mario, adapt its y position to the sprite's height of Super Mario
                    if self.sprite == (0, 0, 48, 16, 16) or self.sprite == (0, 0, 48, -16, 16) or self.sprite == (0, 48, 104, 16, 16) or self.sprite == (0, 48, 104, -16, 16):
                        self.y -= 16
                    if self.direction:
                        self.sprite = (0, 0, 72, 16, 32)
                    else:
                        self.sprite = (0, 0, 72, -16, 32)


        # If not being above a block nor jumping, the set the "floor to fall" to its default value. If Super Mario, we have to increase this value because Mario's height increases
        if not self.touching_up and not self.jumping:
            self.aux = 216 if not self.big else 200

        # If we are above or under a block, stop jumping
        if self.touching_down or self.touching_up:
            self.jumping = False


        # If touching a normal or question block from below and it is not destroyed, destroy it
        # We put this here and not directly when we set touching_down so we cannot destroy 2 blocks at the same time
        if self.touching_down:
            for i in range(len(objects)):
                # Get the normal and question blocks (in Board we extended the lists nblocks and qblocks after the fifth element)
                if i > 4:
                    if not objects[i].destroyed:
                        # If the block that Mario is touching from below is the block of the loop, destroy that exact block if it has not been destroyed yet
                        if objects[i].pos[0][0] == self.touching_down[0] and objects[i].pos[0][1] == self.touching_down[1]:
                            objects[i].destroy(self.big)
