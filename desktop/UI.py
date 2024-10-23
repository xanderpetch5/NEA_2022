import sys, re
import pygame
import dataGathering


class Text_Info_Box:
    def __init__(self, text, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.base_font = pygame.font.Font(None, 32)
        self.scroll = 0

        font_width, self.font_height = (self.base_font.size(text))
        print(font_width / width)
        lines = []
        line = ""
        words = text.split(' ')
        for word in words:
            if self.base_font.size(line + word)[0] > width:
                lines.append(line)
                line = ""
            line += word + ' '
        lines.append(line)
        print(self.font_height)
        self.lines = lines

    def hypertext(self,line,text,count ):
        if text in line:
            split_line = re.split(rf'({text})',line) # splits line but keeps delimiter



    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                if self.scroll < 0:
                    self.scroll += 10
            elif event.button == 5:
                if self.scroll > -(self.font_height * len(self.lines)) + self.height / 2:
                    self.scroll -= 10

    def render(self):
        pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, self.width + 5, self.height))
        for count, line in enumerate(self.lines):
            text_surface = self.base_font.render(line, True, (255, 255, 255))
            if ((self.y + self.scroll + (self.font_height * count)) > self.y - 2) and (
                    (self.y + self.scroll + (self.font_height * count)) < (self.y + self.height - 30)):
                screen.blit(text_surface, (self.x + 4, self.y + self.scroll + (self.font_height * count) + 2))
                self.hypertext(line, 'Selway',count)



class Button:
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.base_font = pygame.font.Font(None, 32)
        self.pressed = False
        self.colour = (100, 100, 100)
        self.colour_cycle = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x <= event.pos[0] <= self.x + self.width and self.y <= event.pos[
                1] <= self.y + self.height:
                self.colour = (150, 150, 150)
                self.pressed = True

    def render_button(self):
        if self.pressed:
            self.colour_cycle += 1
            print(self.colour_cycle)
        if self.colour_cycle > 10:  # makes the colour change for 1/6 of a seconds if pressed
            self.pressed = False
            self.colour_cycle = 0
            self.colour = (100, 100, 100)
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))  # draw the button


class DropDown(Button):
    def __init__(self, x, y, height, width, choices):
        # Call the constructor of the parent class
        super().__init__(x, y, height, width)
        self.choices = choices
        self.selected = False
        self.selected_option = None

    def handle_event(self, event):
        # Handle the event only if it is a mouse button press
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the button press occurred on the dropdown menu
            if self.x <= event.pos[0] <= self.x + self.width and self.y <= event.pos[1] <= self.y + self.height:
                # Toggle the selected flag variable change the color of the menu
                self.selected = not self.selected
                self.colour = (150, 150, 150) if self.selected else (100, 100, 100)
            elif self.selected:
                # If the dropdown menu is selected, check if the button press occurred on a choice
                for i, choice in enumerate(self.choices):
                    if self.x <= event.pos[0] <= self.x + self.width and self.y + self.height * (i + 1) <= event.pos[
                        1] <= self.y + self.height * (i + 2):
                        # If the button press occurred on a choice, store the selected option and unselect the menu
                        self.selected_option = choice
                        self.selected = False
                        self.colour = (100, 100, 100)

    def render_text(self, font):
        # Render the selected option on the button if it is not None, otherwise render the default text
        txt = font.render(self.selected_option or 'Toggle', True, (255, 255, 255))
        screen.blit(txt, (self.x + 5, self.y + 5))

    def render_button(self):
        # Call the render_button method of the parent class
        super().render_button()

        # Render the text on the button
        self.render_text(self.base_font)

        # If the dropdown menu is selected, render the choices on the screen
        if self.selected:
            rect_height = len(self.choices) * self.height
            pygame.draw.rect(screen, self.colour, (self.x, self.y + self.height, self.width, rect_height))
            for i, choice in enumerate(self.choices):
                choice_txt = self.base_font.render(choice, True, (255, 255, 255))
                screen.blit(choice_txt, (self.x + 5, self.y + self.height * (i + 1) + 5))


class TextBox:
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.height = 32
        self.user_text = ''
        self.output = None
        self.base_font = pygame.font.Font(None, 20)
        self.active = False
        self.backspace_held = False
        self.delete_toggle = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x <= event.pos[0] <= self.x + self.width and self.y <= event.pos[1] <= self.y + self.height:
                self.active = True
            else:
                self.active = False
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.backspace_held = True
            elif event.key == pygame.K_RETURN:
                self.output = self.user_text
                self.user_text = ''
                self.active = False
            else:
                self.user_text += event.unicode
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE:
                self.backspace_held = False

    def render_text(self):
        if self.backspace_held:
            self.delete_toggle += 1
            if self.delete_toggle > 2:
                self.user_text = self.user_text[:-1]
                self.delete_toggle = 0
        if not self.active:
            color = (100, 100, 100)
        else:
            color = (150, 150, 150)

        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

        text_surface = self.base_font.render(self.user_text, True, (255, 255, 255))
        screen.blit(text_surface, (self.x + 4, self.y + 6))


def gather_data(name, choice):
    if choice == "Artist":
            item = dataGathering.Artist(name)
            print(item.get_name())
            print(item.get_top_song())
    elif choice == "Album":
            item = dataGathering.Album(name)
            print(item.get_name())
    elif choice == "Song":
            item = dataGathering.Song(name,None)
            print(item.get_track_name())


def run():
    pygame.init()
    global screen
    screen = pygame.display.set_mode((960, 540))
    clock = pygame.time.Clock()
    entered = True

    box = TextBox(280, 50, 400)
    dropdown = DropDown(420, 100, 32, 120, ['Song', 'Artist', 'Album'])
    text_info = Text_Info_Box(str(dataGathering.Artist("eliott smith").find_intro_paragraphs()),
                              0, 0, 500, 300)

    last_ouput = ''

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            box.handle_event(event)
            dropdown.handle_event(event)
            text_info.handle_event(event)
            if box.output is not None and box.output != last_ouput:

                last_ouput = box.output
                choice = dropdown.selected_option
                if last_ouput != '' and choice is not None:
                    entered = True
                    (gather_data(last_ouput, choice))
                    screen.fill((10, 10, 10))
        screen.fill((10, 10, 10))
        text_info.render()
        if not entered:
            box.render_text()
            dropdown.render_button()
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    run()
