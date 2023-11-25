# Imports
import numpy as np
import matplotlib.pyplot as plt
import time
from multiprocessing import Pool, cpu_count, Queue, Process
from math import sqrt, fabs


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


def call_mandelbrot_serial(xmin, xmax, ymin, ymax, N, results, i):
    results.put({i: mandelbrot_serial(xmin, xmax, ymin, ymax, N)})


def mandelbrot_static(xmin, xmax, ymin, ymax, N=100):
    results = Queue()
    processes = []
    count = cpu_count() // 2
    arr_upper = np.ndarray(shape=(0, N // count))
    arr_lower = np.ndarray(shape=(0, N // count))
    incx = fabs((xmax - xmin) / count)

    x, i = xmin, 0
    while i < cpu_count():
        i += 1
        if i == count + 1:
            x = xmin  # refresh x to xmin

        if i > count:
            p = Process(target=call_mandelbrot_serial, args=(x, x + incx, ymin, 0, N // count, results, i))
            p.start()
            processes.append(p)
            x += incx
        else:
            p = Process(target=call_mandelbrot_serial, args=(x, x + incx, 0, ymax, N // count, results, i))
            p.start()
            processes.append(p)
            x += incx

    result_set = {}
    for p in processes:
        result_set.update(results.get())

    i = 1

    for p in processes:
        if i <= count:
            if i == 1:
                arr_upper = np.vstack([arr_upper, result_set[i]])
            else:
                arr_upper = np.concatenate((arr_upper, result_set[i]), axis=1)
        else:
            if i == count + 1:
                arr_lower = np.vstack([arr_lower, result_set[i]])
            else:
                arr_lower = np.concatenate((arr_lower, result_set[i]), axis=1)
        i += 1

    for p in processes:
        p.join()

    return np.append(arr_upper, arr_lower, axis=0)


def mandelbrot_dynamic(xmin, xmax, ymin, ymax, N=100):
    incx = fabs((xmax - xmin) / N)
    incy = fabs((ymax - ymin) / N)
    x, y, myList, lst, n = xmin, ymax, [], [], 1
    while y > ymin and n <= N:
        while x < xmax:
            lst.append(complex(x, y))
            x += incx
        x = xmin
        y -= incy
        myList.extend(lst[:N])
        n += 1
        lst = []

    with Pool() as pool:
        result = pool.map(mandelbrot, myList)

    return np.reshape(np.array(result), (N, N))

xmin = -2.25
xmax = 0.75
ymin = -1.5
ymax = 1.5

start_time = time.time()
arr = mandelbrot_static(xmin, xmax, ymin, ymax, N=600)
end_time = time.time()
execution_time = end_time - start_time
execution_time *= 1000
print(f"Wykonano w czasie {execution_time} ms.")
plt.imshow(arr, extent=[xmin, xmax, ymin, ymax])
plt.savefig('MandelBrot.png')
plt.show()

start_time = time.time()
arr = mandelbrot_dynamic(xmin, xmax, ymin, ymax, N=600)
end_time = time.time()
execution_time = end_time - start_time
execution_time *= 1000
print(f"Wykonano w czasie {execution_time} ms.")
plt.imshow(arr, extent=[xmin, xmax, ymin, ymax])
plt.savefig('MandelBrot.png')
plt.show()
