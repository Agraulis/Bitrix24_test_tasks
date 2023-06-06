import cv2
import numpy as np

FILE_NAME = "ticker"
TEXT = "HI 1234567890 It's very funny"
DURATION = 3
SIZE = 100
FPS = 30

# создаем видео
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(f'{FILE_NAME}.mp4', fourcc, FPS, (SIZE, SIZE))

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
thickness = 2
color = (255, 125, 255)
bg_color = (0, 125, 0)
text_size, _ = cv2.getTextSize(TEXT, font, font_scale, thickness)
text_width, text_height = text_size
scroll_speed = (text_width + SIZE) / DURATION

# создаем фон
background = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)
background[:] = bg_color

# начальное положение текста
x = SIZE
y = int((SIZE - text_height) / 2)

# генерируем кадры
for i in range(FPS * DURATION):
    img = background.copy()
    cv2.putText(img, TEXT, (x, y), font, font_scale, color, thickness)

    shift = int(scroll_speed // FPS)
    x -= shift if shift else 1
    if x < -text_width:
        x = SIZE

    # записываем кадр в видео
    out.write(img)

# закрываем видео
out.release()
