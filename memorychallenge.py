
#MEMORY GAME
import pygame
import random
import time



#from pygame import mixer
pygame.init()
pygame.mixer.init()
match_sound = pygame.mixer.Sound("correct.mp3")
wrong_sound = pygame.mixer.Sound("wrong.mp3")
winning_sound = pygame.mixer.Sound("winsound.wav")
losing_music = pygame.mixer.Sound("losemusic.mp3")
background_music = pygame.mixer.Sound("music.mp3")
background_music.play(-1)
#game variables and constants
WIDTH = 1550
HEIGHT = 790
white = (255, 255, 255)
black = (0, 0 , 0)
green = (0, 255, 0)
gray = (128,128,128)
blue = (0,0,255)
red = (255,0,0)
cards_matched=0
# Frame rate-How fast game runs
fps = 60
timer = pygame.time.Clock()

rows = 6
cols = 6
correct = [
           [0,0,0,0,0,0],
           [0,0,0,0,0,0],
           [0,0,0,0,0,0],
           [0,0,0,0,0,0],
           [0,0,0,0,0,0],
           [0,0,0,0,0,0]]
new_board = True
options_list = []
used = []
spaces = []
first_guess = False
second_guess = False
first_guess_num = 0
second_guess_num = 0
score = 0 
best_score = 0
least_time=0
matches = 0 
cards_matched = 0
game_over = False
pink = "#F98B88"
remaining_turns = 50

#Creating screen 
screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption('Matching Game!')
title_font = pygame.font.Font('freesansbold.ttf',50)
normal_font = pygame.font.Font('freesansbold.ttf',26)


