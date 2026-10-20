#HONORABLE MENTION FOR [Mehmet](in Hackclub)!!


# So basically, to scan every obstacle like I did on the obstacle.py 


class SpatialGrid:
    def __init__(self, cell_size=64):
        self.cell_size = cell_size
        self.cells = {}

    def _cell_range(self, rect):
        _min_x = rect.left // self.cell_size
        _max_x = (rect.right - 1) // self.cell_size
        _min_y = rect.top // self.cell_size
        _max_y = (rect.bottom - 1) // self.cell_size

        #Math makes me sleepy...

        for cell_x in range(_min_x, _max_x + 1):
            for cell_y in range(_min_y, _max_y + 1):
                yield cell_x, cell_y
    

    def insert(self, obstacle):
        for cell in self._cell_range(obstacle.rect):
            self.cells.setdefault(cell, []).append(obstacle) #There is more than just the simple stuffs in pygame...
    
    def query(self, rect):
        nearby = []
        already_seen = set()

        for cell in self._cell_range(rect):
            for obstacle in self.cells.get(cell,[]):
                obstacle_id = id(obstacle) #OHHH MEMORY ID? We learn smth new everyday

                if obstacle_id not in already_seen:
                    already_seen.add(obstacle_id)
                    nearby.append(obstacle)
        return nearby
    
