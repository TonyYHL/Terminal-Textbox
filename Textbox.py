from copy import deepcopy, copy
from getkey import getkey, keys
from os import system

class textbox():
    enable_live = False

    def __init__(self,height=10,width=30,border="wave") -> None:
        self.border = border
        self.width = width
        self.height = height
        self.boxes = []
        self.str_rep = ""
    
    def create_box(self,position=(0,0),text="",width=0,height=0,overflow="...",priority=1,override=True) -> None:
        self.boxes.append({
            "position" : position, # x and y
            "text" : text,
            "width":width,
            "height":height,
            "overflow":overflow,
            "priority" : priority,
            "override":override,
            "colour" : "", # This is used in the textbox
            "variables" : {"is highlighted":False,
                            "overflow length":len(overflow),
                            "change line":False}
        })
    
    @classmethod
    def enable_liveedit(self) -> None:
        textbox.enable_live = True

    def live_edit(self) -> None:
        def clear() -> None:
            system("clear")
        def main_menu() -> None:
            print("***Press key to edit the textbox***")
            print("(C) Textbox configuration    (B) Edit a box")
        
        def tc_w() -> None:
            print(f"(W) Width: {self.width}")
        def tc_h() -> None:
            print(f"(H) Height: {self.height}")
        def tc_b() -> None:
            if self.border == "wave":
                print("Border type:\n       space   line    star    > wave <    empty")
            elif self.border == "star":
                print("Border type:\n       space   line    > star <    wave    empty")
            elif self.border == "line":
                print("Border type:\n       space   > line <    star    wave    empty")
            elif self.border == "space":
                print("Border type:\n       > space <   line    star    wave    empty")
            elif self.border == "empty":
                print("Border type:\n       space   line    star    wave    > empty <")
        def tc() -> None:
            while True:
                clear()
                print(self.__repr__())
                tc_w()
                tc_h()
                tc_b()
                print("(X) Exit")
                keyboard = getkey()
                if keyboard == "h":
                    new_height = int(input("New height: "))
                    if new_height <= 0:
                        input("Invalid!")
                    else:
                        self.height = new_height
                elif keyboard == "w":
                    new_width = int(input("New width: "))
                    if new_width <= 0:
                        input("Invalid!")
                    else:
                        self.width = new_width
                elif keyboard == keys.LEFT:
                    if self.border == "wave":
                        self.border = "star"
                    elif self.border == "star":
                        self.border = "line"
                    elif self.border == "line":
                        self.border = "space"
                    elif self.border == "space":
                        self.border = "empty"
                    elif self.border == "empty":
                        self.border = "wave"
                elif keyboard == keys.RIGHT:
                    if self.border == "wave":
                        self.border = "empty"
                    elif self.border == "empty":
                        self.border = "space"
                    elif self.border == "space":
                        self.border = "line"
                    elif self.border == "line":
                        self.border = "star"
                    elif self.border == "star":
                        self.border = "wave"
                elif keyboard == "x":
                    return
        
        def insert_str(string, str_to_insert, index):
            return string[:index] + str_to_insert + string[index:]
        def et(editing_box) -> str:
            if editing_box["variables"]["is highlighted"]:
                editing_box["variables"]["is highlighted"] = False
                editing_box["text"] = copy(editing_box["variables"]["text"])
            bstr = copy(editing_box["text"])
            bstr = bstr.replace("\033","\\033").replace("\n","\\n")
            len_bstr = len(bstr)
            cursor_index = len_bstr
            while True:
                clear()
                print(self.__repr__())
                len_bstr = len(bstr)
                if cursor_index < 0:
                    cursor_index = len_bstr
                elif cursor_index > len_bstr:
                    cursor_index = len_bstr
                print("""\033[0m*** Editing Text ***
Press Enter to finish.
""")
                if len_bstr != 0:
                    print(insert_str(bstr,"|",cursor_index))
                else:
                    print("|")
                keyboard = getkey()
                if keyboard == keys.ENTER:
                    return bstr.replace("\\033","\033").replace("\\n","\n")
                elif keyboard == keys.LEFT:
                    cursor_index -= 1
                elif keyboard == keys.RIGHT:
                    cursor_index += 1
                elif keyboard == keys.BACKSPACE:
                    if cursor_index != 0:
                        bstr = bstr[:cursor_index - 1] + bstr[cursor_index:]
                        cursor_index -= 1
                    #input("")
                else:
                    #bstr = bstr[:cursor_index] + bstr[cursor_index + 1:]
                    bstr = insert_str(bstr,keyboard,cursor_index)
                    cursor_index += 1

        def eb() -> None:
            editing_index = 0
            while True:
                clear()
                print(self.__repr__())
                try:
                    editing_box = self.boxes[editing_index]
                except IndexError:
                    editing_index = -1
                    editing_box = self.boxes[editing_index]
                if self.boxes != []:
                    print(f"""*** Use Left and Right arrow to change between boxes ***
id: {editing_index} pos: {editing_box["position"]}
    W          to adjust the position
A   S   D                       of the textbox

(T) Edit text
(I) Width: {editing_box["width"]}
(H) Height: {editing_box["height"]}
(P) Priority: {editing_box["priority"]}
(O) Overflow: {editing_box["overflow"]}
(R) Override text: {str(editing_box["override"])}

(L) Highlight the box by filling the box with characters
(Z) Delete box

""")
                print("""(N) Create a new textbox
(X) Exit
""")
                keyboard = getkey()
                if keyboard == keys.LEFT:
                    editing_index -= 1
                elif keyboard == keys.RIGHT:
                    editing_index += 1
                elif keyboard == "t":
                    self.boxes[editing_index]["text"] = copy(str(et(editing_box)))
                elif keyboard == "h":
                    new_height = int(input("New height: "))
                    if new_height <= 0:
                        input("Invalid!")
                    else:
                        editing_box["height"] = new_height
                elif keyboard == "i":
                    new_height = int(input("New width: "))
                    if new_height <= 0:
                        input("Invalid!")
                    else:
                        editing_box["width"] = new_height
                elif keyboard == "p":
                    new_height = int(input("New priority: "))
                    if new_height < 0:
                        input("Invalid!")
                    else:
                        editing_box["priority"] = new_height
                elif keyboard == "o":
                    new_height = input("New overflow: ")
                    editing_box["overflow"] = new_height
                    editing_box["variables"]["overflow length"] = len(new_height)
                elif keyboard == "r":
                    print("Override: (T) True (F) False")
                    r_key = getkey()
                    if r_key == "t":
                        editing_box["override"] = True
                    else:
                        editing_box["override"] = False
                elif keyboard == "w":
                    editing_box["position"] = (editing_box["position"][0],editing_box["position"][1]-1)
                elif keyboard == "s":
                    editing_box["position"] = (editing_box["position"][0],editing_box["position"][1]+1)
                elif keyboard == "a":
                    editing_box["position"] = (editing_box["position"][0]-1,editing_box["position"][1])
                elif keyboard == "d":
                    editing_box["position"] = (editing_box["position"][0]+1,editing_box["position"][1])
                elif keyboard == "z":
                    self.boxes.remove(self.boxes[editing_index])
                elif keyboard == "n": # New
                    self.create_box(text="\033[0mNot Edited",width=15,height=1)

                elif keyboard == "l":
                    if editing_box["variables"]["is highlighted"] == False:
                        editing_box["variables"]["is highlighted"] = True
                        editing_box["variables"]["text"] = copy(editing_box["text"])
                        editing_box["text"] = ""
                        for i in range(editing_box["height"]):
                            for j in range(editing_box["width"]):
                                editing_box["text"] += "@"
                    else:
                        editing_box["variables"]["is highlighted"] = False
                        editing_box["text"] = copy(editing_box["variables"]["text"])
                elif keyboard == "x":
                    return

        if not textbox.enable_live:
            print("Live edit is disabled!")
            return
        editing = True
        while editing:
            if self.boxes == []:
                self.create_box(text="(T) Edit",width=10,height=1,priority=0)
            clear()
            print(self.__repr__())
            main_menu()
            print("(X) Save and quit")
            keyboard = getkey()
            if keyboard == "c": # c complete
                tc()
            elif keyboard == "b":
                eb()
            elif keyboard == "x":
                clear()
                print(f"box = textbox(height={self.height},width={self.width},border=\"{self.border}\")")
                for box in self.boxes:
                    txt = box['text'].replace('\033','\\033').replace("\n","\\n")
                    print(f"box.create_box(position={box['position']}),width={box['width']},height={box['height']},priority={box['priority']},overflow=\"{box['overflow']}\",override={box['override']},text=\"{txt}\")")
                return

    def __repr__(self) -> str:

        saved_box = deepcopy(self.boxes)

        if self.border == "space":
            border_horizontal_char = " "
            border_verticle_char = " "
        elif self.border == "line":
            border_horizontal_char = "-"
            border_verticle_char = "|"
        elif self.border == "star":
            border_horizontal_char = "*"
            border_verticle_char = "*"
        elif self.border == "wave":
            border_horizontal_char = "~"
            border_verticle_char = "$"
        elif self.border == "empty":
            border_horizontal_char = ""
            border_verticle_char = ""
        
        complete_str = ""

        # Top border
        top_b_str = ""
        for i in range(self.width):
            top_b_str += f"{border_horizontal_char}"
        complete_str += top_b_str + "\n"

        # Body
        try:
            printing_box = self.boxes[0]
        except IndexError:
            return "Empty"
        for j in range(self.height):
            line = f"{border_verticle_char}"
            line_change = True
            new_colour = ""
            change = False # This enables colour
            for box in self.boxes: # This is used for \n
                box["variables"]["change line"] = False

            for i in range(self.width):
                replace = []
                for box in self.boxes:
                    if box["position"][0] <= i < box["position"][0] + box["width"]:
                        if box["position"][1] <= j < box["position"][1] + box["height"]:

                            if box["priority"] < printing_box["priority"]: # This enables the priority system
                                printing_box = box
                                change = True
                                new_colour = printing_box["colour"]
                            else:
                                if not (printing_box["position"][0] <= i < printing_box["position"][0] + printing_box["width"]):
                                    printing_box = box
                                    change = True
                                    new_colour = printing_box["colour"]
                                elif not (printing_box["position"][1] <= j < printing_box["position"][1] + printing_box["height"]):
                                    printing_box = box
                                    change = True
                                    new_colour = printing_box["colour"]
                            if box["override"] == True:
                                replace.append(box)
                try:
                    replace.remove(printing_box)
                except:
                    pass
                    
                for box in replace:
                    box["text"] = box["text"][1:]

                # Sort colour
                if change:
                    line += "\033[0m"
                    line += new_colour
                    change = False
                if line_change:
                    line += printing_box["colour"]
                    line_change = False

                # This section adds text to the line
                if printing_box["variables"]["change line"]: # used for \n to change the line
                    line += " "
                    continue

                if printing_box["position"][0] <= i < printing_box["position"][0] + printing_box["width"]:
                    if printing_box["position"][1] <= j < printing_box["position"][1] + printing_box["height"]:
                        if printing_box["text"] != "":
                            if printing_box["text"][0] == "\033":
                                color_txt = ""
                                for c in range(6):
                                    color_txt += printing_box["text"][0]
                                    if printing_box["text"][0] == "m":
                                        printing_box["colour"] = color_txt
                                        break
                                    printing_box["text"] = printing_box["text"][1:]
                                printing_box["text"] = printing_box["text"][1:]
                                line += color_txt
                                line += printing_box["text"][0]
                                printing_box["text"] = printing_box["text"][1:]
                            elif printing_box["text"][0] == "\n":
                                printing_box["variables"]["change line"] = True
                                line += " "
                                printing_box["text"] = printing_box["text"][1:]
                            else:
                                line += printing_box["text"][0]
                                printing_box["text"] = printing_box["text"][1:]
                        else:
                            line += " "
                    else:
                        line += " "
                else:
                    line += " "
                
                # This enables overflow system
                overflow_length = printing_box["variables"]["overflow length"]
                if i+overflow_length == printing_box["width"] + printing_box["position"][0]:
                    if j+1 == printing_box["position"][1] + printing_box["height"]:
                        if printing_box["text"] != "":
                            line = line[:-overflow_length]
                            line += printing_box["overflow"]
                            printing_box["text"] = ""

            line += "\033[0m"
            line += f"{border_verticle_char}"
            complete_str += line + "\n"
        
        # Bottom border
        top_b_str = ""
        for i in range(self.width):
            top_b_str += f"{border_horizontal_char}"
        complete_str += top_b_str + "\n"

        self.boxes = saved_box
        return complete_str

    def get_str(self) -> str:
        self.str_rep = self.__repr__().replace("\033","\\033").replace("\n","\\n")
        return self.str_rep
