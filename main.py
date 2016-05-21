#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
from math import pow
import random
import json
import numpy as np

from PyQt4.QtCore import * 
from PyQt4.QtGui import * 

import pyqtgraph as pg
import pyqtgraph.opengl as gl
pg.setConfigOptions(antialias=True)
pg.setConfigOption('background', (255, 255, 255))
import numpy as np

from gui.mainwindow import Ui_MainWindow
from gui.pgviewer import Ui_PGViewer
from gui.pg3dviewer import Ui_PG3DViewer
from gui.tableviewer import Ui_TableViewer
from gui.viewermanager import Ui_ViewerManager
from gui.caldialog import Ui_CalDialog
from gui.errdialog import Ui_ErrDialog

from core.kepler import Planet, Planet_system, diffeq_vxy, diffeq_vxyz, RK4, RK4z

"""
Tree View Model Class
"""

class TreeViewModel(QAbstractItemModel):
    headers = "Name", "Mass", "Init X", "Init Y", "Init Z", "Init VX", "Init VY", "Init VZ"
    def __init__(self, parent=None):
        super(TreeViewModel, self).__init__()
        physicist = ["Newton", "Leibniz", "Galileo", "Descartes", "Taylor",  "Euler",  "Kepler",  "Brahe",   "MaxWell", "Einstein", "Poincare"]
        computer =  ["Pascal", "Babbage", "Ada",     "Turing",    "Mauchly", "Eckert", "Kenneth", "Ritchie", "Knuth",   "Rossum",   "Neumann" ]
        self.items = [[random.choice(physicist), "0", "0", "0", "0", "0", "0", "0"],
                      [random.choice(computer),  "0", "0", "0", "0", "0", "0", "0"]]
        #self.items = [["Sun", "1.989e30", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0"],
        #              ["Earth",  "5.972e24", "1.496e11", "0", "0", "0", "29.4e3", "0"]]

    def index(self, row, column, parent=QModelIndex()):
        return self.createIndex(row, column, None)

    def parent(self, child):
        return QModelIndex()

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            try:
                return self.items[index.row()][index.column()]
            except:
                return
        return

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return
        if orientation == Qt.Horizontal:
            return self.headers[section]

    def addRow(self, name, mass, x0, y0, z0, vx0, vy0, vz0):
        self.beginInsertRows(QModelIndex(), len(self.items),1)
        self.items.append([name, mass, x0, y0, z0, vx0, vy0, vz0])#[name, mass, x0, y0, z0, vx0, vy0, vz0])
        self.endInsertRows()

    def removeRows(self, rowIndexes):
        for row in sorted(rowIndexes, reverse=True):
            self.beginRemoveRows(QModelIndex(), row, row+1)
            del self.items[row]
            self.endRemoveRows()

    def flags(self, index):
        return super(TreeViewModel, self).flags(index) | Qt.ItemIsEditable

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            self.items[index.row()][index.column()] = value
            return True
        return False

    def chk_duplicate(self):
        for i in range(len(self.items)):
            for k in range(len(self.items)-i-1):
                if self.items[i][2] == self.items[-k-1][2] \
                   and self.items[i][3] == self.items[-k-1][3] \
                   and self.items[i][4] == self.items[-k-1][4]:
                   return True
                   break
        return False

    def chk_filled(self):
        for i in range(len(self.items)):
            for k in range(1, 8):
                if self.items[i][k] == "":
                    return True
                    break
        return False

    def values(self, i):
        return self.items[i][0], \
               float(eval(self.items[i][1])), \
               float(eval(self.items[i][2])), \
               float(eval(self.items[i][3])), \
               float(eval(self.items[i][4])), \
               float(eval(self.items[i][5])), \
               float(eval(self.items[i][6])), \
               float(eval(self.items[i][7]))

class ValidateLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(ValidateLineEdit, self).__init__(parent)

        regexp = QRegExp("[0-9e\.\+\-\*\(\)/]*")
        validator = QRegExpValidator(regexp)
        self.setValidator(validator)


class Delegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(Delegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        if index.column() == 0:
            return QLineEdit(parent)
        else:
            return ValidateLineEdit(parent)#QLineEdit(parent)

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole)
        editor.setText(str(value))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())

