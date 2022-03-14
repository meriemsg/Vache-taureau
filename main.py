

import sys
from objects import *

pygame.init()

# ------------------------------------------
# Variables of the program
running = True
ww, wh = 1000, 600
space = int(ww / 32)


# ------------------------------------------

def create_window(ww, wh):
    'Create the display window'
    window_width, window_height = ww, wh
    window_title = 'Jeu VT'
    pygame.display.set_caption(window_title)
    icon = pygame.image.load('ico.png')
    pygame.display.set_icon(icon)
    return pygame.display.set_mode((window_width, window_height))


def arrange_button(screen, width, height, colour, horiz, vert, spacing):
    'Place number buttons 0 to 9 in a neat fashion'
    buttonlist = []
    # Place zero button
    buttonlist.append(Number_Button(width, height, (horiz + (width + spacing), vert), colour, '0'))
    buttonlist[-1].make_button()
    buttonlist[-1].place_button(screen)
    # Place buttons 1-9
    for v in range(1, 4):
        for h in range(3):
            number = (3 * (v - 1)) + (h + 1)
            pos = (horiz + h * (width + spacing), vert + v * (height + spacing))
            buttonlist.append(Number_Button(width, height, pos, colour, str(number)))
            buttonlist[-1].make_button()
            buttonlist[-1].place_button(screen)

    return buttonlist


window = create_window(ww, wh)
window.fill((208, 169, 245))

state = State()
state.set_real_number()

button_list = arrange_button(window, int(ww / 16), int(wh / 16), (255, 159, 176), int(ww * 1 / 8), int(0.55 * wh), space)

quit_button = Quit_Button(int(ww * 1 / 8), int(wh / 16), (int(ww * 7 / 16), int(wh * 14 / 16)), (247, 167, 216))
quit_button.make_button()
quit_button.place_button(window)
button_list.append(quit_button)

clear_button = Clear_Button(int(ww * 1 / 8), int(wh / 16), (int(ww * 7 / 16), int(wh * 12 / 16)), (247, 167, 216))
clear_button.make_button()
clear_button.place_button(window)
button_list.append(clear_button)

input_button = Input_Button(int(ww * 1 / 8), int(wh / 16), (int(ww * 7 / 16), int(wh * 10 / 16)), (203, 226, 188))
input_button.make_button()
input_button.place_button(window)
button_list.append(input_button)

score_board = Score_Board(int(ww * 6 / 8), int(wh / 8), (int(ww * 2 / 16), int(wh * 1 / 16)), (159, 190, 255))
score_board.colour_board()
score_board.score_display(window)

input_board = Input_Board(int(ww * 1 / 4), int(wh / 8), (int(ww * 3 / 8), int(wh * 2 / 8)), (159, 190, 255))
input_board.colour_board()
input_board.number_display(window)

history_board = History_Board(int(ww*0.65/2), int(wh/2), (int(ww*10/16),int(wh*7/16)), (159, 190, 255))
history_board.colour_board()
history_board.number_display(window)
button_list.append(input_button)



# print(state.real_number)
pygame.display.update()

while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_ESCAPE]:
                running = False

        if event.type == pygame.MOUSEMOTION:
            mouse = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONUP:
            for button in button_list:
                if button.collisionrect.collidepoint(mouse) and isinstance(button,
                                                                           Number_Button) and button.pushed == False and input_board.inputted_digits != 4:
                    # Add digit to guess
                    button.button_clicked(window)
                    input_board.update_number(window, button.text)
                    pygame.display.update()

                if button.collisionrect.collidepoint(mouse) and isinstance(button, Quit_Button):
                    # Quit the game
                    running = False

                if button.collisionrect.collidepoint(mouse) and isinstance(button, Clear_Button):
                    # Clear the input board and unpush the number buttons to reset the guess
                    input_board.reset_board(window)
                    for i in button_list:
                        if isinstance(i, Number_Button) and i.pushed == True:
                            i.button_clicked(window)
                    pygame.display.update()

                if button.collisionrect.collidepoint(mouse) and isinstance(button,
                                                                           Input_Button) and input_board.inputted_digits == 4:
                    # Check the guess and give feedback. Reset the the input board and number buttons
                    score_board.update_board(window, *state.hit_blow_checker(input_board.number_list))
                    input_board.reset_board(window)
                    for i in button_list:
                        if isinstance(i, Number_Button) and i.pushed == True:
                            i.button_clicked(window)
                    pygame.display.update()

    if state.guesses_used == state.total_guess_number or score_board.hit == 4:
        if score_board.hit == 4:
            score_board.display_text(window, 'You win!', 1000)
            score_board.display_text(window, 'The number was', 1000)
            score_board.display_text(window, '{}'.format(''.join(state.real_number)), 1000)
        else:
            score_board.display_text(window, 'You lose,', 1000)
            score_board.display_text(window, 'the number was', 1000)
            score_board.display_text(window, '{}'.format(''.join(state.real_number)), 1000)

        score_board.reset_board(window)
        input_board.reset_board(window)
        for i in button_list:
            if isinstance(i, Number_Button) and i.pushed == True:
                i.button_clicked(window)
        state.reset_state()
        pygame.display.update()

pygame.quit()
sys.exit()