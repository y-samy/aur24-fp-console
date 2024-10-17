class Box:
    def __init__(self, dest_coords: dict, pickup_coords):
        self.dest_coords = dest_coords
        self.pickup_coords = pickup_coords
        self.is_picked_up = False

class BoxHandler:
    def __init__(self):
        self.boxes = []

    def pickup(self, box_num: int):
        self.boxes[box_num].is_picked_up = True

    def drop(self, box_num: int):
        self.boxes[box_num].is_picked_up = False

    def receive_coords(self, coords: str):
        coords = coords.split("&")
        coords = {'X': coords[0][2:], 'Y': coords[1][2:]}
        is_unique = True
        for box in self.boxes:
            if box.dest_coords == coords:
                is_unique = False
                break
        if is_unique:
            new_box = Box(coords, 1) # TODO: ADD PARAMETERS
            self.boxes.append(new_box)
            print(coords)