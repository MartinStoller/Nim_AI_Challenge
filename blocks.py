from pygame_textinput import *

BLOCKSIZE = 60

class Block:
    def __init__(self, id, colour, position, size):
        self.size = size  # int: edge length
        self.colour = colour  # (R, G, B)
        self.id = id  # int
        self.position = position  # (x, y)

    def render(self, screen):
        pygame.draw.rect(screen, self.colour, (self.position[0], self.position[1], self.size, self.size))


def drawAllBlocks(screen, piles):
    """
    :param screen: =SCREEN
    :param piles: vgl Nim class: Piles is an Array [nr_blocks(line1), nr_blocks(line2), ..., nr_blocks(line4)
    :return: nothing

    takes the amount of blocks per line from piles and creates block objects with desired coordinates accordingly
    then it puts all block objects in a list and iteratively draws them on screen
    """

    blocks_line1 = []
    blocks_line2 = []
    blocks_line3 = []
    blocks_line4 = []

    position = (272, 353)
    for i in range(piles[0]):
        blocks_line1.append(Block(i, (0, 100, 255), position, BLOCKSIZE))
    position = (352, 433)
    for i in range(piles[1]):
        blocks_line2.append(Block((i*10), (0, 100, 255), position, BLOCKSIZE))
        position = (position[0]-80, position[1])
    position = (432, 513)
    for i in range(piles[2]):
        blocks_line3.append(Block((i*100), (0, 100, 255), position, BLOCKSIZE))
        position = (position[0]-80, position[1])
    position = (512, 593)
    for i in range(piles[3]):
        blocks_line4.append(Block((i*1000), (0, 100, 255), position, BLOCKSIZE))
        position = (position[0]-80, position[1])

    block_list = itertools.chain(blocks_line1, blocks_line2, blocks_line3, blocks_line4)
    for block in block_list:
        block.render(screen)
