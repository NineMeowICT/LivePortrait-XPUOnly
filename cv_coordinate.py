import cv2
from ffmpeg import FFmpeg

def mouse_callback(event, x, y, flags, param):
    global x_start, y_start, x_end, y_end, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        x_start, y_start = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            x_end, y_end = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if x_end < x_start:
            x_start, x_end = x_end, x_start
        if y_end < y_start:
            y_start, y_end = y_end, y_start

        width = x_end - x_start
        height = y_end - y_start
        print(f"Selection: Top Left: ({x_start}, {y_start}), Width: {width}, Height: {height}")
        print("If you want to exit, press 'q'.")


x_start, y_start, x_end, y_end = 0, 0, 0, 0
drawing = False

video_path = input('Please enter the video path: ')
cap = cv2.VideoCapture(video_path)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Video", width, height)
cv2.setMouseCallback("Video", mouse_callback)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if drawing:
        cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)

    cv2.imshow("Video", frame)

    key = cv2.waitKey(25) & 0xFF
    if key == ord('q') or key == 27:
        break

cap.release()
cv2.destroyAllWindows()

crop = input('Do you want to crop the video using FFmpeg (You need to install FFmpeg at first)? (y/n) ')

if crop == 'y':
    while True:
        square = input("In order to make the output video a square, please specify the side length. (follow width(w) or height(h))")
        try:
            assert square in ("w","h")
        except AssertionError:
            print("Please input a valid option (w/h).")
            continue
        break
    
    if square == 'h':
        length = y_end - y_start
    else:
        length = x_end - x_start

        
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input(video_path)
        .output(
            "output.mp4",
            {"codec:v": "libx264", "an": None},
            vf=f"crop={length}:{length}:{x_start}:{y_start}"
        )
    )

    ffmpeg.execute()

