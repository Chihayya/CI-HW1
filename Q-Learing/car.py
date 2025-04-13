import math as m
import random as r
from axis import *

class Car():
    """
    A class object that describes a car

    """
    def __init__(self):
        """
        A constructor of a car object which shape is a circle

        members:
            diameter: default is 6
            radius: half of diameter
            phi: 模型車的車頭方向, [-90°, 270°]
            phi_max: 270°
            phi_min: -90°
            theta: 方向盤的轉動角度, [-40°, 40°]
            theta_max: 40°
            theta_min: -40°
            xini_max: 4.5
            xini_min: -4.5
            x: default is 0, [-4.5, 4.5] => 隨機生成方向能更好的泛化模型
            y: default is 0
        """
        self.diameter = 6
        self.radius = self.diameter // 2
        self.phi = 0 # Car head angle
        self.phi_max = 270
        self.phi_min = -90
        self.theta = 0 # Steering Wheel angle
        self.theta_max = 40
        self.theta_min = -40
        self.xini_max = 4.5
        self.xini_min = -4.5
        self.x = 0
        self.y = 0

    def reset(self):
        self.phi = 90 # 預設車頭方向永遠朝前
        self.theta = 0

        xini_range = (self.xini_max - self.xini_min - self.diameter)
        self.x = r.uniform(-1, 1)*xini_range # initialize x position at [-3, 3]
        self.y = 0

    def setThetaAngle(self, input_theta):
        if self.theta_min <= input_theta and input_theta <= self.theta_max:
            self.theta = input_theta
        elif input_theta < self.theta_min: # 若方向盤角度小於最低角度，強制打回最低角度
            self.theta = self.theta_min
        elif input_theta > self.theta_max:
            self.theta = self.theta_max
             
    def setCarPosition(self, input_position: Point2D):
        self.x = input_position.x
        self.y = input_position.y
    
    def getPosition(self, input_obj='center'):
        """
        A method that can get the state of the object of the car

        Args:
            input_obj: the object of the car
        
        Returns:
            each object's position
        """
        base = Point2D(self.x, self.y)
        
        if input_obj == 'left_sensor': 
            angle = (self.phi + 45) % 360
            offset = Point2D(self.radius, 0).rotate(angle)
            return base + offset

        elif input_obj == 'right_sensor':
            angle = (self.phi - 45) % 360
            offset = Point2D(self.radius, 0).rotate(angle)
            return base + offset

        elif input_obj == 'front_sensor':
            angle = self.phi % 360
            offset = Point2D(self.radius, 0).rotate(angle)
            return base + offset

        elif input_obj == 'center':
            return base
        
        else:
            raise ValueError(f"Invalid input_obj: {input_obj}")
        
    def getCarWheelPosition(self):
        """
        A method that calculates the global position of the front wheel.

        Returns:
            Point2D: the front wheel's position based on car's current pose.
        """

        wheel_global_angle = self.phi - self.theta  # 車身角度 - 方向盤角度 = 車輪角度
        base = Point2D(self.x, self.y)
        offset = Point2D(self.radius, 0).rotate(wheel_global_angle)  # 向前半徑長，並依車輪角度旋轉

        return base + offset
    
    def setCarAngle(self, input_phi):
        """
        A method that can set the car head angle(phi)

        Args:
            input_phi: input angle

        """
        car_angle = input_phi % 360

        if car_angle > 270:
            car_angle -= 360 # [-90, 270]
        
        self.phi = input_phi

    def tick(self):
        """
        A method that represents the next action of the car (t -> t+1)

        """

        car_rad = self.phi/180*m.pi # 車頭方向之弳度
        steering_wheel_rad = self.theta/180*m.pi # 方向盤方向之弳度

        # delta x = cos(φ+θ) + sin(θ)*sin(φ)
        # delta y = sin(φ+θ) - sin(θ)*cos(φ)
        new_x = m.cos(car_rad+steering_wheel_rad) + m.sin(steering_wheel_rad)*m.sin(car_rad) + self.x
        new_y = m.sin(car_rad+steering_wheel_rad) - m.sin(steering_wheel_rad)*m.cos(car_rad) + self.y
        new_phi = self.phi - ((m.asin(2*m.sin(steering_wheel_rad)/self.diameter)) / m.pi * 180)

        self.setCarPosition(Point2D(new_x, new_y))
        self.setCarAngle(new_phi)
