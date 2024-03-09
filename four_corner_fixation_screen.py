import pygame
import random
import time

class FourCornerFixationScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 60)
        self.clock = pygame.time.Clock()
        self.score = 0
        self.current_number = None
        self.number_timer = 0
        self.response_allowed = False
        self.game_active = False
        self.start_time = time.time()
        self.options = ["Start"]
        self.back_button_rect = None
        self.duration_options = [15, 30, 45, 60]  # Game duration options
        self.selected_duration_index = 0  # Index of the selected duration option
        self.up_button_rect = pygame.Rect(0, 0, 0, 0)  # To be defined in display method
        self.down_button_rect = pygame.Rect(0, 0, 0, 0)  # To be defined in display method
        self.current_mode = "Random"
        self.mode_options = ["Random", "Clockwise"]
        self.current_mode_index = 0  # Index of the selected mode
        self.mode_up_button_rect = pygame.Rect(0, 0, 0, 0)  # To be defined in display method
        self.mode_down_button_rect = pygame.Rect(0, 0, 0, 0)
        self.end_time = None
        self.five_count = 0
        self.correct_presses = 0
        self.missed_presses = 0
        self.incorrect_presses = 0
        self.finish_button_rect=pygame.Rect(0, 0, 0, 0)
        self.has_responded = False
        self.number_position = None

    def start_game(self):
        self.game_active = True
        self.score = 0
        self.current_number = None
        self.number_timer = time.time()
        self.response_allowed = False
        selected_duration = self.duration_options[self.selected_duration_index]
        self.end_time = time.time() + selected_duration
        self.five_count = 0
        self.correct_presses = 0
        self.missed_presses = 0
        self.incorrect_presses = 0


    def draw_number(self):
        if self.current_number is not None and self.number_position is not None:
            number_surface = self.font.render(str(self.current_number), True, (0, 0, 0))
            number_rect = number_surface.get_rect(center=self.number_position)
            self.screen.blit(number_surface, number_rect)

    def update_game(self):
        current_time = time.time()

    # Determine if it's time to display a new number
        if self.game_active and current_time - self.number_timer > 1:
        # Check for missed press of number 5
            if self.current_number == 5 and not self.has_responded:
                self.missed_presses += 1

        # Generate a new number and reset the timer
            self.current_number = random.randint(1, 9)
            if self.current_number == 5:
                self.five_count += 1
            self.number_timer = current_time
            self.has_responded = False  # Reset response flag for the new number
        
            if self.current_mode == "Clockwise":
                self.update_clockwise_mode(current_time)
            else:  # Default to Random mode
                self.update_random_mode(current_time)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.game_active and not self.has_responded:
        # Record response
            self.has_responded = True

        # Check correctness of the response
            if self.current_number == 5:
                self.correct_presses += 1
            else:
                self.incorrect_presses += 1

    # Check if the game time has ended
        if current_time > self.end_time:
        # Count a missed press if the game ends with a 5 on screen and no response was made
            if self.current_number == 5 and not self.has_responded:
                self.missed_presses += 1
            self.game_active = False

    def update_random_mode(self, current_time):
        # Logic for updating game in Random mode
        number_surface = self.font.render(str(self.current_number), True, (0, 0, 0))
        number_width, number_height = number_surface.get_size()
        screen_width, screen_height = self.screen.get_size()
        x_pos = random.randint(50 + number_width//2, screen_width - 50 - number_width//2)
        y_pos = random.randint(50 + number_height//2, screen_height - 150 - number_height//2)
        self.number_position = (x_pos, y_pos)
        
    def update_clockwise_mode(self, current_time):
            # Duration each number stays in one corner
        duration_in_corner = 1  # In seconds

    # Current time in the game (relative to start of clockwork mode)
        current_time = time.time() - self.start_time

    # Determine the corner based on the time
        corner_index = int(current_time / duration_in_corner) % 4

    # Coordinates for each corner
        top_left = (50, 50)
        top_right = (self.screen.get_width() - 100, 50)
        bottom_right = (self.screen.get_width() - 100, self.screen.get_height() - 150)
        bottom_left = (50, self.screen.get_height() - 150)
        corners = [top_left, top_right, bottom_right, bottom_left]

    # Set the number's position to the current corner
        self.number_position = corners[corner_index]
        
        
    def display_statistics(self):
        stats = [
            f"Number of 5s shown: {self.five_count}",
            f"Correct presses: {self.correct_presses}",
            f"Missed presses (5s): {self.missed_presses}",
            f"Incorrect presses (non-5s): {self.incorrect_presses}"
        ]
        y = 150
        for stat in stats:
            text_surface = self.font.render(stat, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.screen.get_width() / 2, y))
            self.screen.blit(text_surface, text_rect)
            y += 50

    def display_screen(self):
        self.screen.fill((255, 255, 255))

        if self.game_active:
            self.update_game()
            self.draw_number()
            self.finish_button()
            
        else:
            if self.end_time is not None:  # Check if the game has ended
                self.display_statistics()
            else:
                self.display_game_options()

        self.draw_back_button()
        
    def display_game_description(self):
        description = [
            "Welcome to Four Corner Fixation!",
            "In this game, numbers will appear randomly on the screen.",
            "Your task is to press the spacebar when the number 5 appears.",
        ]
        y = 100
        margin = 20  # Margin for the rectangle around the text

    # Determine the height and width of the description box
        max_text_width = 0
        total_text_height = margin  # Start with top margin
        for line in description:
            text_surface = self.font.render(line, True, (0, 0, 0))
            max_text_width = max(max_text_width, text_surface.get_width())
            total_text_height += text_surface.get_height() + 10  # 10 is line spacing

        total_text_height += margin  # Add bottom margin

    # Draw the rectangle around the description
        rect_x = (self.screen.get_width() - max_text_width) / 2 - margin
        rect_y = y - margin
        rect_width = max_text_width + margin * 2
        rect_height = total_text_height
        pygame.draw.rect(self.screen, (200, 200, 200), [rect_x, rect_y, rect_width, rect_height])

    # Draw the text within the rectangle
        for line in description:
            text_surface = self.font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.screen.get_width() / 2, y))
            self.screen.blit(text_surface, text_rect)
            y += text_surface.get_height() + 10  # Increment y by text height and line spacing

        return y + margin  # Return Y-coordinate for next element, considering bottom margin

    def display_game_options(self):
        starting_y = self.display_game_description()+50
    # Calculate the starting Y-coordinate for the options below the "Start" option
        option_y = starting_y
        for i, option in enumerate(self.options):
            text = self.font.render(option, True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.screen.get_width() / 2, option_y + i * 50))
            self.screen.blit(text, text_rect)
    
    # Update starting_y to be below the last option
        starting_y = option_y + len(self.options) * 50

    # Display the duration option
        duration = self.duration_options[self.selected_duration_index]
        duration_text = self.font.render(f"Game Time: {duration} seconds", True, (0, 0, 0))
        duration_rect = duration_text.get_rect(center=(self.screen.get_width() / 2, starting_y))
        self.screen.blit(duration_text, duration_rect)
    
        self.up_button_rect = pygame.Rect(duration_rect.right + 10, duration_rect.top - 10, 20, 20)
        pygame.draw.polygon(self.screen, (0, 0, 0), [(self.up_button_rect.left, self.up_button_rect.bottom), (self.up_button_rect.right, self.up_button_rect.bottom), (self.up_button_rect.centerx, self.up_button_rect.top)])

        self.down_button_rect = pygame.Rect(duration_rect.right + 10, duration_rect.bottom + 10, 20, 20)
        pygame.draw.polygon(self.screen, (0, 0, 0), [(self.down_button_rect.left, self.down_button_rect.top), (self.down_button_rect.right, self.down_button_rect.top), (self.down_button_rect.centerx, self.down_button_rect.bottom)])

    # Display the mode option
        current_mode = self.mode_options[self.current_mode_index]
        mode_text = self.font.render(f"Mode: {current_mode}", True, (0, 0, 0))
        mode_rect = mode_text.get_rect(center=(self.screen.get_width() / 2, starting_y + 50))
        self.screen.blit(mode_text, mode_rect)

        self.mode_up_button_rect = pygame.Rect(mode_rect.right + 10, mode_rect.top - 10, 20, 20)
        pygame.draw.polygon(self.screen, (0, 0, 0), [(self.mode_up_button_rect.left, self.mode_up_button_rect.bottom), (self.mode_up_button_rect.right, self.mode_up_button_rect.bottom), (self.mode_up_button_rect.centerx, self.mode_up_button_rect.top)])

        self.mode_down_button_rect = pygame.Rect(mode_rect.right + 10, mode_rect.bottom + 10, 20, 20)
        pygame.draw.polygon(self.screen, (0, 0, 0), [(self.mode_down_button_rect.left, self.mode_down_button_rect.top), (self.mode_down_button_rect.right, self.mode_down_button_rect.top), (self.mode_down_button_rect.centerx, self.mode_down_button_rect.bottom)])

    def draw_back_button(self):
        back_button_text = self.font.render("Back", True, (0, 0, 0))
        self.back_button_rect = back_button_text.get_rect(center=(100, self.screen.get_height() - 50))
        self.screen.blit(back_button_text, self.back_button_rect)
        
        
    def finish_button(self):
        finish_button_text = self.font.render("Finish game", True, (0, 0, 0))
        button_width, button_height = finish_button_text.get_size()
        button_x = self.screen.get_width() - button_width - 50  # Adjusted x-coordinate
        button_y = self.screen.get_height() - button_height - 50
        self.finish_button_rect = finish_button_text.get_rect(topleft=(button_x, button_y))
        self.screen.blit(finish_button_text, self.finish_button_rect)
        

    def check_click(self, position):
        starting_y = 150  # The starting Y-coordinate for the description, same as in display_game_description
        for _ in range(3):  # Assuming there are three lines of description
            starting_y += 40
        starting_y += 50  # Additional space after the title, same as in display_game_options

    # Calculate Y-coordinate for "Start" button
        start_button_y = starting_y

        for i, option in enumerate(self.options):
            text = self.font.render(option, True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.screen.get_width() / 2, start_button_y + i * 50))
            if text_rect.collidepoint(position):
                return option
        if self.finish_button_rect.collidepoint(position) and self.game_active:
            self.finish_game()
            return "Finish"
        for i, option in enumerate(self.options):
            text = self.font.render(option, True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.screen.get_width()/2, 150 + i*50))
            if text_rect.collidepoint(position):
                return option
        if self.up_button_rect.collidepoint(position):
            self.selected_duration_index = (self.selected_duration_index + 1) % len(self.duration_options)
            return "Duration Changed"
        elif self.down_button_rect.collidepoint(position):#לתקן שיהיה גם 30 ו 60
            self.selected_duration_index = (self.selected_duration_index - 1 +len(self.duration_options))% len(self.duration_options)
            return "Duration Changed"
        
        if self.mode_up_button_rect.collidepoint(position):
            print(self.current_mode_index)
            self.current_mode_index = (self.current_mode_index + 1) % len(self.mode_options)
            self.current_mode = self.mode_options[self.current_mode_index]
            print(self.current_mode_index)
            return "Mode Changed"
        elif self.mode_down_button_rect.collidepoint(position):
            self.current_mode_index = (self.current_mode_index - 1 + len(self.mode_options)) % len(self.mode_options)
            self.current_mode = self.mode_options[self.current_mode_index]
            return "Mode Changed"



        return None
    
    def check_finish_button_click(self, position):
        if self.game_active and self.finish_button_rect.collidepoint(position):
            self.finish_game()
    
    def finish_game(self):
        self.end_time = time.time()
        self.game_active = False

    def handle_option_click(self, option):
        if option == "Start":
            self.start_game()


#להוסיף אפשרויות זמן 
