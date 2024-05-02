from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
from PIL import Image, ImageDraw
from django.http import JsonResponse
import time
import random

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
# views.py 파일 내부에 있는 코드 예제

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import numpy as np

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

def point_on_img(image_path, points, output_path=None, radius=5):
    image = cv2.imread(image_path)

    # 랜덤 점 생성 및 표시
    for point in points:
        x, y = point
        cv2.circle(image, (x, y), radius, (0, 0, 255), -1)

   
    if output_path:
        cv2.imwrite(output_path, image)
    return image

# 특정 영역 내 점 개수 세기
def count_points_in_grid(frame, points, grid_size=100):
    # NumPy 출력 옵션 변경
    np.set_printoptions(threshold=np.inf)
    grid_counts = np.zeros((grid_size-1, grid_size-1), dtype=int)
    for x, y in points:
        grid_x = min(int(x // (frame.shape[1] / grid_size)), grid_size-2)
        grid_y = min(int(y // (frame.shape[0] / grid_size)), grid_size-2)
        grid_counts[grid_y, grid_x] += 1

    #print(f"{grid_counts}\n")
    return grid_counts



# 특정 영역 내 점이 많은 경우 사각형 그리기
def draw_rectangles(image, points, grid_counts, threshold=2):
    height, width, _ = image.shape
    grid_size = 100

    for point in points:
        x, y = point
        grid_x = x // grid_size
        grid_y = y // grid_size

        if grid_counts[grid_y, grid_x] >= threshold:
            print(f"{grid_x, grid_y} 위험")
            top_left = (grid_x * grid_size, grid_y * grid_size)
            bottom_right = ((grid_x + 1) * grid_size, (grid_y + 1) * grid_size)
            cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 2)

    return image


# 이미지 재생
def video_stream(request):
    def frame_generator():
        i = 0
        while i < 5:
            i += 1
            image_width = 1920
            image_height = 1080

            num_points = np.random.randint(0, 500)  # 생성할 점의 개수
            points = [(np.random.randint(0, image_width), np.random.randint(0, image_height)) for _ in range(num_points)]
            # 그리드 크기 설정
            grid_size_x = 10  # 가로 방향으로 나눌 그리드의 수
            grid_size_y = 10  # 세로 방향으로 나눌 그리드의 수

            # 그리드 각 셀에 대한 카운트를 저장할 배열 초기화
            grid_counts = np.zeros((grid_size_y, grid_size_x), dtype=int)

            # 각 점이 어느 그리드 셀에 속하는지 확인
            for x, y in points:
                grid_x = min(x // (image_width // grid_size_x), grid_size_x - 1)
                grid_y = min(y // (image_height // grid_size_y), grid_size_y - 1)
                grid_counts[grid_y, grid_x] += 1

            # 그리드 카운트 출력
            print(grid_counts)
            print()

            for _ in range(num_points):
                x = random.randint(0, image_width)
                y = random.randint(0, image_height)
                points.append((x, y))

            # 이미지 경로 설정 시 i를 문자열로 변환
            image_path = "static/img_results/" + str(i) + ".jpg"
            output_path = f'static/{i}.jpg'

            # point_on_img 함수로부터 수정된 이미지 받아오기
            frame = point_on_img(image_path=image_path, points=points)
            if frame is None or not frame.any():
                break


            # 특정 영역 내 점 개수 세기
            grid_counts = count_points_in_grid(frame, points, grid_size=100)

            # 특정 영역 내 점이 많은 경우 사각형 그리기
            frame = draw_rectangles(frame, points, grid_counts, threshold=2)

            # 받아온 이미지를 JPEG 형식으로 인코딩
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                continue
                
            image = jpeg.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n\r\n')
            
       


    return StreamingHttpResponse(frame_generator(), content_type='multipart/x-mixed-replace; boundary=frame')


