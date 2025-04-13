import math as m
import random as r
from car import *

class Playground():
    def __init__(self):
        """
        A constructor of a playground for simulating car movement

        members:
            path_line_filename: 路徑座標檔案
            borders: 模擬環境的邊界
            destination: 模擬環境的終點(長方形)
            start: 模擬環境的起點(線)
            car: 模擬自走車
            car_init_pos: 模擬自走車初始位置
            car_init_angle: 模擬自走車初始角度
            front_sensor_intersect: 前感測器與線段之交點
            left_sensor_intersect: 左感測器與線段之交點
            right_sensor_intersect: 右感測器與線段之交點
            done: 模擬過程是否結束
            isHitBorder: 模擬過程是否撞牆

        """

        self.path_line_filename = "軌道座標點.txt"
        self.borders = [] 
        self.destination = [] # [0] => 左上角座標, [1] => 右下角座標
        self.start = Line2D(Point2D(-6, 0), Point2D(6, 0))
        self.car = Car()
        self.car_init_pos = None
        self.car_init_angle = None
        self.front_sensor_intersect = []
        self.left_sensor_intersect = []
        self.right_sensor_intersect = []
        self.done = False
        self.isHitBorder = False
        self.readPathFiles()
        self.initialize()

    def initialize(self):
        self.done = False
        self.isHitBorder = False
        self.car.reset()
        
        if self.car_init_pos != None:
            self.car.setCarPosition(self.car_init_pos)

        if self.car_init_angle != None:
            self.car.setCarAngle(self.car_init_angle)

        self.checkDone()
        self.adjustSensor()
        return self.state

        
    def readPathFiles(self):
        """
        A method that reads a outside file to construct a simulation environment
        """

        try:
            with open(self.path_line_filename, 'r', encoding='UTF-8') as f:
                lines = f.readlines()
                
                self.borders.clear()
                self.destination.clear()


                # get init pos and angle
                pos_angle = [float(v) for v in lines[0].split(',')]
                self.car_init_pos = Point2D(pos_angle[0], pos_angle[1])
                self.car_init_angle = pos_angle[2]

                # get destination field
                dest_arr1 = [float(v) for v in lines[1].split(',')]
                dest_arr2 = [float(v) for v in lines[2].split(',')]
                dest_left_up_point = Point2D(dest_arr1[0], dest_arr1[1])
                dest_right_down_point = Point2D(dest_arr2[0], dest_arr2[1])
                self.destination.append(dest_left_up_point)
                self.destination.append(dest_right_down_point)

                # get border lines
                for i in range(3, len(lines) - 1):  # 從第4行開始，一直到倒數第2行
                    curr_line = lines[i]
                    next_line = lines[i + 1]

                    p_arr = [float(v) for v in curr_line.split(',')]
                    np_arr = [float(v) for v in next_line.split(',')]

                    p1 = Point2D(p_arr[0], p_arr[1])
                    p2 = Point2D(np_arr[0], np_arr[1])

                    self.borders.append(Line2D(p1, p2))

        except Exception:
            print("無法開啟座標檔案!")

    @property
    def n_actions(self):
        """
        A method to return a action about steering wheel's angle
        which action is [0, theta_range-1]

        """

        theta_range = self.car.theta_max - self.car.theta_min
        return theta_range-1
    
    @property
    def state(self):
        """
        A method that return the state of the sensors
        determined by if there is a intersect point or not

        Returns:
            state: [front_dist, right_dist, left_dist] => 車輛中心點與感測器偵測之交點的距離
        """
        if len(self.front_sensor_intersect) == 0:
            front_dist = -1
        else:
            front_dist = self.car.getPosition('center').distanceToPoint(self.front_sensor_intersect[0])
        
        if len(self.left_sensor_intersect) == 0:
            left_dist = -1
        else:
            left_dist = self.car.getPosition('center').distanceToPoint(self.left_sensor_intersect[0])
            
        if len(self.right_sensor_intersect) == 0:
            right_dist = -1
        else:
            right_dist = self.car.getPosition('center').distanceToPoint(self.right_sensor_intersect[0])

        state = [front_dist, right_dist, left_dist]

        return state
    
    def checkDone(self):
        """
        A method to determine that the simulation is over or not
        
        the condition is 2 type
        1. the car is at the destination field
        2. the car is hit the borders

        """

        if self.done:
            return self.done
        
        done = False

        # get the vehicle's data
        car_center_position = self.car.getPosition('center')

        # 1. the car is in the destination field
        isAtDestination = car_center_position.isInRect(self.destination[0], self.destination[1])
        
        if isAtDestination:
            done = True

        # 2. the car is hit the border
        for border in self.borders:
            distance_center_to_line = car_center_position.distanceToLine(border)

            # 若距離小於車輛半徑，檢查碰撞點是否屬於 border 的向量範圍內
            if distance_center_to_line < self.car.radius:

                # 求出向量後假設碰撞線之方程式，藉由方程式推出碰撞點再進行範圍檢測
                if border.slope == 0: # border 為 horizontal line, collided_line 即為 vertical line
                    slope_collided_line = None
                    collided_line = Line2D(car_center_position, Point2D(car_center_position.x, car_center_position.y+1))
                elif border.slope == None: # 相反
                    slope_collided_line = 0
                    collided_line = Line2D(car_center_position, Point2D(car_center_position.x+1, car_center_position.y))
                else:
                    slope_collided_line = -1 / border.slope
                    collided_line_vector_x = 1
                    collided_line_vector_y = slope_collided_line - (slope_collided_line * car_center_position.x) + car_center_position.y
                    collided_line = Line2D(car_center_position, Point2D(car_center_position.x + collided_line_vector_x, car_center_position.y + collided_line_vector_y))

                is_collided, collided_point = border.lineCollidedCheck(collided_line)

                is_point_in_line = border.pointInLine(collided_point)

                if is_point_in_line:
                    done = True
                    self.isHitBorder = True
                    break

        self.done = done
        return done
    
    def adjustSensor(self):
        """
        A method to adjust the sensors' states

        藉由車輛前, 左, 右感測器的座標與車輛中心的座標形成的線段方程式
        利用線段方程式去檢測交點距離
        """

        car_center_position = self.car.getPosition('center')
        car_front_sensor_position = self.car.getPosition('front_sensor')
        car_left_sensor_position = self.car.getPosition('left_sensor')
        car_right_sensor_position = self.car.getPosition('right_sensor')

        front_vector = Line2D(car_center_position, car_front_sensor_position)
        left_vector = Line2D(car_center_position, car_left_sensor_position)
        right_vector = Line2D(car_center_position, car_right_sensor_position)

        # 檢測每道邊界與 sensors 的交點
        for border in self.borders:

            # 計算碰撞點
            is_front_sensor_collided, front_collided_point = front_vector.lineCollidedCheck(border)
            is_left_sensor_collided, left_collided_point = left_vector.lineCollidedCheck(border)
            is_right_sensor_collided, right_collided_point = right_vector.lineCollidedCheck(border)

            # 做出碰撞線
            front_collided_line = Line2D(car_center_position, front_collided_point)
            left_collided_line = Line2D(car_center_position, left_collided_point)
            right_collided_line = Line2D(car_center_position, right_collided_point)


            # 如果碰撞點在線向量裡面才加入 and 兩條線夾角為0(相同向量)
            if is_front_sensor_collided and border.pointInLine(front_collided_point)  :
                v_fs_x = front_vector.end.x - front_vector.start.x
                v_fs_y = front_vector.end.y - front_vector.start.y
                v_cs_x = front_collided_line.end.x - front_collided_line.start.x
                v_cs_y = front_collided_line.end.y - front_collided_line.start.y
                if (v_fs_x * v_cs_x + v_fs_y * v_cs_y) > 0 :
                    self.front_sensor_intersect.append(front_collided_point)
            
            if is_left_sensor_collided and border.pointInLine(left_collided_point) :
                v_ls_x = left_vector.end.x - left_vector.start.x
                v_ls_y = left_vector.end.y - left_vector.start.y
                v_cs_x = left_collided_line.end.x - left_collided_line.start.x
                v_cs_y = left_collided_line.end.y - left_collided_line.start.y
                if (v_ls_x * v_cs_x + v_ls_y * v_cs_y) > 0 :
                    self.left_sensor_intersect.append(left_collided_point)
                
            
            if is_right_sensor_collided and border.pointInLine(right_collided_point) :
                v_rs_x = right_vector.end.x - right_vector.start.x
                v_rs_y = right_vector.end.y - right_vector.start.y
                v_cs_x = right_collided_line.end.x - right_collided_line.start.x
                v_cs_y = right_collided_line.end.y - right_collided_line.start.y
                if (v_rs_x * v_cs_x + v_rs_y * v_cs_y) > 0 :
                    self.right_sensor_intersect.append(right_collided_point)
        
        # 將測得的交點依照與 sensor 的距離做排序
        self.front_sensor_intersect.sort(
            key=lambda p: p.distanceToPoint(car_center_position)
        )
        self.left_sensor_intersect.sort(
            key=lambda p: p.distanceToPoint(car_center_position)
        )
        self.right_sensor_intersect.sort(
            key=lambda p: p.distanceToPoint(car_center_position)
        )
        
    def clearSensor(self):
        self.front_sensor_intersect.clear()
        self.left_sensor_intersect.clear()
        self.right_sensor_intersect.clear()
    
    def calculate_SteeringWheelAngle(self, random_input_action):
        new_theta = self.car.theta_min + random_input_action*(self.car.theta_max - self.car.theta_min) / (self.n_actions-1)

        return new_theta
    
    def step(self, action=None):
        """
        A method that set the environment to next frame

        """

        if action:
            new_theta = self.calculate_SteeringWheelAngle(action)
            self.car.setThetaAngle(new_theta)

        if self.done and not self.isHitBorder:
            return self.state
        else:
            self.clearSensor()
            self.car.tick()
            self.checkDone()
            self.adjustSensor()
            return self.state