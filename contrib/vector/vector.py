# Copyright (c) 2009 The Super Effective Team (www.supereffective.org).
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name(s) of the copyright holders nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AS IS AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL THE COPYRIGHT HOLDERS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Two-dimensional vector geometry library.

"""

from __future__ import division

import math
import weakref


def cached(func):
    """Decorate a function as a caching property.

    :Parameters:
        `func` : function
            The getter function to decorate.

    """
    cached_name = "_cached_%s" % func.func_name

    # The keywords 'getattr' and 'cached_name' are used to optimise the common
    # case (return cached value) by bringing the used names to local scope.
    def fget(self, getattr=getattr, cached_name=cached_name):
        try:
            return getattr(self, cached_name)
        except AttributeError:
            value = func(self)
            setattr(self, cached_name, value)
            return value

    def fset(self, value):
        assert not hasattr(self, cached_name)
        setattr(self, cached_name, value)

    fget.func_name = "get_" + func.func_name
    fset.func_name = "set_" + func.func_name

    return property(fget, fset, doc=func.func_doc)


class Vector(tuple):
    """Two-dimensional float vector implementation.

    """

    def __str__(self):
        """Construct a concise string representation.

        """
        return "Vector((%.2f, %.2f))" % self

    def __repr__(self):
        """Construct a precise string representation.

        """
        return "Vector((%r, %r))" % self

    @property
    def x(self):
        """The horizontal coordinate.

        """
        return self[0]

    @property
    def y(self):
        """The vertical coordinate.

        """
        return self[1]

    @cached
    def length(self):
        """The length of the vector.

        """
        return math.sqrt(self.length2)

    @cached
    def length2(self):
        """The square of the length of the vector.

        """
        vx, vy = self
        return vx ** 2 + vy ** 2

    @cached
    def angle(self):
        """The angle the vector makes to the positive x axis in the range
        (-180, 180].

        """
        vx, vy = self
        return math.degrees(math.atan2(vy, vx))

    @property
    def is_zero(self):
        """Flag indicating whether this is the zero vector.

        """
        return self[0] == 0.0 and self[1] == 0.0

    def __add__(self, other):
        """Add the vectors componentwise.

        :Parameters:
            `other` : Vector
                The object to add.

        """
        return Vector((self[0] + other[0], self[1] + other[1]))

    def __radd__(self, other):
        """Add the vectors componentwise.

        :Parameters:
            `other` : Vector
                The object to add.

        """
        return Vector((other[0] + self[0], other[1] + self[1]))

    def __sub__(self, other):
        """Subtract the vectors componentwise.

        :Parameters:
            `other` : Vector
                The object to subtract.

        """
        return Vector((self[0] - other[0], self[1] - other[1]))

    def __rsub__(self, other):
        """Subtract the vectors componentwise.

        :Parameters:
            `other` : Vector
                The object to subtract.

        """
        return Vector((other[0] - self[0], other[1] - self[1]))

    def __mul__(self, other):
        """Either multiply the vector by a scalar or compute the dot product
        with another vector.

        :Parameters:
            `other` : Vector or float
                The object by which to multiply.

        """
        try:
            other = float(other)
            return Vector((self[0] * other, self[1] * other))
        except TypeError:
            return self[0] * other[0] + self[1] * other[1]

    def __rmul__(self, other):
        """Either multiply the vector by a scalar or compute the dot product
        with another vector.

        :Parameters:
            `other` : Vector or float
                The object by which to multiply.

        """
        try:
            other = float(other)
            return Vector((other * self[0], other * self[1]))
        except TypeError:
            return other[0] * self[0] + other[1] * self[1]

    def __div__(self, other):
        """Divide the vector by a scalar.

        :Parameters:
            `other` : float
                The object by which to divide.

        """
        return Vector((self[0] / other, self[1] / other))

    def __truediv__(self, other):
        """Divide the vector by a scalar.

        :Parameters:
            `other` : float
                The object by which to divide.

        """
        return Vector((self[0] / other, self[1] / other))

    def __floordiv__(self, other):
        """Divide the vector by a scalar, rounding down.

        :Parameters:
            `other` : float
                The object by which to divide.

        """
        return Vector((self[0] // other, self[1] // other))

    def __neg__(self):
        """Compute the unary negation of the vector.

        """
        return Vector((-self[0], -self[1]))

    def rotated(self, angle):
        """Compute the vector rotated by an angle.

        :Parameters:
            `angle` : float
                The angle (in degrees) by which to rotate.

        """
        vx, vy = self
        angle = math.radians(angle)
        ca, sa = math.cos(angle), math.sin(angle)
        return Vector((vx * ca - vy * sa, vx * sa + vy * ca))

    def scaled_to(self, length):
        """Compute the vector scaled to a given length.

        :Parameters:
            `length` : float
                The length to which to scale.

        """
        vx, vy = self
        s = length / self.length
        v = Vector((vx * s, vy * s))
        v.length = length
        return v

    def safe_scaled_to(self, length):
        """Compute the vector scaled to a given length, or just return the
        vector if it was the zero vector.

        :Parameters:
            `length` : float
                The length to which to scale.

        """
        if self.is_zero:
            return self
        return self.scaled_to(length)

    def normalised(self):
        """Compute the vector scaled to unit length.

        """
        vx, vy = self
        l = self.length
        v = Vector((vx / l, vy / l))
        v.length = 1.0
        return v

    def safe_normalised(self):
        """Compute the vector scaled to unit length, or just return the vector
        if it was the zero vector.

        """
        if self.is_zero:
            return self
        return self.normalised()

    def perpendicular(self):
        """Compute the perpendicular.

        """
        vx, vy = self
        return Vector((-vy, vx))

    def dot(self, other):
        """Compute the dot product with another vector.

        :Parameters:
            `other` : Vector
                The vector with which to compute the dot product.

        """
        return self[0] * other[0] + self[1] * other[1]

    def cross(self, other):
        """Compute the cross product with another vector.

        :Parameters:
            `other` : Vector
                The vector with which to compute the cross product.

        """
        return self[0] * other[1] - self[1] * other[0]

    def project(self, other):
        """Compute the projection of another vector onto this one.

        :Parameters:
            `other` : Vector
                The vector of which to compute the projection.

        """
        return self * self.dot(other) / self.dot(self)

    def angle_to(self, other):
        """Compute the angle made to another vector in the range [0, 180].

        :Parameters:
            `other` : Vector
                The vector with which to compute the angle.

        """
        if not isinstance(other, Vector):
            other = Vector(other)
        a = abs(other.angle - self.angle)
        return min(a, 360 - a)

    def signed_angle_to(self, other):
        """Compute the signed angle made to another vector in the range
        (-180, 180].

        :Parameters:
            `other` : Vector
                The vector with which to compute the angle.

        """
        if not isinstance(other, Vector):
            other = Vector(other)
        a = other.angle - self.angle
        return min(a + 360, a, a - 360, key=abs)

    def distance_to(self, other):
        """Compute the distance to another point vector.

        :Parameters:
            `other` : Vector
                The point vector to which to compute the distance.

        """
        return (other - self).length


class Line(object):
    """Two-dimensional vector (directed) line implementation.

    Lines are defined in terms of a perpendicular vector and the distance from
    the origin. The direction of the line proceeds from the right of the vector
    to the left.

    """

    def __init__(self, direction, distance):
        """Create a Line object.

        :Parameters:
            `direction` : Vector
                A (non-zero) vector perpendicular to the line.
            `distance` : float
                The distance from the origin to the line.

        """
        if not isinstance(direction, Vector):
            direction = Vector(direction)
        self.direction = direction.normalised()
        self.along = self.direction.perpendicular()
        self.distance = distance

    def __str__(self):
        """Construct a concise string representation.

        """
        return "Line(%s, %.2f)" % (self.direction, self.distance)

    def __repr__(self):
        """Construct a precise string representation.

        """
        return "Line(%r, %r)" % (self.direction, self.distance)

    @classmethod
    def from_points(cls, first, second):
        """Create a Line object from two (distinct) points.

        :Parameters:
            `first`, `second` : Vector
                The vectors used to construct the line.

        """
        if not isinstance(first, Vector):
            first = Vector(first)
        along = (second - first).normalised()
        direction = -along.perpendicular()
        distance = first.dot(direction)
        return cls(direction, distance)

    @cached
    def offset(self):
        """The projection of the origin onto the line.

        """
        return self.direction * self.distance

    def project(self, point):
        """Compute the projection of a point onto the line.

        :Parameters:
            `point` : Vector
                The point to project onto the line.

        """
        parallel = self.along.project(point)
        return parallel + self.offset

    def reflect(self, point):
        """Reflect a point in the line.

        :Parameters:
            `point` : Vector
                The point to reflect in the line.

        """
        if not isinstance(point, Vector):
            point = Vector(point)
        offset_distance = point.dot(self.direction) - self.distance
        return point - 2 * self.direction * offset_distance

    def distance_to(self, point):
        """Return the (signed) distance to a point.

        :Parameters:
            `point` : Vector
                The point to measure the distance to.

        """
        if not isinstance(point, Vector):
            point = Vector(point)
        return point.dot(self.direction) - self.distance

    def is_on_left(self, point):
        """Determine if the given point is left of the line.

        :Parameters:
            `point` : Vector
                The point to locate.

        """
        return self.distance_to(point) < 0

    def is_on_right(self, point):
        """Determine if the given point is right of the line.

        :Parameters:
            `point` : Vector
                The point to locate.

        """
        return self.distance_to(point) > 0

    def parallel(self, point):
        """Return a line parallel to this one through the given point.

        :Parameters:
            `point` : Vector
                The point through which to trace a line.

        """
        if not isinstance(point, Vector):
            point = Vector(point)
        distance = point.dot(self.direction)
        return Line(self.direction, distance)

    def perpendicular(self, point):
        """Return a line perpendicular to this one through the given point. The
        orientation of the line is consistent with ``Vector.perpendicular``.

        :Parameters:
            `point` : Vector
                The point through which to trace a line.

        """
        if not isinstance(point, Vector):
            point = Vector(point)
        direction = self.direction.perpendicular()
        distance = point.dot(direction)
        return Line(direction, distance)



class LineSegment(object):
    """Two-dimensional vector (directed) line segment implementation.

    Line segments are defined in terms of a line and the minimum and maximum
    distances from the base of the altitude to that line from the origin. The
    distances are signed, strictly they are multiples of a vector parallel to
    the line.

    """

    def __init__(self, line, min_dist, max_dist):
        """Create a LineSegment object.

        Distances are measured according to the direction of the 'along'
        attribute of the line.

        :Parameters:
            `line` : Line
                The line to take a segment of.
            `min_dist` : float
                The minimum distance from the projection of the origin.
            `max_dist` : float
                The maximum distance from the projection of the origin.

        """
        self.line = line
        self.min_dist = min_dist
        self.max_dist = max_dist

    def __str__(self):
        """Construct a concise string representation.

        """
        params = (self.line, self.min_dist, self.max_dist)
        return "LineSegment(%s, %.2f, %.2f)" % params

    def __repr__(self):
        """Construct a precise string representation.

        """
        params = (self.line, self.min_dist, self.max_dist)
        return "LineSegment(%r, %r, %r)" % params

    @classmethod
    def from_points(cls, first, second):
        """Create a LineSegment object from two (distinct) points.

        :Parameters:
            `first`, `second` : Vector
                The vectors used to construct the line.

        """
        if not isinstance(first, Vector):
            first = Vector(first)
        if not isinstance(second, Vector):
            second = Vector(second)
        line = Line.from_points(first, second)
        d1, d2 = first.dot(line.along), second.dot(line.along)
        return cls(line, min(d1, d2), max(d1, d2))

    @cached
    def length(self):
        """The length of the line segment.

        """
        return abs(self.max_dist - self.min_dist)

    def _endpoints(self):
        """Compute the two endpoints of the line segment.

        """
        start = self.line.along * self.min_dist + self.line.offset
        end = self.line.along * self.max_dist + self.line.offset
        return start, end

    @cached
    def start(self):
        """One endpoint of the line segment (corresponding to 'min_dist').

        """
        start, end = self._endpoints()
        self.mid = (start + end) / 2
        self.end = end
        return start

    @cached
    def mid(self):
        """The midpoint of the line segment.

        """
        start, end = self._endpoints()
        self.start = start
        self.end = end
        return (start + end) / 2

    @cached
    def end(self):
        """One endpoint of the line segment (corresponding to 'max_dist').

        """
        start, end = self._endpoints()
        self.start = start
        self.mid = (start + end) / 2
        return end

    def project(self, point):
        """Compute the projection of a point onto the line segment.

        :Parameters:
            `point` : Vector
                The point to minimise the distance to.

        """
        if not isinstance(point, Vector):
            point = Vector(point)
        distance = point.dot(self.line.along)
        if distance >= self.max_dist:
            return self.end
        elif distance <= self.min_dist:
            return self.start
        return self.line.along * distance + self.line.offset

    def distance_to(self, point):
        """Return the shortest distance to a given point.

        :Parameters:
            `point` : Vector
                The point to measure the distance to.

        """
        if not isinstance(point, Vector):
            point = Vector(point)
        distance = point.dot(self.line.along)
        if distance >= self.max_dist:
            return self.end.distance_to(point)
        elif distance <= self.min_dist:
            return self.start.distance_to(point)
        else:
            return abs(self.line.distance_to(point))


class Triangle(object):
    """Two-dimensional vector (oriented) triangle implementation.

    """

    def __init__(self, base, primary, secondary):
        """Create a Triangle object.

        The two vectors that define the edges from the base point are ordered.
        If the vectors are counter-clockwise and the triangle is considered
        counter-clockwise, ditto clockwise.

        :Parameters:
            `base` : Vector
                A point vector of a base point of the triangle.
            `primary` : Vector
                The vector from the base point to one of the others.
            `secondary` : Vector
                The vector from the base point to the final point.

        """
        if not isinstance(base, Vector):
            base = Vector(base)
        if not isinstance(primary, Vector):
            primary = Vector(primary)
        if not isinstance(secondary, Vector):
            secondary = Vector(secondary)
        self.base = base
        self.primary = primary
        self.secondary = secondary

    def __str__(self):
        """Construct a concise string representation.

        """
        params = (self.base, self.primary, self.secondary)
        return "Triangle(%s, %s, %s)" % params

    def __repr__(self):
        """Construct a precise string representation.

        """
        params = (self.base, self.primary, self.secondary)
        return "Triangle(%r, %r, %r)" % params

    @classmethod
    def from_points(cls, base, first, second):
        """Create a Triangle object from its three points.

        :Parameters:
            `base` : Vector
                The base point of the triangle.
            `first`, `second` : Vector
                The other two points of the triangle.

        """
        if not isinstance(base, Vector):
            base = Vector(base)
        primary = first - base
        secondary = second - base
        return cls(base, primary, secondary)

    @cached
    def area(self):
        """The unsigned area of the triangle.

        """
        area = self.primary.cross(self.secondary) / 2
        self.is_clockwise = (area < 0)
        return abs(area)

    @cached
    def is_clockwise(self):
        """True if the primary and secondary are clockwise.

        """
        area = self.primary.cross(self.secondary) / 2
        self.area = abs(area)
        return (area < 0)

    @cached
    def first(self):
        """The point at the end of the primary vector.

        """
        return self.base + self.primary

    @cached
    def second(self):
        """The point at the end of the secondary vector.

        """
        return self.base + self.secondary


class Rectangle(object):
    """Two-dimensional vector (axis-aligned) rectangle implementation.

    """

    def __init__(self, lo, hi):
        """Create a Rectangle object.

        :Parameters:
            `lo` : Vector
                The lower left corner of the box.
            `hi` : Vector
                The upper right corner of the box.

        """
        if not isinstance(lo, Vector):
            lo = Vector(lo)
        if not isinstance(hi, Vector):
            hi = Vector(hi)
        self.lo = lo
        self.hi = hi

    def __str__(self):
        """Construct a concise string representation.

        """
        params = (self.lo, self.hi)
        return "Rectangle(%s, %s)" % params

    def __repr__(self):
        """Construct a precise string representation.

        """
        params = (self.lo, self.hi)
        return "Rectangle(%r, %r)" % params

    @classmethod
    def as_bounding(cls, points):
        """Create a Rectangle object from a selection of bounded points.

        :Parameters:
            `points` : Vectors
                The points to bound.

        """
        xs, ys = zip(*points)
        lo = (min(xs), min(ys))
        hi = (max(xs), max(ys))
        return cls(lo, hi)


def v(*args):
    """Construct a vector from an iterable or from multiple arguments. Valid
    forms are therefore: ``v((x, y))`` and ``v(x, y)``.

    """
    if len(args) == 1:
        return Vector(args[0])
    return Vector(args)


#: The zero vector.
zero = Vector((0, 0))

#: The unit vector on the x-axis.
unit_x = Vector((1, 0))

#: The unit vector on the y-axis.
unit_y = Vector((0, 1))

#: The x-axis line.
x_axis = Line(unit_y, 0.0)

#: The y-axis line.
y_axis = Line(-unit_x, 0.0)
