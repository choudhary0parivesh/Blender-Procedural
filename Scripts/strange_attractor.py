import numpy as np, pandas as pd, datashader as ds
from datashader import transfer_functions as tf
from datashader import utils
from datashader.colors import inferno, viridis
from numba import jit
from math import sin, cos, sqrt, fabs

@jit(nopython=True)
def G(x, mu):
    return mu * x + 2 * (1 - mu) * x**2 / (1.0 + x**2)

@jit(nopython=True)
def Gumowski_Mira(x, y, a, b, mu, *o):
    xn = y + a*(1 - b*y**2)*y  +  G(x, mu)
    yn = -x + G(xn, mu)
    return xn, yn

@jit(nopython=True)
def Clifford(x, y, a, b, c, d, *o):
    return sin(a * y) - c * cos(a * x), \
           sin(b * x) + d * cos(b * y)

@jit(nopython=True)
def Hopalong1(x, y, a, b, c, *o):
    return y - sqrt(fabs(b * x - c)) * np.sign(x), \
           a - x

@jit(nopython=True)
def Symmetric_Icon(x, y, a, b, g, om, l, d, *o):
    zzbar = x*x + y*y
    p = a*zzbar + l
    zreal, zimag = x, y
    
    for i in range(1, d-1):
        za, zb = zreal * x - zimag * y, zimag * x + zreal * y
        zreal, zimag = za, zb
    
    zn = x*zreal - y*zimag
    p += b*zn
    
    return p*x + g*zreal - om*y, \
           p*y - g*zimag + om*x

n=100000000

@jit(nopython=True)
def trajectory_coords(fn, x0, y0, a, b=0, c=0, d=0, e=0, f=0, n=n):
    x, y = np.zeros(n), np.zeros(n)
    x[0], y[0] = x0, y0
    for i in np.arange(n-1):
        x[i+1], y[i+1] = fn(x[i], y[i], a, b, c, d, e, f)
    return x,y

def trajectory(fn, x0, y0, a, b=0, c=0, d=0, e=0, f=0, n=n):
    x, y = trajectory_coords(fn, x0, y0, a, b, c, d, e, f, n)
    return pd.DataFrame(dict(x=x,y=y))

# df = trajectory(Clifford, 0, 0, -1.3, -1.3, -1.8, -1.9)
# df = trajectory(Hopalong1, 0, 0, -11.0, 0.05, 0.5)
# df = trajectory(Symmetric_Icon,0.01, 0.01, 2.32, 0.0, 0.75, 0.0, -2.32, 5)
df = trajectory(Gumowski_Mira,0, 1, 0.008, 0.05, -0.496)
# df.to_csv("ab.csv", sep=',')
cvs = ds.Canvas(plot_width = 4000, plot_height = 4000)
agg = cvs.points(df, 'x', 'y')
print(agg.values[190:195,190:195],"\n")
ds.transfer_functions.Image.border=0

# tf.shade(agg, cmap = ["white", "black"])

utils.export_image(tf.shade(agg, cmap = ["white", "black"]),filename='Oct2431doshade.png')
