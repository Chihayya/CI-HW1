import numpy as np
import pickle
from playground import Playground
from axis import *

# 超參數
EPISODES = 50000
ALPHA = 0.1  # 學習率
GAMMA = 0.95  # 折扣因子
EPSILON = 0
EPSILON_DECAY = 0.9999
EPSILON_MIN = 0

# 離散化函數
def discretize_state(state, bins=(20, 20, 20)):
    return tuple(np.digitize(s, np.linspace(0, 100, b)) if s != -1 else 0 for s, b in zip(state, bins))

# 初始化
env = Playground()
n_actions = env.n_actions

try:
    with open("q_table.pkl", "rb") as f:
        q_table = pickle.load(f)
        print("✅ 成功載入 Q-table！")
except FileNotFoundError:
    print("⚠️ 找不到 Q-table，將從空的 q_table 開始。")
    q_table = {}

# 建構獎勵因子
first_reward_rect = [Point2D(-3, 19), Point2D(3, 13)]
second_reward_rect = [Point2D(-3, 9), Point2D(3, 7)]
third_reward_rect = [Point2D(21,19), Point2D(27, 13)]
fourth_reward_rect = [Point2D(21,35), Point2D(27,29)]
pass_time = 0

for episode in range(EPISODES):
    state = discretize_state(env.initialize())
    total_reward = 0
    done = False
    steps = 0
    is_first_rewarded = False
    is_second_rewarded = False
    is_third_rewarded = False
    is_fourth_rewarded = False

    while not done and steps < 500:
        # 探索或利用
        if np.random.rand() < EPSILON or state not in q_table:
            action = np.random.randint(0, n_actions)
        else:
            action = np.argmax(q_table[state])

        next_state_raw = env.step(action)
        next_state = discretize_state(next_state_raw)


        if env.done:
            # 判斷是撞牆還是到達終點
            car_center = env.car.getPosition('center')
            done = True
            if car_center.isInRect(env.destination[0], env.destination[1]):
                reward = 10.0  # 成功抵達終點
                pass_time += 1
                # print(f"目前集數: {episode}")
                # print(f"Result: 抵達終點, state: {state}, car_x: {env.car.x}, car_y: {env.car.y}")
            else:
                reward = -1.0  # 撞牆
        else:
            reward = -0.001  # 正常移動中

            if not is_first_rewarded:
                car_center = env.car.getPosition('center')

                if car_center.isInRect(first_reward_rect[0], first_reward_rect[1]):
                    is_first_rewarded = True
                    reward = 3.0
            elif not is_second_rewarded:
                car_center = env.car.getPosition('center')

                if car_center.isInRect(second_reward_rect[0], second_reward_rect[1]):
                    is_second_rewarded = True
                    reward = 3.0
            elif not is_third_rewarded:
                car_center = env.car.getPosition('center')

                if car_center.isInRect(third_reward_rect[0], third_reward_rect[1]):
                    is_third_rewarded = True
                    reward = 3.0
            elif not is_fourth_rewarded:
                car_center = env.car.getPosition('center')

                if car_center.isInRect(fourth_reward_rect[0], fourth_reward_rect[1]):
                    is_fourth_rewarded = True
                    reward = 3.0
                

        total_reward += reward

        # 初始化 Q table 條目
        if state not in q_table:
            q_table[state] = np.zeros(n_actions)
        if next_state not in q_table:
            q_table[next_state] = np.zeros(n_actions)

        # Q-learning 更新
        q_table[state][action] += ALPHA * (reward + GAMMA * np.max(q_table[next_state]) - q_table[state][action])

        state = next_state
        steps += 1
        # print(f"States: [{tuple(int(s) for s in state)}], x:{car_center.x}, y:{car_center.y}")

    EPSILON = max(EPSILON * EPSILON_DECAY, EPSILON_MIN)
    if (episode + 1) % 100 == 0:
        print(f"Episode {episode+1}: Total Reward = {total_reward:.2f}, Epsilon = {EPSILON:.3f}")
        accuracy = pass_time
        print(f"Accuracy: {accuracy}%")
        pass_time = 0


# 儲存 Q-table
with open("q_table.pkl", "wb") as f:
    pickle.dump(q_table, f)
    print("訓練完成")