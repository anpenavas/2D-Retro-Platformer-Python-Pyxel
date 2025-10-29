class Special:
    def __init__(self, pos: list, sprite: tuple):
        """
            This magic method is used to declare the attributes of the class.
            @param pos: set the position of the special object as a list: [x, y]
            @param sprite: set the sprite of the special object as a tuple: (img, u, v, width, height)
        """
        self.sprite = sprite
        self.pos = pos
        self.active = False
        self.added = False
        self.init_time = 0
    
    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, pos: list):
        if type(pos) != list:
            raise TypeError("The position must be a list [x, y]")
        else:
            self.__pos = pos

    @property
    def sprite(self):
        return self.__sprite

    @sprite.setter
    def sprite(self, sprite: tuple):
        if type(sprite) != tuple:
            raise TypeError("The sprite must be a tuple (img, u, v, width, height)")
        elif len(sprite) != 5:
            raise ValueError("The sprite must contain 5 element (img, u, v, width, height)")
        else:
            self.__sprite = sprite