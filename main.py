import pygame
import sys
from menu import Menu
from visual_skills_1 import CategoryScreen
from four_corner_fixation_screen import FourCornerFixationScreen
from LanguageSelection import LanguageSelection

# Define game states
MENU = "menu"
CATEGORY_SCREEN = "category_screen"
FOUR_CORNER_FIXATION = "four_corner_fixation"
LANGUAGE_SELECTION = "language_selection"



# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set up the screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Computer Aided Vision Therapy")

# Initialize game state
game_state = LANGUAGE_SELECTION
language_screen = LanguageSelection(screen)
selected_language = None

def game_loop():
    global game_state
    menu = Menu(screen,None)
    current_category_screen = None
    current_game_screen = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == LANGUAGE_SELECTION:
                    selected_language = language_screen.check_click(event.pos)
                    if selected_language:
                          game_state = MENU
                          menu = Menu(screen, selected_language)
                elif game_state == MENU:
                    selected_option = menu.check_click(event.pos)
                    if selected_option:
                        game_state = CATEGORY_SCREEN
                        current_category_screen = CategoryScreen(screen, selected_option)
                elif game_state == CATEGORY_SCREEN and current_category_screen:
                    if current_category_screen.back_button_rect.collidepoint(event.pos):
                        game_state = MENU
                        current_category_screen = None
                    else:
                        selected_game = current_category_screen.check_click(event.pos)
                        if selected_game == "Four Corner Fixation":
                            game_state = FOUR_CORNER_FIXATION
                            current_game_screen = FourCornerFixationScreen(screen)
                elif game_state == FOUR_CORNER_FIXATION and current_game_screen:
                    clicked_option = current_game_screen.check_click(event.pos)
                    if clicked_option == "Mode Changed":
                    # Redraw the screen to reflect the mode change
                        current_game_screen.display_screen()
                    elif clicked_option == "Finish":
                    # The finish button was clicked; handle any specific logic here
                    # Since we already call finish_game in check_click, we might not need additional logic here
                        pass
                    elif current_game_screen.back_button_rect.collidepoint(event.pos):
                        game_state = CATEGORY_SCREEN
                        current_game_screen = None
                    
                    else:
                        selected_option = current_game_screen.check_click(event.pos)
                        if selected_option:
                            current_game_screen.handle_option_click(selected_option)

        screen.fill((255, 255, 255))  # Fill the screen with a white background
        if game_state == LANGUAGE_SELECTION:
            language_screen.display_screen()
        elif game_state == MENU:
            menu.display_menu()
        elif game_state == CATEGORY_SCREEN and current_category_screen:
            current_category_screen.display_screen()
        elif game_state == FOUR_CORNER_FIXATION and current_game_screen:
            current_game_screen.display_screen()

        pygame.display.update()

if __name__ == "__main__":
    game_loop()
