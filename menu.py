import pygame

class Menu:
    def __init__(self, screen,language):
        self.screen = screen
        self.language=language
        self.font = pygame.font.SysFont('arial', 40)
        self.options_english = ["Visual Skills 1"]  # List of catagories for now just 1
        self.options_hebrew = ["כישוריים חזותיים 1"] 

    def display_menu(self):
        title = self.font.render("Computer Aided Vision Therapy", True, (0, 0, 0))
        title_rect = title.get_rect(center=(self.screen.get_width()/2, 50))

        self.screen.blit(title, title_rect)
        options = self.options_hebrew if self.language == 'Hebrew' else self.options_english


        for i, option in enumerate(options):
            text = self.font.render(option, True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.screen.get_width()/2, 150 + i*50))
            self.screen.blit(text, text_rect)
            
    def check_click(self, position):
        options = self.options_hebrew if self.language == 'Hebrew' else self.options_english
        for i, option in enumerate(options):
            text = self.font.render(option, True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.screen.get_width()/2, 150 + i*50))
            if text_rect.collidepoint(position):
                return option
        return None
