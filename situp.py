import cv2
import mediapipe as mp
import numpy as np
import os

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
# drawing line and dot
lineColor = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=8)
dotColor = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=10)

def done(message="辛苦了，恭喜做完"):
    os.system(f"cowsay --character dragon {message}")

# point2 is mid point
def calculateAngle(pose_landmarks, point1, point2, point3):
    p1X, p1Y = pose_landmarks[point1][1], pose_landmarks[point1][2]
    p2X, p2Y = pose_landmarks[point2][1], pose_landmarks[point2][2]
    p3X, p3Y = pose_landmarks[point3][1], pose_landmarks[point3][2]
    radians = np.arctan2(p3Y-p2Y, p3X-p2X) - np.arctan2(p1Y-p2Y, p1X-p2X)
    angle = np.abs(radians*180/np.pi)
    if angle > 180:
        angle = 360-angle
    return angle

def calculateDis(point1, point2):
    return abs(point1 - point2)

def sit_up(sit_up_time):
    # 開啟camera
    cap = cv2.VideoCapture(0)
    # count: push up次數, status: 狀態, up或down
    count, status = 0, None
    # for find the max distances of x-axis
    maxDis = 0
    calories = 0
    # 開始抓鏡頭
    while True:
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        # 如果成功抓到鏡頭
        if ret:
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # 抓mediapipe pose的33個landmarks
            result = pose.process(imgRGB)
            landmarks = result.pose_landmarks
            height, width, channel = img.shape
            # find some landmarks
            if landmarks:
                mpDraw.draw_landmarks(img, landmarks, mpPose.POSE_CONNECTIONS, dotColor, lineColor)
                pose_landmarks = []
                # find all 33 pose_landmarks
                for lmid, landmark in enumerate(landmarks.landmark):
                    xPos, yPos = int(landmark.x * width), int(landmark.y * height)
                    pose_landmarks.append([lmid, xPos, yPos])

            # 如果有抓到landmarks座標
            if len(pose_landmarks) != 0:
                # 以左肩與左膝的x軸距離當作衡量仰臥起坐標準
                dis = calculateDis(pose_landmarks[11][1], pose_landmarks[25][1])
                left_angle = calculateAngle(pose_landmarks, 11, 23, 25)
                right_angle = calculateAngle(pose_landmarks, 12, 24, 26)
                knee_angle = calculateAngle(pose_landmarks, 23, 25, 27)
                if knee_angle < 100:
                    # 找出左肩與左膝的x軸最大距離
                    if maxDis < dis:
                        maxDis = dis
                    # 距離大於最大距離的五分之四
                    if dis >= maxDis*(4/5) and left_angle >= 130:
                        # 狀態設為下去
                        status = "down"
                    # 距離小於或等於最大距離的一半
                    elif dis <= maxDis*(2/5) and status=="down" and left_angle <= 60:
                        # 狀態改為up
                        status = "up"
                        # 算做完完整一下
                        count += 1
                        calories += 0.3
                    # 距離大於最大距離的五分之四
                    if dis >= maxDis*(4/5) and right_angle >= 130:
                        # 狀態設為下去
                        status = "down"
                    # 距離小於或等於最大距離的一半
                    elif dis <= maxDis*(2/5) and status=="down" and right_angle <= 60:
                        # 狀態改為up
                        status = "up"
                        # 算做完完整一下
                        count += 1
                        calories += 0.3

            # 把次數放在左上角
            # cv2.putText(img, f"count: {count}", (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)
            cv2.putText(img, f"count: {count}", (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,140,255), 1)
            cv2.putText(img, f"consume calories: {calories}", (img.shape[1]//3+10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)

            cv2.imshow("Sit up", img)

        if count == sit_up_time:
            done()
            break

        # 按q結束camera
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    sit_up(1)

if __name__ == "__main__":
    main()