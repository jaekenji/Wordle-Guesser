import customtkinter as ctk

class Wordle:
    def __init__(self):
        self.app                     = None
        self.squares_frame           = None
        self.squares_and_labels      = {}
        self.square_row_now          = 0
        self.square_now              = 0
        self.square_colors           = {
            "#79B851": "#F3C237", 
            "#F3C237": "#292929", 
            "#292929": "#79B851"
        }
        self.start()     

    def start(self):
        if not self.initialize():
            print("[!] Failed to configure app.")

        if not self.build_squares_frame():
            print("[!] Failed to build squares' frame.")

        if not self.build_squares():
            print("[!] Failed to build squares.")
        
        self.app.mainloop()

    def initialize(self):
        self.app                     = ctk.CTk()
        self.app.geometry(
            "500x665"
        )
        self.app.title(
            "Wordle"
        )
        self.app.resizable(
            False, 
            False
        )
        self.app.configure(
            fg_color                 = "#101010"
        )
        self.app.bind(
            "<KeyPress>", 
            self.key_clicked
        )
        return True

    def build_squares_frame(self):
        self.squares_frame           = ctk.CTkFrame(
            self.app, 
            width                    = 340, 
            height                   = 410, 
            fg_color                 = "#101010",
            bg_color                 = "#101010",
            border_width             = 0
        )
        self.squares_frame.place(
            x                        = 80,
            y                        = 120
        )
        return True

    def build_squares(self):
        for row in range(6):
            for column in range(5):
                square               = self.create_square(row, column)
                label                = self.create_label(square)
                self.squares_and_labels[(row, column)] = (square, label)
        return True

    def create_square(self, row, col):
        square                       = ctk.CTkFrame(
            self.squares_frame, 
            width                    = 60,
            height                   = 60, 
            corner_radius            = 10, 
            fg_color                 = "#101010",
            border_color             = "#252525",
            border_width             = 2
        )
        square.place(
            x                        = col * 70,
            y                        = row * 70
        )                         
        return square             
                                  
    def create_label(self, square):
        square_label = ctk.CTkLabel(
            square,               
            text                     = "", 
            font                     = ("Shoika Bold", 30), 
            text_color               = "#F0F0F0"
        )
        square_label.place(
            relx                     = 0.5,
            rely                     = 0.5,
            anchor                   = "center"
        )
        return square_label

    def key_clicked(self, event):
        key = event.char.upper()

        if key in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and event.char.isalpha() and self.square_now < 5:
            self.type_letter(key)

        if event.keysym == "BackSpace":
            self.delete_letter()

        if event.keysym == "space":
            self.change_color()

        if event.keysym == "Return" and  self.square_now == 5 and self.verify_squares():
            self.square_row_now     += 1
            self.square_now          = 0
            # do something here

    def type_letter(self, letter):
        square                       = self.squares_and_labels[(self.square_row_now, self.square_now)][0]
        square.configure(
            border_color             = "#707070"
        )
        square_label                 = self.squares_and_labels[(self.square_row_now, self.square_now)][1]
        square_label.configure(
            text                     = letter
        )
        self.square_now             += 1

    def delete_letter(self):
        if self.square_now == 0:
            return

        self.square_now             -= 1
        square                       = self.squares_and_labels[(self.square_row_now, self.square_now)][0]
        square.configure(
            fg_color                 = "#101010",
            border_color             = "#252525"
        )
        square_label                 = self.squares_and_labels[(self.square_row_now, self.square_now)][1]
        square_label.configure(
            text                     = ""
        )

    def change_color(self):
        if self.square_now == 0:
            return

        square                       = self.squares_and_labels[(self.square_row_now, self.square_now - 1)][0]
        current_color                = square.cget("fg_color")

        if current_color not in self.square_colors:
            next_color               = "#79B851"
        else:
            next_color               = self.square_colors[current_color]

        square.configure(
            fg_color                 = next_color,
            border_color             = next_color,
        )

    def verify_squares(self):
        return True

if __name__ == "__main__":
    Wordle()