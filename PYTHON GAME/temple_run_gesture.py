import cv2
import mediapipe as mp
import numpy as np
import pygame
import random
import time
import sys

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# Initialize Pygame for the game
pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
SKY_BLUE = (135, 206, 235)
GROUND_COLOR = (139, 69, 19)
PLAYER_COLOR = (52, 152, 219)
OBSTACLE_COLOR = (139, 69, 19)
COIN_COLOR = (255, 215, 0)
TEXT_COLOR = (255, 255, 255)

# Game variables
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 150
player_lane = 1  # 0: left, 1: center, 2: right
player_state = "running"  # running, jumping, rolling
player_width = 40
player_height = 80

lane_positions = [SCREEN_WIDTH // 4, SCREEN_WIDTH // 2, 3 * SCREEN_WIDTH // 4]

obstacles = []
coins = []
score = 0
game_speed = 3
is_playing = False
jump_count = 0
roll_count = 0

# Gesture variables
current_gesture = "none"
last_gesture_time = 0
gesture_cooldown = 0.5  # seconds

# Initialize Pygame screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gesture-Controlled Temple Run")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont('Arial', 30)
large_font = pygame.font.SysFont('Arial', 50)

# Game functions
def init_game():
    global player_x, player_y, player_lane, player_state, obstacles, coins, score, game_speed, is_playing
    player_x = SCREEN_WIDTH // 2
    player_y = SCREEN_HEIGHT - 150
    player_lane = 1
    player_state = "running"
    obstacles = []
    coins = []
    score = 0
    game_speed = 3
    is_playing = True

def draw_player():
    # Body
    pygame.draw.rect(screen, PLAYER_COLOR, (player_x - player_width//2, player_y - player_height, player_width, player_height))
    
    # Head
    pygame.draw.circle(screen, (241, 196, 15), (player_x, player_y - player_height - 10), 20)
    
    # Animation based on state
    if player_state == "jumping":
        pygame.draw.rect(screen, PLAYER_COLOR, (player_x - player_width//2, player_y - player_height, player_width, player_height))
    elif player_state == "rolling":
        pygame.draw.ellipse(screen, PLAYER_COLOR, (player_x - player_width//2, player_y - player_height//2, player_width, player_height//2))

def draw_background():
    # Sky
    screen.fill(SKY_BLUE)
    
    # Mountains
    pygame.draw.polygon(screen, (44, 62, 80), [
        (0, SCREEN_HEIGHT - 100),
        (200, SCREEN_HEIGHT - 300),
        (400, SCREEN_HEIGHT - 100)
    ])
    pygame.draw.polygon(screen, (44, 62, 80), [
        (300, SCREEN_HEIGHT - 100),
        (500, SCREEN_HEIGHT - 300),
        (700, SCREEN_HEIGHT - 100)
    ])
    
    # Ground
    pygame.draw.rect(screen, GROUND_COLOR, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
    
    # Path (3 lanes)
    lane_width = SCREEN_WIDTH // 4
    pygame.draw.rect(screen, (141, 110, 99), (lane_positions[0] - lane_width//2, SCREEN_HEIGHT - 100, lane_width, 20))
    pygame.draw.rect(screen, (141, 110, 99), (lane_positions[1] - lane_width//2, SCREEN_HEIGHT - 100, lane_width, 20))
    pygame.draw.rect(screen, (141, 110, 99), (lane_positions[2] - lane_width//2, SCREEN_HEIGHT - 100, lane_width, 20))

def generate_obstacle():
    if random.random() < 0.02:  # 2% chance per frame
        lane = random.randint(0, 2)
        obstacle_type = random.choice(["low", "high"])
        y_pos = SCREEN_HEIGHT - 120 if obstacle_type == "low" else SCREEN_HEIGHT - 180
        obstacles.append({
            "x": SCREEN_WIDTH,
            "y": y_pos,
            "lane": lane,
            "width": 50,
            "height": 60 if obstacle_type == "low" else 30,
            "type": obstacle_type
        })

def generate_coin():
    if random.random() < 0.03:  # 3% chance per frame
        lane = random.randint(0, 2)
        y_pos = random.choice([SCREEN_HEIGHT - 180, SCREEN_HEIGHT - 150])
        coins.append({
            "x": SCREEN_WIDTH,
            "y": y_pos,
            "lane": lane,
            "width": 30,
            "height": 30,
            "collected": False
        })

def update_obstacles():
    global obstacles, score
    for obstacle in obstacles[:]:
        obstacle["x"] -= game_speed
        
        # Remove off-screen obstacles
        if obstacle["x"] + obstacle["width"] < 0:
            obstacles.remove(obstacle)
            continue
        
        # Draw obstacle
        pygame.draw.rect(screen, OBSTACLE_COLOR, 
                         (obstacle["x"], obstacle["y"], obstacle["width"], obstacle["height"]))
        
        # Collision detection
        if (player_lane == obstacle["lane"] and 
            player_x - player_width//2 < obstacle["x"] + obstacle["width"] and
            player_x + player_width//2 > obstacle["x"]):
            
            if (player_state == "running" or 
                (player_state == "jumping" and obstacle["type"] == "low") or
                (player_state == "rolling" and obstacle["type"] == "high")):
                return False
    
    return True

def update_coins():
    global coins, score
    for coin in coins[:]:
        coin["x"] -= game_speed
        
        # Remove off-screen coins
        if coin["x"] + coin["width"] < 0:
            coins.remove(coin)
            continue
        
        # Draw coin if not collected
        if not coin["collected"]:
            pygame.draw.circle(screen, COIN_COLOR, 
                              (coin["x"] + coin["width"]//2, coin["y"] + coin["height"]//2), 
                              coin["width"]//2)
            
            # Collection detection
            if (player_lane == coin["lane"] and 
                player_x - player_width//2 < coin["x"] + coin["width"] and
                player_x + player_width//2 > coin["x"] and
                player_y - player_height < coin["y"] + coin["height"] and
                player_y > coin["y"]):
                
                coin["collected"] = True
                score += 10

def update_player():
    global player_state, player_y, jump_count, roll_count
    
    # Update player position based on lane
    target_x = lane_positions[player_lane]
    player_x = player_x * 0.9 + target_x * 0.1  # Smooth movement
    
    # Update player state
    if player_state == "jumping":
        jump_count += 1
        jump_height = abs(np.sin(jump_count * 0.1) * 100)
        player_y = SCREEN_HEIGHT - 150 - jump_height
        
        if jump_count > np.pi / 0.1:  # At the top of sine wave
            player_state = "running"
            jump_count = 0
            player_y = SCREEN_HEIGHT - 150
    
    elif player_state == "rolling":
        roll_count += 1
        player_y = SCREEN_HEIGHT - 100
        
        if roll_count > 30:  # Roll duration
            player_state = "running"
            roll_count = 0
            player_y = SCREEN_HEIGHT - 150
    
    return player_x

def draw_score():
    score_text = font.render(f"Score: {int(score)}", True, TEXT_COLOR)
    screen.blit(score_text, (20, 20))

def draw_gesture_display():
    gesture_text = font.render(f"Gesture: {current_gesture}", True, TEXT_COLOR)
    screen.blit(gesture_text, (SCREEN_WIDTH - 200, 20))

def game_over_screen():
    screen.fill((0, 0, 0))
    game_over_text = large_font.render("GAME OVER", True, TEXT_COLOR)
    final_score_text = font.render(f"Final Score: {int(score)}", True, TEXT_COLOR)
    restart_text = font.render("Press SPACE to restart", True, TEXT_COLOR)
    
    screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 100))
    screen.blit(final_score_text, (SCREEN_WIDTH//2 - final_score_text.get_width()//2, SCREEN_HEIGHT//2))
    screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 50))

def detect_gesture(hand_landmarks):
    # Get key points
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    
    # Calculate distances
    thumb_index_dist = np.sqrt((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)
    index_middle_dist = np.sqrt((index_tip.x - middle_tip.x)**2 + (index_tip.y - middle_tip.y)**2)
    
    # Check for closed fist (thumb over fingers)
    if thumb_tip.y < index_tip.y and thumb_tip.y < middle_tip.y:
        # Determine if hand is on left or right side of screen
        if wrist.x < 0.4:  # Left side
            return "left"
        elif wrist.x > 0.6:  # Right side
            return "right"
    
    # Check for open palm (fingers extended)
    if (index_tip.y < wrist.y and middle_tip.y < wrist.y and 
        ring_tip.y < wrist.y and pinky_tip.y < wrist.y):
        return "jump"
    
    # Check for peace sign (index and middle extended, others folded)
    if (index_tip.y < wrist.y and middle_tip.y < wrist.y and 
        ring_tip.y > wrist.y and pinky_tip.y > wrist.y and
        thumb_index_dist > 0.1):
        return "roll"
    
    return "none"

def process_gesture(gesture):
    global player_state, player_lane, current_gesture, last_gesture_time
    
    current_time = time.time()
    if current_time - last_gesture_time < gesture_cooldown:
        return
    
    current_gesture = gesture
    
    if gesture == "left" and player_lane > 0:
        player_lane -= 1
        last_gesture_time = current_time
    elif gesture == "right" and player_lane < 2:
        player_lane += 1
        last_gesture_time = current_time
    elif gesture == "jump" and player_state == "running":
        player_state = "jumping"
        last_gesture_time = current_time
    elif gesture == "roll" and player_state == "running":
        player_state = "rolling"
        last_gesture_time = current_time

# Main game loop
def main():
    global is_playing, score, game_speed, current_gesture
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    init_game()
    
    while True:
        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_playing:
                    init_game()
        
        # Read webcam frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process frame with MediaPipe Hands
        results = hands.process(rgb_frame)
        
        # Detect gesture
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                gesture = detect_gesture(hand_landmarks)
                process_gesture(gesture)
                
                # Draw hand landmarks
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2))
        else:
            current_gesture = "none"
        
        # Display webcam feed with gesture info
        cv2.putText(frame, f"Gesture: {current_gesture}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Hand Gesture Detection', frame)
        
        # Game logic
        if is_playing:
            draw_background()
            generate_obstacle()
            generate_coin()
            
            if not update_obstacles():
                is_playing = False
            
            update_coins()
            player_x = update_player()
            draw_player()
            draw_score()
            draw_gesture_display()
            
            # Increase difficulty
            score += 0.1
            game_speed = 3 + int(score / 1000)
        else:
            game_over_screen()
        
        pygame.display.flip()
        clock.tick(60)
        
        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()

if __name__ == "__main__":
    main()
