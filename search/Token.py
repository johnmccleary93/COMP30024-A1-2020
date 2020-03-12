class Token:
    def __init__(self, color, coords, size=1):
        self.color = color
        self.coords = coords
        self.size = size #Can we assume that on initialization, will never include a stack