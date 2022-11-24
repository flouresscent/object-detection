import cv2
import numpy as np

img_path = "src/img_to_choose_obj.png"
img = cv2.imread(img_path)
copy = img.copy()

video_path = "src/video.mp4"
video = cv2.VideoCapture(video_path)

border_color = [76, 210, 101]

main_win_show = True

click_num = 0
ltp = [0, 0]
rbp = [0, 0]
slctd_obj = False

def select_obj(event, x, y, flags, param):
    global img, copy, click_num, ltp, rbp, slctd_obj
        
    if event == cv2.EVENT_LBUTTONDOWN:
        if click_num == 0:
            img = copy.copy()
            slctd_obj = False

            ltp = [x, y]
            click_num += 1

        else:
            rbp = [x, y]
            click_num = 0
            print("[INFO] The object is selected.")

            slctd_obj = True

            cv2.imshow("choosed obj", img[ltp[1]:rbp[1], ltp[0]:rbp[0]]) #! debug
            cv2.imwrite("src/obj.jpg", img[ltp[1]:rbp[1], ltp[0]:rbp[0]])
            print("[INFO] The selected object is saved.")

            cv2.rectangle(img, (ltp[0], ltp[1]), (rbp[0], rbp[1]), (border_color[0], border_color[1], border_color[2]), 2)

cv2.namedWindow("main")
cv2.setMouseCallback("main", select_obj)
cv2.imshow("main", img)

while True:
    if slctd_obj:
        if main_win_show:
            cv2.destroyWindow("main")
            main_win_show = False

        success, frame = video.read()

        #methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR, cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED] 

        img_to_find_obj = cv2.imread("src/img_to_find_obj5.png")
        obj = cv2.imread("src/obj.jpg")

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        frame_gray = cv2.GaussianBlur(frame_gray, (5, 5), 0)
        frame_gray = cv2.Canny(frame_gray, 50, 300)
        cv2.imshow("test", frame_gray)

        obj_gray = cv2.cvtColor(obj, cv2.COLOR_RGB2GRAY)
        obj_gray = cv2.GaussianBlur(obj_gray, (5, 5), 0)
        obj_gray = cv2.Canny(obj_gray, 50, 300)
        cv2.imwrite("src/obj_proc.jpg", obj_gray)
        cv2.imshow("test1", obj_gray)

        result = cv2.matchTemplate(frame_gray, obj_gray, cv2.TM_CCOEFF)
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)

        (startX, startY) = maxLoc
        endX = startX + obj.shape[1]
        endY = startY + obj.shape[0]

        cv2.rectangle(frame, (startX, startY), (endX, endY), (255, 0, 0), 2)
        cv2.imshow("result", frame)

        print("[INFO] The work of program is finished automatically.")
        print("[INFO] Video is fully processed.")

    if cv2.waitKey(20) & 0xFF == 27:
        print("[INFO] The program is certified by pressing 'ESC'.")
        break

cv2.destroyAllWindows()