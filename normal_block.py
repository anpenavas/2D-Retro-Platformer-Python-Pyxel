from block import Block

class Normal_Block(Block):
    def __init__(self, pos: tuple):
        """Since we are inheriting the Block class, call its __init__, passing as parameters if the block is touchable, its sprite and its position"""
        # Although self.pos is simply (x, y), we put this tuple into a list so we can simplify the algorithm with a simple loop
        super().__init__(True, (0, 0, 16, 16, 16), [pos])
        self.destroyed = False

    def destroy(self, big: bool):
        """
            This method destroys the block.
            @param big: if mario is Super Mario or not
        """
        # Destroy the block by setting its sprite to the background sprite and emptying its position (x, y); only if mario is Super Mario
        if big:
            self.destroyed = True
            self.sprite = (0, 0, 0, 16, 16)
            self.pos = []