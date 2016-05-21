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

import sys
from math import pow
#import matplotlib.pyplot as plt
#from PyQt.QtCore import QObject
from pyqtgraph.Qt import QtGui, QtCore
#import pyqtgraph.opengl as gl
import pyqtgraph as pg
#import vispy
#from vispy.plot import Fig
#import vispy.mpl_plot as plt
import numpy as np
#vispy.use(app="PyQt5",gl='pyopengl2')

G = 6.674e-11

class Planet:
    def __init__(self, name, mass, x0, y0, vx0, vy0):
        self.name = name
        self.mass = mass
        self.x = [x0] #{0:x0}
        self.y = [y0] #{0:y0}
        self.vx = [vx0] #{0:vx0}
        self.vy = [vy0] #{0:vy0}
        self.k1 = {"x":None, "y":None, "vx":None, "vy":None}
        self.k2 = {"x":None, "y":None, "vx":None, "vy":None}
        self.k3 = {"x":None, "y":None, "vx":None, "vy":None}
        self.k4 = {"x":None, "y":None, "vx":None, "vy":None}

    def modify_planet(self, name, mass, x0, y0, vx0, vy0):
        self.name = name
        self.mass = mass
        self.x[0] = x0 #{0:x0}
        self.y[0] = y0 #{0:y0}
        self.vx[0] = vx0 #{0:vx0}
        self.vy[0] = vy0 #{0:vy0}

    def update_data(self, step, x, y, vx, vy):
        self.x.append(x) #update({step:x})
        self.y.append(y) #update({step:y})
        self.vx.append(vx) #update({step:vx})
        self.vy.append(vy) #update({step:vy})

    def  update_k1(self, x, y, vx, vy):
        self.k1.update({"x":x, "y":y, "vx":vx, "vy":vy})

    def  update_k2(self, x, y, vx, vy):
        self.k2.update({"x":x, "y":y, "vx":vx, "vy":vy})

    def  update_k3(self, x, y, vx, vy):
        self.k3.update({"x":x, "y":y, "vx":vx, "vy":vy})

    def  update_k4(self, x, y, vx, vy):
        self.k4.update({"x":x, "y":y, "vx":vx, "vy":vy})

class Planet_system(list):
    def __init__(self):
        list.__init__(self)

    def add_planet(self, name, mass, x0, y0, vx0, vy0):
        list.append(self, Planet(name, mass, x0, y0, vx0, vy0))

def diffeq_vxy(Planet_system, n, step, dim):
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

def RK4(Planet_system, dt, step):
    planet_number = len(Planet_system)
    for i in range(planet_number):
        k1_x = dt * Planet_system[i].vx[step]
        k1_y = dt * Planet_system[i].vy[step]
        k1_vx, k1_vy = diffeq_vxy(Planet_system, i, step, 1)
        k1_vx *= dt
        k1_vy *= dt
        Planet_system[i].update_k1(k1_x, k1_y, k1_vx, k1_vy)

    for i in range(planet_number):
        k2_x = dt * (Planet_system[i].vx[step] + Planet_system[i].k1["vx"]/2)
        k2_y = dt * (Planet_system[i].vy[step] + Planet_system[i].k1["vy"]/2)
        k2_vx, k2_vy = diffeq_vxy(Planet_system, i, step, 2)
        k2_vx *= dt
        k2_vy *= dt
        Planet_system[i].update_k2(k2_x, k2_y, k2_vx, k2_vy)

    for i in range(planet_number):
        k3_x = dt * (Planet_system[i].vx[step] + Planet_system[i].k2["vx"]/2)
        k3_y = dt * (Planet_system[i].vy[step] + Planet_system[i].k2["vy"]/2)
        k3_vx, k3_vy = diffeq_vxy(Planet_system, i, step, 3)
        k3_vx *= dt
        k3_vy *= dt
        Planet_system[i].update_k3(k3_x, k3_y, k3_vx, k3_vy)

    for i in range(planet_number):
        k4_x = dt * (Planet_system[i].vx[step] + Planet_system[i].k3["vx"])
        k4_y = dt * (Planet_system[i].vy[step] + Planet_system[i].k3["vy"])
        k4_vx, k4_vy = diffeq_vxy(Planet_system, i, step, 4)
        k4_vx *= dt
        k4_vy *= dt
        Planet_system[i].update_k4(k4_x, k4_y, k4_vx, k4_vy)

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
        Planet_system[i].update_data(step+1, x, y, vx, vy)

