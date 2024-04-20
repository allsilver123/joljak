from PIL import Image, ImageDraw

def point_on_img(image_path, points, output_path, radius=100):

    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    for point in points:
        x, y = point
        left_up = (x - radius, y - radius)
        right_down = (x + radius, y + radius)
        draw.ellipse([left_up, right_down], fill='red')
    
    image.save(output_path)

image_paths = [
    '../static/image1.png', 
    '../static/image2.png', 
    '../static/image3.png'
]

points = [(100,100), (150, 200), (200,250)]

for i, image_path in enumerate(image_paths):
    output_path = f'modified_{i}.png'
    point_on_img(image_path, [points[i]], output_path)