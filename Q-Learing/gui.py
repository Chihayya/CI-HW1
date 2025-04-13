import pygame
import time
import pickle
import numpy as np
from playground import Playground
from axis import *

# 載入 Q-table
try:
    with open("q_table.pkl", "rb") as f:
        q_table = pickle.load(f)
        print("✅ 成功載入 Q-table")
except FileNotFoundError:
    print("❌ 找不到 Q-table，請先訓練")
    exit()

# Pygame 初始化
pygame.init()
WIDTH, HEIGHT = 600, 600  # 放大視野來看全圖
SCALE = 5 # 縮小比例，讓地圖更多內容能顯示在畫面中
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Q-learning 自走車 GUI")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
car_path = []

# 顏色
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# 工具函數

def draw_state_info(state):
    text_surface = font.render(f"State: {state}", True, BLACK)
    screen.blit(text_surface, (10, 10))

def draw_position_info(pos_x, pos_y):
    text_surface = font.render(f"Pos: {pos_x, pos_y}", True, BLACK)
    screen.blit(text_surface, (10, 30))

def world_to_screen(p):
    return int(p.x * SCALE + WIDTH / 2), int(HEIGHT / 2 - p.y * SCALE)

def draw_path(path, radius):
    for pos in path:
        draw_circle(pos, radius, GREEN, 1)

def draw_rect(p1, p2):
    x1, y1 = world_to_screen(p1)
    x2, y2 = world_to_screen(p2)

    rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
    pygame.draw.rect(screen, YELLOW, rect)
    

def draw_line(p1, p2, color=GRAY, width=2):
    pygame.draw.line(screen, color, world_to_screen(p1), world_to_screen(p2), width)

def draw_circle(p, radius_in_units, color=BLUE, width=0):
    pixel_radius = int(radius_in_units * SCALE)
    pygame.draw.circle(screen, color, world_to_screen(p), pixel_radius, width)

def discretize_state(state, bins=(20, 20, 20)):
    return tuple(np.digitize(s, np.linspace(0, 100, b)) if s != -1 else 0 for s, b in zip(state, bins))

# GUI 模擬一個 episode
def run_qlearning_gui():
    is_running = True

    while is_running:
        env = Playground()
        state_raw = env.initialize()
        state = discretize_state(state_raw)
        done = False
        step = 0

        while not done and step < 500:
            screen.fill(WHITE)
            car_path.append(env.car.getPosition('center'))

            # 畫邊界與終點
            for wall in env.borders:
                draw_line(wall.start, wall.end, GRAY)
            draw_rect(env.destination[0], env.destination[1])

            # 畫車子與感測器
            draw_path(car_path, env.car.radius)
            draw_circle(env.car.getPosition('center'), env.car.radius, BLUE)

            # draw sensors
            if env.left_sensor_intersect:
                draw_line(env.car.getPosition('left_sensor'), env.left_sensor_intersect[0], RED, 1)
            if env.front_sensor_intersect:
                draw_line(env.car.getPosition('front_sensor'), env.front_sensor_intersect[0], RED, 1)
            if env.right_sensor_intersect:
                draw_line(env.car.getPosition('right_sensor'), env.right_sensor_intersect[0], RED, 1)

            # draw state msg & position msg
            draw_state_info(state_raw)
            draw_position_info(env.car.x, env.car.y)

            # 執行決策
            if state in q_table:
                action = np.argmax(q_table[state])
            else:
                action = np.random.randint(env.n_actions)

            state_raw = env.step(action)
            next_state = discretize_state(state_raw)

            state = next_state
            done = env.done
            step += 1

            pygame.display.flip()
            clock.tick(30)
            time.sleep(0.1)

        # 檢查是否成功到達終點
        car_center = env.car.getPosition("center")
        if car_center.isInRect(env.destination[0], env.destination[1]):
            print("🎉 成功到達終點！")
            is_running = False
        else:
            print("🔁 未到終點，重試...")
            time.sleep(2)

if __name__ == '__main__':
    run_qlearning_gui()
    pygame.quit()