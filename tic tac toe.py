import pygame
import sys

pygame.init()


WIDTH, HEIGHT = 300, 400  
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (128, 128, 128)  
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)


font = pygame.font.Font(None, 40)


board = [[None]*BOARD_COLS for _ in range(BOARD_ROWS)]
player = 'X'
game_over = False
difficulty = None


def draw_lines():
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT - 100), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT - 100), LINE_WIDTH)


def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)

  
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        pygame.draw.line(screen, RED, (SPACE, SPACE), (WIDTH - SPACE, HEIGHT - 100 - SPACE), LINE_WIDTH)

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        pygame.draw.line(screen, RED, (WIDTH - SPACE, SPACE), (SPACE, HEIGHT - 100 - SPACE), LINE_WIDTH)

    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            pygame.draw.line(screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, 0), (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - 100), LINE_WIDTH)
            break

    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            pygame.draw.line(screen, RED, (0, row * SQUARE_SIZE + SQUARE_SIZE // 2), (WIDTH, row * SQUARE_SIZE + SQUARE_SIZE // 2), LINE_WIDTH)
            break


def mark_square(row, col, player):
    board[row][col] = player


def available_square(row, col):
    return board[row][col] is None


def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                return False
    return True


def check_winner(player):
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True

    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] == player:
            return True

    if board[2][0] == board[1][1] == board[0][2] == player:
        return True

    if board[0][0] == board[1][1] == board[2][2] == player:
        return True

    return False


def display_message(message):
    text = font.render(message, True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 80))


def restart():
    global game_over
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = None
    game_over = False


def ai_move():
    global difficulty

    if difficulty == 'easy':
        depth = 1
    elif difficulty == 'medium':
        depth = 3
    elif difficulty == 'hard':
        depth = 5

    best_score = -float('inf')
    best_move = None

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                board[row][col] = 'O'
                score = minimax(board, 0, False, depth)
                board[row][col] = None
                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    return best_move

def minimax(board, depth, is_maximizing, max_depth):
    if check_winner('O'):
        return 1
    elif check_winner('X'):
        return -1
    elif is_board_full():
        return 0

    if depth >= max_depth:
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] is None:
                    board[row][col] = 'O'
                    score = minimax(board, depth + 1, False, max_depth)
                    board[row][col] = None
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] is None:
                    board[row][col] = 'X'
                    score = minimax(board, depth + 1, True, max_depth)
                    board[row][col] = None
                    best_score = min(score, best_score)
        return best_score


def select_difficulty():
    global difficulty
    while True:
        screen.fill(BG_COLOR)
        
        display_message("Select Difficulty:")
        easy_text = font.render("Easy", True, WHITE)
        medium_text = font.render("Medium", True, WHITE)
        hard_text = font.render("Hard", True, WHITE)

        screen.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(medium_text, (WIDTH // 2 - medium_text.get_width() // 2, HEIGHT // 2))
        screen.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                if (WIDTH // 2 - easy_text.get_width() // 2 <= mouseX <= WIDTH // 2 + easy_text.get_width() // 2) and (HEIGHT // 2 - 50 <= mouseY <= HEIGHT // 2 - 50 + easy_text.get_height()):
                    difficulty = 'easy'
                    restart()
                    main_game_loop()
                elif (WIDTH // 2 - medium_text.get_width() // 2 <= mouseX <= WIDTH // 2 + medium_text.get_width() // 2) and (HEIGHT // 2 <= mouseY <= HEIGHT // 2 + medium_text.get_height()):
                    difficulty = 'medium'
                    restart()
                    main_game_loop()
                elif (WIDTH // 2 - hard_text.get_width() // 2 <= mouseX <= WIDTH // 2 + hard_text.get_width() // 2) and (HEIGHT // 2 + 50 <= mouseY <= HEIGHT // 2 + 50 + hard_text.get_height()):
                    difficulty = 'hard'
                    restart()
                    main_game_loop()
def main_game_loop():
    global player, game_over

    draw_lines()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player == 'X':
                mouseX = event.pos[0]
                mouseY = event.pos[1]

                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE

                if available_square(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, player)
                    if check_winner(player):
                        game_over = True
                        display_message(f'Player {player} wins!')
                    elif is_board_full():
                        game_over = True
                        display_message('It\'s a draw!')
                    player = 'O'
                    draw_figures()

            if not game_over and player == 'O':
                row, col = ai_move()
                mark_square(row, col, player)
                if check_winner(player):
                    game_over = True
                    display_message(f'Player {player} wins!')
                elif is_board_full():
                    game_over = True
                    display_message('It\'s a draw!')
                player = 'X'
                draw_figures()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()
                    player = 'X'
                    game_over = False
                elif event.key == pygame.K_b:
                    select_difficulty() 

            
            draw_button("Back to Menu", WIDTH // 2 - 100, HEIGHT - 50, 200, 40, select_difficulty)

        pygame.display.update()

def draw_button(text, x, y, width, height, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, WHITE, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, BLACK, (x, y, width, height))

    text_surface = font.render(text, True, BLACK if (x < mouse[0] < x + width and y < mouse[1] < y + height) else WHITE)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)


select_difficulty()