"""
Main Window Class
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Kepler Manager")

        self.viewer = Viewer()
        self.viewer3d = Viewer3D()
        self.tableViewer = TableViewer()
        self.caldialog = CalDialog()
        self.errdialog = ErrDialog()
        self.cal_stop = False

        regexp = QRegExp("[0-9e\.\+\-\*\(\)/]*")
        validator = QRegExpValidator(regexp)

        self.ui.lineEdit_G.setValidator(validator)
        self.ui.lineEdit_TimeIncrement.setValidator(validator)
        self.ui.lineEdit_StopTime.setValidator(validator)
        #self.ui.actionAbout_Kepler.triggered.connect(self.about_Kepler)
        #self.ui.actionPreference.triggered.connect(self.preference)
        self.ui.actionSave.triggered.connect(self.save_file)
        self.ui.actionLoad_your_settings.triggered.connect(self.load_file)
        self.ui.actionLoad_SOL.triggered.connect(self.load_SOL)
        self.ui.actionViewer.triggered.connect(self.open_viewer)
        #self.ui.actionTable_Viewer.triggered.connect(self.open_tableviewer)
        #self.ui.actionHow_to_use.triggered.connect(self.show_help)
        #self.ui.actionHow_does_this_work.triggered.connect(self.show_mechanism)

        #self.ui.comboBox_Choose2Dor3D.currentIndexChanged.connect(self.choose2dor3d)
        self.ui.pushButton_AddPlanet.clicked.connect(self.add_planet)
        self.ui.pushButton_DeletePlanet.clicked.connect(self.remove_planets)

        self.ui.lineEdit_G.setText("6.674e-11")

        self.ui.pushButton_Calc.clicked.connect(self.calc)

        self.planets_attribute = TreeViewModel()
        self.planets = Planet_system()
        self.resultcontainer = ResultContainer()

        self.ui.treeView_PlanetAttribute.setModel(self.planets_attribute)
        self.ui.treeView_PlanetAttribute.setItemDelegate(Delegate())

    def add_planet(self):
        self.planets_attribute.addRow("","0","0","0","0","0","0","0")

    def add_planet_from_f(self, name, mass, x0, y0, z0, vx0, vy0, vz0):
        self.planets_attribute.addRow(name, mass, x0, y0, z0, vx0, vy0, vz0)

    def selected_rows(self):
        rows = []
        for index in self.ui.treeView_PlanetAttribute.selectedIndexes():
            if index.column() == 0:
                rows.append(index.row())
        return rows

    def remove_planets(self):
        self.planets_attribute.removeRows(self.selected_rows())

    def calc(self):
        if self.ui.lineEdit_G.text() == ""\
           or self.ui.lineEdit_TimeIncrement.text() == ""\
           or self.ui.lineEdit_StopTime.text() == "":
            pass
        elif self.planets_attribute.chk_duplicate():
            self.errdialog.setWindowTitle("Error Message")
            self.errdialog.ui.label_ErrMSG.setText("Initial position is a duplicate")
            self.errdialog.show()
            self.errdialog.ui.pushButton_ErrOK.clicked.connect(self.errdialog.close)
            pass
        elif self.planets_attribute.chk_filled():
            pass
        else:
            for i in range(len(self.planets)):
                self.planets.del_planet(-1)
            dt = float(eval(self.ui.lineEdit_TimeIncrement.text()))
            end = float(eval(self.ui.lineEdit_StopTime.text()))
            sum_step = int(end // dt + 1)
            G = float(eval(self.ui.lineEdit_G.text()))
            if len(self.planets_attribute.items) >= 2:
                self.caldialog.ui.progressBar_Cal.setRange(0, sum_step)
                self.caldialog.ui.pushButton_CalStop.clicked.connect(self.cal_rupt)
                self.caldialog.show()
                if self.ui.comboBox_Choose2Dor3D.currentText() == "2D":
                    for i in range(len(self.planets_attribute.items)):
                        name, mass, x0, y0, z0, vx0, vy0, vz0 = self.planets_attribute.values(i)
                        self.planets.add_planet(name, mass, x0, y0, z0, vx0, vy0, vz0)
                    for i in range(sum_step):
                        if self.cal_stop:
                            for k in range(len(self.planets)):
                                del self.planets[k]
                            self.caldialog.close()
                            self.cal_stop = False
                            break
                        self.caldialog.ui.progressBar_Cal.setValue(i)
                        RK4(self.planets, dt, i, G)
                        #print(i)
                    self.resultcontainer.load_from_ps(dt, end, True, self.planets)
                    self.caldialog.close()
                    self.open_viewer()
                    self.viewer.set_result(self.resultcontainer.results)

                else:
                    for i in range(len(self.planets_attribute.items)):
                        name, mass, x0, y0, z0, vz0, vy0, vz0 = self.planets_attribute.values(i)
                        self.planets.add_planet(name, mass, x0, y0, z0, vz0, vy0, vz0)
                    for i in range(sum_step):
                        if self.cal_stop:
                            for k in range(len(self.planets)):
                                del self.planets[k]
                            self.caldialog.close()
                            self.cal_stop = False
                            break
                        self.caldialog.ui.progressBar_Cal.setValue(i)
                        RK4z(self.planets, dt, i, G)
                    self.resultcontainer.load_from_ps(dt, end, False, self.planets)
                    self.caldialog.close()
                    self.open_viewer()
                    self.viewer.set_result(self.resultcontainer.results)
            else:
                pass

    def load_file(self):
        filedialog = QFileDialog()
        filedialog.setDirectory("./settings")
        filepath = filedialog.getOpenFileName(filter="Kepler Planet Settings (*.kps)")
        if filepath == "":
            pass
        else:
            with open(filepath, "r") as f:
                file = json.load(f)
            self.planets_attribute.items = []
            for i in range(len(file)):
                self.add_planet_from_f(file[i][0],\
                                       file[i][1],\
                                       file[i][2],\
                                       file[i][3],\
                                       file[i][4],\
                                       file[i][5],\
                                       file[i][6],\
                                       file[i][7])

    def load_SOL(self):
        with open("./settings/SOL.kps", "r") as f:
            file = json.load(f)
        self.planets_attribute.items = []
        for i in range(len(file)):
            self.add_planet_from_f(file[i][0],\
                                   file[i][1],\
                                   file[i][2],\
                                   file[i][3],\
                                   file[i][4],\
                                   file[i][5],\
                                   file[i][6],\
                                   file[i][7])

    def save_file(self):
        filedialog = QFileDialog()
        filedialog.setDirectory("./settings")
        filepath = filedialog.getSaveFileName(filter="Kepler Planet Settings (*.kps)")
        if filepath == "":
            pass
        else:
            with open(filepath, "w") as f:
                json.dump(self.planets_attribute.items, f, sort_keys=True, indent=4)

    def cal_rupt(self):
        self.cal_stop = True

    def open_viewer(self):
        self.viewer.show()

    def open_viewer3d(self):
        self.viewer3d.show()

class CalDialog(QDialog):
    def __init__(self, parent=MainWindow):
        super(CalDialog, self).__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_CalDialog()
        self.ui.setupUi(self)

        self.setWindowTitle("Progress of Calculation")

class Viewer(QMainWindow):
    def __init__(self, parent=MainWindow):
        super(Viewer, self).__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_ViewerManager()
        self.ui.setupUi(self)

        self.setWindowTitle("Kepler Viewer")
        
        regexp = QRegExp("[0-9e\.\+\-\*\(\)/]*")
        validator = QRegExpValidator(regexp)

        self.plot_widget = []#Plot()
        self.plot3d_widget = []#Plot3D()
        self.resultcontainer = ResultContainer()
        self.planets_attribute = TreeViewModel()
        self.timer = QTimer()
        self.planets_attribute.items=[]
        #self.plot_widget.plotw.append(pg.GraphicsLayoutWidget())
        self.ui.lineEdit_Time.setValidator(validator)

        self.ui.treeView_PlanetAttribute.setModel(self.planets_attribute)
        self.ui.pushButton_showtime.clicked.connect(self.show_arrow_here)
        self.ui.actionSave.triggered.connect(self.save_file)
        self.ui.actionLoad.triggered.connect(self.load_file)
        self.plot = []
        self.plot_xy = []
        self.plot_xz = []
        self.plot_yz = []
        self.arrow = []
        self.text = []
        self.arrow_xy = []
        self.text_xy = []
        self.arrow_xz = []
        self.text_xz = []
        self.arrow_yz = []
        self.text_yz = []
        self.initarrow = []
        self.inittext = []
        self.initarrow_xy = []
        self.inittext_xy = []
        self.initarrow_xz = []
        self.inittext_xz = []
        self.initarrow_yz = []
        self.inittext_yz = []
        self.arrow_here_xy = []
        #self.text_here_xy = []
        self.arrow_here_xz = []
        #self.text_here_xz = []
        self.arrow_here_yz = []
        #self.text_here_yz = []
        self.anim = []
        self.anim_xy = []
        self.anim_xz = []
        self.anim_yz = []
        self.pos = []
        self.plot_3d = []
        self.timeindex = 0

    def add_planet(self, name, mass, x0, y0, z0, vx0, vy0, vz0):
        self.planets_attribute.addRow(name, mass, x0, y0, z0, vx0, vy0, vz0)

    def selected_rows(self):
        rows = []
        for index in self.ui.treeView_PlanetAttribute.selectedIndexes():
            if index.column() == 0:
                rows.append(index.row())
        return rows

    def remove_planets(self, i):
        self.planets_attribute.removeRows(i)

    def set_result(self, result):
        self.resultcontainer.load_from_result(result)
        self.planets_attribute.items = []
        for i in range(len(result["planets"])):
            self.add_planet(result["planets"][i]["name"],\
                            result["planets"][i]["mass"],\
                            result["planets"][i]["x"][0],\
                            result["planets"][i]["y"][0],\
                            result["planets"][i]["z"][0],\
                            result["planets"][i]["vx"][0],\
                            result["planets"][i]["vy"][0],\
                            result["planets"][i]["vz"][0])
        self.plot = []
        self.plot_xy = []
        self.plot_xz = []
        self.plot_yz = []
        self.arrow = []
        self.text = []
        self.arrow_xy = []
        self.text_xy = []
        self.arrow_xz = []
        self.text_xz = []
        self.arrow_yz = []
        self.text_yz = []
        self.initarrow = []
        self.inittext = []
        self.initarrow_xy = []
        self.inittext_xy = []
        self.initarrow_xz = []
        self.inittext_xz = []
        self.initarrow_yz = []
        self.inittext_yz = []
        self.arrow_here_xy = []
        #self.text_here_xy = []
        self.arrow_here_xz = []
        #self.text_here_xz = []
        self.arrow_here_yz = []
        #self.text_here_yz = []
        self.anim = []
        self.anim_xy = []
        self.anim_xz = []
        self.anim_yz = []
        self.pos = []
        self.plot_3d = []
        self.timeindex = 0
        self.plot_result()

    def load_file(self):
        filedialog = QFileDialog()
        filedialog.setDirectory("./results")
        filepath = filedialog.getOpenFileName(filter="Kepler Result Data (*.krd)")
        if filepath == "":
            pass
        else:
            self.planets_attribute.items = []
            with open(filepath, "r") as f:
                file = json.load(f)
            self.set_result(file)

    def save_file(self):
        filedialog = QFileDialog()
        filedialog.setDirectory("./results")
        filepath = filedialog.getSaveFileName(filter="Kepler Result Data (*.krd)")
        if filepath == "":
            pass
        else:
            with open(filepath, "w") as f:
                json.dump(self.resultcontainer.results, f, sort_keys=True, indent=4)


    def plot_result(self):
        self.plot_widget.append(Plot())
        self.plot3d_widget.append(gl.GLViewWidget())#(GLViewer())#(Plot3D())
        if len(self.plot_widget) >= 2:
            self.plot_widget.pop(0)
        if len(self.plot3d_widget) >= 2:
            self.plot3d_widget.pop(0)
        if self.resultcontainer.results["dim"]:#self.resultcontainer.chk_2dor3d == True:
            self.plot_widget[-1].show()
            p = self.plot_widget[-1].plotw.addPlot(row=0, col=0)
            p.addLegend()
            p.showGrid(True, True)
            for i in range(len(self.resultcontainer.results["planets"])):
                self.plot.append(p.plot(x=self.resultcontainer.results["planets"][i]["x"],\
                                        y=self.resultcontainer.results["planets"][i]["y"],\
                                        pen=(255/len(self.resultcontainer.results["planets"])*(i+1),
                                             255/len(self.resultcontainer.results["planets"])*i,
                                             255/len(self.resultcontainer.results["planets"])*(len(self.resultcontainer.results["planets"])-i-1)),\
                                        name=self.resultcontainer.results["planets"][i]["name"]))
                self.arrow.append(pg.CurveArrow(self.plot[i]))
                self.text.append(pg.TextItem(self.resultcontainer.results["planets"][i]["name"], anchor=(0.5, -1.0)))
                #self.arrow.append(pg.ArrowItem())
                self.initarrow.append(pg.ArrowItem())
                self.inittext.append(pg.TextItem(self.resultcontainer.results["planets"][i]["name"]+" Init",anchor=(0.5, -1.0)))
                self.arrow_here_xy.append(pg.ArrowItem())
                #self.text_here_xy.append(pg.TextItem("Here", anchor=(0.5, -1.0)))
                self.initarrow[i].setPos(self.resultcontainer.results["planets"][i]["x"][0],\
                                         self.resultcontainer.results["planets"][i]["y"][0])
                self.inittext[i].setPos(self.resultcontainer.results["planets"][i]["x"][0],\
                                        self.resultcontainer.results["planets"][i]["y"][0])
                #p.addItem(arrow[i])
                self.text[i].setParentItem(self.arrow[i])
                self.initarrow[i].setParentItem(self.plot[i])
                p.addItem(self.inittext[i])
                self.arrow_here_xy[i].setParentItem(self.plot[i])
                #p.addItem(initarrow[i])
                self.anim.append(self.arrow[i].makeAnimation(loop=-1))
            for i in range(len(self.resultcontainer.results["planets"])):
                self.anim[i].start()
        else:
            self.plot_widget[-1].resize(450,900)
            self.plot_widget[-1].show()
            p_xy = self.plot_widget[-1].plotw.addPlot(row=0, col=0)
            p_xz = self.plot_widget[-1].plotw.addPlot(row=1, col=0)
            p_yz = self.plot_widget[-1].plotw.addPlot(row=2, col=0)
            p_xy.addLegend()
            #p_xz.addLegend()
            #p_yz.addLegend()
            p_xy.setLabel('left',"Y")
            p_xy.setLabel('bottom',"X")
            p_xz.setLabel('left',"Z")
            p_xz.setLabel('bottom',"X")
            p_yz.setLabel('left',"Z")
            p_yz.setLabel('bottom',"Y")
            p_xy.showGrid(True, True)
            p_xz.showGrid(True, True)
            p_yz.showGrid(True, True)
            for i in range(len(self.resultcontainer.results["planets"])):
                self.plot_xy.append(p_xy.plot(self.resultcontainer.results["planets"][i]["x"],\
                                              self.resultcontainer.results["planets"][i]["y"],\
                                              pen=(255/len(self.resultcontainer.results["planets"])*(i+1),
                                                   255/len(self.resultcontainer.results["planets"])*i,
                                                   255/len(self.resultcontainer.results["planets"])*(len(self.resultcontainer.results["planets"])-i-1)),\
                                              name=self.resultcontainer.results["planets"][i]["name"]))
                self.plot_xz.append(p_xz.plot(self.resultcontainer.results["planets"][i]["x"],\
                                              self.resultcontainer.results["planets"][i]["z"],\
                                              pen=(255/len(self.resultcontainer.results["planets"])*(i+1),
                                                   255/len(self.resultcontainer.results["planets"])*i,
                                                   255/len(self.resultcontainer.results["planets"])*(len(self.resultcontainer.results["planets"])-i-1)),\
                                              name=self.resultcontainer.results["planets"][i]["name"]))
                self.plot_yz.append(p_yz.plot(self.resultcontainer.results["planets"][i]["y"],\
                                              self.resultcontainer.results["planets"][i]["z"],\
                                              pen=(255/len(self.resultcontainer.results["planets"])*(i+1),
                                                   255/len(self.resultcontainer.results["planets"])*i,
                                                   255/len(self.resultcontainer.results["planets"])*(len(self.resultcontainer.results["planets"])-i-1)),\
                                              name=self.resultcontainer.results["planets"][i]["name"]))
                self.arrow_xy.append(pg.CurveArrow(self.plot_xy[i]))
                self.arrow_xz.append(pg.CurveArrow(self.plot_xz[i]))
                self.arrow_yz.append(pg.CurveArrow(self.plot_yz[i]))
                self.text_xy.append(pg.TextItem(self.resultcontainer.results["planets"][i]["name"], anchor=(0.5, -1.0)))
                self.text_xz.append(pg.TextItem(self.resultcontainer.results["planets"][i]["name"], anchor=(0.5, -1.0)))
                self.text_yz.append(pg.TextItem(self.resultcontainer.results["planets"][i]["name"], anchor=(0.5, -1.0)))
                self.initarrow_xy.append(pg.ArrowItem())
                self.initarrow_xz.append(pg.ArrowItem())
                self.initarrow_yz.append(pg.ArrowItem())
                self.inittext_xy.append(pg.TextItem(self.resultcontainer.results["planets"][i]["name"]+" Init",anchor=(0.5, -1.0)))
                self.inittext_xz.append(pg.TextItem(self.resultcontainer.results["planets"][i]["name"]+" Init",anchor=(0.5, -1.0)))
                self.inittext_yz.append(pg.TextItem(self.resultcontainer.results["planets"][i]["name"]+" Init",anchor=(0.5, -1.0)))
                self.arrow_here_xy.append(pg.ArrowItem())
                self.arrow_here_xz.append(pg.ArrowItem())
                self.arrow_here_yz.append(pg.ArrowItem())
                #self.text_here_xy.append(pg.TextItem("Here", anchor=(0.5, -1.0)))
                #self.text_here_xz.append(pg.TextItem("Here", anchor=(0.5, -1.0)))
                #self.text_here_yz.append(pg.TextItem("Here", anchor=(0.5, -1.0)))
                self.initarrow_xy[i].setPos(self.resultcontainer.results["planets"][i]["x"][0],\
                                            self.resultcontainer.results["planets"][i]["y"][0])
                self.initarrow_xz[i].setPos(self.resultcontainer.results["planets"][i]["x"][0],\
                                            self.resultcontainer.results["planets"][i]["z"][0])
                self.initarrow_yz[i].setPos(self.resultcontainer.results["planets"][i]["y"][0],\
                                            self.resultcontainer.results["planets"][i]["z"][0])
                self.inittext_xy[i].setPos(self.resultcontainer.results["planets"][i]["x"][0],\
                                           self.resultcontainer.results["planets"][i]["y"][0])
                self.inittext_xz[i].setPos(self.resultcontainer.results["planets"][i]["x"][0],\
                                           self.resultcontainer.results["planets"][i]["z"][0])
                self.inittext_yz[i].setPos(self.resultcontainer.results["planets"][i]["y"][0],\
                                           self.resultcontainer.results["planets"][i]["z"][0])
                self.text_xy[i].setParentItem(self.arrow_xy[i])
                self.text_xz[i].setParentItem(self.arrow_xz[i])
                self.text_yz[i].setParentItem(self.arrow_yz[i])
                self.initarrow_xy[i].setParentItem(self.plot_xy[i])
                self.initarrow_xz[i].setParentItem(self.plot_xz[i])
                self.initarrow_yz[i].setParentItem(self.plot_yz[i])
                p_xy.addItem(self.inittext_xy[i])
                p_xz.addItem(self.inittext_xz[i])
                p_yz.addItem(self.inittext_yz[i])
                self.arrow_here_xy[i].setParentItem(self.plot_xy[i])
                self.arrow_here_xz[i].setParentItem(self.plot_xz[i])
                self.arrow_here_yz[i].setParentItem(self.plot_yz[i])
                self.anim_xy.append(self.arrow_xy[i].makeAnimation(loop=-1))
                self.anim_xz.append(self.arrow_xz[i].makeAnimation(loop=-1))
                self.anim_yz.append(self.arrow_yz[i].makeAnimation(loop=-1))
            for i in range(len(self.resultcontainer.results["planets"])):
                self.anim_xy[i].start()
                self.anim_xz[i].start()
                self.anim_yz[i].start()
            self.plot3d_widget[-1].show()
            #self.plot3d_widget[-1].opts['distance'] = 2000
            gx = gl.GLGridItem()
            gx.rotate(90, 0, 1, 0)
            #gx.scale(10,10,10)
            #gx.translate(-10, 0, 0)
            self.plot3d_widget[-1].addItem(gx)#.glplotw.addItem(gx)
            ax = gl.GLAxisItem(antialias=True)
            self.plot3d_widget[-1].addItem(ax)
            gy = gl.GLGridItem()
            gy.rotate(90, 1, 0, 0)
            #gy.translate(0, -10, 0)
            self.plot3d_widget[-1].addItem(gy)#.glplotw.addItem(gy)
            gz = gl.GLGridItem()
            #gz.translate(0, 0, -10)
            self.plot3d_widget[-1].addItem(gz)#.glplotw.addItem(gz)
            for i in range(len(self.resultcontainer.results["planets"])):
                self.pos.append([])
                x = np.array(self.resultcontainer.results["planets"][i]["x"])
                y = np.array(self.resultcontainer.results["planets"][i]["y"])
                z = np.array(self.resultcontainer.results["planets"][i]["z"])
                """self.pos[i] = np.vstack([self.resultcontainer.results["planets"][i]["x"],
                                         self.resultcontainer.results["planets"][i]["y"],
                                         self.resultcontainer.results["planets"][i]["z"]]).transpose()
                """
                self.pos[i] = np.vstack([x,y,z]).transpose()
                self.plot_3d.append(gl.GLLinePlotItem(pos=self.pos[i],\
                                                      color=pg.glColor(255/len(self.resultcontainer.results["planets"])*(i+1),
                                                                       255/len(self.resultcontainer.results["planets"])*i,
                                                                       255/len(self.resultcontainer.results["planets"])*(len(self.resultcontainer.results["planets"])-i-1)),\
                                                      width=1.0,\
                                                      antialias=True))
                self.plot3d_widget[-1].addItem(self.plot_3d[i])#.glplotw.addItem(self.plot_3d[i])
                self.plot3d_widget[-1].qglColor(Qt.white)
                self.plot3d_widget[-1].renderText(self.resultcontainer.results["planets"][i]["x"][0],\
                                                  self.resultcontainer.results["planets"][i]["y"][0],\
                                                  self.resultcontainer.results["planets"][i]["z"][0],\
                                                  self.resultcontainer.results["planets"][i]["name"])
                """for k in range(len(self.resultcontainer.results["planets"][i]["x"])):
                    self.pos[i].append([self.resultcontainer.results["planets"][i]["x"][k],
                                        self.resultcontainer.results["planets"][i]["y"][k],
                                        self.resultcontainer.results["planets"][i]["z"][k]])
                self.plot_3d.append(gl.GLLinePlotItem(pos=self.pos[i], antialias=True))
                self.plot3d_widget[-1].glplotw.addItem(self.plot_3d[i])"""
                """for k in range(len(self.resultcontainer.results["planets"][i]["x"])):
                    pts = np.vstack([self.resultcontainer.results["planets"][i]["x"][k],
                                     self.resultcontainer.results["planets"][i]["y"][k],
                                     self.resultcontainer.results["planets"][i]["z"][k]])
                    plt = gl.GLLinePlotItem(pos=pts, antialias=True)
                    self.plot3d_widget[-1].glplotw.addItem(plt)"""


    def show_arrow_here(self):
        time = float(eval(self.ui.lineEdit_Time.text()))
        if time >= self.resultcontainer.results["end"]:
            time = self.resultcontainer.results["end"]
        step = int(time // self.resultcontainer.results["dt"])
        self.ui.lineEdit_Time.setText(str(step * self.resultcontainer.results["dt"]))
        if self.resultcontainer.results["dim"]:
            for i in range(len(self.resultcontainer.results["planets"])):
                self.arrow_here_xy[i].setPos(self.resultcontainer.results["planets"][i]["x"][step],\
                                             self.resultcontainer.results["planets"][i]["y"][step])
                #self.text_here_xy[i].setPos(self.resultcontainer.results["planets"][i]["x"][step],\
                #                            self.resultcontainer.results["planets"][i]["y"][step])
                """self.text_here_xy[i].setText('[%0.1f]'%(step*self.resultcontainer.results["dt"]))"""
        else:
            for i in range(len(self.resultcontainer.results["planets"])):
                self.arrow_here_xy[i].setPos(self.resultcontainer.results["planets"][i]["x"][step],\
                                             self.resultcontainer.results["planets"][i]["y"][step])
                self.arrow_here_xz[i].setPos(self.resultcontainer.results["planets"][i]["x"][step],\
                                             self.resultcontainer.results["planets"][i]["z"][step])
                self.arrow_here_yz[i].setPos(self.resultcontainer.results["planets"][i]["y"][step],\
                                             self.resultcontainer.results["planets"][i]["z"][step])
                #self.text_here_xy[i].setPos(self.resultcontainer.results["planets"][i]["x"][step],\
                #                            self.resultcontainer.results["planets"][i]["y"][step])
                #self.text_here_xz[i].setPos(self.resultcontainer.results["planets"][i]["x"][step],\
                #                            self.resultcontainer.results["planets"][i]["z"][step])
                #self.text_here_yz[i].setPos(self.resultcontainer.results["planets"][i]["y"][step],\
                #                            self.resultcontainer.results["planets"][i]["z"][step])


class Plot(QMainWindow):
    def __init__(self, parent=Viewer):
        super(Plot, self).__init__()
        self.plotw = pg.GraphicsLayoutWidget()
        #self.plotw.append(pg.GraphicsLayoutWidget())
        self.setCentralWidget(self.plotw)
        self.setWindowTitle("Kepler Viewer")

class Plot3D(QMainWindow):
    def __init__(self, parent=Viewer):
        super(Plot3D, self).__init__()
        self.glplotw = gl.GLViewWidget()
        self.setCentralWidget(self.glplotw)
        self.setWindowTitle("Kepler Viewer (3D)")

class Viewer3D(QMainWindow):
    def __init__(self, parent=MainWindow):
        super(Viewer3D, self).__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_PG3DViewer()
        self.ui.setupUi(self)

        self.setWindowTitle("Kepler Viewer")
        
        self.plot = []
        
"""class GLViewer(gl.GLViewWidget):
    def paintGL(self, *args, **kwds):
        gl.GLViewWidget.paintGL(self, *args, **kwds)
        self.qglColor(Qt.white)"""

class TableViewer(QMainWindow):
    def __init__(self, Parent=MainWindow):
        super(TableViewer, self).__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_TableViewer()
        self.ui.setupUi(self)

        self.setWindowTitle("Kepler Table Viewer")

class ErrDialog(QDialog):
    def __init__(self):
        super(ErrDialog, self).__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_ErrDialog()
        self.ui.setupUi(self)

class ResultContainer():
    def __init__(self):
        self.results = {"dt": None,
                        "end": None,
                        "dim": None,
                        "planets": []}

    def load_from_ps(self, dt, end, dim, Planet_system):
        self.results["dt"] = dt
        self.results["end"] = end
        self.results["dim"] = dim
        self.results["planets"] = []
        for i in range(len(Planet_system)):
            self.results["planets"].append({"name": Planet_system[i].name,
                                            "mass": Planet_system[i].mass,
                                            "x": Planet_system[i].x,
                                            "y": Planet_system[i].y,
                                            "z": Planet_system[i].z,
                                            "vx": Planet_system[i].vx,
                                            "vy": Planet_system[i].vy,
                                            "vz": Planet_system[i].vz })

    def load_from_result(self, result):
        self.results["dt"] = result["dt"]
        self.results["end"] = result["end"]
        self.results["dim"] = result["dim"]
        self.results["planets"] = result["planets"]

    def chk_2dor3d(self):
        sum_z = 0
        for i in range(len(self.results["planets"])):
            for k in range(1, len(self.results["planets"][i]["x"])):
                sum_z += abs(self.results["planets"][i]["z"][k])
        if sum_z == 0:
            return True
        else:
            return False


def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()