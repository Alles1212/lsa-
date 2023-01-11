import cv2
import cowsay
import mediapipe as mp
import os
import random
import time

# mediapipe tool
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
# drawing line and dot
lineColor = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=5)
dotColor = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=10)

def calculateDis(point1, point2):
    distance = abs(point1 - point2)
    return distance

def rest_for_situp():
    character_name = []
    for name in cowsay.char_names:
        character_name.append(name)

    random.shuffle(character_name)
    time.sleep(6)
    for i in range(17, -1, -1):
        time.sleep(1)
        if i > 10: text = f"倒數{i}秒"
        elif i == 0: text = f"start!!!"
        else: text = f"倒數{i}秒，準備好仰臥起坐姿勢"

        if character_name[i] == "default":
            os.system(f"cowsay '我是{character_name[i]}, {text}'")
        else:
            os.system(f"cowsay --character {character_name[i]} '我是{character_name[i]}, {text}'")


def push_up(push_up_time):
    # 開啟camera
    cap = cv2.VideoCapture(0)
    # count: push up次數, status: 狀態, up或down
    count, status = 0, None
    # for find the max distances of y-axis
    maxDis = 0
    calories = 0
    # 開始抓鏡頭
    while True:
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        # 如果成功抓到鏡頭
        if ret:
            # convert BGR to RGB
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # 抓mediapipe pose的33個pose_landmarks
            result = pose.process(imgRGB)
            landmarks = result.pose_landmarks

            height, width, channel = img.shape # won't use channel, for commemorate
            if landmarks:
                mpDraw.draw_landmarks(img, result.pose_landmarks, mpPose.POSE_CONNECTIONS, dotColor, lineColor)
                pose_landmarks = []
                # find all 33 pose_landmarks
                for lmid, landmark in enumerate(landmarks.landmark):
                    xPos = int(landmark.x * width)
                    yPos = int(landmark.y * height)
                    pose_landmarks.append([lmid, xPos, yPos])

                # too_close = False
                # 當有找到pose_landmarks
                if len(pose_landmarks) != 0:
                    # 用左肩與左肘的y軸距離當作衡量push up的標準
                    # 13 and 11
                    left_shoulder, left_elbow = pose_landmarks[13][2], pose_landmarks[11][2]
                    dis = calculateDis(left_shoulder, left_elbow)
                    # find another to calculate the distance between user and camera!!!
                    # find another to calculate the distance between user and camera!!!
                    # find another to calculate the distance between user and camera!!!
                    # if dis > 200:
                    #     cv2.rectangle(img, (0, 0), (width, height), (0, 0, 0), cv2.FILLED)
                    #     cv2.putText(img, "Too Close!!!", (width//10, height//2), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 2)
                    #     too_close = True
                    # if not too_close:
                    cv2.circle(img, (pose_landmarks[13][1], left_shoulder), 8, (255, 255, 0), cv2.FILLED)
                    cv2.circle(img, (pose_landmarks[11][1], left_elbow), 8, (255, 255, 0), cv2.FILLED)
                    cv2.putText(img, str(dis), (pose_landmarks[11][1], left_elbow), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2)
                    # 找左肩與左肘的最大距離
                    if maxDis < dis:
                        maxDis = dis
                    # 距離小於等於30算下去
                    if dis <= 30:
                        # 狀態設為下去
                        status = "down"
                        cv2.circle(img, (pose_landmarks[11][1], pose_landmarks[11][2]), 15, (0, 255, 255), cv2.FILLED)
                        cv2.circle(img, (pose_landmarks[12][1], pose_landmarks[12][2]), 15, (0, 255, 255), cv2.FILLED)
                        cv2.circle(img, (pose_landmarks[13][1], pose_landmarks[13][2]), 15, (0, 255, 255), cv2.FILLED)
                        cv2.circle(img, (pose_landmarks[14][1], pose_landmarks[14][2]), 15, (0, 255, 255), cv2.FILLED)
                    # 距離做到最大距離了五分之三且狀態是下去
                    elif dis >= maxDis*(3/5) and status=="down":
                        # 狀態改up
                        status = "up"
                        # 算做完完整一下
                        count += 1
                        maxDis = dis
                    calories = count * 0.5
            # 把次數放在左上角
            cv2.putText(img, f"count: {count}", (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,140,255), 1)
            cv2.putText(img, f"consume calories: {calories}", (img.shape[1]//3+10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)


            cv2.imshow("Push up", img)
        if push_up_time == count:
            os.system("gnome-terminal -- 'sl'")
            break

        # 按q結束camera
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    rest_for_situp()


def main():
    push_up(5)


if __name__ == "__main__":
    main()
