import pygame
import numpy as np
import time





# ====== Sample Code for Smart Design Technology Blog ======

# Intel Realsense D435 cam has RGB camera with 1920×1080 resolution
# Depth camera is 1280x720
# FOV is limited to 69deg x 42deg (H x V) - the RGB camera FOV

# If you run this on a non-Intel CPU, explore other options for rs.align
# On the NVIDIA Jetson AGX we build the pyrealsense lib with CUDA

import pyrealsense2 as rs
import mediapipe as mp
import cv2
import numpy as np
import datetime as dt

font = cv2.FONT_HERSHEY_SIMPLEX
org = (20, 100)
fontScale = .5
color = (0, 50, 255)
thickness = 1

# ====== Realsense ======
realsense_ctx = rs.context()
connected_devices = []  # List of serial numbers for present cameras
for i in range(len(realsense_ctx.devices)):
    detected_camera = realsense_ctx.devices[i].get_info(rs.camera_info.serial_number)
    print(f"{detected_camera}")
    connected_devices.append(detected_camera)
device = connected_devices[0]  # In this example we are only using one camera
pipeline = rs.pipeline()
config = rs.config()
background_removed_color = 153  # Grey

# ====== Mediapipe ======
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# ====== Enable Streams ======
config.enable_device(device)

# # For worse FPS, but better resolution:
# stream_res_x = 1280
# stream_res_y = 720
# # For better FPS. but worse resolution:
stream_res_x = 640
stream_res_y = 480

stream_fps = 15

config.enable_stream(rs.stream.depth, stream_res_x, stream_res_y, rs.format.z16, stream_fps)
config.enable_stream(rs.stream.color, stream_res_x, stream_res_y, rs.format.bgr8, stream_fps)
profile = pipeline.start(config)

align_to = rs.stream.color
align = rs.align(align_to)

# ====== Get depth Scale ======
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print(f"\tDepth Scale for Camera SN {device} is: {depth_scale}")

# ====== Set clipping distance ======
clipping_distance_in_meters = 0.7
clipping_distance = clipping_distance_in_meters / depth_scale
print(f"\tConfiguration Successful for SN {device}")

# ====== Get and process images ======
print(f"Starting to capture images on SN: {device}")








def draw_board():
    screen.fill(WHITE)
    # Draw horizontal lines
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, BLACK, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
    # Draw vertical lines
    for i in range(1, BOARD_COLS):
        pygame.draw.line(screen, BLACK, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_symbols():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3, LINE_WIDTH)
            elif board[row][col] == -1:
                pygame.draw.line(screen, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), LINE_WIDTH)
                pygame.draw.line(screen, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4),
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), LINE_WIDTH)

# def get_row_col_from_mouse(pos):
#     x, y = pos
#     row = y // SQUARE_SIZE
#     col = x // SQUARE_SIZE
#     return row, col



def is_board_full():
    return not any(0 in row for row in board)

def is_winner(player):
    # Check rows
    for row in board:
        if all(cell == player for cell in row):
            return True
    # Check columns
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            return True
    # Check diagonals
    if all(board[i][i] == player for i in range(BOARD_ROWS)) or \
       all(board[i][BOARD_COLS - 1 - i] == player for i in range(BOARD_ROWS)):
        return True
    return False











def Coordinate_trnsfrm(coordinates):
    X, Y, Z = coordinates

    Row, Col = -1, -1


    if Y > 0.80:
        # 1
        if 0.35 < Z < 0.43 and 0.60 < X < 0.70:
            Row, Col = 0, 0
        # 4
        elif 0.35 < Z < 0.43 and 0.42 < X < 0.60:
            Row, Col = 1, 0
        # 7
        elif 0.35 < Z < 0.43 and 0.25 < X < 0.40:
            Row, Col = 2, 0
    if Y > 0.75:
        # 2
        if 0.45 < Z < 0.50 and 0.60 < X < 0.70:
            Row, Col = 0, 1
        # 5
        elif 0.45 < Z < 0.50 and 0.44 < X < 0.56:
            Row, Col = 1, 1
        # 8
        elif 0.45 < Z < 0.50 and 0.27 < X < 0.40:
            Row, Col = 2, 1

    if Y > 0.70:
        # 3
        if 0.50 < Z < 0.60 and 0.58 < X < 0.70:
            Row, Col = 0, 2
        # 6
        elif 0.50 < Z < 0.60 and 0.45 < X < 0.55:
            Row, Col = 1, 2
        # 9
        elif 0.50 < Z < 0.60 and 0.25 < X < 0.45:
            Row, Col = 2, 2


    return Row, Col

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 10
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
board = np.zeros((BOARD_ROWS, BOARD_COLS))

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

