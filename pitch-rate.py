#!/usr/bin/env python3

import math

g = 9.81                        # grav acc in meters/second^2
r0 = 6_378_100                  # Earth radius in meters
muggc = 3.986004418e+14         # geocentric gravitational constant

def exhaustVelocityFromISP(isp: float) -> float:
    return isp * g

def simStage(x: float, y: float, vx: float, vy: float, stageTime: float,
        thrust: float, massEmpty: float, massPropellant: float,
        massFull: float, isp: float, pitchStart: float, pitchEnd: float,
        pitchRateDeg: float) -> (float, float, float, float):
    t = 0                       # time in sec
    dt = 1                      # time step
    dvexp = 0                   # delta-v expended
    mass = massFull
    velocityE = isp * g         # tsfc = 1 / velocityE
    dm = -(thrust / velocityE * dt)
    pitchRate = math.radians(pitchRateDeg)
    pitch = 0                   # vertical ascent

    # loop with some small dt, thrust is constant thrust (in Newtons -- not
    # kN), g is 9.8 m/s, mdot is based on thrust and ISP (should be in kg/sec)
    # -- so thrust, g and mdot are constants based on the rocket (and the
    # planet for g):

    while t <= stageTime:
        rm3 = math.sqrt(x ** 2 + y ** 2) ** 3

        uy = math.sin(pitch)            # thrust vector
        ux = math.cos(pitch)

        ddvexp = (thrust / mass) * dt
        dx = vx * dt
        dy = vy * dt
        dvx = (-muggc * x / rm3 + thrust / mass * ux) * dt;
        dvy = (-muggc * y / rm3 + thrust / mass * uy) * dt;

        dvexp += ddvexp
        x += dx
        y += dy
        vx += dvx
        vy += dvy
        mass += dm
        t += dt

        if pitchStart < t:          # vertical ascent
            continue
        if t < pitchEnd:            # pitch program
            pitch += pitchRate * dt
            continue
        pitch = math.atan2(vy, vx)  # gravity turn

    print('x = {0:.0f} m'.format(x))
    print('x - r0 (altitude) = {0:.0f} m'.format(x - r0))
    print('y (cross-range) = {0:.0f} m'.format(y))
    print('vx (vertical speed) = {0:.1f} m/s'.format(vx))
    print('vy (horizontal speed) = {0:.1f} m/s'.format(vy))
    print('pitch = {0:.1f} deg'.format(math.degrees(pitch)))
    v = math.sqrt(vx ** 2 + vy ** 2)
    print('speed = {0:.1f} m/s'.format(v))
    print('delta-v expended = {0:.1f} m/s'.format(dvexp))
    return (x, y, vx, vy)


def main():
    stage1Empty = 21_054 + 2_316 + 20_830
    stage1Propellant = 284_089
    stage1Full = stage1Empty + stage1Propellant
    simStage(r0, 0, 0, 0, 253, 3_827_000, stage1Empty, stage1Propellant, stage1Full, 311.3, 10, 20, 4.8)


if __name__ == '__main__':
    main()
