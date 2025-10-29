class Block:
    def __init__(self, touchable, sprite, pos):
        """
            This magic method is used to declare the attributes of the class.
            @param touchable: set if the block can be touched by Mario (for example, Mario cannot touch a bush but he can touch a question block)
            @param sprite: set the sprite of the block as a tuple: (img, u, v, width, height)
            @pos: set the positions of the all the blocks as a list containing the each position as a tuple (x, y)
        """
        self.touchable = touchable
        self.sprite = sprite
        self.pos = pos

    @property
    def touchable(self):
        return self.__touchable

    @touchable.setter
    def touchable(self, touchable: bool):
        if type(touchable) != bool:
            raise TypeError("The touchable attribute must be boolean")
        else:
            self.__touchable = touchable

    @property
    def sprite(self):
        return self.__sprite

    @sprite.setter
    def sprite(self, sprite: tuple):
        if type(sprite) != tuple:
            raise TypeError("The sprite must be a tuple (img, u, v, width, height)")
        else:
            self.__sprite = sprite
    
    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, pos: list):
        if type(pos) != list:
            raise TypeError("The position must be a list containing all the positions (in the case of the normal or question block, it would be a list with only 1 element). Each position is (x, y)")
        else:
            self.__pos = pos