game_over = False

current_player = 1

while not game_over:
    start_time = dt.datetime.today().timestamp()

    # Get and align frames
    frames = pipeline.wait_for_frames()
    aligned_frames = align.process(frames)
    aligned_depth_frame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame()



    # Process images
    depth_image = np.asanyarray(aligned_depth_frame.get_data())
    depth_image_flipped = cv2.flip(depth_image, 1)
    color_image = np.asanyarray(color_frame.get_data())

    depth_image_3d = np.dstack(
        (depth_image, depth_image, depth_image))  # Depth image is 1 channel, while color image is 3
    background_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0),
                                  background_removed_color, color_image)

    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

    images = cv2.flip(background_removed, 1)
    color_image = cv2.flip(color_image, 1)
    color_images_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

    # Process hands
    results = hands.process(color_images_rgb)
    clock = pygame.time.Clock()
    if results.multi_hand_landmarks:
        number_of_hands = len(results.multi_hand_landmarks)
        i = 0
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(images, handLms, mpHands.HAND_CONNECTIONS)
            org2 = (20, org[1] + (20 * (i + 1)))
            hand_side_classification_list = results.multi_handedness[i]
            hand_side = hand_side_classification_list.classification[0].label
            middle_finger_knuckle = results.multi_hand_landmarks[i].landmark[8]
            x = int(middle_finger_knuckle.x * len(depth_image_flipped[0]))
            y = int(middle_finger_knuckle.y * len(depth_image_flipped))
            if x >= len(depth_image_flipped[0]):
                x = len(depth_image_flipped[0]) - 1
            if y >= len(depth_image_flipped):
                y = len(depth_image_flipped) - 1
            mfk_distance = depth_image_flipped[y, x] * depth_scale  # meters
            mfk_distance_feet = mfk_distance * 3.281  # feet

            coordinates = [middle_finger_knuckle.x,middle_finger_knuckle.y,mfk_distance];



            row, col = Coordinate_trnsfrm(coordinates)
            if board[row][col] == 0:
                board[row][col] = current_player
                if is_winner(current_player):
                    print(f"Player {current_player} wins!")
                    game_over = True
                elif is_board_full():
                    print("It's a tie!")
                    game_over = True
                else:
                    current_player = -current_player

    draw_board()
    draw_symbols()
    pygame.display.flip()
    clock.tick(10)


    # Display FPS
    time_diff = dt.datetime.today().timestamp() - start_time
    fps = int(1 / time_diff)
    org3 = (20, org[1] + 60)
    images = cv2.putText(images, f"FPS: {fps}", org3, font, fontScale, color, thickness, cv2.LINE_AA)

    name_of_window = 'SN: ' + str(device)

    # Display images
    cv2.namedWindow(name_of_window, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(name_of_window, images)
    key = cv2.waitKey(1)
    # Press esc or 'q' to close the image window



# Create Tic-Tac-Toe board






# Main game loop


# while not game_over:
#     for event in pygame.event.get():
#         GetHands()
#         if event.type == pygame.QUIT:
#             game_over = True
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             if pygame.mouse.get_pressed()[0]:
#                 mouse_pos = pygame.mouse.get_pos()
#                 row, col = get_row_col_from_mouse(mouse_pos)
#                 if board[row][col] == 0:
#                     board[row][col] = current_player
#                     if is_winner(current_player):
#                         print(f"Player {current_player} wins!")
#                         game_over = True
#                     elif is_board_full():
#                         print("It's a tie!")
#                         game_over = True
#                     else:
#                         current_player = -current_player


print(f"Application Closing")
pipeline.stop()
print(f"Application Closed.")



pygame.quit()
