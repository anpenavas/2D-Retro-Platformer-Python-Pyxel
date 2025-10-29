from block import Block
from coin import Coin
from mushroom import Mushroom
import time

class Question_Block(Block):
    def __init__(self, pos: tuple, special: int):
        """Since we are inheriting the Block class, call its __init__, passing as parameters if the block is touchable, its sprite and its position"""
        # Although self.pos is simply (x, y), we put this tuple into a list so we can simplify the algorithm with a simple loop
        super().__init__(True, (0, 16, 0, 16, 16), [pos])
        self.destroyed = False

        # 66.6% chance of being a coin, 33.3% chance of being a mushroom.
        if special == 1:
            self.special = Mushroom([pos[0], pos[1]-self.sprite[4]])
        else:
            self.special = Coin([pos[0], pos[1]-self.sprite[4]])

    def destroy(self, big: bool):
        """
            This method destroys the block.
            @param big: we actually do not need this parameter, but we keep it so we can simplify the algorithm (call destroy both for Question_Block and Normal_Block)
        """
        self.destroyed = True
        # Set the block's sprite to the clear block
        self.sprite = (0, 16, 16, 16, 16)
        # Activate the special object of the block
        self.special.active = True
        # Set the time when the special object has been activated, so we can display it for some seconds in the case of the Coin
        self.special.init_time = time.time()
