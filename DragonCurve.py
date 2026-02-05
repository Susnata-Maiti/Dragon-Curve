import pygame
import sys
import math

# Function to generate Dragon Curve sequence
def dragon_curve_sequence(order):
    seq = "F"
    for _ in range(order):
        new_seq = ""
        for c in seq:
            if c == "F":
                new_seq += "F+G"
            elif c == "G":
                new_seq += "F-G"
            else:
                new_seq += c
        seq = new_seq
    return seq

# Function to draw curve step by step
def draw_dragon_curve(screen, seq, length, start_pos, delay):
    x, y = start_pos
    angle = 0
    points = [(x, y)]

    for move in seq:
        if move in ("F", "G"):
            x += length * math.cos(math.radians(angle))
            y += length * math.sin(math.radians(angle))
            new_point = (x, y)
            pygame.draw.line(screen, (0, 255, 255), points[-1], new_point, 2)
            points.append(new_point)
            pygame.display.flip()
            pygame.time.delay(delay)  # slow down drawing
        elif move == "+":
            angle += 90
        elif move == "-":
            angle -= 90

# Function to display text on screen
def draw_text(screen, text, pos, size=36, color=(255, 255, 255)):
    font = pygame.font.Font(None, size)
    surf = font.render(text, True, color)
    screen.blit(surf, pos)

# Main program
def main():
    pygame.init()
    width, height = 1000, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Dragon Curve Fractal (PyGame)")

    input_box = pygame.Rect(width//2 - 100, height//2 - 20, 200, 40)
    color_inactive = (200, 200, 200)
    color_active = (255, 255, 255)
    color = color_inactive
    active = False
    text = ''
    order = None

    clock = pygame.time.Clock()

    # Step 1: Input loop
    while order is None:
        screen.fill((0, 0, 0))
        draw_text(screen, "Enter order of Dragon's Curve and press Enter:", (200, 300), 32)
        txt_surface = pygame.font.Font(None, 36).render(text, True, color)
        width_box = max(200, txt_surface.get_width()+10)
        input_box.w = width_box
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        try:
                            order = int(text)
                        except ValueError:
                            order = 12  # fallback
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        clock.tick(30)

    # Step 2: Draw fractal slowly
    screen.fill((0, 0, 0))
    seq = dragon_curve_sequence(order)
    length = 5  # pixel length of each segment
    start_pos = (width // 2, height // 2)
    draw_dragon_curve(screen, seq, length, start_pos, delay=10)  # delay in ms

    # Keep window open
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
