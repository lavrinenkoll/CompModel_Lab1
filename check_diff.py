from main import *


# show result for data with different a and s and calculate percent of normal distribution
sum = 0; all = 0; n = 10000; default_n = 20
for i in range (-200,210,10):
    for j in range(5,210,10):
        a = i/10
        s = j/10
        print("\na: ", a, ", s: ", s)
        data = generate(a, s, n)
        info_data(data)
        intervals, count_experemental = set_intervals(data, default_n)
        density, count_teor = density_func(intervals, a, s, n)
        count_experemental_group, count_teor_group = group(count_experemental, count_teor, default_n)

        chi2_exp = calculate_chi2(count_experemental_group, count_teor_group)
        print("Хі квадрат експериментальний:", chi2_exp, end="\n")
        k = compare_chi2(chi2_exp, len(count_experemental_group))
        sum += k
        all+=1


# analyze percent of normal distribution and input data
print("\nВідповідають нормальному закону: ", sum)
print("Всього: ", all)
print("Відповідають нормальному закону: ", sum/all*100, "%")