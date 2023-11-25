import time
from math import fabs
from multiprocessing import Pool, cpu_count, Queue, Process

import matplotlib.pyplot as plt
import numpy as np


def mandelbrot(c, max_iterations=100):
    z = 0
    for i in range(max_iterations):
        z = z ** 2 + c
        if z.real ** 2 + z.imag ** 2 > 4:
            return i + 1
        if i == max_iterations - 1:
            return 0


def mandelbrot_serial(xmin, xmax, ymin, ymax, N=100):
    incx = fabs((xmax - xmin) / N)
    incy = fabs((ymax - ymin) / N)
    x, y, myList, n, arr = xmin, ymax, [], 1, np.ndarray(shape=(0, N))
    while y > ymin and n <= N:
        while x < xmax:
            i = mandelbrot(complex(x, y), 100)
            myList.append(i)
            x += incx
        arr = np.append(arr, np.array([myList[:N]]), axis=0)
        x = xmin
        y -= incy
        myList = []
        n += 1
    return arr


xmin = -2.25
xmax = 0.75
ymin = -1.5
ymax = 1.5

print('mandelbrot_serial, Resolution 600x600:')
start = time.time()
arr = mandelbrot_serial(xmin, xmax, ymin, ymax, N=600)
end = time.time()
print(f'{end - start} secs')
plt.imshow(arr, extent=[xmin, xmax, ymin, ymax])
plt.savefig('MandelBrot.png')
plt.show()
