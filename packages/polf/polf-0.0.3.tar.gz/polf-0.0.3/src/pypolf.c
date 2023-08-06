#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <math.h>

#ifndef M_PI
    #define M_PI 3.14159265358979323846
#endif

#define __M_PI_POW M_PI*2

static PyObject* _line_xy(double p0x, double p0y, double p1x, double p1y, double t) {
    return Py_BuildValue("[dd]", (p0x + p1x) * t, (p0y + p1y) * t);
}

static PyObject* line_xy(PyObject *self, PyObject *args) {
    double p0x;
    double p0y;
    double p1x;
    double p1y;
    double t;
    
    if (!PyArg_ParseTuple(args, "ddddd", &p0x, &p0y, &p1x, &p1y, &t)) {
        return NULL;
    }
    
    return _line_xy(p0x, p0y, p1x, p1y, t);
}


static PyObject* cubic_bezier_xy(PyObject *self, PyObject *args) {
    double p0x;
    double p0y;
    double p1x;
    double p1y;
    double p2x;
    double p2y;
    double p3x;
    double p3y;
    double t;
    
    if (!PyArg_ParseTuple(args, "ddddddddd", &p0x, &p0y, &p1x, &p1y, &p2x, &p2y, &p3x, &p3y, &t)) {
        return NULL;
    }
    
    return Py_BuildValue(
        "[dd]",
        (1 - t) * (1 - t) * (1 - t) * p0x + 3 * t * (1 - t) * (1 - t) * p1x + 3 * t * t * (1 - t) * p2x + t * t * t * p3x,
        (1 - t) * (1 - t) * (1 - t) * p0y + 3 * t * (1 - t) * (1 - t) * p1y + 3 * t * t * (1 - t) * p2y + t * t * t * p3y);
}


static PyObject* quadratic_bezier_xy(PyObject *self, PyObject *args) {
    double p0x;
    double p0y;
    double p1x;
    double p1y;
    double p2x;
    double p2y;
    double t;

    if (!PyArg_ParseTuple(args, "ddddddd", &p0x, &p0y, &p1x, &p1y, &p2x, &p2y, &t)) {
        return NULL;
    }

    return Py_BuildValue(
        "[dd]",
        (1 - t) * (1 - t) * p0x + 2 * (1 - t) * t * p1x + t * t * p2x,
        (1 - t) * (1 - t) * p0y + 2 * (1 - t) * t * p1y + t * t * p2y);
}


static double _angleBetween(double v0x, double v0y, double v1x, double v1y) {
    const double p = v0x * v1x + v0y * v1y;
    const double n = sqrt(((v0x * v0x) + (v0y * v0y)) * ((v1x * v1x) + (v1y * v1y)));
    if ((v0x * v1y - v0y * v1x) < 0) {
        return (-(acos(p / n)));
    } else {
        return acos(p / n);
    }
};


