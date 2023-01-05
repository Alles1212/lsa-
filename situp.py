import cv2
from PoseModule import PoseModule

cap = cv2.VideoCapture('situp3.mov')#沒有要用影片要實際用的話，'situp3.mov'改0
count, status = 0, None
# for find the max distances of y-axis
maxDis = 0
poseDetector = PoseModule()
while True:
    ret, img = cap.read()
    if ret:
        try:
            # img = cv2.resize(img, (img.shape[1], img.shape[0]))
            poseDetector.findPose(img)
            lmList = poseDetector.findPosition(img)
        except:
            pass

        if len(lmList) != 0:
            dis = poseDetector.calculateX_axisDis(img, 11, 25)
            # dis = poseDetector.calculateX_axisDis(img, 25, 11)
            if maxDis < dis:
                maxDis = dis
            if dis >= maxDis*(4/5):
                status = "down"
            elif dis <= maxDis*(1/2) and status=="down":
                status = "up"
                count += 1

        cv2.putText(img, f"count: {count}", (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)

        cv2.imshow("Sit up", img)


    if cv2.waitKey(1) == ord('q'):
        break
