# mysite/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import numpy as np
import random
import json
import cv2
import base64, asyncio
import numpy as np

pixel_per_meter = 120


# 이미지에 점을 그리는 함수
def point_on_img(image_path, points, output_path=None, radius=5):
    image = cv2.imread(image_path)
    for point in points:
        x, y = point
        cv2.circle(image, (x, y), radius, (0, 0, 255), -1)
    if output_path:
        cv2.imwrite(output_path, image)
    return image

# 특정 영역 내 점이 많은 경우 사각형을 그리는 함수
def draw_rectangles(frame, error_pos):

    for pos in error_pos:
            x = pos[0][0]
            y = pos[0][1]
            human = pos[1]

            start_x = max(x - pixel_per_meter // 2, 0)
            end_x = min(x + pixel_per_meter // 2, 1920)
            start_y = max(y - pixel_per_meter // 2, 0)
            end_y = min(y + pixel_per_meter // 2, 1080)
            cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (0, 255, 255), 2)

    return frame

class VideoStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        # 연결이 끊어졌을 때의 처리
        pass

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['type']
        
        if message_type == 'start_stream':
            await self.start_stream()

    async def start_stream(self):
        i = 0
        while i < 1:
            i += 1
            image_width = 1920
            image_height = 1080
            
            num_points = np.random.randint(0, 500)  # 생성할 점의 개수
            points = [(np.random.randint(0, image_width), np.random.randint(0, image_height)) for _ in range(num_points)]
            # 그리드 크기 설정
            area_size_x = image_width // pixel_per_meter  # 가로 방향으로 나눌 그리드의 수
            area_size_y = image_height // pixel_per_meter  # 세로 방향으로 나눌 그리드의 수

            # 그리드 각 셀에 대한 카운트를 저장할 배열 초기화
            area_counts = np.zeros((area_size_y, area_size_x), dtype=int)

            # 각 점이 어느 그리드 셀에 속하는지 확인
            for x in range(area_size_x):
                for y in range(area_size_y):
                    start_x = x * pixel_per_meter
                    end_x = x * pixel_per_meter + (pixel_per_meter - 1)
                    start_y = y * pixel_per_meter
                    end_y = y * pixel_per_meter + (pixel_per_meter - 1)
                    area_counts[y][x] = sum(1 for point in points if point[0] >= start_x and point[0] <= end_x and point[1] >= start_y and point[1] <= end_y)

            # 이미지 경로 설정 시 i를 문자열로 변환
            image_path = "static/img_results/" + str(i) + ".jpg"
            output_path = f'static/out/{i}.jpg'
            error_pos = []

            max_cnt = 0
            for base_point in points:
                count = sum(1 for point in points if base_point[0] - pixel_per_meter // 2 <= point[0] <= base_point[0] + pixel_per_meter // 2 and base_point[1] - pixel_per_meter // 2 <= point[1] <= base_point[1] + pixel_per_meter // 2)
                if count >= 6:
                    error_pos.append([base_point, count])

                if max_cnt < count:
                    max_cnt = count
            
            # point_on_img 함수로부터 수정된 이미지 받아오기
            frame = point_on_img(image_path=image_path, points=points)
            
            if frame is None or not frame.any():
                break

            # 특정 영역 내 점이 많은 경우 사각형 그리기
            frame = draw_rectangles(frame, error_pos)
            cv2.imwrite(output_path, frame)

            # 받아온 이미지를 JPEG 형식으로 인코딩
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            
            image = jpeg.tobytes()
            base64_image = base64.b64encode(image).decode('utf-8')
         
            area_counts_list = area_counts.tolist()
            # 변환된 이미지 데이터를 웹소켓을 통해 전송
            await self.send(text_data=json.dumps({
                'type': 'frame',
                'image_data': base64_image,
                'points' : points,
                'area_counts' : area_counts_list
            }))
            await asyncio.sleep(0.1)  # 잠시 대기하여 이미지를 조금씩 전송