static PyObject* elliptical_arc_xy(PyObject *self, PyObject *args) {
    double p0x;
    double p0y;
    double rx;
    double ry;
    double xAxisRotation;
    unsigned short int largeArc;
    unsigned short int sweep;
    double p1x;
    double p1y;
    double t;    
    
    if (!PyArg_ParseTuple(args, "ddddHppddd", &p0x, &p0y, &rx, &ry, &xAxisRotation,
                          &largeArc, &sweep, &p1x, &p1y, &t)) {
        return NULL;
    }
    
    // If the endpoints are identical, then this is equivalent to omitting the elliptical arc segment entirely
    if ((p0x == p1x) && (p0y == p1y)) {
        return Py_BuildValue("[dd]", p0x, p0y);
    }
    
    // If rx = 0 or ry = 0 then this arc is treated as a straight line segment joining the endpoints
    if ((rx == 0) || (ry == 0)) {
        return _line_xy(p0x, p0y, p1x, p1y, t);
    }

    // In accordance to: http://www.w3.org/TR/SVG/implnote.html#ArcOutOfRangeParameters
    // absolutify radius
    if (rx < 0) {
        rx *= -1;
    }
    if (ry < 0) {
        ry *= -1;
    }
    
    xAxisRotation = fmod((fmod(xAxisRotation, 360) + 360), 360);
    const double _xAxisRotationRadians = xAxisRotation * M_PI / 180;


    // Following "Conversion from endpoint to center parameterization"
    // http://www.w3.org/TR/SVG/implnote.html#ArcConversionEndpointToCenter

    // Step #1: Compute transformedPoint
    const double _dx = (p0x - p1x) / 2;
    const double _dy = (p0y - p1y) / 2;
    const double _transformedPointX = cos(_xAxisRotationRadians) * _dx + sin(_xAxisRotationRadians) * _dy;
    const double _transformedPointY = (-sin(_xAxisRotationRadians)) * _dx + cos(_xAxisRotationRadians) * _dy;
    
    
    // Ensure radii are large enough
    const double _radiiCheck = (_transformedPointX * _transformedPointX) / (rx * rx) +
                               (_transformedPointY * _transformedPointY) / (ry * ry);
    if (_radiiCheck > 1) {
        rx = sqrt(_radiiCheck) * rx;
        ry = sqrt(_radiiCheck) * ry;
    }
    
    // Step #2: Compute transformedCenter
    const double _cSquareNumerator = (rx * rx) * (ry * ry) - (rx * rx) *
                                     (_transformedPointY * _transformedPointY) -
                                     (ry * ry) * (_transformedPointX * _transformedPointX);
    const double _cSquareRootDenom = (rx * rx) * (_transformedPointY * _transformedPointY) +
                                     (ry * ry) * (_transformedPointX * _transformedPointX);
    double _cRadicand = _cSquareNumerator / _cSquareRootDenom;
    double _cCoef;
    if (_cRadicand < 0) {
        _cRadicand = 0;
        _cCoef = 0;
    } else if (largeArc != sweep) {
        _cCoef = sqrt(_cRadicand);
    } else {
        _cCoef = (-(sqrt(_cRadicand)));
    }
    
    const double _transformedCenterX = _cCoef * ((rx * _transformedPointY) / ry);
    const double _transformedCenterY = _cCoef * (-(ry * _transformedPointX) / rx);
    
    // Step #3: Compute center
    const double _centerX = cos(_xAxisRotationRadians) * _transformedCenterX -
                            sin(_xAxisRotationRadians) * _transformedCenterY +
                            ((p0x + p1x) / 2);
    const double _centerY = sin(_xAxisRotationRadians) * _transformedCenterX +
                            cos(_xAxisRotationRadians) * _transformedCenterY +
                            ((p0y + p1y) / 2);

    // Step #4: Compute start/sweep angles
    // Start angle of the elliptical arc prior to the stretch and rotate operations.
    // Difference between the start and end angles
    const double _startVectorX = (_transformedPointX - _transformedCenterX) / rx;
    const double _startVectorY = (_transformedPointY - _transformedCenterY) / ry;
    const double _startAngle = _angleBetween(1, 0, _startVectorX, _startVectorY);
    
    const double _endVectorX = ((-_transformedPointX) - _transformedCenterX) / rx;
    const double _endVectorY = ((-_transformedPointY) - _transformedCenterY) / ry;
    
    double _sweepAngle = _angleBetween(_startVectorX, _startVectorY, _endVectorX, _endVectorY);
    
    if ((!sweep) && (_sweepAngle > 0)) {
        _sweepAngle -= __M_PI_POW;
    } else if ((sweep) && (_sweepAngle < 0)) {
        _sweepAngle += __M_PI_POW;
    }
    _sweepAngle = fmod(_sweepAngle,  __M_PI_POW);
    
    // From http://www.w3.org/TR/SVG/implnote.html#ArcParameterizationAlternatives
    const double _angle = _startAngle + _sweepAngle * t;
    const double _ellipseComponentX = rx * cos(_angle);
    const double _ellipseComponentY = ry * sin(_angle);
    
    return Py_BuildValue(
        "[dd]",
        cos(_xAxisRotationRadians) * _ellipseComponentX - sin(_xAxisRotationRadians) * _ellipseComponentY + _centerX,
        sin(_xAxisRotationRadians) * _ellipseComponentX + cos(_xAxisRotationRadians) * _ellipseComponentY + _centerY);
}

/**
 * Module methods definition.
 **/
