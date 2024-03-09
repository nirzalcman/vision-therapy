import pygame
class LanguageSelection:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('arial', 40)
        self.options = ['For English press here', 'ןאכ ץחל תירבעל']
        self.selected_language = None

    def display_screen(self):
        for i, option in enumerate(self.options):
            text = self.font.render(option, True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.screen.get_width()/2, 150 + i*50))
            self.screen.blit(text, text_rect)

    def check_click(self, position):
        for i, option in enumerate(self.options):
            text = self.font.render(option, True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.screen.get_width()/2, 150 + i*50))
            if text_rect.collidepoint(position):
                if i == 0:  # English
                    self.selected_language = 'English'
                elif i == 1:  # Hebrew
                    self.selected_language = 'Hebrew'
                return self.selected_language
        return None
