==============
Vector Library
==============

:Author: Richard Thomas
:Contact: vector@supereffective.org
:Date: 2009-07-17

This is a collection of convenient abstractions for two dimensional floating
point vectors in Python_.

.. _Python: http://www.python.org/

History
=======

*Version 0.3*

- Minor optimisations.
- Added a length2 property to vectors.
- Fixed badly broken angle_to computations.
- Iterable arguments are no longer allowed, arguments should be indexable. This
  allows for further optimisation as objects are only converted to vectors if
  they need to be. Instance attributes are always vectors.
- Improved existing documentation; clarfications.

*Version 0.2*

- Triangle class added.
- Vector.is_zero added.
- Vector.scaled_to added.
- Vector.safe_scaled_to added.
- Vector.safe_normalised added.
- Rectangle class added.
- Line.parallel added.
- Line.perpendicular added.
- v function added.
- Released 15th March 2009.

*Version 0.1*

- Vector, Line and LineSegment classes added.
- Released 22nd January 2009.


Vector API
==========

Vector objects are two dimensional floating point vectors. They form the core
of the vector library. They are initialised with a suitable sequence of floats
or integers::

    >>> from vector import Vector
    >>> v = Vector((1, 2))
    >>> assert v == Vector([1, 2])

The most important piece of functionality is easy vector arithmetic. Not only
can vectors be added together and scaled, suitable constructor arguments can
be used instead of one of the arguments. For example::

    >>> from vector import Vector
    >>> v = Vector((1, 2))
    >>> assert v * 2 == Vector((2, 4))
    >>> assert v + (0, -1) == Vector((1, 1))
    >>> assert v + Vector((0, -1)) == (1, 1)

There are a few module level constants for common vectors:

    ``vector.zero``
        The zero vector (``Vector((0, 0))``).
    ``vector.unit_x``
        A unit vector in the x direction (``Vector((1, 0))``).
    ``vector.unit_y``
        A unit vector in the y direction (``Vector((0, 1))``).

As a convenience there is a module level function to construct vectors with a
more straightforward syntax. It isn't used internally for efficiency reasons,
but it makes explicitly describing vectors externally a lot prettier::

    >>> from vector import v, Vector
    >>> assert v(1, 2) == Vector((1, 2))
    >>> assert v((1, 2)) == Vector((1, 2))

The following properties and methods are available on the Vector class and its
instances:

    ``Vector.x``
        *property:* Alias for the x-coordinate.
    ``Vector.y``
        *property:* Alias for the y-coordinate.
    ``Vector.length``
        *property:* The length of the vector.
    ``Vector.length2``
        *property:* The squared length of the vector.
    ``Vector.angle``
        *property:* The angle to the positive x-axis. (-180, 180].
    ``Vector.is_zero``
        *property:* Flag indicating whether the vector is the zero vector.
    ``Vector.rotated(angle)``
        *method:* Create a copy of the vector rotated by the given angle.
    ``Vector.scaled_to(length)``
        *method:* Create a copy of the vector scaled to a given length.
    ``Vector.safe_scaled_to(length)``
        *method:* As above but returns the zero vector if given a zero vector.
    ``Vector.normalised()``
        *method:* Create a copy of the vector scaled to unit length.
    ``Vector.safe_normalised()``
        *method:* As above but returns the zero vector if given a zero vector.
    ``Vector.perpendicular()``
        *method:* Create a copy of the vector rotated by 90 degrees.
    ``Vector.dot(other)``
        *method:* Compute the dot product with another vector.
    ``Vector.cross(other)``
        *method:* Compute the cross product with another vector.
    ``Vector.project(other)``
        *method:* Compute the projection of a vector onto this one.
    ``Vector.angle_to(other)``
        *method:* Compute the absolute angle made to another vector. [0, 180].
    ``Vector.signed_angle_to(other)``
        *method:* Compute the signed angle made to another vector. (-180, 180].
    ``Vector.distance_to(other)``
        *method:* Compute the distance to another vector.

Line API
========

Line objects are representations of infinite and oriented lines. Their
internal representation is as a perpendicular direction and a distance from
the origin and they can be initialised with these quantities::

    >>> from vector import Line
    >>> l = Line((1, 1), 2.0)

In the above construction the direction of the line is from the right of the
direction vector to the left. Alternatively they can be initialised from a pair
of points on the line::

    >>> from vector import Line
    >>> l = Line.from_points((0, 1), (1, 0))

