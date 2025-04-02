import os
import pygame
from math import*
import time
import random

import PygameFW as fw

















class Func:
    def __init__(self, func, name, color=None, width=3):
        self.name = name
        self.color = color
        self.width = width
        self.func = func
        self.visible = True

        if color == None:
            random.seed(time.time())
            r = random.randint(0,255)
            g = int(str(random.randint(1000,1255))[1:])
            b = int(str(random.randint(10000,10255))[2:])
            self.color = (r, g, b)
        

    def F(self, x):
        return eval(self.func)






class Graph:
    def __init__(self,
        screen_width=1200, screen_height=675,
        bg_color=(255,255,255),
        graph_resolution=5,
        window_caption='Graph',
        epilepsy=False):

        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        os.environ['SDL_VIDEO_CENTERED'] = '1'



        k = sum(bg_color)/len(bg_color)



        self.interface_color = (255*(k<255/2), 255*(k<255/2), 255*(k<255/2))

        self.interface_color = (255-bg_color[0], 255-bg_color[1], 255-bg_color[2])

        self.epilepsy = epilepsy


        self.width = screen_width
        self.height = screen_height

        self.ppu = 100
        self.caption = window_caption
        self.bg_color = bg_color
        pygame.display.set_caption(window_caption)

        self.res = graph_resolution

        self.side_panel_i = 0

        self.show_axes = False
        self.show_grid = False
        self.show_cursor_pos = False

        self.aa = False

        self.funcs = []
        self.points = []

        self.buttons_f = []
        self.buttons_init = [['A-A','Anti-Aliasing',0],
                              [' #','Show Grid',1],
                              ['AXS','Show Axes',1],
                              ['x,y','Show Cursor Position',0]]

        self.buttons = [0]*len(self.buttons_init)
        self.buttons_text = [0]*len(self.buttons_init)


        self.font = [0]*128
        for i in range(2,128):
            self.font[i] = pygame.font.Font(None,i)



        self.zero_x = screen_width // 2
        self.zero_y = screen_height // 2



        self.mouse_touching_l = False
        self.mouse_touching_r = False
        self.mouse_scrolling_u = False
        self.mouse_scrolling_d = False





    def line(self, x, y , x2, y2, color, width):
        pygame.draw.line(self.screen, color, (x,y), (x2,y2), width)

    def aaline(self, x, y , x2, y2, color, width):
        pygame.draw.aaline(self.screen, color, (x,y), (x2,y2), width)

    def circle(self, x, y, color, width):
        pygame.draw.circle(self.screen, color, (x,y), width)

    def rect(self, x, y , lenght, height, color, width):
        pygame.draw.rect(self.screen, color, (x,y,lenght,height), width)
    
    def textout(self, x, y, size, color, text):
        out = self.font[size].render(text, 1, color)
        self.screen.blit(out, (x,y))



    def add_funcs(self, funcs):
        for i in range(len(funcs)):
            self.funcs.append(funcs[i])


    def calc_point_to_soa(self, x_screen, y_screen):
        x = (x_screen - self.zero_x)/self.ppu
        y = (self.zero_y - y_screen)/self.ppu

        return x, y

    def calc_point_to_screen(self, x_soa, y_soa):
        x = self.zero_x + x_soa*self.ppu
        y = self.zero_y - y_soa*self.ppu

        return x, y


    def render_funcs(self):
        if self.funcs == []:
            return 0


        for i in range(len(self.funcs)):
            f = self.funcs[i]


            x_screen = 0
            y_screen = 1

            x_screen_prev = 0
            y_screen_prev = 0

            if f.visible:

                while x_screen <= self.width:
                    

                    x_soa = self.calc_point_to_soa(x_screen,0)[0]

                    try:
                        y_soa = f.F(x_soa)
                    except:
                        y_soa = f.F(x_soa+0.001)

                    y_screen = self.calc_point_to_screen(0,y_soa)[1]

                    if (y_screen_prev > 0 and y_screen_prev < self.height or 
                        y_screen > 0 and y_screen < self.height):
                        if self.aa:
                            self.aaline(x_screen_prev, y_screen_prev, x_screen, y_screen, f.color, f.width)
                        else:
                            self.line(x_screen_prev, y_screen_prev, x_screen, y_screen, f.color, f.width)

                    x_screen_prev = x_screen
                    y_screen_prev = y_screen
                    

                    x_screen += self.res


    

    def draw_axes(self):
        self.line(self.zero_x, 0, self.zero_x, self.height, self.interface_color, 2)
        self.line(0, self.zero_y, self.width, self.zero_y, self.interface_color, 2)


    def draw_grid(self):
        ppu_len = len(str(int(self.ppu)))

        div = 10**(ppu_len-2.69897)

        step = self.ppu / div


        for i in range(25):

            x = i*step + (self.zero_x % step)
            y = i*step + (self.zero_y % step)

            self.line(x, 0, x, self.height, (127,127,127), 1)
            self.line(0, y, self.width, y, (127,127,127), 1)


            txt_x = str(round(((x-self.zero_x)/step)/div,3))
            self.textout(x+3, self.height-18, 20, self.interface_color, txt_x)

            txt_y = str(round(((self.zero_y-y)/step)/div,3))
            self.textout(self.width-len(txt_y)*7, y+3, 20, self.interface_color, txt_y)


    def draw_cursor_pos(self):
        self.line(self.mouse_x, self.mouse_y, self.mouse_x, self.zero_y, self.interface_color, 1)
        self.line(self.mouse_x, self.mouse_y, self.zero_x, self.mouse_y, self.interface_color, 1)

        cords = str('(' + 
            str(round(self.calc_point_to_soa(self.mouse_x,0)[0], 3)) + '; ' +
            str(round(self.calc_point_to_soa(0, self.mouse_y)[1], 3)) + ')')

        self.textout(self.mouse_x, self.mouse_y-24, 24, self.interface_color, cords)


    def draw_interface(self):

        if self.side_panel_i == 1:
            x = 350
        else:
            x = 50

        self.rect(0, 0, x, self.height, self.bg_color, 0)
        self.rect(0, 0, x, self.height, self.interface_color, 2)
        self.line(47, 0, 47, self.height, self.interface_color, 2)

        if self.side_panel_i == 1:
            for i in range(len(self.funcs)):
                self.textout(
                    58, 20+i*45, 24, self.interface_color, ('"' + self.funcs[i].name + '" ' + 'F(x) = '+ self.funcs[i].func))


            for i in range(len(self.buttons)):
                self.textout(
                    58, self.height-45*(i+1)-1+20, 24, self.interface_color, self.buttons[i].text)

        

        

    def mouse_events(self):
        if self.mouse_touching_r:
            self.zero_x += self.mouse_dx
            self.zero_y += self.mouse_dy


    def buttons_events(self):
        for i in range(len(self.funcs)):
            self.funcs[i].visible = not self.controls.get_value(self.buttons_f[i])[0]

        self.aa = self.controls.get_value(self.buttons[0])[0]
        self.show_grid = self.controls.get_value(self.buttons[1])[0]
        self.show_axes = self.controls.get_value(self.buttons[2])[0]
        self.show_cursor_pos = self.controls.get_value(self.buttons[3])[0]

    def events(self):
        if self.epilepsy:
            self.interface_color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            self.bg_color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))




    def render(self):

        running = True

        self.mouse_x = 0
        self.mouse_y = 0

        self.controls = fw.Controls()

        for i in range(len(self.funcs)):
            cf = self.funcs[i].color
            cf_c = (int(cf[0]*0.7), int(cf[1]*0.7), int(cf[2]*0.7))
            cf_s = (int(cf[0]*0.4), int(cf[1]*0.4), int(cf[2]*0.4))
            self.buttons_f.append(fw.Button(
                x=2, y=2+i*45, dx=45, dy=46, mode='toggle', border_size=0,
                color_fill=cf,
                color_fill_covered=cf_c,
                color_fill_selected=cf_s))
        self.controls.add(self.buttons_f)


        for i in range(len(self.buttons_init)):
            cf = self.bg_color
            cf_c = (int(cf[0]*0.7), int(cf[1]*1), int(cf[2]*0.7))
            cf_s = (int(cf[0]*0.4), int(cf[1]*1), int(cf[2]*0.4))

            self.buttons[i] = fw.Button(
                    x=1, y=self.height-45*(i+1)-1, dx=47, dy=46, mode='toggle', border_size=1,
                    color_fill=cf,
                    color_fill_covered=cf_c,
                    color_fill_selected=cf_s,
                    color_border=self.interface_color,
                    color_border_covered=self.interface_color,
                    color_border_selected=self.interface_color,
                    text=self.buttons_init[i][1],
                    selected_left=self.buttons_init[i][2])

            self.buttons_text[i] = fw.Text(
                    x=3, y=self.height-45*(i+1)+8,
                    font_size=24,
                    color=self.interface_color,
                    value=self.buttons_init[i][0])


        self.controls.add(self.buttons)

        self.controls.add(self.buttons_text)


        while running:
            mouse_pos = pygame.mouse.get_pos()

            self.mouse_xl = self.mouse_x
            self.mouse_yl = self.mouse_y

            self.mouse_x = mouse_pos[0]
            self.mouse_y = mouse_pos[1]

            self.mouse_dx = self.mouse_x - self.mouse_xl
            self.mouse_dy = self.mouse_y - self.mouse_yl


            self.screen.fill(self.bg_color)


            self.mouse_events()
            self.buttons_events()
            self.events()


            if self.show_grid:
                self.draw_grid()

            if self.show_axes:
                self.draw_axes()

            if self.show_cursor_pos:
                self.draw_cursor_pos()


            self.render_funcs()

            self.draw_interface()



            for event in pygame.event.get():
                self.controls.events(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return 0


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        self.side_panel_i ^= 1



                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.mouse_touching_l = True
                    if event.button == 3:
                        self.mouse_touching_r = True


                    if event.button == 4:
                        self.mouse_scrolling_u = True

                        if self.ppu < 80000:

                            self.zero_x -= (self.mouse_x-self.zero_x) * 0.15
                            self.zero_y -= (self.mouse_y-self.zero_y) * 0.15

                            self.ppu = round(self.ppu * 1.15, 3)

                        


                    if event.button == 5:
                        self.mouse_scrolling_d = True

                        if self.ppu > 1.2:

                            self.zero_x += (self.mouse_x-self.zero_x) * 0.15
                            self.zero_y += (self.mouse_y-self.zero_y) * 0.15

                            self.ppu =  round(self.ppu * 0.85, 3)

                        


                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.mouse_touching_l = False
                    if event.button == 3:
                        self.mouse_touching_r = False


                    if event.button == 4:
                        self.mouse_scrolling_u = False
                    if event.button == 5:
                        self.mouse_scrolling_d = False

            self.screen = self.controls.render(self.screen)


            pygame.display.flip()
