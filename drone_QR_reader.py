import cv2
import json

testVideo = True

if not testVideo:
    cap = cv2.VideoCapture(2)
else:
    cap = cv2.VideoCapture('flight.mp4')
    
detector = cv2.QRCodeDetector()

width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

frameCount = 0
foundCode = False
text = ""
color = (0,0,0)
if not testVideo:
    writer = cv2.VideoWriter('flight.mp4', cv2.VideoWriter_fourcc(*'XVID'),20,(width, height))
while True:
    _, frame = cap.read()
    
    if testVideo and frame is None:
        break
        
    data, _, _ = detector.detectAndDecode(frame)
    
    if data:
        try:
            jsonObject = json.loads(data)
            text = jsonObject['text']
            color = jsonObject['color']
            foundCode = True
            frameCount = 20
        except:
            print('data error')
        
    if data or foundCode:
        cv2.putText(frame, text, (10,120), cv2.FONT_HERSHEY_SIMPLEX,1.5, color, 5)
        frameCount -= 1
        if(frameCount == 0):
            foundCode = False

    if not testVideo:
        writer.write(frame)
    
    cv2.imshow('camera', frame)

    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

cap.release()
if not testVideo:
    writer.release()
cv2.destroyAllWindows()
