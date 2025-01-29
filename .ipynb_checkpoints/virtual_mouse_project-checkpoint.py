{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "d521419f-e594-4cec-931c-fd5bf39526a2",
   "metadata": {},
   "outputs": [],
   "source": [
    "import cv2\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "e620e1c8-c6c4-4c96-9e85-39cdd1a6908a",
   "metadata": {},
   "outputs": [],
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
   "execution_count": 4,
   "id": "78b3a19a-f563-4e69-83e0-c18b33877882",
   "metadata": {},
   "outputs": [],
   "source": [
    "screen_width, screen_height = pyautogui.size()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "99c14dae-4ebe-4fc7-9887-5fe43dd9fb0e",
   "metadata": {},
   "outputs": [],
   "source": [
    "mouse = Controller()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
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
   "execution_count": 7,
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
   "execution_count": 8,
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
   "execution_count": 9,
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
   "execution_count": 10,
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
   "execution_count": 11,
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
   "execution_count": 12,
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
   "execution_count": 13,
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
   "execution_count": 14,
   "id": "c8a217f1-8dc0-475d-bd51-01ce2b55d080",
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\pradu\\AppData\\Roaming\\Python\\Python312\\site-packages\\google\\protobuf\\symbol_database.py:55: UserWarning: SymbolDatabase.GetPrototype() is deprecated. Please use message_factory.GetMessageClass() instead. SymbolDatabase.GetPrototype() will be removed soon.\n",
      "  warnings.warn('SymbolDatabase.GetPrototype() is deprecated. Please '\n"
     ]
    },
    {
     "ename": "KeyboardInterrupt",
     "evalue": "",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mKeyboardInterrupt\u001b[0m                         Traceback (most recent call last)",
      "Cell \u001b[1;32mIn[14], line 38\u001b[0m\n\u001b[0;32m     35\u001b[0m         cv2\u001b[38;5;241m.\u001b[39mdestroyAllWindows()\n\u001b[0;32m     37\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;18m__name__\u001b[39m \u001b[38;5;241m==\u001b[39m \u001b[38;5;124m'\u001b[39m\u001b[38;5;124m__main__\u001b[39m\u001b[38;5;124m'\u001b[39m:\n\u001b[1;32m---> 38\u001b[0m     main()\n",
      "Cell \u001b[1;32mIn[14], line 12\u001b[0m, in \u001b[0;36mmain\u001b[1;34m()\u001b[0m\n\u001b[0;32m     10\u001b[0m frame\u001b[38;5;241m=\u001b[39mcv2\u001b[38;5;241m.\u001b[39mflip(frame,\u001b[38;5;241m1\u001b[39m)\n\u001b[0;32m     11\u001b[0m frameRGB\u001b[38;5;241m=\u001b[39mcv2\u001b[38;5;241m.\u001b[39mcvtColor(frame,cv2\u001b[38;5;241m.\u001b[39mCOLOR_BGR2RGB)\n\u001b[1;32m---> 12\u001b[0m processed\u001b[38;5;241m=\u001b[39mhands\u001b[38;5;241m.\u001b[39mprocess(frameRGB)\n\u001b[0;32m     14\u001b[0m landmarks_list\u001b[38;5;241m=\u001b[39m[]\n\u001b[0;32m     16\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m processed\u001b[38;5;241m.\u001b[39mmulti_hand_landmarks:\n",
      "File \u001b[1;32m~\\AppData\\Roaming\\Python\\Python312\\site-packages\\mediapipe\\python\\solutions\\hands.py:153\u001b[0m, in \u001b[0;36mHands.process\u001b[1;34m(self, image)\u001b[0m\n\u001b[0;32m    132\u001b[0m \u001b[38;5;28;01mdef\u001b[39;00m \u001b[38;5;21mprocess\u001b[39m(\u001b[38;5;28mself\u001b[39m, image: np\u001b[38;5;241m.\u001b[39mndarray) \u001b[38;5;241m-\u001b[39m\u001b[38;5;241m>\u001b[39m NamedTuple:\n\u001b[0;32m    133\u001b[0m \u001b[38;5;250m  \u001b[39m\u001b[38;5;124;03m\"\"\"Processes an RGB image and returns the hand landmarks and handedness of each detected hand.\u001b[39;00m\n\u001b[0;32m    134\u001b[0m \n\u001b[0;32m    135\u001b[0m \u001b[38;5;124;03m  Args:\u001b[39;00m\n\u001b[1;32m   (...)\u001b[0m\n\u001b[0;32m    150\u001b[0m \u001b[38;5;124;03m         right hand) of the detected hand.\u001b[39;00m\n\u001b[0;32m    151\u001b[0m \u001b[38;5;124;03m  \"\"\"\u001b[39;00m\n\u001b[1;32m--> 153\u001b[0m   \u001b[38;5;28;01mreturn\u001b[39;00m \u001b[38;5;28msuper\u001b[39m()\u001b[38;5;241m.\u001b[39mprocess(input_data\u001b[38;5;241m=\u001b[39m{\u001b[38;5;124m'\u001b[39m\u001b[38;5;124mimage\u001b[39m\u001b[38;5;124m'\u001b[39m: image})\n",
      "File \u001b[1;32m~\\AppData\\Roaming\\Python\\Python312\\site-packages\\mediapipe\\python\\solution_base.py:340\u001b[0m, in \u001b[0;36mSolutionBase.process\u001b[1;34m(self, input_data)\u001b[0m\n\u001b[0;32m    334\u001b[0m   \u001b[38;5;28;01melse\u001b[39;00m:\n\u001b[0;32m    335\u001b[0m     \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_graph\u001b[38;5;241m.\u001b[39madd_packet_to_input_stream(\n\u001b[0;32m    336\u001b[0m         stream\u001b[38;5;241m=\u001b[39mstream_name,\n\u001b[0;32m    337\u001b[0m         packet\u001b[38;5;241m=\u001b[39m\u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_make_packet(input_stream_type,\n\u001b[0;32m    338\u001b[0m                                  data)\u001b[38;5;241m.\u001b[39mat(\u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_simulated_timestamp))\n\u001b[1;32m--> 340\u001b[0m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_graph\u001b[38;5;241m.\u001b[39mwait_until_idle()\n\u001b[0;32m    341\u001b[0m \u001b[38;5;66;03m# Create a NamedTuple object where the field names are mapping to the graph\u001b[39;00m\n\u001b[0;32m    342\u001b[0m \u001b[38;5;66;03m# output stream names.\u001b[39;00m\n\u001b[0;32m    343\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_output_stream_type_info \u001b[38;5;129;01mis\u001b[39;00m \u001b[38;5;28;01mNone\u001b[39;00m:\n",
      "\u001b[1;31mKeyboardInterrupt\u001b[0m: "
     ]
    }
   ],
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
