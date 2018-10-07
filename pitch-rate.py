#!/usr/bin/env python3

g = 9.81                   # grav acc in m/s^2

def exhaustVelocityFromISP(isp: float) -> float:
    return isp * g

def simStage(stageTime: int, thrust: float, massEmpty: float, massPropellant: float, massFull: float, isp: float) -> int:
    x = 0                      # altitude in meters
    v = 0                      # velocity in meters/sec
    t = 0                      # time in sec
    dt = 1
    mass = massFull
    velocityE = isp * g        # tsfc = 1 / velocityE
    dm = - (thrust / velocityE * dt)

    # loop with some small dt, thrust is constant thrust (in Newtons -- not
    # kN), g is 9.8 m/s, mdot is based on thrust and ISP (should be in kg/sec)
    # -- so thrust, g and mdot are constants based on the rocket (and the
    # planet for g):

    while t <= stageTime:
        dx = v * dt
        dv = (thrust/mass - g) * dt
        x += dx
        v += dv
        mass += dm
        t += dt

    print('x = {0:.0f}'.format(x))
    print('v = {0:.1f}'.format(v))


def main():
    stage1Empty = 21_054 + 2_316 + 20_830
    stage1Propellant = 284_089
    stage1Full = stage1Empty + stage1Propellant
    simStage(253, 3_827_000, stage1Empty, stage1Propellant, stage1Full, 311.3)


if __name__ == '__main__':
    main()
