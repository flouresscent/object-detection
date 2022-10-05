from array import array
from lib.libs import *
from lib.video_proc import *

class App(tkinter.Tk):
    image = Image.open("video-opencv/frame0-00-00.10.jpg")
    click_num = 0
    left_top_point = array('i', [0, 0])
    right_bottom_point = array('i', [0, 0])

    def choose_obj(self, args):
        x = self.winfo_pointerx() - self.winfo_rootx()
        y = self.winfo_pointery() - self.winfo_rooty()

        if (self.click_num == 0):
            self.left_top_point = [x, y]
            print("left_top_point " + str(self.left_top_point))
            print(self.click_num)

        if (self.click_num == 1):
            self.right_bottom_point = [x, y]
            print("right_bottom_point " + str(self.right_bottom_point))
            print(self.click_num)

            self.image.crop((self.left_top_point[0], self.left_top_point[1], self.right_bottom_point[0], self.right_bottom_point[1])).save('src/test_crop.jpg', quality=95)
            self.click_num = 0

        self.click_num += 1

    def __init__(self):
        SAVING_FRAMES_PER_SECOND = 10

        super().__init__()
        self.title("Object Detection")

        filename, _ = os.path.splitext("video")
        filename += "-opencv"
        # создаем папку по названию видео файла
        if not os.path.isdir(filename):
            os.mkdir(filename)
        # читать видео файл    
        cap = cv2.VideoCapture()
        cap.open("src/video.mp4")
        # получить FPS видео
        fps = cap.get(cv2.CAP_PROP_FPS)
        # если SAVING_FRAMES_PER_SECOND выше видео FPS, то установите его на FPS (как максимум)
        saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
        # получить список длительностей для сохранения
        saving_frames_durations = get_saving_frames_durations(cap, saving_frames_per_second)

        count = 0
        print("Обработка видео")
        while True:
            is_read, frame = cap.read()
            if not is_read:
                print("Обработка видео завершена успешно")
                
                # выйти из цикла, если нет фреймов для чтения
                break
            # получаем продолжительность, разделив количество кадров на FPS
            frame_duration = count / fps
            try:
                # получить самую раннюю продолжительность для сохранения
                closest_duration = saving_frames_durations[0]
            except IndexError:
                # список пуст, все кадры длительности сохранены
                break
            if frame_duration >= closest_duration:
                # если ближайшая длительность меньше или равна длительности кадра,
                # затем сохраняем фрейм
                frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
                cv2.imwrite(os.path.join(filename, f"frame{frame_duration_formatted}.jpg"), frame) 
                # удалить точку продолжительности из списка, так как эта точка длительности уже сохранена
                try:
                    saving_frames_durations.pop(0)
                except IndexError:
                    pass
            # увеличить количество кадров
            count += 1



        self.frame = tkinter.Frame(self)
        self.frame.grid()

        self.image = Image.open("video-opencv/frame0-00-00.10.jpg")

        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas = tkinter.Canvas(self, width = self.image.width, height = self.image.height)
        self.c_image = self.canvas.create_image(0, 0, anchor = 'nw', image = self.photo)
        self.canvas.grid(row = 2, column = 2)

        self.canvas.bind('<Button-1>', self.choose_obj)
        
        

if __name__ == '__main__':
    app = App()
    app.mainloop()
    
