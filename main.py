from lib.libs import *

class App(tkinter.Tk):
    def cursor_position_print(self, args):
        x = self.winfo_pointerx() - self.winfo_rootx()
        y = self.winfo_pointery() - self.winfo_rooty()
        print("х={} y={}".format(x, y))

    def __init__(self):
        super().__init__()
        self.title("Object Detection")

        self.frame = tkinter.Frame(self)
        self.frame.grid()

        self.image = Image.open("src/test.jpg")
        self.photo = ImageTk.PhotoImage(self.image)

        self.canvas = tkinter.Canvas(self, width = 500, height = 500)
        self.c_image = self.canvas.create_image(0, 0, anchor = 'nw', image = self.photo)
        self.canvas.grid(row = 2, column = 2)

        self.bind('<Motion>', self.cursor_position_print)
        

if __name__ == '__main__':
    app = App()
    app.mainloop()
    
