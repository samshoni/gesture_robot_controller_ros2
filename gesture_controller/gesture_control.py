import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import cv2
import mediapipe as mp


class GestureController(Node):
    def __init__(self):
        super().__init__('gesture_controller')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)

        # Mediapipe setup
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1)
        self.mp_draw = mp.solutions.drawing_utils

        # Camera setup
        self.cap = cv2.VideoCapture(0)
        self.timer = self.create_timer(0.1, self.detect_gesture)

    def detect_gesture(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        cmd = Twist()

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                # Finger tip landmarks
                tip_ids = [4, 8, 12, 16, 20]
                fingers_up = []

                # Thumb: Check if thumb tip is to the left of the base
                if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 2].x:
                    fingers_up.append(True)
                else:
                    fingers_up.append(False)

                # Other fingers: Check tip higher (y smaller) than pip joint
                for i in range(1, 5):
                    if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i] - 2].y:
                        fingers_up.append(True)
                    else:
                        fingers_up.append(False)

                total_fingers = fingers_up.count(True)

                # === Gesture Mapping ===
                if total_fingers == 0:
                    self.get_logger().info("✊ Fist detected → Moving forward")
                    cmd.linear.x = 0.3
                elif total_fingers == 5:
                    self.get_logger().info("🖐 Open Palm detected → Stopping")
                    cmd.linear.x = 0.0
                elif fingers_up[1] and fingers_up[2] and not fingers_up[3] and not fingers_up[4]:
                    self.get_logger().info("✌ Peace Sign → Move backward")
                    cmd.linear.x = -0.2
                elif fingers_up[0] and not any(fingers_up[1:]):
                    self.get_logger().info("👉 Thumb Right → Turn right")
                    cmd.angular.z = -0.5
                elif not fingers_up[0] and fingers_up[1] and not any(fingers_up[2:]):
                    self.get_logger().info("👈 Index Only → Turn left")
                    cmd.angular.z = 0.5
                else:
                    self.get_logger().info("✋ Unknown gesture → Stop")
                    cmd.linear.x = 0.0
                    cmd.angular.z = 0.0

        self.publisher_.publish(cmd)

        # Show webcam feed
        cv2.imshow('Gesture Controller', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            rclpy.shutdown()

    def destroy_node(self):
        self.cap.release()
        cv2.destroyAllWindows()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = GestureController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

