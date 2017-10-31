# -*- coding: utf-8 -*-

import sys
import json
import matplotlib.pyplot as plt
from libs.Interface.template import QtGui, QtCore, Ui_MainWindow
from libs.Interface.dialog import Ui_Dialog as Dialog
from libs.Polygon.polygon import Polygon
from libs.Document.documentTemplate import Document


T_VERT = 0
T_ANGS = 1
T_AZIMUT = 2
T_LADOS = 3
T_COORD_X = 4
T_COORD_Y = 5


class NewTemplate(Dialog):
    def __init__(self):
        self.dial = QtGui.QDialog()
        Dialog.setupUi(self, self.dial)


class MainWindow(Ui_MainWindow):
    def __init__(self):
        self.ui = QtGui.QMainWindow()
        Ui_MainWindow.setupUi(self, self.ui)

        # Columns name of Table result
        vert = 'Vert.'
        angs = 'Angulos internos\n º    \'    "'.decode('utf-8')
        azimut = 'Rumbos'
        lados = 'Lados'
        coord_x = 'Coordenadas x'
        coord_y = 'Coordenadas y'
        l1 = [vert, angs, azimut, lados, coord_x, coord_y]

        # Setup headers of tables
        self.tableResult.setColumnCount(len(l1))
        self.tableResult.setHorizontalHeaderLabels(l1)
        self.tableResult.resizeColumnsToContents()
        self.tableResult.resizeRowsToContents()

        # Function for buttons
        # New file
        QtCore.QObject.connect(self.actionNew, QtCore.SIGNAL('triggered()'),
                               self.dialog_new)
        # Save as
        QtCore.QObject.connect(self.actionSave_as,
                               QtCore.SIGNAL('triggered()'), self.save_as)
        # Save
        QtCore.QObject.connect(self.actionSave, QtCore.SIGNAL('triggered()'),
                               self.save)
        # Open file
        QtCore.QObject.connect(self.actionOpen, QtCore.SIGNAL('triggered()'),
                               self.open_file)
        # Update a data
        QtCore.QObject.connect(self.actionEdit, QtCore.SIGNAL('triggered()'),
                               self.update_data)
        # Generate PDF
        QtCore.QObject.connect(self.actionToPdf, QtCore.SIGNAL('triggered()'),
                               self.dialog_genPdf)
        # Calculate angle, azimuths, bearings, area
        QtCore.QObject.connect(self.calcBtn, QtCore.SIGNAL('clicked()'),
                               self.calculate)

        # data of polygon
        self.data = dict()
        self.data_empty()

    def dialog_genPdf(self):
        filename = QtGui.QFileDialog.getSaveFileName(
            self.ui, "Exportar como...", filter="*.pdf")
        if filename:
            f = str(filename)
            if not f.endswith('.pdf'):
                f = f + '.pdf'
            d = Document()
            self.data['title'] = "<u>PLANILLA DE CÁLCULO DE \
                COORDENADAS Y SUPERFICIE</u>"
            self.get_vertices()
            d.save(f, self.data)

    def calculate(self):
        self.data['coords'] = self.get_coords()
        if self.data['coords']:
            p = Polygon()
            p.polygon_from_list(self.data['coords'])
            self.data['angs'] = p.origin_list(p.angles())
            self.data['azimuths'] = p.azimuths()
            edges = p.edges()
            edges.reverse()
            self.data['edges'] = edges
            self.data['area'] = p.area()
            if self.data['edges']:
                self.data['perim'] = sum(self.data['edges'])
            if self.data['angs']:
                self.data['sum_angs'] = sum(self.data['angs'])
            self.get_vertices()
            self.show_data()

    def get_coords(self):
        n = self.tableResult.rowCount()
        coordinates = []
        for i in range(n):
            tmp_x = str(self.tableResult.item(i, T_COORD_X).text())
            x = float(tmp_x)
            tmp_y = str(self.tableResult.item(i, T_COORD_Y).text())
            y = float(tmp_y)
            coordinates.append((x, y))
        return coordinates

    def get_vertices(self):
        n = self.tableResult.rowCount()
        self.data['vertices'] = []
        for i in range(n):
            vert = str(self.tableResult.item(i, T_VERT).text())
            self.data['vertices'].append(vert)

    def show_data(self):
        # self.get_vertices()
        self.clear_table()
        # print "VERTICES", self.data['vertices']
        self.perito.setText(self.data["proficient"])
        self.plane_of.setText(self.data['plane_of'])
        self.location.setText(self.data['location'])
        self.possession.setText(self.data['possession'])
        self.homeowner.setText(self.data['homeowner'])
        self.date.setText(self.data['date'])
        n = len(self.data['coords'])
        p = Polygon()
        for i in range(n):
            if self.data['coords']:
                x, y = self.data['coords'][i]
                self.tableResult.insertRow(i)
                self.tableResult.setItem(i, T_COORD_X,
                                         QtGui.QTableWidgetItem(str(x)))
                self.tableResult.setItem(i, T_COORD_Y,
                                         QtGui.QTableWidgetItem(str(y)))
                if not self.data['vertices']:
                    self.tableResult.setItem(i, T_VERT,
                                            QtGui.QTableWidgetItem(str(i)))
                else:
                    v = self.data['vertices'][i]
                    self.tableResult.setItem(i, T_VERT,
                                            QtGui.QTableWidgetItem(str(v)))
            if self.data['angs']:
                d1, m1, s1 = p.decdeg2dms(self.data['angs'][i])
                # a = "%d  %d  %s" % (int(d1), int(m1), "{0:.2f}".format(s1))
                a = "%d  %d  %d" % (int(d1), int(m1), int(round(s1)))
                self.tableResult.setItem(i, T_ANGS,
                                         QtGui.QTableWidgetItem(
                                             a.decode('utf-8')))
            if self.data['azimuths']:
                d2, m2, s2 = p.decdeg2dms(self.data['azimuths'][i])
                az = "%d  %d  %d" % (int(d2), int(m2), int(round(s2)))
                self.tableResult.setItem(i, T_AZIMUT,
                                         QtGui.QTableWidgetItem(
                                             az.decode('utf-8')))
            if self.data['edges']:
                b = "{0: .2f}".format(self.data['edges'][i])
                self.tableResult.setItem(i, T_LADOS,
                                         QtGui.QTableWidgetItem(b))
        area = "{0: .2f}".format(self.data['area'])
        self.label_area.setText(area)
        per = "{0: .2f}".format(self.data['perim'])
        self.label_perim.setText(per)
        sang = "{0: .2f}".format(self.data['sum_angs'])
        self.label_sumAngs.setText(sang)
        self.showGraph()

        self.tableResult.resizeColumnsToContents()
        self.tableResult.resizeRowsToContents()

    def showGraph(self):
        plt.cla()
        ax = self.figure.add_subplot(111)
        if self.data['coords']:
            xs = []
            ys = []
            for x, y in self.data['coords']:
                tmp = str(x).split('.')
                s1 = tmp[0] + '.' + tmp[1]
                if len(tmp[0]) > 4:
                    s1 = tmp[0][-3:] + '.' + tmp[1]
                tmp = str(y).split('.')
                s2 = tmp[0] + '.' + tmp[1]
                if len(tmp[0]) > 4:
                    s2 = tmp[0][-3:] + '.' + tmp[1]
                xs.append(float(s1))
                ys.append(float(s2))
            tmp = str(self.data['coords'][0][0]).split('.')
            lastx = tmp[0] + '.' + tmp[1]
            if len(tmp[0]) > 4:
                lastx = tmp[0][-3:] + '.' + tmp[1]
            tmp = str(self.data['coords'][0][1]).split('.')
            lasty = tmp[0] + '.' + tmp[1]
            if len(tmp[0]) > 4:
                lasty = tmp[0][-3:] + '.' + tmp[1]
            xs.append(float(lastx))
            ys.append(float(lasty))
            ax.plot(ys, xs, '.-')
            ax.set_title('Poligono')
            self.canvas.draw()

    def clear_table(self):
        for i in range(self.tableResult.rowCount()):
            self.tableResult.removeRow(0)

    def data_empty(self):
        self.data['vertices'] = []
        self.data['coords'] = []
        self.data['angs'] = []
        self.data['azimuths'] = []
        self.data['edges'] = []
        self.data['area'] = 0
        self.data['perim'] = 0
        self.data['sum_angs'] = 0
        self.data['plane_of'] = ''
        # self.data['proficient'] = 'Ing. COPA, Rodi Alfredo'
        self.data['proficient'] = ''
        self.data['location'] = ''
        self.data['possession'] = ''
        self.data['homeowner'] = ''
        self.data['date'] = ''
        self.data['filename'] = ''
        self.data['title'] = ''

    def dialog_new(self):
        ui = NewTemplate()
        ui.dial.exec_()
        if ui.dial.result():
            self.data_from_dialog(ui)

    def save_as(self):
        filename = QtGui.QFileDialog.getSaveFileName(
            self.ui, "Guardar como...", filter="*.json")
        if filename:
            if str(filename).endswith('.json'):
                self.data['filename'] = str(filename).strip()
            else:
                self.data['filename'] = str(filename).strip() + '.json'
            self.get_vertices()
            with open(self.data['filename'], 'w') as f:
                json.dump(self.data, f)

    def save(self):
        self.get_vertices()
        if self.data['filename']:
            with open(self.data['filename'], 'w') as f:
                json.dump(self.data, f)
        else:
            self.save_as()

    def open_file(self):
        filename = QtGui.QFileDialog.getOpenFileName(
            self.ui, 'Abrir archivo...', filter='*.json')
        if filename:
            if str(filename).endswith('json'):
                with open(str(filename), 'r') as f:
                    self.data = json.load(f)
                    self.show_data()

    def update_data(self):
        ui = NewTemplate()

        ui.perito.setText(self.data['proficient'])
        ui.plane_of.setText(self.data['plane_of'])
        ui.location.setText(self.data['location'])
        ui.possession.setText(self.data['possession'])
        ui.homeowner.setText(self.data['homeowner'])
        ui.date.setText(self.data['date'])
        coords_text = ''
        for x, y in self.data['coords']:
            coords_text += str(x) + ' ' + str(y) + '\n'
        ui.coordText.setPlainText(coords_text)
        ui.dial.exec_()
        if ui.dial.result():
            tmp = self.data['filename']
            self.data_from_dialog(ui)
            self.data['filename'] = tmp

    def data_from_dialog(self, ui):
        self.clear_table()
        self.data_empty()
        self.data['proficient'] = str(ui.perito.text().toUtf8()).decode(
            'utf-8')
        self.data['plane_of'] = str(ui.plane_of.text().toUtf8()).decode(
            'utf-8')
        self.data['location'] = str(ui.location.text().toUtf8()).decode(
            'utf-8')
        self.data['possession'] = str(ui.possession.text().toUtf8()).decode(
            'utf-8')
        self.data['homeowner'] = str(ui.homeowner.text().toUtf8()).decode(
            'utf-8')
        self.data['date'] = str(ui.date.text().toUtf8()).decode('utf-8')
        coord_text = str(ui.coordText.toPlainText())
        for e in coord_text.split('\n'):
            coord = e.split()
            if len(coord) == 2:
                try:
                    x = float(coord[0])
                    y = float(coord[1])
                    self.data['coords'].append((x, y))
                except ValueError:
                    msg = "(%s, %s) no es una coordenada valida" % \
                        (coord[0], coord[1])
                    QtGui.QMessageBox.critical(ui.dial, 'Advertencia', msg)
        self.show_data()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myapp = MainWindow()
    myapp.ui.show()
    sys.exit(app.exec_())
