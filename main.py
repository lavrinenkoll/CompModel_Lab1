import numpy as np
import random
import matplotlib.pyplot as plt
import math
import scipy.integrate


# generate data by formula with values a and s
def generate(a, s, n):
    data = np.zeros(n)
    for i in range(0,n):
        sum = 0
        for j in range (0,12,1):
            random_value = random.uniform(0,1)
            sum += random_value
        sum -=6
        data[i] = s*sum + a
    return data


# show info about data, draw histogram
def info_data(data, title = "", graph = False):
    mean = np.mean(data)
    var = np.var(data)
    sr = var**(1/2)

    if graph:
        plt.hist(data, bins=20)
        plt.title(title)
        plt.show()

    print("Середнє експериментальне:", mean)
    print("Середньоквадратичне експериментальне:", sr)
    print("Дисперсія експериментальне:", var)

    return mean, sr, var


# calculate intervals and count in intervals for data
def set_intervals(data, n):
    min = np.min(data)
    max = np.max(data)
    step = (max-min)/(n-1)
    intervals = []
    for i in range(0,n):
        intervals.append(min-step/2+i*step)

    count_in_intervals = np.zeros(n-1)
    for i in range(0,n-1):
        for j in range(0,len(data)):
            if data[j] > intervals[i] and data[j] <= intervals[i+1]:
                count_in_intervals[i] += 1

    return intervals, count_in_intervals


# group intervals with count less than 5 in experiment and theory
def group(count_in_intervals, count_teor, n):
    for i in range(0,n-2):
        if count_in_intervals[i] < 5:
            count_in_intervals[i+1] += count_in_intervals[i]
            count_teor[i+1] += count_teor[i]
            count_teor[i] = 0
            count_in_intervals[i] = 0

    count_in_intervals = count_in_intervals[count_in_intervals != 0]
    count_teor = [x for x in count_teor if x != 0]

    if count_in_intervals[-1] < 5:
        count_in_intervals[-2]+=count_in_intervals[-1]
        count_teor[-2]+=count_teor[-1]
        count_in_intervals[-1] = 0
        count_teor[-1] = 0

    count_in_intervals = count_in_intervals[count_in_intervals != 0]
    count_teor = [x for x in count_teor if x != 0]

    return count_in_intervals, count_teor


# density function
def func(x, a, s):
    return (math.e**(-(x-a)**2/(2*s*s)))/(s*(2*math.pi)**(1/2))


# calculate density and count in intervals for theory
def density_func(intervals, a, s, n):
    density = []
    for i in range(0, len(intervals)-1):
        density.append(scipy.integrate.quad(func, intervals[i], intervals[i+1], args=(a, s))[0])

    count_in_intervals = []
    for i in range(0, len(density)):
        count_in_intervals.append(abs(density[i]*n))
    return density, count_in_intervals


# calculate chi2
def calculate_chi2(count_experemental_group, count_teor_group):
    chi2_exp = 0
    for i in range(0, len(count_experemental_group)):
        chi2_exp += (count_experemental_group[i] - count_teor_group[i])**2/count_teor_group[i]
    return chi2_exp


# compare chi2 with chi2 table and print result
def compare_chi2(chi2_exp, n):
    from scipy.stats import chi2
    chi2_table = chi2.ppf(0.95, n-3)
    print("Хі квадрат табличний:", chi2_table)
    if chi2_exp < chi2_table:
        print("Розподіл нормальний")
        return 1
    else:
        print("Розподіл не нормальний")
        return 0



if __name__ == "__main__":
    # main, show result for data with a and s
    a = 3
    s = 0.5
    n = 10000
    default_n = 20

    print("a: ", a, ", s: ", s)
    data = generate(a, s, n)
    info_data(data, "Гістограма частот для випадкових даних при a = {}, s = {}".format(a, s), True)

    intervals, count_experemental = set_intervals(data, default_n)
    density, count_teor = density_func(intervals, a, s, n)
    count_experemental_group, count_teor_group = group(count_experemental, count_teor, default_n)

    chi2_exp = calculate_chi2(count_experemental_group, count_teor_group)
    print("\nХі квадрат експериментальний:", chi2_exp)
    compare_chi2(chi2_exp, len(count_experemental_group))

