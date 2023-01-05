import cv2
import mediapipe as mp
import numpy as np


class PoseModule:
    # initialize
    def __init__(self, minDection=0.7, minTracking=0.7):
        self.mpPose = mp.solutions.pose # the pose module
        self.pose = self.mpPose.Pose(min_detection_confidence=minDection, min_tracking_confidence=minTracking) # set default min_detection_confidence, min_tracking_confidence=0.7
        self.mpDraw = mp.solutions.drawing_utils # drawing utils
        self.poseLmsStyle = self.mpDraw.DrawingSpec(color=(0, 0, 255), thickness=5) # color of pose landmark
        self.poseConStyle = self.mpDraw.DrawingSpec(color=(0, 255, 0), thickness=5) # connetions of pose landmark

    # find the pose landmarks
    def findPose(self, img, draw=True):
        # cv2 support BGR color, so convert BGR color to RGB for mediapipe
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # find out the pose landmarks
        self.result = self.pose.process(imgRGB)
        # if find out pose landmarks
        if self.result.pose_landmarks:
            if draw:
                # drawing the landmarks and for each landmark connect other landmark which near it
                self.mpDraw.draw_landmarks(img, self.result.pose_landmarks, self.mpPose.POSE_CONNECTIONS, self.poseLmsStyle, self.poseConStyle)


    # find coordinae of landmarks
    def findPosition(self, img, draw=True):
        self.lmList = []
        # lmList[1] represent landmark no.1, lmList[1][1] is x value of landmark no.1, lmList[1][2] is y value of landmark no.1
        height, width, _ = img.shape
        # if find out pose landmarks
        if self.result.pose_landmarks:
            # get the id and landmark (xPos, yPos)
            for id, landmark in enumerate(self.result.pose_landmarks.landmark):
                # calculate xPos and yPos
                xPos, yPos = int(landmark.x * width), int(landmark.y * height)
                # add [id, xPos, yPos] to lmList
                self.lmList.append([id, xPos, yPos])
        # if wanna draw
        if draw:
            self.mpDraw.draw_landmarks(img, self.result.pose_landmarks, self.mpPose.POSE_CONNECTIONS, self.poseLmsStyle, self.poseConStyle)
        # return lmList
        return self.lmList

    # calculate the angle between line_firstAndMid and line_midAndLast
    # first: the first landmark of the pose
    # mid: the middle landmark of the pose
    # last: the last landmark of the pose
    def calculateAngle(self, img, first, mid, last, draw=True):
        xFirst, yFirst = self.lmList[first][1], self.lmList[first][2]
        xMid, yMid = self.lmList[mid][1], self.lmList[mid][2]
        xLast, yLast = self.lmList[last][1], self.lmList[last][2]
        radians = np.arctan2(yLast-yMid, xLast-xMid) - np.arctan2(yFirst-yMid, xFirst-xMid)
        angle = np.abs(radians*180.0/np.pi)
        if angle > 180:
            angle = 360-angle

        # if wanna draw
        if draw:
            cv2.putText(img, str(angle), (xMid-20, yMid+20), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
        # return the angle
        return angle


    # point1 and point2 is landmarks of the pose
    def calculateY_axisDis(self, img, point1, point2, draw=False):
        # get y value of lmList for point1 and point2
        p1Y = self.lmList[point1][2]
        p2Y = self.lmList[point2][2]
        # calculate the distance
        distance = abs(p1Y - p2Y)
        # if wanna draw
        if draw:
            cv2.circle(img, (self.lmList[point1][1], p1Y), 8, (255,255,0), cv2.FILLED)
            cv2.circle(img, (self.lmList[point2][1], p2Y), 8, (255,255,0), cv2.FILLED)
            cv2.putText(img, str(int(distance)), (self.lmList[point1][1], p1Y-30), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,0), 2)
        # return the distance
        return distance


    # point1 and point2 is landmarks of the pose
    def calculateX_axisDis(self, img, point1, point2, draw=True):
        # get x value of lmList for point1 and point2
        p1X = self.lmList[point1][1]
        p2X = self.lmList[point2][1]
        # calculate the distance
        distance = abs(p1X - p2X)
        # if wanna draw
        if draw:
            cv2.circle(img, (p1X, self.lmList[point1][2]), 8, (255,255,0), cv2.FILLED)
            cv2.circle(img, (p2X, self.lmList[point2][2]), 8, (255,255,0), cv2.FILLED)
            cv2.putText(img, str(int(distance)), (p1X, self.lmList[point1][2]), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,0), 2)
        # return the distance
        return distance


def main():
    cap = cv2.VideoCapture(0)
    cTime = 0
    pTime = 0
    count, status = 0, None
    # for find the max distances of y-axis
    maxDis = 0
    poseDetector = PoseModule()
    while True:
        ret, img = cap.read()
        if ret:
            try:
                img = cv2.resize(img, (img.shape[1], img.shape[0]))
                poseDetector.findPose(img)
                lmList = poseDetector.findPosition(img)
            except:
                pass

                # angle = poseDetector.calculateAngle(img, 11, 23, 25)
                # # angle = poseDetector.calculateAngle(img, 12, 14, 16)
                # if angle > 110:
                #     status = "down"
                # elif angle < 45 and status=="down":
                #     status = "up"
                #     count += 1

                # dis = poseDetector.calculateX_axisDis(img, 11, 25)
                # # dis = poseDetector.calculateX_axisDis(img, 25, 11)
                # if maxDis < dis:
                #     maxDis = dis
                # if dis >= maxDis*(4/5):
                #     status = "down"
                # elif dis <= maxDis*(1/2) and status=="down":
                #     status = "up"
                #     count += 1

            if len(lmList) != 0:
                dis = poseDetector.calculateY_axisDis(img, 13, 11)
                if maxDis < dis:
                    maxDis = dis
                if dis <= 10:
                    status = "down"
                elif dis >= maxDis*(4/5) and status=="down":
                    status = "up"
                    count += 1
            cv2.putText(img, f"count: {count}", (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)

            cv2.imshow("img", img)


        if cv2.waitKey(1) == ord('q'):
            break

if __name__ == "__main__":
    main()
