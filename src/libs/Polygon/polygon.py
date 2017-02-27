# -*- coding: utf-8 -*-

import math


class Polygon:

    def __init__(self):
        self.points = []

    def add_point(self, p):
        """
        P.add_point(p)
        Add the point p to polygon
        Param:
            p A tuple like (x, y)
        """
        if len(p) == 2:
            self.points.append(p)

    def angle_between_2p(self, p1, p2, p3):
        """
        P.angle_between_2p(p1, p2, p3) -> float
        Calculate the angle between p1 and p2.
        Param:
            p1 First point where is a tuple like (x, y)
            p2 Second point where is a tuple like (x, y)
            p3 Third point where is a tuple like (x, y)

        Return:
            float The angle in decimal degree.
        """
        a = self.get_distance(p2, p3)
        b = self.get_distance(p1, p2)
        c = self.get_distance(p1, p3)
        aux = (a**2 - b**2 - c**2)/(-2*b*c)
        angle = math.degrees(math.acos(aux))
        ls = [p3, p1, p2]
        if self.area_from_list(ls) < 0:
            angle = 360 - angle
        return angle

    def amount_points(self):
        """
        P.amount_point() -> Int
        Amount of points in the polygon.
        Return:
            Int Amount of points
        """
        return len(self.points)

    def angles(self):
        """
        P.angles() -> [angle1, angle2, ..., angleN]
        Calculate the angles of a polygon.
        Return:
            A angles list of polygon in decimal degree.
        """
        res = []
        n = self.amount_points()
        for i in range(n):
            p1 = self.points[i]
            p2 = self.points[(i+1) % n]
            p3 = self.points[(i-1) % n]
            a = self.angle_between_2p(p1, p2, p3)
            res.append(a)
        return res

    def azimuths(self):
        """
        P.azimuths() -> [azimuth1, azimuth2, ..., azimuthN]
        Calculate the azimuths of a polygon forward.
        Return:
            A list with the azimuths of polygon.
        """
        res = []
        n = self.amount_points()
        pts = list(range(1, n + 1))
        pts.reverse()
        for i in pts:
            p1 = self.points[i % n]
            p2 = self.points[i-1]
            a = self.get_azimuth(p1, p2)
            res.append(a)
        return res

    def get_azimuth(self, p1, p2):
        """
        P.get_azimuth(p1, p2) -> float
        Calculate the azimuth given two points.
        Params:
            p1 A tuple like (x1, y1)
            p2 A tuple like (x2, y2)
        Return:
            float azimuth in degree.
        """
        x1, y1 = p1
        x2, y2 = p2
        c = 0
        a = x2-x1
        b = y2-y1
        if a >= 0 and b >= 0:
            c = 0
        elif (a >= 0 and b < 0) or (a < 0 and b < 0):
            c = 180
        else:
            c = 360
        at = math.atan(a/b)
        d = math.degrees(at)
        ret = c + d
        return ret

    def decdeg2dms(self, dd):
        """
        P.decdeg2dms(dd) -> (deg, min, sec)
        Convert a decimal degree to degrees, minutes and seconds
        Params:
            dd A decimal degree
        Return:
            A tuple (deg, min, sec)
        """
        is_positive = dd >= 0
        d = abs(dd)
        m, s = divmod(d*3600, 60)
        deg, m = divmod(m, 60)
        deg = deg if is_positive else -deg
        return (deg, m, s)

    def edges(self):
        """
        P.edges() -> [edge1, edge2, ..., edgeN]
        Returns an edges list of a polygon
        """
        n = self.amount_points()
        res = []
        for i in range(n):
            p1 = self.points[i]
            p2 = self.points[(i+1) % n]
            b = self.get_distance(p1, p2)
            res.append(b)
        return res

    def get_distance(self, p1, p2):
        """
        P.get_distance(p1, p2) -> float
        Calculate the distence between points
        Params:
            p1 A tuple like (x1, y1)
            p2 A tuple like (x2, y2)
        Return:
            float The distance
        """
        x1, y1 = p1
        x2, y2 = p2
        dx = x2 - x1
        dy = y2 - y1
        res = math.sqrt(dx ** 2 + dy ** 2)
        return res

    def area_from_list(self, lis):
        """
        P.area_from_list(lis) -> float
        Calculate the polygon area.
        Params:
            lis A points list of a polygon
        Return:
            float A area of polygon
        """
        res = 0
        n = len(lis)
        for i in range(n):
            x1, y1 = lis[i]
            x2, y2 = lis[(i+1) % n]
            res += x1*y2 - y1*x2
        return res/2

    def area(self):
        """
        P.area() -> float
        Return the area of current polygon
        """
        return self.area_from_list(self.points)

    def list_sort(self):
        """
        list_sort() -> list
        Sort a list in counter-clockwise
        """
        n = len(self.points)
        self.points.reverse()
        self.points.insert(0, self.points.pop(n-1))

    def origin_list(self, lis):
        """
        P.origin_list(lis) -> list
        Return a list sorted in clockwise
        """
        ret = lis
        x = ret.pop(0)
        ret.reverse()
        ret.insert(0, x)
        return ret

    def polygon_from_list(self, lis):
        """
        P.polygon_from_list(lis) -> list
        Constructs a polygon given a points list
        Params:
            lis A points list like [(y1, x1), (y2, x2), ..., (yN, xN)]
                sorted in clockwise
        Return a points list like [(x1, y1), ..., (xN, yN)] sorted in
        counter-clockwise
        """
        for e in lis:
            if len(e) == 2:
                y, x = e
                self.add_point((x, y))
        self.list_sort()
