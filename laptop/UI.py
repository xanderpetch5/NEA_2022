import pygame

pygame.init()
global screen
screen = pygame.display.set_mode((960, 540))

import pygame
from PIL import Image


class BarChart:
    def __init__(self, rect_x, rect_y, rect_width, rect_height, text, bar_max, bar_value):
        self.rect_x = rect_x
        self.rect_y = rect_y
        self.rect_width = rect_width
        self.rect_height = rect_height
        self.text = text
        self.bar_max = bar_max
        self.bar_value = bar_value

    def render(self):
        pygame.draw.rect(screen, (75,75,75), (self.rect_x - 5, self.rect_y -5, self.rect_width + 10, self.rect_height + 40))
        pygame.draw.rect(screen, (200,200,200), (self.rect_x, self.rect_y, self.rect_width, self.rect_height))
        bar_height = (self.bar_value / self.bar_max) * self.rect_height
        pygame.draw.rect(screen, (120,0,0), (self.rect_x, self.rect_y + self.rect_height - bar_height, self.rect_width, bar_height+2))
        font = pygame.font.Font(None, 28)
        text = font.render(self.text, True, (255,255,255))
        text_rect = text.get_rect()
        text_rect.centerx = self.rect_x + self.rect_width // 2
        text_rect.centery = self.rect_y + self.rect_height + 20
        screen.blit(text, text_rect)

class Text_Info_Box:
    def __init__(self, text, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_size = 32
        self.base_font = pygame.font.Font(None, self.font_size)
        self.scroll = 0
        self.get_lines(text)

    def get_lines(self, text):
        if isinstance(text, list):
            text = "          ".join(text)
        text = text.replace("[", "")
        text = text.replace("]", "")
        text = text.replace("'", "")
        text = text.replace('"', "")
        lines = []
        line = ""
        words = text.split(' ')
        for word in words:
            if self.base_font.size(line + word)[0] > self.width:
                lines.append(line)
                line = ""
            line += word + ' '
        lines.append(line)
        self.lines = lines
        self.font_height = self.base_font.size("H")[1]

    def handle_event(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.x <= mouse_x <= self.x + self.width + 5 and self.y <= mouse_y <= self.y + self.height:

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    if self.scroll < 0:
                        self.scroll += 15
                elif event.button == 5:
                    if self.scroll > -(self.font_height * len(self.lines)) + self.height / 2:
                        self.scroll -= 15

    def render(self):
        pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, self.width + 5, self.height))


        for count, line in enumerate(self.lines):
            text_surface = self.base_font.render(line, True, (255, 255, 255))
            if ((self.y + self.scroll + (self.font_height * count)) > self.y - 2) and (
                    (self.y + self.scroll + (self.font_height * count)) < (self.y + self.height - 30)):
                screen.blit(text_surface, (self.x + 4, self.y + self.scroll + (self.font_height * count) + 2))

class Button:
    def __init__(self, x, y, height, width, text):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.text = text
        self.base_font = pygame.font.Font(None, 32)
        self.pressed = False
        self.colour = (100, 100, 100)
        self.colour_cycle = 0
        self.colour_change = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x <= event.pos[0] <= self.x + self.width and self.y <= event.pos[1] <= self.y + self.height:
                self.colour = (125, 125, 125)
                self.pressed = True
                self.colour_change = True
                return True
        return False

    def render_button(self):
        self.pressed = False
        if self.colour_change:
            self.colour_cycle += 1
        if self.colour_cycle > 10:
            self.colour_change = False
            self.colour_cycle = 0
            self.colour = (100, 100, 100)
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))

        text_surface = self.base_font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x + self.width // 2, self.y + self.height // 2)
        screen.blit(text_surface, text_rect)


class Nav_Bar:
    def __init__(self, button_choices, button_spacing):
        self.buttons = [Button(count * button_spacing, 0, 40, button_spacing, i) for count, i in
                        enumerate(button_choices)]

    def handle_event(self, event):
        for button in self.buttons:
            if button.handle_event(event) and button.pressed:
                match button.text:
                    case "Search":
                        return 1
                    case "User Settings":
                        return 2
                    case "Find Similar":
                        return 6
        return None

    def render_buttons(self):
        for i in self.buttons:
            i.render_button()