def main():
    end = 3600*24*365
    dt = 3600#0.001
    sum_step = int(end // dt + 1)
    planets = Planet_system()
    planets.add_planet("Sun", 1.989e30, 0.0, 0.0, 0.0, 0.0)
    planets.add_planet("Earth", 5.972e24, 1.496e11, 0.0, 0.0, 29.4e3)
    #planets.add_planet("Earth2", 5.972e24, 1.496e11+4.055e8, 0.0, 0.0, 40.4e3)
    planets.add_planet("Moon", 7.348e22, 1.496e11+4.055e8, 0.0, 0.0, 29.4e3+1.01e3)
    #planets.add_planet("planet2", 0.01, 1.2, 0.0, 0.0, 1.2)
    #planets.add_planet("Earth", 5.972e24,0.0, 0.0, 0.0, 0.0)
    #planets.add_planet("Moon", 7.348e22, 4.055e8, 0.0, 0.0, 1.01e3)
    for i in range(sum_step):
        RK4(planets, dt, i)
        print(i)

    app = QtGui.QApplication([])
    w = QtGui.QMainWindow()
    cw = pg.GraphicsLayoutWidget()
    w.show()
    w.resize(400,600)
    w.setCentralWidget(cw)
    w.setWindowTitle('pyqtgraph example: Arrow')
    p2 = cw.addPlot(row=1, col=0)
    z  = [0]*8761
    #plt.plot(planets[0].x, planets[0].y, z, "rs-")
    #plt.plot(planets[1].x, planets[1].y, z, "b:")
    #plt.plot(planets[2].x, planets[2].y, z, "g:")
    
    c = []
    c.append(p2.plot(x=planets[0].x, y=planets[0].y, color="b"))#z=[0]*8761))
    c.append(p2.plot(x=planets[1].x, y=planets[1].y, cloor="r"))#z=[0]*8761))
    a = []
    a.append(pg.CurveArrow(c[0]))
    a.append(pg.CurveArrow(c[1]))
    #a2 = pg.CurveArrow(c2)
    
    a[0].setStyle(headLen=40)
    p2.addItem(a[0])
    p2.addItem(a[1])
    anim = []
    anim.append(a[0].makeAnimation(loop=-1))
    anim.append(a[1].makeAnimation(loop=-1))
    
    #anim = a[0].makeAnimation(loop=-1)
    #anim2 = a[1].makeAnimation(loop=-1)
    
    anim[0].start()
    anim[1].start()
    

    """w = gl.GLViewWidget()
    w.opts['distance'] = 20
    w.show()
    w.setWindowTitle('pyqtgraph example: GLScatterPlotItem')
    gx = gl.GLGridItem()
    gx.rotate(90, 0, 1, 0)
    gx.translate(-10, 0, 0)
    w.addItem(gx)
    gy = gl.GLGridItem()
    gy.rotate(90, 1, 0, 0)
    gy.translate(0, -10, 0)
    w.addItem(gy)
    gz = gl.GLGridItem()
    gz.translate(0, 0, -10)
    w.addItem(gz)
    #n = 51"""
    """
    y = planets[1].y #np.linspace(-10,10,n)
    x = planets[1].x #np.linspace(-10,10,100)
    z = [0]*8762
    for i in range(len(planets[1].x)):
        yi = np.array([y[i]])
        pts = np.vstack([x[i],yi,z[i]]).transpose()
    #    yi = np.array([y[i]]*100)
    #    d = (x**2 + yi**2)**0.5
    #    z = 10 * np.cos(d) / (d+1)
    #    pts = np.vstack([x,yi,z]).transpose()
        plt = gl.GLLinePlotItem(pos=pts, color=pg.glColor(225,225,225), width=10, antialias=True)
        w.addItem(plt)"""
    #sp1 = gl.GLScatterPlotItem(pos=[planets[1].x, planets[1].y, [0]*8761], size=[0.5]*8761, color=[[0.0, 1.0, 0.0, 0.5]]*8761, pxMode=False)
    #sp1.translate(5,5,0)
    #w.addItem(sp1)
    sys.exit(app.exec_())
    """
    #plt.plot(planets[1].x[0], planets[1].y[0], "bs-")
    #plt.plot(planets[1].x[720], planets[1].y[720], "bs-")
    #plt.plot(planets[2].x, planets[2].y, "g:")
    #plt.draw()
    #plt.show(True)
    fig = Fig()
    ax = fig[0, 0]
    ax.plot(planets[1].x, planets[1].y, z)
def fn(x, y):
    return np.cos((x**2 + y**2)**0.5)"""

if __name__ == "__main__":
    main()
