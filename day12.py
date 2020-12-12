
from enum import Enum
from math import sin, cos, atan2, sqrt
from math import radians as rad
from math import degrees as deg

class navigation(Enum):
    north   = "N"
    south   = "S"
    east    = "E"
    west    = "W"
    left    = "L"
    right   = "R"
    forward = "F"

class instruction:
    def __init__(self, nav: navigation, val: int):
        self.nav = nav
        self.val = val
    
    def __repr__(self):
        return self.nav.value + str(self.val)

class vec:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"
    
    __repr__ = __str__
    
    def __add__(self, other):
        return vec(self.x + other.x, self.y + other.y)
    
    def __ladd__(self, other):
        self = self + other
    
    def __mul__(self, a):
        return vec(self.x * a, self.y * a)

    def __lmul__(self, a):
        self = self * a

    def __rmul__(self, a):
        return self * a

    def __neg__(self):
        return -1*self

    def __abs__(self):
        return sqrt(self.x**2 + self.y**2)
    
    def angle(self):
        return deg(atan2(self.y, self.x))
    
    def rotate(self, angle):
        a = abs(self) * vec.unit_at_angle(self.angle() + angle)
        return vec(round(a.x), round(a.y))
    
    def unit_at_angle(angle):
        return vec(cos(rad(angle)), sin(rad(angle)))

east = vec(1, 0)
west = -east
north = vec(0, 1)
south = -north

direction_map = {navigation.east: east, navigation.west: west, navigation.south: south, navigation.north: north}

class ship:
    def __init__(self, heading = 0, pos = vec(0, 0), waypoint = vec(10, 1)):
        self.heading = heading
        self.pos = pos
        self.waypoint = waypoint
    
    def move(self, displacement: vec):
        self.pos += displacement

    def move_waypoint(self, displacement: vec):
        self.waypoint += displacement

    def rotate_waypoint(self, angle):
        self.waypoint = self.waypoint.rotate(angle)
    
    def forward(self, distance):
        self.move(distance * self.waypoint)
    
    def rotate(self, angle):
        self.heading += angle
        self.heading = (self.heading + 180) % 360 - 180
    
    def get_m_dist(self):
        return abs(self.pos.x) + abs(self.pos.y)


instructions = []

with open('day12-input', 'r') as f:
    for line in f:
        line = line.strip()
        nav = navigation(line[0])
        val = int(line[1:])
        instructions.append(instruction(nav, val))


# part 1: follow instructions, figure out distance to final destination

def move(boat: ship, inst: instruction):
    if inst.nav in direction_map:
        boat.move(inst.val * direction_map[inst.nav])
    elif inst.nav == navigation.left:
        boat.rotate(inst.val)
    elif inst.nav == navigation.right:
        boat.rotate(-inst.val)
    elif inst.nav == navigation.forward:
        boat.move(inst.val * vec.unit_at_angle(boat.heading))

boat = ship()

for inst in instructions:
    move(boat, inst)

print(boat.get_m_dist())

# part 2: different instructions this time around

def follow(boat: ship, instruction: instruction):
    if inst.nav in direction_map:
        boat.move_waypoint(inst.val * direction_map[inst.nav])
    elif inst.nav == navigation.left:
        boat.rotate_waypoint(inst.val)
    elif inst.nav == navigation.right:
        boat.rotate_waypoint(-inst.val)
    elif inst.nav == navigation.forward:
        boat.forward(inst.val)

boat1 = ship()

for inst in instructions:
    follow(boat1, inst)

print(boat1.get_m_dist())