import pygame

# Colors
GRAY = (200, 200, 200)
BLUE = (0, 120, 255)

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val):
        self.rect = pygame.Rect(x, y, w, h)  # The track
        self.handle_rect = pygame.Rect(x, y, 20, h)  # The handle
        self.min_val = min_val
        self.max_val = max_val
        self.val = max_val  # Current value
        self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, BLUE, self.handle_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.handle_rect.x = max(self.rect.x, min(event.pos[0], self.rect.right - self.handle_rect.width))
            self.val = ((self.handle_rect.x - self.rect.x) / (self.rect.width - self.handle_rect.width)) * (self.max_val - self.min_val) + self.min_val