class DropDown(Button):
    def __init__(self, x, y, height, width, text, choices):
        super().__init__(x, y, height, width, text)
        self.choices = choices
        self.selected = False
        self.selected_option = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x <= event.pos[0] <= self.x + self.width and self.y <= event.pos[1] <= self.y + self.height:
                self.selected = not self.selected
                self.colour = (150, 150, 150) if self.selected else (100, 100, 100)
            elif self.selected:
                for i, choice in enumerate(self.choices):
                    if self.x <= event.pos[0] <= self.x + self.width and self.y + self.height * (i + 1) <= event.pos[
                        1] <= self.y + self.height * (i + 2):
                        self.selected_option = choice
                        self.selected = False
                        self.colour = (100, 100, 100)

    def render_text(self, font):
        if self.selected_option:
            txt = font.render(self.selected_option, True, (255, 255, 255))
        else:
            txt = font.render(self.text, True, (255, 255, 255))
        screen.blit(txt, (self.x + 5, self.y + 5))

    def render_button(self):
        if self.pressed:
            self.colour_cycle += 1
            print(self.colour_cycle)
        if self.colour_cycle > 10:
            self.pressed = False
            self.colour_cycle = 0
            self.colour = (100, 100, 100)
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))

        if not self.selected:
            self.render_text(self.base_font)

        if self.selected:
            rect_height = len(self.choices) * self.height
            pygame.draw.rect(screen, self.colour, (self.x, self.y + self.height, self.width, rect_height))
            for i, choice in enumerate(self.choices):
                choice_txt = self.base_font.render(choice, True, (255, 255, 255))
                screen.blit(choice_txt, (self.x + 5, self.y + self.height * (i + 1) + 5))


class TextBox:
    def __init__(self, x, y, width, initial_text):
        self.x = x
        self.y = y
        self.width = width
        self.height = 32
        self.user_text = ''
        self.initial_text = initial_text
        self.output = None
        self.base_font = pygame.font.Font(None, 32)
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

        if not self.active and self.user_text == '':
            text_surface = self.base_font.render(self.initial_text, True, (150, 150, 150))
            screen.blit(text_surface, (self.x + 4, self.y + 6))

        text_surface = self.base_font.render(self.user_text, True, (255, 255, 255))
        screen.blit(text_surface, (self.x + 4, self.y + 6))


class PasswordBox(TextBox):
    def __init__(self, x, y, width, initial_text):
        super(PasswordBox, self).__init__(x, y, width, initial_text)
        self.masked_text = ''

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

        if not self.active and self.user_text == '':
            text_surface = self.base_font.render(self.initial_text, True, (150, 150, 150))
            screen.blit(text_surface, (self.x + 4, self.y + 6))
        self.masked_text = "*" * len(self.user_text)
        text_surface = self.base_font.render(self.masked_text, True, (255, 255, 255))
        screen.blit(text_surface, (self.x + 4, self.y + 6))


class Text:
    def __init__(self, text_x, text_y, text, text_size, rect_width, rect_height):
        self.x, self.y, self.text = text_x, text_y, text
        self.rect_width, self.rect_height = rect_width, rect_height
        self.base_font = pygame.font.Font(None, text_size)

    def render_text(self):
        text_surface = self.base_font.render(self.text, True, (255, 255, 255))
        pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, self.rect_width, self.rect_height))
        screen.blit(text_surface, (self.x+5, self.y+5))

class Song_Result:
    def __init__(self,x,y,song_name,artist_name,album_cover_dir):
        self.uri = ""
        self.x,self.y=x,y
        self.song_name, self.artist_name, self.album_cover = song_name,artist_name,album_cover_dir
        self.song_name = Text(self.x+100,self.y,self.song_name,45,400,50)
        self.artist_name = Text(self.x+100,self.y+50,self.artist_name,35,300,50)
        self.next_button = Button(self.x+800,self.y,100,100,"-->")
        self.image= pygame.image.load(album_cover_dir)
        self.image = pygame.transform.scale(self.image,(100,100))

    def handle_event(self,event):
        self.next_button.handle_event(event)

    def render(self):
        pygame.draw.rect(screen, (75,75,75), (self.x,self.y,900, 100 ))
        screen.blit(self.image, (self.x,self.y))
        self.next_button.render_button()
        self.song_name.render_text()
        self.artist_name.render_text()


