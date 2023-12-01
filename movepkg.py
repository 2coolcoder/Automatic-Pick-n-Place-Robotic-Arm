import serial
import time
import numpy as np
import math as m

contact_sw = 0


def pos(a):
    while a > m.pi:
        a -= 2 * m.pi
    while a <= -m.pi:
        a += 2 * m.pi
    return a


def deg(q):
    return int(q * 180 / m.pi)


def equals(a, b):
    a = a - b
    if a < 0.001 and a > -0.001:
        return True
    return False


class robot:
    def __init__(self):
        self.arduino = serial.Serial(
            port="COM5", baudrate=115200, timeout=50)
        time.sleep(5)
        self.l = 46.0
        self.l0 = 24/self.l

        self.pos = np.array([2+self.l0, 0, 0], np.float64)

    def go(self, x, y, z, magnet=0):
        q0 = m.atan2(y, x)
        q1 = q2 = 0
        a = m.sqrt(x**2 + y**2) - self.l0
        b = z
        # print(q0, a, b)
        sq = m.sqrt(a**2 + b**2)
        c1 = m.acos(sq / 2)
        c2 = m.acos(a / sq)
        Q1 = []
        Q1.append(pos(c1 + c2))
        Q1.append(pos(c1 - c2))
        Q1.append(pos(-c1 + c2))
        Q1.append(pos(-c1 - c2))

        # print(Q1)

        for q in Q1:
            exp = a - m.cos(q)
            if exp > 1 or exp < -1:
                continue
            q1q2 = m.acos(exp)
            if (equals(a, m.cos(q) + m.cos(q1q2)) and equals(b, m.sin(q) + m.sin(q1q2)) and pos(q1q2 - q) < 0):
                # print("Q0:", deg(q0), "Q1: ", deg(pos(q)), "Q2: ", deg(
                #     pos(q1q2 - q)), "a:", m.cos(q) + m.cos(q1q2), "b:", m.sin(q) + m.sin(q1q2))
                q1 = pos(q)
                q2 = pos(q1q2 - q)
            q1q2 = pos(-q1q2)
            if (equals(a, m.cos(q) + m.cos(q1q2)) and equals(b, m.sin(q) + m.sin(q1q2)) and pos(q1q2 - q) < 0):
                # print("Q0: ", deg(q0), "Q1: ", deg(pos(q)), "Q2: ", deg(
                #     pos(q1q2 - q)), "a:", m.cos(q) + m.cos(q1q2), "b:", m.sin(q) + m.sin(q1q2))
                q1 = pos(q)
                q2 = pos(q1q2 - q)

        # self.arduino.reset_input_buffer()
        # Bstring= bytes("s"+ str(int(deg(q0))) + " " + str(int(deg(q1))) + " " + str(int(deg(q2))), "utf-8")
        Bstring = bytes(
            "s{3}{0: 04} {1: 04} {2: 04}e".format(int(deg(q0)), int(deg(q1)), int(deg(q2)), magnet), "utf-8")
        # print(Bstring)
        self.arduino.write(Bstring)
        self.arduino.flush()

        s = self.arduino.readline()
        # self.arduino.reset_input_buffer()
        print(s)
        global contact_sw
        contact_sw = int(s[1])-ord('0')
        print("contact sw:", contact_sw)

    def move(self, dest, n=10, magnet=0):
        dest = np.array(dest, np.float64)
        dest[0] += 60
        dest[2] += 16
        dest = dest/self.l
        # print(dest)
        dir = np.array(dest - self.pos, dtype=np.float64)
        n = int(np.sum(np.square(dir)) * n)+1
        dir = dir / n
        for i in range(1, n):
            self.pos = self.pos + dir
            self.go(self.pos[0], self.pos[1], self.pos[2], magnet)
        self.go(dest[0], dest[1], dest[2], magnet)
        self.pos[:] = dest[:]

    def shift(self, delta, magnet=1):
        delta = np.float64(delta)
        delta = delta/self.l
        self.pos = self.pos + delta
        self.go(self.pos[0], self.pos[1], self.pos[2], magnet)


if __name__ == "__main__":
    r = robot()
    # r.go(36, 0, 10)
    r.move((36, 0, 10))
    time.sleep(10)
    r.move(np.array([18, -30, 0]), magnet=1)
    time.sleep(10)
    r.move((0, 0, -5))
    # r.move(np.array([1, 0.3, 0]))
    # r.move(np.array([1, 0.4, 1]))
