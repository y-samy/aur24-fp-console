class Box:
    def __init__(self, dest_coords: dict, pickup_coords):
        self.dest_coords = dest_coords
        self.pickup_coords = pickup_coords
        self.is_picked_up = False

class BoxHandler:
    def __init__(self, callback_on_new_box=None):
        self.__boxes = []
        self.__callback_on_new_box = callback_on_new_box # TODO: Handle None

    def set_callback_on_new_box(self, callback_on_new_box):
        self.__callback_on_new_box = callback_on_new_box

    def pickup(self, box_num: int):
        self.__boxes[box_num].is_picked_up = True

    def drop(self, box_num: int):
        self.__boxes[box_num].is_picked_up = False

    def receive_coords(self, coords: str):
        coords = coords.split("&")
        if len(coords) < 2 or not all(coord.startswith(("X=", "Y=")) for coord in coords):
            print("Invalid coordinates format:", coords)
            return

        coords = {"X": coords[0][2:], "Y": coords[1][2:]}
        is_unique = True
        #self.__callback_on_new_box(coords) #debug
        for i, box in enumerate(self.__boxes):
            if box.dest_coords == coords:
                is_unique = False
                return f"Box {1+i}"
        if is_unique:
            new_box = Box(coords, 1) 
            self.__boxes.append(new_box)
            print("New box added:", coords)
            self.__callback_on_new_box(coords)
            return f"Box {1+len(self.__boxes)}"
        

