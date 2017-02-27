# -*- coding: utf-8 -*-

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape, inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, Spacer
from ..Polygon.polygon import Polygon


class Document:
    """
    Document for calculate coordinates and area of an polygon
    +------------------------------------------------------+
    |                       Title                          |
    |  +-----------------------------------------------+   |
    |  | Table form                                    |   |
    |  +-----------------------------------------------+   |
    |  +-----------------------------------------------+   |
    |  | Main table                                    |   |
    |  +-----------------------------------------------+   |
    |  Sum of angles                                       |
    |  Perimeter                                           |
    |                       Polygon area                   |
    +------------------------------------------------------+
    """

    def __init__(self):
        self.styles = getSampleStyleSheet()
        # Header style
        self.styleHeader = self.styles['Heading1']
        self.styleHeader.alignment = TA_CENTER
        self.styleHeader.fontSize = 24
        # Body text style
        self.styleBodyText = self.styles['BodyText']
        self.styleBodyText.fontSize = 12
        # Normal style
        self.styleNormal = self.styles['Normal']
        # Buffer of texts and objects for write in a file pdf
        self.story = []
        # Data to write
        self.data = dict()
        self.data['title'] = ''
        self.data['spaceBeforeTable'] = ''
        self.data['tableForm'] = ''
        self.data['mainTable'] = ''
        self.data['perim'] = ''
        self.data['sum_angs'] = ''
        self.data['sup'] = ''

    def set_title(self, data):
        self.data['title'] = Paragraph(data['title'].upper(), self.styleHeader)

    def build_form(self, data):
        """
        D.build_form(data)
        Build the Table form
        Params
            - data: Data for the table
        """
        # Fields titles
        t1 = Paragraph("<b>Plano de:</b>", self.styleBodyText)
        t2 = Paragraph("<b>Propiedad:</b>", self.styleBodyText)
        t3 = Paragraph("<b>Ubicación:</b>", self.styleBodyText)
        t4 = Paragraph("<b>Perito:</b>", self.styleBodyText)
        t5 = Paragraph("<b>Propietarios:</b>", self.styleBodyText)
        t6 = Paragraph("<b>Fecha:</b>", self.styleBodyText)
        plane_of = Paragraph(data['plane_of'], self.styleNormal)
        proficient = Paragraph(data['proficient'], self.styleNormal)
        possession = Paragraph(data['possession'], self.styleNormal)
        homeowners = Paragraph(data['homeowner'], self.styleNormal)
        location = Paragraph(data['location'], self.styleNormal)
        date = Paragraph(data['date'], self.styleNormal)
        header_data = [[t1, plane_of, t3, location, t4, proficient],
                       [t2, possession, t5, homeowners, t6, date]]
        styleTable = [
                    # ('BOX',(0,0),(-1,-1),1,colors.black),
                    # ('GRID',(0,0),(-1,-1),0.5,colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 2),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 2),
                    ('TOPPADDING', (0, 0), (-1, -1), 2),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ]
        # Table of form
        t = Table(header_data, style=styleTable, rowHeights=25)

        # Table widths
        t._argW[0] = 70     # plane of
        t._argW[2] = 80     # location
        t._argW[4] = 45     # perito
        t._argW[5] = 125    # proficient

        # Table heights
        t._argH[0] = 20     # first row
        t._argH[1] = 20     # Second row

        self.data['spaceBeforeTable'] = Spacer(1, 0.2*inch)
        self.data['tableForm'] = t

    def save(self, filename, data):
        """
        D.save(filename, data)
        Construct and save a document PDF format
        Params
            - filename: A name file
            - data: Dict with datas for the document (title, table form,
            data for main table, perimeter, sum angles and polygon area)
        """
        self.set_title(data)
        self.build_form(data)
        self.build_table(data)
        self.build_story()
        if not filename.endswith('.pdf'):
            filename = filename + '.pdf'
        self.doc = SimpleDocTemplate(filename, pagesize=landscape(A4),
                                     topMargin=inch/4, bottomMargin=inch/4,
                                     leftMargin=inch/4, rightMargin=inch/4)
        self.doc.build(self.story)

    def build_story(self):
        """
        D.build_story()
        Construct stories for write the document
        """
        self.story.append(self.data['title'])
        self.story.append(self.data['spaceBeforeTable'])
        self.story.append(self.data['tableForm'])
        self.story.append(self.data['mainTable'])
        self.story.append(self.data['spaceBeforeTable'])
        self.story.append(self.data['perim'])
        self.story.append(self.data['sum_angs'])
        self.story.append(self.data['sup'])

    def build_table(self, data):
        """
        D.build_table(data)
        Construct the main table.
        Params
            - data: Dict with datas for the main table
        """
        p = Polygon()
        styleHeader = self.styles['Heading2']
        styleHeader.alignment = TA_CENTER
        styleHeader4 = self.styles['Heading4']
        styleHeader4.alignment = TA_CENTER
        datas = [[Paragraph('Vért.', styleHeader),
                  Paragraph('Ángulos Internos', styleHeader),
                  '', '',
                  Paragraph('Rumbos', styleHeader),
                  '', '',
                  Paragraph('Lados', styleHeader),
                  Paragraph('Vért.', styleHeader),
                  Paragraph('x', styleHeader),
                  Paragraph('y', styleHeader)],
                 [Paragraph('', styleHeader4),
                  Paragraph('º', styleHeader4),
                  Paragraph("'", styleHeader4),
                  Paragraph('"', styleHeader4),
                  Paragraph('º', styleHeader4),
                  Paragraph("'", styleHeader4),
                  Paragraph('"', styleHeader4),
                  Paragraph('m', styleHeader4),
                  Paragraph('', styleHeader4),
                  Paragraph('m', styleHeader4),
                  Paragraph('m', styleHeader4)], ]
        for i in range(len(data['coords'])):
            d1, m1, s1 = p.decdeg2dms(data['angs'][i])
            d2, m2, s2 = p.decdeg2dms(data['azimuths'][i])
            x, y = data['coords'][i]
            b = "{0: .2f}".format(data['edges'][i])
            row = [i, int(d1), int(m1), '{0:.2f}'.format(s1),
                   int(d2), int(m2), '{0:.2f}'.format(s2),
                   b, i, str(x), str(y)]
            datas.append(row)
        styleT = [
                    ('BOX', (0, 0), (-1, -1), 2, colors.black),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                    ('SPAN', (1, 0), (3, 0)),
                    ('SPAN', (4, 0), (6, 0)),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER')
                ]
        t = Table(datas, style=styleT)
        t._argW[0] = 60
        self.data['mainTable'] = t
        area = data['area']
        perim = data['perim']
        sum_angs = data['sum_angs']
        self.data['perim'] = Paragraph(
            "Perímetro:   %s m" % "{0: .2f}".format(perim),
            self.styleNormal)
        self.data['sum_angs'] = Paragraph(
            "Suma de ángulos:   %s" % "{0: .2f}".format(sum_angs),
            self.styleNormal)
        self.data['sup'] = Paragraph(
            "Superficie:   %s m2" % "{0: .2f}".format(area),
            styleHeader)
