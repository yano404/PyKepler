# -*- coding: utf-8 -*-
"""
Copyright (c) 2016 Takayuki Yano All Rights Reserved.

This file is part of PyKepler.

PyKepler is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyKepler is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from math import pow, sqrt

#G = 6.674e-11

class Planet:
    def __init__(self, name, mass, x0, y0, z0, vx0, vy0, vz0):
        self.name = name
        self.mass = mass
        self.x = [x0] #{0:x0}
        self.y = [y0] #{0:y0}
        self.z = [z0] #{0:z0}
        self.vx = [vx0] #{0:vx0}
        self.vy = [vy0] #{0:vy0}
        self.vz = [vz0] #{0:vz0}
        self.k1 = {"x":None, "y":None, "z":None, "vx":None, "vy":None, "vz":None}
        self.k2 = {"x":None, "y":None, "z":None, "vx":None, "vy":None, "vz":None}
        self.k3 = {"x":None, "y":None, "z":None, "vx":None, "vy":None, "vz":None}
        self.k4 = {"x":None, "y":None, "z":None, "vx":None, "vy":None, "vz":None}

    def modify_planet(self, name, mass, x0, y0, z0, vx0, vy0, vz0):
        self.name = name
        self.mass = mass
        self.x[0] = x0
        self.y[0] = y0
        self.z[0] = z0
        self.vx[0] = vx0
        self.vy[0] = vy0
        self.vz[0] = vz0

    def update_data(self, step, x, y, z, vx, vy, vz):
        self.x.append(x) #update({step:x})
        self.y.append(y) #update({step:y})
        self.z.append(z) #update({step:z})
        self.vx.append(vx) #update({step:vx})
        self.vy.append(vy) #update({step:vy})
        self.vz.append(vz) #update({step:vz})

    def  update_k1(self, x, y, z, vx, vy, vz):
        self.k1.update({"x":x, "y":y, "z":z, "vx":vx, "vy":vy, "vz":vz})

    def  update_k2(self, x, y, z, vx, vy, vz):
        self.k2.update({"x":x, "y":y, "z":z, "vx":vx, "vy":vy, "vz":vz})

    def  update_k3(self, x, y, z, vx, vy, vz):
        self.k3.update({"x":x, "y":y, "z":z, "vx":vx, "vy":vy, "vz":vz})

    def  update_k4(self, x, y, z, vx, vy, vz):
        self.k4.update({"x":x, "y":y, "z":z, "vx":vx, "vy":vy, "vz":vz})

class Planet_system(list):
    def __init__(self):
        list.__init__(self)

    def add_planet(self, name, mass, x0, y0, z0, vx0, vy0, vz0):
        list.append(self, Planet(name, mass, x0, y0, z0, vx0, vy0, vz0))

    def del_planet(self, i):
        list.pop(self, i)

def diffeq_vxy(Planet_system, n, step, G, dim):
    result_vx = 0
    result_vy = 0

    for i in range(len(Planet_system)):
        if i != n:
            if dim == 1:
                dist_x = Planet_system[i].x[step] - Planet_system[n].x[step]
                dist_y = Planet_system[i].y[step] - Planet_system[n].y[step]
            elif dim == 2:
                dist_x = (Planet_system[i].x[step] + Planet_system[i].k1["x"]/2)\
                         - (Planet_system[n].x[step] + Planet_system[n].k1["x"]/2)
                dist_y = (Planet_system[i].y[step] + Planet_system[i].k1["y"]/2)\
                         - (Planet_system[n].y[step] + Planet_system[n].k1["y"]/2)
            elif dim == 3:
                dist_x = (Planet_system[i].x[step] + Planet_system[i].k2["x"]/2)\
                         - (Planet_system[n].x[step] + Planet_system[n].k2["x"]/2)
                dist_y = (Planet_system[i].y[step] + Planet_system[i].k2["y"]/2)\
                         - (Planet_system[n].y[step] + Planet_system[n].k2["y"]/2)
            else:
                dist_x = (Planet_system[i].x[step] + Planet_system[i].k3["x"])\
                         - (Planet_system[n].x[step] + Planet_system[n].k3["x"])
                dist_y = (Planet_system[i].y[step] + Planet_system[i].k3["y"])\
                         - (Planet_system[n].y[step] + Planet_system[n].k3["y"])
            result_vx += Planet_system[i].mass * dist_x / pow(dist_x**2 + dist_y**2, 3/2)
            result_vy += Planet_system[i].mass * dist_y / pow(dist_x**2 + dist_y**2, 3/2)
        else:
            pass
    result_vx *= G
    result_vy *= G
    return [result_vx, result_vy]

def RK4(Planet_system, dt, step, G):
    planet_number = len(Planet_system)
    for i in range(planet_number):
        k1_x = dt * Planet_system[i].vx[step]
        k1_y = dt * Planet_system[i].vy[step]
        k1_vx, k1_vy = diffeq_vxy(Planet_system, i, step, G, 1)
        k1_vx *= dt
        k1_vy *= dt
        Planet_system[i].update_k1(k1_x, k1_y, 0, k1_vx, k1_vy, 0)

    for i in range(planet_number):
        k2_x = dt * (Planet_system[i].vx[step] + Planet_system[i].k1["vx"]/2)
        k2_y = dt * (Planet_system[i].vy[step] + Planet_system[i].k1["vy"]/2)
        k2_vx, k2_vy = diffeq_vxy(Planet_system, i, step, G, 2)
        k2_vx *= dt
        k2_vy *= dt
        Planet_system[i].update_k2(k2_x, k2_y, 0, k2_vx, k2_vy, 0)

    for i in range(planet_number):
        k3_x = dt * (Planet_system[i].vx[step] + Planet_system[i].k2["vx"]/2)
        k3_y = dt * (Planet_system[i].vy[step] + Planet_system[i].k2["vy"]/2)
        k3_vx, k3_vy = diffeq_vxy(Planet_system, i, step, G, 3)
        k3_vx *= dt
        k3_vy *= dt
        Planet_system[i].update_k3(k3_x, k3_y, 0, k3_vx, k3_vy, 0)

    for i in range(planet_number):
        k4_x = dt * (Planet_system[i].vx[step] + Planet_system[i].k3["vx"])
        k4_y = dt * (Planet_system[i].vy[step] + Planet_system[i].k3["vy"])
        k4_vx, k4_vy = diffeq_vxy(Planet_system, i, step, G, 4)
        k4_vx *= dt
        k4_vy *= dt
        Planet_system[i].update_k4(k4_x, k4_y, 0, k4_vx, k4_vy, 0)

    for i in range(planet_number):
        x = Planet_system[i].x[step]\
            + (Planet_system[i].k1["x"]\
               + 2*Planet_system[i].k2["x"]\
               + 2*Planet_system[i].k3["x"]\
               + Planet_system[i].k4["x"]) / 6
        y = Planet_system[i].y[step]\
            + (Planet_system[i].k1["y"]\
               + 2*Planet_system[i].k2["y"]\
               + 2*Planet_system[i].k3["y"]\
               + Planet_system[i].k4["y"]) / 6
        vx = Planet_system[i].vx[step]\
            + (Planet_system[i].k1["vx"]\
               + 2*Planet_system[i].k2["vx"]\
               + 2*Planet_system[i].k3["vx"]\
               + Planet_system[i].k4["vx"]) / 6
        vy = Planet_system[i].vy[step]\
            + (Planet_system[i].k1["vy"]\
               + 2*Planet_system[i].k2["vy"]\
               + 2*Planet_system[i].k3["vy"]\
               + Planet_system[i].k4["vy"]) / 6
        Planet_system[i].update_data(step+1, x, y, 0, vx, vy, 0)

def diffeq_vxyz(Planet_system, n, step, G, dim):
    result_vx = 0
    result_vy = 0
    result_vz = 0

    for i in range(len(Planet_system)):
        if i != n:
            if dim == 1:
                dist_x = Planet_system[i].x[step] - Planet_system[n].x[step]
                dist_y = Planet_system[i].y[step] - Planet_system[n].y[step]
                dist_z = Planet_system[i].z[step] - Planet_system[n].z[step]
            elif dim == 2:
                dist_x = (Planet_system[i].x[step] + Planet_system[i].k1["x"]/2)\
                         - (Planet_system[n].x[step] + Planet_system[n].k1["x"]/2)
                dist_y = (Planet_system[i].y[step] + Planet_system[i].k1["y"]/2)\
                         - (Planet_system[n].y[step] + Planet_system[n].k1["y"]/2)
                dist_z = (Planet_system[i].z[step] + Planet_system[i].k1["z"]/2)\
                         - (Planet_system[n].z[step] + Planet_system[n].k1["z"]/2)
            elif dim == 3:
                dist_x = (Planet_system[i].x[step] + Planet_system[i].k2["x"]/2)\
                         - (Planet_system[n].x[step] + Planet_system[n].k2["x"]/2)
                dist_y = (Planet_system[i].y[step] + Planet_system[i].k2["y"]/2)\
                         - (Planet_system[n].y[step] + Planet_system[n].k2["y"]/2)
                dist_z = (Planet_system[i].z[step] + Planet_system[i].k2["z"]/2)\
                         - (Planet_system[n].z[step] + Planet_system[n].k2["z"]/2)
            else:
                dist_x = (Planet_system[i].x[step] + Planet_system[i].k3["x"])\
                         - (Planet_system[n].x[step] + Planet_system[n].k3["x"])
                dist_y = (Planet_system[i].y[step] + Planet_system[i].k3["y"])\
                         - (Planet_system[n].y[step] + Planet_system[n].k3["y"])
                dist_z = (Planet_system[i].z[step] + Planet_system[i].k3["z"])\
                         - (Planet_system[n].z[step] + Planet_system[n].k3["z"])
            result_vx += Planet_system[i].mass * dist_x / pow(dist_x**2 + dist_y**2 + dist_z**2, 3/2)
            result_vy += Planet_system[i].mass * dist_y / pow(dist_x**2 + dist_y**2 + dist_z**2, 3/2)
            result_vz += Planet_system[i].mass * dist_z / pow(dist_x**2 + dist_y**2 + dist_z**2, 3/2)
        else:
            pass
    result_vx *= G
    result_vy *= G
    result_vz *= G
    return [result_vx, result_vy, result_vz]

def RK4z(Planet_system, dt, step, G):
    planet_number = len(Planet_system)
    for i in range(planet_number):
        k1_x = dt * Planet_system[i].vx[step]
        k1_y = dt * Planet_system[i].vy[step]
        k1_z = dt * Planet_system[i].vz[step]
        k1_vx, k1_vy, k1_vz = diffeq_vxyz(Planet_system, i, step, G, 1)
        k1_vx *= dt
        k1_vy *= dt
        k1_vz *= dt
        Planet_system[i].update_k1(k1_x, k1_y, k1_z, k1_vx, k1_vy, k1_vz)

    for i in range(planet_number):
        k2_x = dt * (Planet_system[i].vx[step] + Planet_system[i].k1["vx"]/2)
        k2_y = dt * (Planet_system[i].vy[step] + Planet_system[i].k1["vy"]/2)
        k2_z = dt * (Planet_system[i].vz[step] + Planet_system[i].k1["vz"]/2)
        k2_vx, k2_vy, k2_vz = diffeq_vxyz(Planet_system, i, step, G, 2)
        k2_vx *= dt
        k2_vy *= dt
        k2_vz *= dt
        Planet_system[i].update_k2(k2_x, k2_y, k2_z, k2_vx, k2_vy, k2_vz)

    for i in range(planet_number):
        k3_x = dt * (Planet_system[i].vx[step] + Planet_system[i].k2["vx"]/2)
        k3_y = dt * (Planet_system[i].vy[step] + Planet_system[i].k2["vy"]/2)
        k3_z = dt * (Planet_system[i].vz[step] + Planet_system[i].k2["vz"]/2)
        k3_vx, k3_vy, k3_vz = diffeq_vxyz(Planet_system, i, step, G, 3)
        k3_vx *= dt
        k3_vy *= dt
        k3_vz *= dt
        Planet_system[i].update_k3(k3_x, k3_y, k3_z, k3_vx, k3_vy, k3_vz)

    for i in range(planet_number):
        k4_x = dt * (Planet_system[i].vx[step] + Planet_system[i].k3["vx"])
        k4_y = dt * (Planet_system[i].vy[step] + Planet_system[i].k3["vy"])
        k4_z = dt * (Planet_system[i].vz[step] + Planet_system[i].k3["vz"])
        k4_vx, k4_vy, k4_vz = diffeq_vxyz(Planet_system, i, step, G, 4)
        k4_vx *= dt
        k4_vy *= dt
        k4_vz *= dt
        Planet_system[i].update_k4(k4_x, k4_y, k4_z, k4_vx, k4_vy, k4_vz)

    for i in range(planet_number):
        x = Planet_system[i].x[step]\
            + (Planet_system[i].k1["x"]\
               + 2*Planet_system[i].k2["x"]\
               + 2*Planet_system[i].k3["x"]\
               + Planet_system[i].k4["x"]) / 6
        y = Planet_system[i].y[step]\
            + (Planet_system[i].k1["y"]\
               + 2*Planet_system[i].k2["y"]\
               + 2*Planet_system[i].k3["y"]\
               + Planet_system[i].k4["y"]) / 6
        z = Planet_system[i].z[step]\
            + (Planet_system[i].k1["z"]\
               + 2*Planet_system[i].k2["z"]\
               + 2*Planet_system[i].k3["z"]\
               + Planet_system[i].k4["z"]) / 6
        vx = Planet_system[i].vx[step]\
            + (Planet_system[i].k1["vx"]\
               + 2*Planet_system[i].k2["vx"]\
               + 2*Planet_system[i].k3["vx"]\
               + Planet_system[i].k4["vx"]) / 6
        vy = Planet_system[i].vy[step]\
            + (Planet_system[i].k1["vy"]\
               + 2*Planet_system[i].k2["vy"]\
               + 2*Planet_system[i].k3["vy"]\
               + Planet_system[i].k4["vy"]) / 6
        vz = Planet_system[i].vz[step]\
            + (Planet_system[i].k1["vz"]\
               + 2*Planet_system[i].k2["vz"]\
               + 2*Planet_system[i].k3["vz"]\
               + Planet_system[i].k4["vz"]) / 6
        Planet_system[i].update_data(step+1, x, y, z, vx, vy, vz)

def chk_energy2d(Planet_system, index):
    E = []
    for i in range(len(Planet_system[index].x)):
        K = 1/2 * Planet_system[index].mass *\
            (Planet_system[index].vx[i] ** 2 + Planet_system[index].vy[i] ** 2)
        for k in range(len(Planet_system)):
            if index != k:
                K -= G * Planet_system[index].mass * Planet_system[k].mass\
                     / sqrt( (Planet_system[index].x[i]-Planet_system[k].x[i])**2 + (Planet_system[index].y[i]-Planet_system[k].y[i])**2)
            else:
                pass
        E.append(K)
    return E

def chk_energy3d(Planet_system, index):
    E = []
    for i in range(len(Planet_system[index].x)):
        K = 1/2 * Planet_system[index].mass *\
            (Planet_system[index].vx[i] ** 2 + Planet_system[index].vy[i] ** 2 + Planet_system[index].vz[i] ** 2)
        for k in range(len(Planet_system)):
            if index != k:
                K -= G * Planet_system[index].mass * Planet_system[k].mass\
                     / sqrt((Planet_system[index].x[i]-Planet_system[k].x[i])**2\
                            + (Planet_system[index].y[i]-Planet_system[k].y[i])**2\
                            + (Planet_system[index].z[i]-Planet_system[k].y[i])**2)
            else:
                pass
        E.append(K)
    return E


def main():
    G = 6.674e-11
    end = 3600*24*365
    dt = 3600#0.001
    sum_step = int(end // dt + 1)
    planets = Planet_system()
    planets.add_planet("Sun", 1.989e30, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    planets.add_planet("Earth", 5.972e24, 1.496e11, 0.0, 0.0, 0.0, 29.4e3, 0.0)
    #planets.add_planet("Earth2", 5.972e24, 1.496e11+4.055e8, 0.0, 0.0, 40.4e3)
    planets.add_planet("Moon", 7.348e22, 1.496e11+4.055e8, 0.0, 0.0, 0.0, 29.4e3+1.01e3, 0.0)
    #planets.add_planet("planet2", 0.01, 1.2, 0.0, 0.0, 1.2)
    #planets.add_planet("Earth", 5.972e24,0.0, 0.0, 0.0, 0.0)
    #planets.add_planet("Moon", 7.348e22, 4.055e8, 0.0, 0.0, 1.01e3)
    for i in range(sum_step):
        RK4(planets, dt, i, G)
        print(i)

    #fig = plt.figure()
    #ax = Axes3D(fig)
    #ax.plot_wireframe(planets[0].x, planets[0].y, planets[0].z, color="#cccccc")
    #ax.plot_wireframe(planets[1].x, planets[1].y, planets[1].z, color="#00cccc")
    #ax.plot_wireframe(planets[2].x, planets[2].y, planets[2].z, color="#ff0000")

    #plt.plot(planets[0].x, planets[0].y, planets[0].z, "rs-")
    #plt.plot(planets[1].x, planets[1].y, planets[1].z, "b:")
    #plt.plot(planets[2].x, planets[2].y, planets[2].z, "g:")
    fig = plt.figure()
    #ax = plt.subplot(111)
    plt.plot(planets[1].x[0], planets[1].y[0], "bs-")
    ax.plot(planets[1].x[0], planets[1].y[0], "bs-")
    ax.plot(planets[2].x, planets[2].y, "g:")
    #plt.draw()
    plt.show()

if __name__ == "__main__":
    main()
