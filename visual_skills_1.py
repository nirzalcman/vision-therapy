import pygame

class CategoryScreen:
    def __init__(self, screen, category_name):
        self.screen = screen
        self.category_name = category_name
        self.back_button_rect = None
        self.font = pygame.font.SysFont('arial', 40)
        # Add a list of games for the category
        if category_name == "Visual Skills 1":
            self.games = ["Four Corner Fixation"]

    def display_screen(self):
        title = self.font.render(self.category_name, True, (0, 0, 0))
        title_rect = title.get_rect(center=(self.screen.get_width()/2, 50))
        self.screen.blit(title, title_rect)
        self.draw_back_button()

        # Display list of games
        for i, game in enumerate(self.games):
            text = self.font.render(game, True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.screen.get_width()/2, 150 + i*50))
            self.screen.blit(text, text_rect)
    
    def check_click(self, position):
        for i, game in enumerate(self.games):
            text = self.font.render(game, True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.screen.get_width()/2, 150 + i*50))
            if text_rect.collidepoint(position):
                return game
        return None
    
    def draw_back_button(self):
        back_button_text = self.font.render("Back", True, (0, 0, 0))
        self.back_button_rect = back_button_text.get_rect(center=(100, self.screen.get_height() - 50))
        self.screen.blit(back_button_text, self.back_button_rect)
