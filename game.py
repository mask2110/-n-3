import cv2
import mediapipe as mp
import pygame
from mosquito import Mosquito
from bee import Bee
from hand import Hand

# Kích thước màn hình
screen_width = 1280
screen_height = 720

def is_fist(hand_landmarks):
    # Lấy vị trí của đầu ngón tay và lòng bàn tay
    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]
    middle_tip = hand_landmarks.landmark[12]
    ring_tip = hand_landmarks.landmark[16]
    pinky_tip = hand_landmarks.landmark[20]
    palm_base = hand_landmarks.landmark[0]

    # Tính toán khoảng cách giữa các đầu ngón tay và lòng bàn tay
    def distance(tip, base):
        return ((tip.x - base.x) ** 2 + (tip.y - base.y) ** 2) ** 0.5

    # Nếu tất cả các đầu ngón tay gần lòng bàn tay thì coi là nắm tay
    if (distance(thumb_tip, palm_base) < 0.1 and
        distance(index_tip, palm_base) < 0.1 and
        distance(middle_tip, palm_base) < 0.1 and
        distance(ring_tip, palm_base) < 0.1 and
        distance(pinky_tip, palm_base) < 0.1):
        return True

    return False

# Khởi tạo Pygame
pygame.init()
pygame.display.set_caption("Game")
screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

# Tải ảnh nền
background = pygame.image.load("Assets/background.jpg")
background = pygame.transform.scale(background, (screen_width, screen_height))

# Tạo đối tượng muỗi, ong và tay
mosquito = Mosquito()
bee = Bee()
hand = Hand()

# Mediapipe khởi tạo
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Khởi tạo webcam
cap = cv2.VideoCapture(0)

# Vòng lặp game chính
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Đọc khung hình từ webcam
    success, frame = cap.read()
    if success:
        frame = cv2.flip(frame, 1)  # Lật khung hình cho đúng hướng gương
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Lấy tọa độ của ngón tay cái để di chuyển bàn tay
                x = int(hand_landmarks.landmark[4].x * screen_width)
                y = int(hand_landmarks.landmark[4].y * screen_height)
                hand.follow_mediapipe_hand(x, y)

                # Kiểm tra nếu cử chỉ tay "đóng lại" (fist) được phát hiện
                if is_fist(hand_landmarks):
                    hand.check_collision(mosquito, bee)  # Trigger sự kiện giết muỗi hoặc ong

                # Vẽ landmarks lên hình webcam để debug
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Hiển thị hình ảnh webcam (để debug)
        cv2.imshow('Hand Tracking', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Vẽ nền lên màn hình
    screen.blit(background, (0, 0))

    # Vẽ muỗi, ong và tay
    mosquito.draw(screen)
    bee.draw(screen)
    hand.draw(screen)

    # Cập nhật màn hình
    pygame.display.update()

# Thoát Pygame và giải phóng webcam
pygame.quit()
cap.release()
cv2.destroyAllWindows()
