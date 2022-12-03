from django.shortcuts import render
from django.http import HttpResponse
import cv2
from django.views.decorators.csrf import csrf_exempt

def main_html(request):
    return render(request, "main.html")
    # return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def open_camera(request):
    import cv2

    cam = cv2.VideoCapture(0)

    cv2.namedWindow("test")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            value = scan_qrcode("opencv_frame_0.png")
            print("value", value)
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1

    cam.release()
    
    cv2.destroyAllWindows()

@csrf_exempt
def scan_qrcode(filename):
    print("A")
    try:
        img = cv2.imread(filename)
        detect = cv2.QRCodeDetector()
        value, points, straight_qrcode = detect.detectAndDecode(img)
        print("B")
        return value
    except:
        print("C")
        return

# open_camera()
