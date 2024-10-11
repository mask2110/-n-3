# mosquito.py
import pygame
import random

class Mosquito:
    def __init__(self):
        # Kích thước ngẫu nhiên
        random_size_value = random.uniform(0.5, 1.5)  # Ví dụ cho giá trị kích thước ngẫu nhiên
        size = (int(64 * random_size_value), int(64 * random_size_value))  # Kích thước mặc định

        # Vị trí ban đầu
        start_pos = (random.randint(0, 1280 - size[0]), random.randint(0, 720 - size[1]))

        # Định nghĩa rect để quản lý va chạm và di chuyển
        self.rect = pygame.Rect(start_pos[0], start_pos[1], size[0], size[1])

        # Tải hình ảnh muỗi
        self.image = pygame.image.load("Assets/muoi.png")
        self.image = pygame.transform.scale(self.image, size)

        # Biến để theo dõi animation
        self.current_frame = 0
        self.animation_timer = 0

    def draw(self, surface):
        # Vẽ muỗi lên màn hình tại vị trí rect
        surface.blit(self.image, (self.rect.x, self.rect.y))
