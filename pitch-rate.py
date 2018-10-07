#!/usr/bin/env python3

import math

g = 9.81                        # grav acc in meters/second^2
r0 = 6_378_100                  # Earth radius in meters
muggc = 3.986004418e+14         # geocentric gravitational constant

def exhaustVelocityFromISP(isp: float) -> float:
    return isp * g

def simStage(x: float, y: float, vx: float, vy: float, stageTime: int, thrust: float, massEmpty: float, massPropellant: float, massFull: float, isp: float, pitchRateDeg: float) -> (float, float, float, float):
    t = 0                       # time in sec
    dt = 1
    mass = massFull
    velocityE = isp * g         # tsfc = 1 / velocityE
    dm = -(thrust / velocityE * dt)
    pitchRate = math.radians(pitchRateDeg)
    pitch = pitchRate           # for now use a fixed starting pitch

    # loop with some small dt, thrust is constant thrust (in Newtons -- not
    # kN), g is 9.8 m/s, mdot is based on thrust and ISP (should be in kg/sec)
    # -- so thrust, g and mdot are constants based on the rocket (and the
    # planet for g):

    while t <= stageTime:
        rm3 = math.sqrt(x ** 2 + y ** 2) ** 3

        uy = math.sin(pitch)            # velocity in meters/sec
        ux = math.cos(pitch)

        dx = vx * dt
        dy = vy * dt
        dvx = (-muggc * x / rm3 + thrust / mass * ux) * dt;
        dvy = (-muggc * y / rm3 + thrust / mass * uy) * dt;

        x += dx
        y += dy
        vx += dvx
        vy += dvy
        mass += dm
        t += dt
        pitch = math.atan2(vy, vx)

    print('x = {0:.0f} m'.format(x))
    print('x - r0 = {0:.0f} m'.format(x - r0))
    print('y = {0:.0f} m'.format(y))
    print('vx = {0:.1f} m/s'.format(vx))
    print('vy = {0:.1f} m/s'.format(vy))
    print('pitch = {0:.1f} deg'.format(math.degrees(pitch)))
    return (x, y, vx, vy)


def main():
    stage1Empty = 21_054 + 2_316 + 20_830
    stage1Propellant = 284_089
    stage1Full = stage1Empty + stage1Propellant
    simStage(r0, 0, 0, 0, 253, 3_827_000, stage1Empty, stage1Propellant, stage1Full, 311.3, 0.0000062)


if __name__ == '__main__':
    main()
