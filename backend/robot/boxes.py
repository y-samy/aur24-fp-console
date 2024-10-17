class Box:
    def __init__(self, dest_coords, pickup_coords):
        self.dest_coords = dest_coords
        self.pickup_coords = pickup_coords

class BoxHandler:
    def __init__(self):
        self.boxes = []
        self.accepting_boxes = False

    def store_box(self, box):
        if self.accepting_boxes:
            if box not in self.boxes:
                self.boxes.append(box)
                print(self.boxes)

