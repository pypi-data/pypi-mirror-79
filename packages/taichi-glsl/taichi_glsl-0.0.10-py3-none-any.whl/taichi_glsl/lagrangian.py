'''
Some helper functions that might be useful in physics simulation.
'''

import taichi as ti
import taichi_glsl as tl


@ti.func
def boundReflect(pos, vel, pmin=0, pmax=1, gamma=1, gamma_perpendicular=1):
    '''
    Reflect particle velocity from a rectangular boundary (if collides).

    `boundaryReflect` takes particle position, velocity and other parameters.
    Detect if the particle collides with the rect boundary given by ``pmin``
    and ``pmax``, if collide, returns the velocity after bounced with boundary,
    otherwise return the original velocity without any change.

    :parameter pos: (Vector)
        The particle position.

    :parameter vel: (Vector)
        The particle velocity.

    :parameter pmin: (scalar or Vector)
        The position lower boundary. If vector, it's the bottom-left of rect.

    :parameter pmin: (scalar or Vector)
        The position upper boundary. If vector, it's the top-right of rect.
    '''
    cond = pos < pmin and vel < 0 or pos > pmax and vel > 0
    for j in ti.static(range(pos.n)):
        if cond[j]:
            vel[j] *= -gamma
            for k in ti.static(range(pos.n)):
                if k != j:
                    vel[k] *= gamma_perpendicular
    return vel


@ti.func
def ballBoundReflect(pos, vel, center, radius, anti_fall=0, anti_depth=0.1):
    ret = vel
    above = tl.distance(pos, center) - radius
    if above <= 0:
        normal = tl.normalize(pos - center)
        NoV = tl.dot(vel, normal)
        if ti.static(anti_fall):
            NoV -= anti_fall * tl.smoothstep(above, 0, -anti_depth)
        if NoV < 0:
            ret -= NoV * normal
    return ret


@ti.func
def momentumExchange(v1, v2, disp, m1=1, m2=1, gamma=1):
    '''
    Exchange momentum (bounce) between two objects.

    `momentumExchange` should be invocated when a bounce occurred.
    It takes the velocity of two objects before bounce, and returns the
    velocity of two objects after bounce.

    This function is most useful in rigid-body simulation with collision.
    For example::

        if distance(pos[i], pos[j]) < radius[i] + radius[j]:
            # Collision detected! Perform a momentum exchange:
            vel[i], vel[j] = momentumExchange(
                vel[i], vel[j], mass[i], mass[j], pos[i] - pos[j], 0.8)

    :parameter v1: (Vector)
        The velocity vector of the first object to bounce.
        Or, the velocity vector at the collision point in first object.

    :parameter v2: (Vector)
        The velocity vector of the second object to bounce.
        Or, the velocity vector at the collision point in second object.

    :parameter disp: (Vector)
        The displacement vector from between two object.
        Or, the normal vector of collision surface.
        Specifically, for balls or circles, `disp` is `pos1 - pos2`.

    :parameter m1: (scalar)
        The mass of the first object to bounce.

    :parameter m2: (scalar)
        The mass of the second object to bounce.

    :parameter gamma: (scalar)
        The decrease factor of bounce, in range [0, 1], determines how
        much energy is conserved after the bounce process. If 1, then
        no energy is loss; if 0, then the collided objects will stops
        immediately.

    :return: (tuple of Vector)
        The return value is a tuple of velocity of two objects after bounce.
        Specifically the first element is for the velocity of first object
        (previously to be `v1`), and same to the second element.

    :note:
        For usage example, check out this:
        https://github.com/taichi-dev/taichi_three/blob/master/examples/many_balls.py
    '''
    vel1 = v1.dot(disp)
    vel2 = v2.dot(disp)

    sm1 = ti.sqrt(m1)
    sm2 = ti.sqrt(m2)
    itsm = 1 / ti.sqrt(m1 + m2)

    kero1 = vel1 * sm1
    kero2 = vel2 * sm2

    smd1 = sm2 * itsm
    smd2 = -sm1 * itsm

    kos = 2 * (kero1 * smd1 + kero2 * smd2)
    kero1 -= kos * smd1
    kero2 -= kos * smd2

    vel1 = kero1 / sm1
    vel2 = kero2 / sm2

    disp *= gamma

    v1 -= v1.dot(disp) * disp
    v2 -= v2.dot(disp) * disp

    v1 += vel1 * disp
    v2 += vel2 * disp

    return v1, v2
