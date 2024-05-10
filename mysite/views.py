from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import cv2, random, json, requests, ftplib
from PIL import Image, ImageDraw
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import numpy as np
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse
from common.models import CustomUser

@csrf_exempt
def upload(request):
    if request.method == 'POST':
        file = request.FILES['video']
        with open('/home/work/file_bak/202401/django-server/mysite/mysite/data/video.mp4', 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return HttpResponse('<script>alert("File uploaded successfully"); location.href="/proxy/8000/main/"; </script>')
    return HttpResponse('Only POST requests are allowed')

@login_required(login_url='/login/')
def main_page(request):
    return render(request, 'main_page.html')

is_start = 0
def start(request):
    global is_start
    is_start = 1
    video_path = '/home/work/file_bak/202401/django-server/mysite/mysite/data/video.mp4'
    cap = cv2.VideoCapture(video_path)
    
    return HttpResponse('ok')

def point_on_img(image_path, points, output_path=None, radius=5):
    image = cv2.imread(image_path)

    # 랜덤 점 생성 및 표시
    for point in points:
        x, y = point
        cv2.circle(image, (x, y), radius, (0, 0, 255), -1)
    # 현재 점을 기준으로 x 픽셀 기준으로 
   
    if output_path:
        cv2.imwrite(output_path, image)
    return image

# 특정 영역 내 점이 많은 경우 사각형 그리기
def draw_rectangles(frame, points, area_counts, threshold=5):
    for grid_y in range(len(area_counts)):
        for grid_x in range(len(area_counts[0])):
            
            if area_counts[grid_y][grid_x] >= threshold:
                x1 = grid_x * (frame.shape[1] // len(area_counts[0]))
                y1 = grid_y * (frame.shape[0] // len(area_counts))
                x2 = (grid_x + 1) * (frame.shape[1] // len(area_counts[0]))
                y2 = (grid_y + 1) * (frame.shape[0] // len(area_counts))
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return frame

# 이미지 재생
def video_stream(request):
    def frame_generator():
        i = 0
        while True:
            i += 1
            image_width = 1920
            image_height = 1080

            num_points = np.random.randint(0, 500)  # 생성할 점의 개수
            points = [(np.random.randint(0, image_width), np.random.randint(0, image_height)) for _ in range(num_points)]
            # 그리드 크기 설정
            area_size_x = 10  # 가로 방향으로 나눌 그리드의 수
            area_size_y = 10  # 세로 방향으로 나눌 그리드의 수

            # 그리드 각 셀에 대한 카운트를 저장할 배열 초기화
            area_counts = np.zeros((area_size_y, area_size_x), dtype=int)

            # 각 점이 어느 그리드 셀에 속하는지 확인
            for x, y in points:
                grid_x = min(x // (image_width // area_size_x), area_size_x - 1)
                grid_y = min(y // (image_height // area_size_y), area_size_y - 1)
                area_counts[grid_y, grid_x] += 1

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

            # 특정 영역 내 점이 많은 경우 사각형 그리기
            frame = draw_rectangles(frame, points, area_counts, threshold=5)

            # 받아온 이미지를 JPEG 형식으로 인코딩
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                continue
                
            image = jpeg.tobytes()

            points_data = json.dumps(points)

            # 이미지 데이터와 points 데이터를 함께 전송
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n\r\n')
            
    return StreamingHttpResponse(frame_generator(), content_type='multipart/x-mixed-replace; boundary=frame')

def msg_test(request): 
    session = ftplib.FTP()

    session.connect('125.6.40.93', 21) # 두 번째 인자는 port number
    session.login("zol_zac", "zol_zac")   # FTP 서버에 접속
    
    uploadfile = open('./static/out/1.jpg' ,mode='rb') #업로드할 파일 open
    
    session.encoding='utf-8'
    session.storbinary('STOR ' + '/send.jpg', uploadfile) #파일 업로드
    
    uploadfile.close() # 파일 닫기
    
    session.quit() # 서버 나가기
    # 데이터베이스 조회 로직 (예시)
    # message = 조회 로직...
    
    all_phone_numbers = list(CustomUser.objects.values_list('phone_number', flat=True))
    print(all_phone_numbers)
    # API 엔드포인트 설정
    url = "https://alimtalk-api.bizmsg.kr/v2/sender/send"

    # 요청 헤더 설정
    headers = {
        "userid": "ibeobom",
        "Content-type": "application/json",
    }

    # 메시지 데이터 설정
    data2 = {
        
        "message_type": "AT", 
        "phn": "821012345678",
        "profile": "dc468edce77a32d860ae5ddad48a535aef6be9b3",
        "msg": "여기에 메시지 내용을 입력하세요.",
        # 필요한 나머지 필드들도 추가
    }
    data = [{
            "message_type": "ai",
            "phn": "821076466676",
            "profile": "dc468edce77a32d860ae5ddad48a535aef6be9b3",
            "tmplId": "alimtalktest_001",
            "msg": "hihihihihih",
            "smsKind": "M",
            "msgSms": "hi",
            "smsSender": "01026495219", "smsLmsTit": "[카카오뮤직] 회원가입 안내", "reserveDt": "00000000000000",
            "img_url" : "http://zol_jac.theseung.com/send.jpg"

    }]
    # JSON 형식으로 데이터 변환
    json_data = json.dumps(data)

    try:
        response = requests.post(url, headers=headers, data=json_data)
        print(response.content)
        if response.status_code == 200:
            print("succ")
            # 성공적으로 메시지를 보냈다면,
            return JsonResponse({'message': 'Message sent successfully'}, status=200)
        else:
            print("failed")
            # API 호출 실패
            return JsonResponse({'error': 'Failed to send message'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
        