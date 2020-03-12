class Token:
    def __init__(self, color, coords):
        self.color = color
        self.coords = coords
        self.size = 1 #Can we assume that on initialization, will never include a stack