static PyMethodDef PolfMethods[] = {
    {
        "line_xy", line_xy, METH_VARARGS,
        "Computes the coordinate of a point in a line parametrized"
        " in the range ``t`` from 0 to 1.\n\n"
        "Algorithm: ``B(t) = p0 + (p1 - p0) * t , 0 <= t <= 1``\n\n"
        ":param p0x: X value for starting point.\n"
        ":type p0x: float\n"
        ":param p0y: Y value for starting point.\n"
        ":type p0y: float\n"
        ":param p1x: X value for ending point.\n"
        ":type p1x: float\n"
        ":param p1y: Y value for ending point.\n"
        ":type p1y: float\n"
        ":param t: Number in the range from 0 to 1 that parametrizes"
        " the location in the line.\n"
        ":type t: float\n"
        ":returns: Point inside the line for the value ``t``.\n"
        ":rtype: list\n"
    },
    {
        "cubic_bezier_xy", cubic_bezier_xy, METH_VARARGS,
        "Computes the coordinate of a point in a cubic Bézier curve"
        " parametrized in the range ``t`` from 0 to 1.\n\n"
        "Algorithm: ``B(t) = (1-t)**3 * p0 + 3*(1-t)**2 * t * p1 + 3*(1-t)**2"
        " * p2 + t**3 * p3 , 0 <= t <= 1``\n\n"
        ":param p0x: X value for starting point.\n"
        ":type p0x: float\n"
        ":param p0y: Y value for starting point.\n"
        ":type p0y: float\n"
        ":param p1x: X value for first control point.\n"
        ":type p1x: float\n"
        ":param p1y: Y value for first control point.\n"
        ":type p1y: float\n"
        ":param p2x: X value for second control point.\n"
        ":type p2x: float\n"
        ":param p2y: Y value for second control point.\n"
        ":type p2y: float\n"
        ":param p3x: X value for ending point.\n"
        ":type p3x: float\n"
        ":param p3y: Y value for ending point.\n"
        ":type p3y: float\n"
        ":param t: Number in the range from 0 to 1 that parametrizes"
        " the location in the cubic Bézier curve.\n"
        ":type t: float\n"
        ":returns: Point inside the cubic Bézier curve for the value ``t``.\n"
        ":rtype: list\n"
    },
    {
        "quadratic_bezier_xy", quadratic_bezier_xy, METH_VARARGS,
        "Computes the coordinate of a point in a quadratic Bézier curve"
        " parametrized in the range ``t`` from 0 to 1.\n\n"
        "Algorithm: ``B(t) = (1-t)**2 * p0 + 2*(1-t)*t *p1 + t**2 * p2``\n\n"
        ":param p0x: X value for starting point.\n"
        ":type p0x: float\n"
        ":param p0y: Y value for starting point.\n"
        ":type p0y: float\n"
        ":param p1x: X value for control point.\n"
        ":type p1x: float\n"
        ":param p1y: Y value for control point.\n"
        ":type p1y: float\n"
        ":param p2x: X value for ending point.\n"
        ":type p2x: float\n"
        ":param p2y: Y value for ending point.\n"
        ":type p2y: float\n"
        ":param t: Number in the range from 0 to 1 that parametrizes"
        " the location in the quadratic Bézier curve.\n"
        ":type t: float\n"
        ":returns: Point inside the quadratic bezier curve for the value ``t``.\n"
        ":rtype: list\n"
    },
    {
        "elliptical_arc_xy", elliptical_arc_xy, METH_VARARGS,
        "Computes the coordinate of a point in a elliptical arc parametrized in"
        " the range ``t`` from 0 to 1.\nThis implementation follows"
        " `SVG2 specification <https://www.w3.org/TR/SVG2/implnote.html>`_.\n\n"
        ":param p0x: X value for starting point.\n"
        ":type p0x: float\n"
        ":param p0y: Y value for starting point.\n"
        ":type p0y: float\n"
        ":param rx: Arc width.\n"
        ":type rx: float\n"
        ":param ry: Arc height.\n"
        ":type ry: float\n"
        ":param x_axis_rotation: Arc rotation on x axis.\n"
        ":type x_axis_rotation: float\n"
        ":param large_arc: ``large-arc`` flag that specifies how the arc is drawn.\n"
        ":type large_arc: bool\n"
        ":param sweep: ``sweep`` flag that specifies how the arc is drawn.\n"
        ":type sweep: bool\n"
        ":param p1x: X value for ending point.\n"
        ":type p1x: float\n"
        ":param p1y: Y value for ending point.\n"
        ":type p1y: float\n"
        ":param t: Number in the range from 0 to 1 that parametrizes"
        " the location in the elliptical arc.\n"
        ":type t: float\n"
        ":returns: Point inside the elliptical arc for the value ``t``.\n"
        ":rtype: list\n"
    },
    {NULL, NULL, 0, NULL}
};


/**
 * Module definition.
 **/
static PyModuleDef polf = {
    PyModuleDef_HEAD_INIT,
    "polf",
    "Calculate points on lines.",
    -1,
    PolfMethods,
};

/**
 * Module initialization function.
 **/
PyMODINIT_FUNC PyInit_polf(void)
{
    PyObject *m;
    m = PyModule_Create(&polf);
    if (m == NULL) {
        return NULL;
    }

    if (PyModule_AddStringConstant(m, "__version__", "0.0.3") < 0) {
        Py_DECREF(m);
        return NULL;
    }

    if (PyModule_AddStringConstant(m, "__title__", "polf") < 0) {
        Py_DECREF(m);
        return NULL;
    }

    return m;
}