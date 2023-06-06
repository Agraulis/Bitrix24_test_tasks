from django.http import FileResponse
from django.views.generic import TemplateView
import cv2
import numpy as np
from .models import Request


class MakeTicker(TemplateView):
    template_name = 'mainapp/index.html'

    def post(self, request, *args, **kwargs):
        file_name = "ticker"
        text = request.POST["textinput"]
        duration = 3
        size = 100
        fps = 30

        # сохраним запрос в БД
        req = Request()
        req.text = text
        req.background_color = 'green' if request.POST['selectbasic'] == '1' else 'blue'
        req.save()

        # создаем видео
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(f'{file_name}.mp4', fourcc, fps, (size, size))

        font = cv2.FONT_HERSHEY_COMPLEX
        font_scale = 1
        thickness = 3
        color = (255, 125, 255)
        bg_color = (0, 128, 0) if request.POST['selectbasic'] == '1' else (255, 0, 0)
        text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
        text_width, text_height = text_size
        scroll_speed = (text_width + size) // duration

        # создаем фон
        background = np.zeros((size, size, 3), dtype=np.uint8)
        background[:] = bg_color

        # начальное положение текста
        x = size
        y = int((size - text_height) / 2)

        # генерируем кадры
        for i in range(fps * duration):
            img = background.copy()
            cv2.putText(img, text, (x, y), font, font_scale, color, thickness)

            shift = scroll_speed // fps
            x -= shift if shift else 1
            if x < -text_width:
                x = size

            # записываем кадр в видео
            out.write(img)

        # закрываем видео
        out.release()

        response = FileResponse(open(f'./{file_name}.mp4', 'rb'), as_attachment=True)

        return response
