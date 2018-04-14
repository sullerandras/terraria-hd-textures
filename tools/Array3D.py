import copy

TRANSPARENT = (0, 0, 0, 0)

class Array3D(object):
    def __init__(self, data, width=0, height=0, depth=0):
        if width == 0 or height == 0 or depth == 0:
            raise Exception('Invalid parameters: width: %s, height: %s, depth: %s' % (width, height, depth))
        if depth != 4:
            raise Exception('Depth must be 4 but got %d' % depth)
        super(Array3D, self).__init__()
        self.data = data
        self.width = width
        self.height = height
        self.depth = depth

    def isOpaque(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return self.data[y][x * self.depth + 3] > 0

    def isTransparent(self, x, y):
        return not self.isOpaque(x, y)

    def anyNeighborsAreOpaque(self, x, y):
        return self.isOpaque(x - 1, y) or self.isOpaque(x + 1, y) or self.isOpaque(x, y - 1) or self.isOpaque(x, y + 1)

    def getPixelAt(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return
        return self.data[y][x * self.depth : (x + 1) * self.depth]

    def setPixelAt(self, x, y, color):
        if len(color) != self.depth:
            raise Exception('Color len should be %d but got %d' % (self.depth, len(color)))
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return
        for i in range(self.depth):
            if color[i] < 0 or color[i] > 255:
                raise Exception('Invalid color component: %d' % color[i])
            self.data[y][x * self.depth + i] = color[i]

    def copyAndRotate(self, fromx, fromy, tox, toy, width, height, rotation):
        rotation = rotation % 4
        for x in range(width):
            for y in range(height):
                if rotation == 0:
                    self.setPixelAt(tox + x, toy + y, self.getPixelAt(fromx + x, fromy + y))
                elif rotation == 1:
                    self.setPixelAt(tox + (height - 1 - y), toy + x, self.getPixelAt(fromx + x, fromy + y))
                elif rotation == 2:
                    self.setPixelAt(tox + (width - 1 - x), toy + (height - 1 - y), self.getPixelAt(fromx + x, fromy + y))
                elif rotation == 3:
                    self.setPixelAt(tox + y, toy + (width - 1 - x), self.getPixelAt(fromx + x, fromy + y))

    def nearestNonSeparator(self, x, y, vertical):
        if (x == self.width - 1) or (y == self.height - 1):
            return TRANSPARENT
        if vertical: # vertical separator line
            if self.isOpaque(x - 1, y):
                return self.getPixelAt(x - 1, y)
            return self.getPixelAt(x + 1, y)
        if not vertical: # horizontal separator line
            if self.isOpaque(x, y - 1):
                return self.getPixelAt(x, y - 1)
            return self.getPixelAt(x, y + 1)
        return TRANSPARENT

    def clone(self):
        return Array3D(copy.deepcopy(self.data), self.width, self.height, self.depth)
