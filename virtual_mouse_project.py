{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "d521419f-e594-4cec-931c-fd5bf39526a2",
   "metadata": {},
   "outputs": [],
   "source": [
    "import cv2\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "e620e1c8-c6c4-4c96-9e85-39cdd1a6908a",
   "metadata": {},
   "outputs": [
    {
     "ename": "ModuleNotFoundError",
     "evalue": "No module named 'angle'",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
      "Cell \u001b[1;32mIn[8], line 4\u001b[0m\n\u001b[0;32m      2\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m \u001b[38;5;21;01mpyautogui\u001b[39;00m\n\u001b[0;32m      3\u001b[0m pyautogui\u001b[38;5;241m.\u001b[39mFAILSAFE \u001b[38;5;241m=\u001b[39m \u001b[38;5;28;01mFalse\u001b[39;00m\n\u001b[1;32m----> 4\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m \u001b[38;5;21;01mangle\u001b[39;00m\n\u001b[0;32m      5\u001b[0m \u001b[38;5;28;01mfrom\u001b[39;00m \u001b[38;5;21;01mpynput\u001b[39;00m\u001b[38;5;21;01m.\u001b[39;00m\u001b[38;5;21;01mmouse\u001b[39;00m \u001b[38;5;28;01mimport\u001b[39;00m Button, Controller\n\u001b[0;32m      6\u001b[0m mouse \u001b[38;5;241m=\u001b[39m Controller()\n",
      "\u001b[1;31mModuleNotFoundError\u001b[0m: No module named 'angle'"
     ]
    }
   ],
   "source": [
    "import mediapipe as mp\n",
    "import pyautogui\n",
    "pyautogui.FAILSAFE = False\n",
    "import angle\n",
    "from pynput.mouse import Button, Controller\n",
    "mouse = Controller()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "78b3a19a-f563-4e69-83e0-c18b33877882",
   "metadata": {},
   "outputs": [],
   "source": [
    "screen_width, screen_height = pyautogui.size()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "99c14dae-4ebe-4fc7-9887-5fe43dd9fb0e",
   "metadata": {},
   "outputs": [],
   "source": [
    "mouse = Controller()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "43c54918-c9a4-4120-9f80-c61527b5dcf9",
   "metadata": {},
   "outputs": [],
   "source": [
    "mpHands=mp.solutions.hands\n",
    "hands=mpHands.Hands(\n",
    "    static_image_mode=False,\n",
    "    model_complexity=1,\n",
    "    min_detection_confidence=0.7,\n",
    "    min_tracking_confidence=0.7,\n",
    "    max_num_hands=1\n",
    ")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "9e9225c9-968f-4bd3-b81e-303ebcec844d",
   "metadata": {},
   "outputs": [],
   "source": [
    "def find_finger_tip(processed):\n",
    "    if processed.multi_hand_landmarks:\n",
    "        hand_landmarks= processed.multi_hand_landmarks[0]\n",
    "        return hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]\n",
    "\n",
    "    return None"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "a53513cc-79db-43d2-a18a-85d014b13d4f",
   "metadata": {},
   "outputs": [],
   "source": [
    "def move_mouse(index_finger_tip):\n",
    "    if index_finger_tip is not None:\n",
    "        x = int(index_finger_tip.x * screen_width)\n",
    "        y = int(index_finger_tip.y * screen_height)\n",
    "\n",
    "        # Ensure the coordinates are within bounds\n",
    "        x = max(1, min(x, screen_width - 1))\n",
    "        y = max(1, min(y, screen_height - 1))\n",
    "        \n",
    "        # print(f\"Moving mouse to: x={x}, y={y}\")  # Debug print statement\n",
    "        pyautogui.moveTo(x, y)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "942ded32-ea77-44f1-871d-b30a272b22ac",
   "metadata": {},
   "outputs": [],
   "source": [
    "def is_left_click(landmarks_list,thumb_index_dist):\n",
    "    return (util.get_angle(landmarks_list[5],landmarks_list[6],landmarks_list[8])<50 and\n",
    "           util.get_angle(landmarks_list[9],landmarks_list[10],landmarks_list[12])>80 and\n",
    "           thumb_index_dist>50)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "da4c15eb-cb7a-4008-a948-6461b5cee479",
   "metadata": {},
   "outputs": [],
   "source": [
    "def is_right_click(landmarks_list,thumb_index_dist):\n",
    "    return((util.get_angle(landmarks_list[9],landmarks_list[10],landmarks_list[12])<50 and\n",
    "           util.get_angle(landmarks_list[5],landmarks_list[6],landmarks_list[8])>80 and\n",
    "           thumb_index_dist>50))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3f4e4be5-da37-4060-b5db-4088499b6506",
   "metadata": {},
   "outputs": [],
   "source": [
    "def is_double_click(landmarks_list,thumb_index_dist):\n",
    "    return((util.get_angle(landmarks_list[5],landmarks_list[6],landmarks_list[8])<50 and\n",
    "           util.get_angle(landmarks_list[9],landmarks_list[10],landmarks_list[12])<50 and\n",
    "           thumb_index_dist>50))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e6ef3b66-93c5-403e-9105-f3af8b253983",
   "metadata": {},
   "outputs": [],
   "source": [
    "def is_screenshot(landmarks_list,thumb_index_dist):\n",
    "    return(util.get_angle(landmarks_list[5],landmarks_list[6],landmarks_list[8])<50 and\n",
    "           util.get_angle(landmarks_list[9],landmarks_list[10],landmarks_list[12])<50 and\n",
    "           thumb_index_dist<50)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "a26b550f-d5b5-4263-b4de-c223ff98a345",
   "metadata": {},
   "outputs": [],
   "source": [
    "def detect_gustures(frame,landmarks_list,processed):\n",
    "    if len(landmarks_list)>=21:\n",
    "\n",
    "        index_finger_tip=find_finger_tip(processed)\n",
    "        #print(index_finger_tip)\n",
    "        thumb_index_dist= util.get_distance([landmarks_list[4],landmarks_list[5]])\n",
    "\n",
    "        if thumb_index_dist is not None and thumb_index_dist < 100:\n",
    "            angle=util.get_angle(landmarks_list[5],landmarks_list[6],landmarks_list[8])\n",
    "            if angle>60:\n",
    "                move_mouse(index_finger_tip)\n",
    "            #move_mouse(index_finger_tip)\n",
    "        #lift click\n",
    "        elif is_left_click(landmarks_list,thumb_index_dist):\n",
    "            mouse.press(Button.left)\n",
    "            mouse.release(Button.left)\n",
    "            cv2.putText(frame, \"Left Click\",(50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2)\n",
    "\n",
    "\n",
    "        #right click\n",
    "        elif is_right_click(landmarks_list,thumb_index_dist):\n",
    "            mouse.press(Button.right)\n",
    "            mouse.release(Button.right)\n",
    "            cv2.putText(frame, \"Right Click\",(50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2)\n",
    "\n",
    "\n",
    "        #double click\n",
    "        elif is_double_click(landmarks_list,thumb_index_dist):\n",
    "            pyautogui.doubleClick()\n",
    "            cv2.putText(frame, \"Double Click\",(50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2)\n",
    "\n",
    "\n",
    "        #screenshot\n",
    "        elif is_screenshot(landmarks_list,thumb_index_dist):\n",
    "            im1=pyautogui.screenshot()\n",
    "            label = random.randint(1,1000)\n",
    "            im1.save(f'my_screenshot_{label}.png')\n",
    "            cv2.putText(frame, \"Screenshot Taken\",(50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c8a217f1-8dc0-475d-bd51-01ce2b55d080",
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "def main():\n",
    "    cap =cv2.VideoCapture(0)\n",
    "    draw= mp.solutions.drawing_utils\n",
    "    try:\n",
    "        while cap.isOpened():\n",
    "            ret,frame =cap.read()\n",
    "\n",
    "            if not ret:\n",
    "                break\n",
    "            frame=cv2.flip(frame,1)\n",
    "            frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)\n",
    "            processed=hands.process(frameRGB)\n",
    "\n",
    "            landmarks_list=[]\n",
    "\n",
    "            if processed.multi_hand_landmarks:\n",
    "                hand_landmarks=processed.multi_hand_landmarks[0]\n",
    "                draw.draw_landmarks(frame,hand_landmarks, mpHands.HAND_CONNECTIONS)\n",
    "                \n",
    "                for lm in hand_landmarks.landmark:\n",
    "                    cx, cy = int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])\n",
    "                    cv2.circle(frame, (cx, cy), 5, (255, 0, 0), cv2.FILLED) \n",
    "                    landmarks_list.append((lm.x, lm.y))\n",
    "\n",
    "                #print(landmarks_list)\n",
    "            detect_gustures(frame,landmarks_list,processed)\n",
    "            \n",
    "\n",
    "            cv2.imshow('Frame',frame)\n",
    "            if cv2.waitKey(1) & 0xFF == ord('q'):\n",
    "                break\n",
    "\n",
    "    finally:\n",
    "        cap.release()\n",
    "        cv2.destroyAllWindows()\n",
    "\n",
    "if __name__ == '__main__':\n",
    "    main()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
