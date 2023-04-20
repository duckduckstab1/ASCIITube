import cv2

from PIL import Image, ImageOps

video = cv2.VideoCapture('video.mp4')

while True:

    ret, frame = video.read()

    if not ret:

        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    size = (80, 60)

    small_gray = cv2.resize(gray, size)

    inverted = cv2.bitwise_not(small_gray)

    image = Image.fromarray(inverted)

    ascii_image = ImageOps.invert(image.convert('L')).convert('1')

    print(ascii_image)

video.release()

