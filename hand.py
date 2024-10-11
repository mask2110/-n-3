import pygame

class Hand:
    def __init__(self):
        # Tải ảnh bàn tay
        self.image = pygame.image.load("Assets/hand.png")  # Tải hình ảnh tay
        self.image = pygame.transform.scale(self.image, (50, 50))  # Kích thước
        self.rect = self.image.get_rect()
        self.score = 0  # Điểm ban đầu

    def follow_mediapipe_hand(self, x, y):
        # Cập nhật vị trí của tay theo tọa độ lấy từ Mediapipe
        self.rect.center = (x, y)

    def check_collision(self, mosquito, bee):
        # Kiểm tra va chạm với muỗi
        if self.rect.colliderect(mosquito.rect):
            self.score += 1  # Tăng điểm
            print("Muỗi bị giết! Điểm số: ", self.score)
            # Có thể reset vị trí muỗi hoặc xóa muỗi tại đây

        # Kiểm tra va chạm với ong
        if self.rect.colliderect(bee.rect):
            self.score -= 1  # Trừ điểm
            print("Ong bị giết! Điểm số: ", self.score)
            # Có thể reset vị trí ong hoặc xóa ong tại đây

    def draw(self, surface):
        # Vẽ hình bàn tay lên màn hình
        surface.blit(self.image, self.rect)