In this case the direction of the line is from the first point to the second.
As a convenience there are a couple of default lines as module level constants:

    ``vector.x_axis``
        The Line object for the x-axis (``Line(unit_y, 0.0)``).
    ``vector.y_axis``
        The Line object for the y-axis (``Line(-unit_x, 0.0)``).

The following attributes, properties and methods are available on the Line
class and its instances:

    ``Line.__init__(direction, distance)``
        *constructor:* Default constructor (see above).
    ``Line.from_points(first, second)``
        *constructor:* Alternate constructor (see above).
    ``Line.direction``
        *attribute:* The perpendicular unit vector.
    ``Line.along``
        *attribute:* The parallel unit vector.
    ``Line.distance``
        *attribute:* The distance from the origin to the line.
    ``Line.offset``
        *property:* The perpendicular offset from the origin.
    ``Line.project(point)``
        *method:* Compute the projection of a point onto the line.
    ``Line.reflect(point)``
        *method:* Compute the reflection a point in the line.
    ``Line.distance_to(point)``
        *method:* Compute the (signed) distance from a point to the line.
    ``Line.is_on_left(point)``
        *method:* Determine if the point is on the left of the line.
    ``Line.is_on_right(point)``
        *method:* Determine if the point is on the right of the line.
    ``Line.parallel(point)``
        *method:* Compute a new line parallel and through a given point.
    ``Line.perpendicular(point)``
        *method:* Compute a new line perpendicular and through a given point.

LineSegment API
===============

LineSegment objects are representations of finite oriented line segments. Their
internal representation is the line of which they form part and two distances
being the distances from the endpoints of the origin's projection onto the
line. They can be initialised as such::

    >>> from vector import Line, LineSegment
    >>> l = Line((1, 1), 2.0)
    >>> s = LineSegment(l, -1.0, 1.0)

The sign of the distance obviously respects the direction of the line. An
alternative constructor allows you to create a LineSegment from its two
endpoints::

    >>> from vector import LineSegment
    >>> s = LineSegment.from_points((0, 1), (1, 0))

The following attributes, properties and methods are available on the
LineSegment class and its instances:

    ``LineSegment.__init__(line, min_dist, max_dist)``
        *constructor:* Default constructor (see above).
    ``LineSegment.from_points(first, second)``
        *constructor:* Alternate constructor (see above).
    ``LineSegment.line``
        *attribute:* The line of which the segment is a part.
    ``LineSegment.min_dist``
        *attribute:* The distance to the start from the origin's projection.
    ``LineSegment.max_dist``
        *attribute:* The distance to the end from the origin's projection.
    ``LineSegment.length``
        *property:* The length on the line segment.
    ``LineSegment.start``
        *property:* The start point of the line segment.
    ``LineSegment.mid``
        *property:* The mid point of the line segment.
    ``LineSegment.end``
        *property:* The end point of the line segment.
    ``LineSegment.project(point)``
        *method:* Compute the projection of a point onto the line segment.
    ``LineSegment.distance_to(point)``
        *method:* Compute the distance from a point to the line segment.


Triangle API
============

Triangle objects are representations of oriented vector triangles. Their
implementation is not finished, please see the code if you are interested
in them.


Rectangle API
=============

Rectangle objects are representations of axis-aligned rectangles, specified by
their lower-left and upper-right corners. They are primarily useful as
a collision area in hashing implementations. There is an alternate constructor
which will produce the smallest rectangle bounding a given set of points.

The following properties and methods are available on the Rectangle class:

    ``Rectangle.__init__(lo, hi)``
        Default constructor (see above).
    ``Rectangle.as_bounding(points)``
        Alternate constructor (see above).


Miscellaneous Notes
===================

A lot of the attributes of objects from this library are caching properties.
This means that their value is computed exactly once. For example, the length
of a vector is computed and thenceforth remembered rather than computed
whenever it is needed.


License
=======

::

  Copyright (c) 2009 The Super Effective Team (www.supereffective.org).

  All rights reserved.

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are met:

  * Redistributions of source code must retain the above copyright notice, this
    list of conditions and the following disclaimer.
  * Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.
  * Neither the name(s) of the copyright holders nor the names of its
    contributors may be used to endorse or promote products derived from this
    software without specific prior written permission.

  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AS IS AND ANY EXPRESS OR
  IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
  EVENT SHALL THE COPYRIGHT HOLDERS BE LIABLE FOR ANY DIRECT, INDIRECT,
  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
