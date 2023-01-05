import cv2
from PoseModule import PoseModule
import os
import cowsay #可在Linux下執行，會有驚喜(記得先sudo pip install cowsay)
import random


def surprise(message="恭喜做完"):
    rand = random.randint(0, 18)
    if rand == 18:
        os.system("gnome-terminal -- 'sl'")
        return
    char = cowsay.char_names[rand]
    if char == "default":
        os.system(f"cowsay {message}")
        return
    os.system(f"cowsay --character {char} {message}")

def push_up(push_up_time):
    # 開啟camera
    cap = cv2.VideoCapture(0)
    # count: push up次數, status: 狀態, up或down
    count, status = 0, None
    # for find the max distances of y-axis
    maxDis = 0
    calories = 0
    # 使用PoseModule初始化mediapipe solutions, pose or drawing_utils...
    poseDetector = PoseModule()
    # 開始抓鏡頭
    while True:
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        # 如果成功抓到鏡頭
        if ret:
            try:
                # 抓mediapipe pose的33個landmarks
                poseDetector.findPose(img)
                # 抓landmarks的座標位置
                lmList = poseDetector.findPosition(img)
            except:
                pass

            # 當有找到landmarks
            if len(lmList) != 0:
                # 用左肩與左肘的y軸距離當作衡量push up的標準
                dis = poseDetector.calculateY_axisDis(img, 13, 11)
                # 找左肩與左肘的最大距離
                if maxDis < dis:
                    maxDis = dis
                if maxDis >= 200:
                    maxDis = 180
                # 距離小於等於15算下去
                if dis <= 30:
                    # 狀態設為下去
                    status = "down"
                    cv2.circle(img, (lmList[11][1], lmList[11][2]), 15, (0, 255, 255), cv2.FILLED)
                    cv2.circle(img, (lmList[12][1], lmList[12][2]), 15, (0, 255, 255), cv2.FILLED)
                    cv2.circle(img, (lmList[13][1], lmList[13][2]), 15, (0, 255, 255), cv2.FILLED)
                    cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 255, 255), cv2.FILLED)
                # 距離做到最大距離了五分之三且狀態是下去
                elif dis >= maxDis*(3/5) and status=="down":
                    # 狀態改up
                    status = "up"
                    # 算做完完整一下
                    count += 1
                    maxDis = 0
                calories = count * 0.5
            # 把次數放在左上角
            cv2.putText(img, f"count: {count}", (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,140,255), 1)
            cv2.putText(img, f"consume calories: {calories}", (img.shape[1]//3+10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)


            cv2.imshow("Push up", img)
        if int(push_up_time) == count:
            surprise()
            break

        # 按q結束camera
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    push_up(0)


if __name__ == "__main__":
    main()
