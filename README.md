# 🤖 Gesture-Controlled TurtleBot3 using ROS 2 + Gazebo

This ROS 2 package enables you to control a TurtleBot3 robot in **Gazebo simulation** using **real-time hand gestures** captured from your webcam. The system uses **MediaPipe** to detect hand landmarks and maps gestures to robot movements via `/cmd_vel`.

---

## ✋ Supported Gestures

| Gesture           | Action            |
|------------------|-------------------|
| ✊ Fist           | Move Forward      |
| 🖐 Open Palm      | Stop              |
| ✌ Peace Sign     | Move Backward     |
| 👉 Thumb Only     | Turn Right        |
| 👈 Index Only     | Turn Left         |

---

## 🧠 Tech Stack

- ROS 2 (Humble)
- OpenCV
- MediaPipe
- TurtleBot3 (Gazebo Simulation)

---

## 📦 Package Name

`gesture_controller`

---

## 📸 How It Works

- Captures webcam video in real-time using OpenCV.
- Uses MediaPipe’s hand landmark model to extract 21 hand keypoints.
- Analyzes finger positions to detect simple gestures.
- Publishes velocity commands (`geometry_msgs/Twist`) to `/cmd_vel`.
- Moves the TurtleBot3 accordingly in Gazebo.

---

## 🔧 Installation

### 1. Clone this repository

```bash
cd ~/gesture_ws/src
git clone https://github.com/YOUR_USERNAME/gesture_robot_controller_ros2.git
