from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
from PIL import Image, ImageDraw
from django.http import JsonResponse
import time
import random

# views.py 파일 내부에 있는 코드 예제

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload(request):
    if request.method == 'POST':
        file = request.FILES['video']
        with open('/home/work/file_bak/202401/django-server/mysite/mysite/data/video.mp4', 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return HttpResponse('<script>alert("File uploaded successfully"); location.href="/proxy/8000/main/"; </script>')
    return HttpResponse('Only POST requests are allowed')

def main_page(request):
    return render(request, 'main_page.html')

is_start = 0
def start(request):
    global is_start
    is_start = 1
    video_path = '/home/work/file_bak/202401/django-server/mysite/mysite/data/video.mp4'
    cap = cv2.VideoCapture(video_path)
    
    return HttpResponse('ok')

import cv2
import random
import time
from django.http import StreamingHttpResponse

def point_on_img(image_path, points, output_path=None, radius=50):
    # 이미지 읽기
    image = cv2.imread(image_path)
    for point in points:
        x, y = point
        top_left = (x - radius, y - radius)
        bottom_right = (x + radius, y + radius)
        cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 2)
    # output_path가 주어진 경우 이미지 저장
    if output_path:
        cv2.imwrite(output_path, image)
    return image  # 수정된 이미지 객체 반환

def video_stream(request):
    def frame_generator():
        i = 0
        while True:
            i += 1
            image_width = 640
            image_height = 480

            num_points = 5
            points = []

            for _ in range(num_points):
                x = random.randint(0, image_width)
                y = random.randint(0, image_height)
                points.append((x, y))

            # 이미지 경로 설정 시 i를 문자열로 변환
            image_path = "static/image" + str(i) + ".png"
            output_path = f'static/modified_{i}.png'

            # point_on_img 함수로부터 수정된 이미지 받아오기
            frame = point_on_img(image_path=image_path, points=points, output_path=output_path)

            # 받아온 이미지를 JPEG 형식으로 인코딩
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                continue
                
            image = jpeg.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n\r\n')

            time.sleep(1)

    return StreamingHttpResponse(frame_generator(), content_type='multipart/x-mixed-replace; boundary=frame')
