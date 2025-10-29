class Enemy:
    def __init__(self, x: int, y: int, sprite: tuple):
        """
            This magic method is used to declare the attributes of the class.
            @param x: set the x position of the enemy
            @param y: set the y position of the enemy
            @param sprite: set the sprite of the enemy as a tuple: (img, u, v, width, height)
        """
        self.alive = True
        self.x = x
        self.y = y
        self.sprite = sprite
        self.direction = False
        self.init_time = 0

    @property
    def x(self):
        return self.__x 
    
    @x.setter
    def x(self, x: int):
        if type(x) != int:
            raise TypeError("The x position must be an integer")
        else:
            self.__x = x
    
    @property
    def y(self):
        return self.__y
    
    @y.setter
    def y(self, y: int):
        if type(y) != int:
            raise TypeError("The y position must be an integer")
        else:
            self.__y = y

    @property
    def sprite(self):
        return self.__sprite
    
    @sprite.setter
    def sprite(self, sprite: tuple):
        if type(sprite) != tuple:
            raise TypeError("The sprite must be a tuple (img, u, v, width, height)")
        else:
            self.__sprite = sprite