def generate_board():
    background_music.play(-1)
    global options_list
    global spaces
    for item in range(rows * cols // 2):
        options_list.append(item)

    for item in range(rows * cols):
        piece = options_list[random.randint(0,len(options_list)-1)]
        spaces.append(piece)
        if piece in used:
            used.remove(piece)
            options_list.remove(piece)
        else:
            used.append(piece)

def draw_backgrounds():

    top_menu= pygame.draw.rect (screen,pink , [0, 0, WIDTH, 100])
    title = title_font.render('The Matching Game!',True,black)
    screen.blit(title,(400,20))
    board_space=pygame.draw.rect (screen, gray, [0, 100, WIDTH, HEIGHT-100])
    bottom_menu= pygame.draw.rect(screen, pink, [10, HEIGHT-100, WIDTH, 100], 0)
    restart_button = pygame.draw.rect(screen, gray, [150,HEIGHT - 90, 200, 80], 0, 5)
    restart_text = title_font.render('Restart',True,black)
    screen.blit(restart_text,(160,720)) 
    cards_matched_text= normal_font.render(f'Cards Matched: {cards_matched}',True,black)
    screen.blit(cards_matched_text, (550,720))
    score_text = normal_font.render(f'Remaining Turns: {remaining_turns}',True,black)
    screen.blit(score_text, (820,720))
    best_text = normal_font.render(f'Previous Best: {best_score}',True,black) 
    screen.blit(best_text, (10,20))
    time_text = normal_font.render(f'Least Time: {least_time}',True,black) 
    screen.blit(time_text, (10,60))
    background_image1=pygame.image.load("boy.png")
    background_image2 = pygame.image.load("brain.png")
    background_position1=(1000,0)
    background_position2=(-40,190)
    screen.blit(background_image1,background_position1)
    screen.blit(background_image2,background_position2)
    return restart_button
def draw_exit_button():
    exit_button = pygame.draw.rect(screen, red, [1400, 10, 100, 40], 0, 5)
    exit_text = normal_font.render('Exit', True, black)
    screen.blit(exit_text, (1420, 20))
    return exit_button

def draw_welcome_screen():
    screen.fill(white)
    
    start_font = pygame.font.Font('freesansbold.ttf', 50)
    
    start_button = pygame.draw.rect(screen,green,[650,500,200,80],0,5)
    start_button_text = start_font.render('Start',True,black)
    screen.blit(start_button_text,(690,515))

    background_image3=pygame.image.load("title.png")
    #background_image4 = pygame.image.load("play.png")
    background_position3=(250,50)
    #background_position4=(-40,190)
    screen.blit(background_image3,background_position3)
    #screen.blit(background_image4,background_position4)
    pygame.display.flip()   

def draw_start_button():
    if show_welcome:
        start_button = pygame.draw.rect(screen,green,[650,500,200,80],0,5)
        start_button_text = normal_font.render('Start',True,black)
        screen.blit(start_button_text,(690,515))
        return start_button

def draw_board():
    global rows
    global cols
    global correct
    board_list = []
    for i in range(cols):
        for j in range(rows):
            piece = pygame.draw.rect(screen,white,[500+i * 75 +10,80+j * 65 + 112, 50, 50],0,4)
            board_list.append(piece)
            '''piece_text = normal_font.render(f'{spaces[i * rows +j]}',True,gray)
            screen.blit(piece_text, (500+i * 75 + 18, 20+j * 65 +120))'''

    for r in range(rows):
        for c in range(cols):
            if correct[r][c] == 1:
                pygame.draw.rect(screen,green,[500+c * 75 +10,80+r * 65 + 110, 54, 54],3,4)
                piece_text = normal_font.render(f'{spaces[c * rows + r]}',True,black)
                screen.blit(piece_text, (500+c * 75 + 18,80+ r * 65 +120))
    return board_list
def check_guesses(first,second):
    global spaces
    global correct
    global score
    global matches
    global cards_matched
    if spaces[first] == spaces[second]:
        col1 = first // rows
        col2 = second // rows
        row1 = first - (first // rows * rows)
        row2 = second - (second // rows * rows)
        if correct[row1][col1] == 0 and correct[row2][col2] == 0:
            correct[row1][col1] = 1
            correct[row2][col2] = 1
            score += 1
            matches += 1
            cards_matched += 1
            match_sound.play()
            match_sound.fadeout(1000)
            
    else:
        score += 1
        wrong_sound.play()
        wrong_sound.fadeout(1000)
    
start_time=None
elapsed_time=0

running = True
show_welcome = True
game_over = False

while running:
    
    
    timer.tick(fps)
    screen.fill(white)
    if new_board:
        generate_board()
        print(spaces)
        new_board = False
        start_time = time.time()

    restart = draw_backgrounds()
    exit_button = draw_exit_button()
    board = draw_board()
    start_button = draw_start_button()
    if first_guess and second_guess:
        check_guesses(first_guess_num , second_guess_num)
        remaining_turns -= 1
        pygame.time.delay(1000)
        first_guess = False
        second_guess = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if show_welcome:
                if start_button.collidepoint(event.pos):
                    show_welcome = False
                    continue
            for i in range(len(board)):
                button = board[i] 
                if not game_over:
                    if button.collidepoint(event.pos) and not first_guess:
                        first_guess = True
                        first_guess_num = i
                  
                    if button.collidepoint(event.pos) and not second_guess and first_guess and i != first_guess_num:
                        second_guess = True
                        second_guess_num = i
            if exit_button.collidepoint(event.pos):
                
                background_music.stop()
                pygame.quit()
                #running = False

            if restart.collidepoint(event.pos):  
                background_music.play(-1)
                options_list=[]
                new_board = True
                used = []
                spaces = []
                
                score = 0
                matches = 0
                #remaining_turns = 20
                first_guess = False
                second_guess = False
                cards_matched = 0
                remaining_turns = 50
                correct = [
                           [0,0,0,0,0,0],
                           [0,0,0,0,0,0],
                           [0,0,0,0,0,0],
                           [0,0,0,0,0,0],
                           [0,0,0,0,0,0],
                           [0,0,0,0,0,0]]
                game_over = False
                start_time = time.time()
            
    if show_welcome:
        draw_welcome_screen()
    else:
        if not game_over:
          current_time=time.time()
          elapsed_time=int(current_time-start_time)
        
        timer_text=normal_font.render(f'Time:{elapsed_time} seconds',True,black)
        screen.blit(timer_text,(1100,30))
        
        
        if cards_matched == rows *cols // 2:
          game_over = True
          winner = pygame.draw.rect(screen, black, [500, HEIGHT - 400,550, 120], 0, 5)  
          winner_text = title_font.render(f'You won in {score} moves!',True,white)
          screen.blit(winner_text, (530,HEIGHT-380))
          time_taken = normal_font.render(f'Time Taken:{elapsed_time}seconds',True,white)
          screen.blit(time_taken,(620,HEIGHT-320))
          winning_sound.play()
          winning_sound.fadeout(1000)
          background_music.stop()

          if best_score > score or best_score == 0:
             best_score = score
          if least_time > elapsed_time or least_time == 0:
             least_time = elapsed_time
         
        if remaining_turns <= 0:
            game_over = True
            loser = pygame.draw.rect(screen, black, [550, HEIGHT - 400,500, 200], 0, 5)
            loser_text = title_font.render(f'Game Over!  ', True, red)
            screen.blit(loser_text, (570, HEIGHT - 380))
            loser_text1 = normal_font.render(f'You ran out of turns', True, red)
            screen.blit(loser_text1, (700, HEIGHT - 325))
            time_taken = normal_font.render(f'Time Taken:{elapsed_time}seconds',True,white)
            screen.blit(time_taken,(600,HEIGHT-280))
            matched_cards = normal_font.render(f'Cards Matched:{cards_matched}',True,white)
            screen.blit(matched_cards,(600,HEIGHT-240))
            losing_music.play()
            losing_music.fadeout(1000)
            background_music.stop()

        if first_guess:
            piece_text = normal_font.render(f'{spaces[first_guess_num]}',True,blue)
            location = (500+first_guess_num // rows * 75 +18, 80+(first_guess_num - (first_guess_num // rows*rows)) * 65 + 120)
            screen.blit(piece_text,(location))
        
        if second_guess:
            piece_text = normal_font.render(f'{spaces[second_guess_num]}',True,blue)
            location = (500+second_guess_num // rows * 75 +18, 80+(second_guess_num - (second_guess_num // rows*rows)) * 65 + 120)
            screen.blit(piece_text,(location))
        pygame.display.flip()
background_music.stop()
pygame.quit()