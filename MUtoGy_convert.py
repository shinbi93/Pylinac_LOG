from pylinac import (TrajectoryLog)
from pylinac import Dynalog
import numpy as np
import matplotlib.pyplot as plt
from pylinac.log_analyzer import MachineLogs

log_file_path1='/home/bi/LOG/log/data/WB+SIB_1.CW_20230603113548/WB+SIB_1.CW_20230603113548.bin'

print("##############################################################")


tlog=TrajectoryLog('/home/bi/LOG/log/data/WB+SIB_1.CW_20230603113548/WB+SIB_1.CW_20230603113548.bin')

mu_value=tlog.axis_data.mu.actual
print(mu_value)
mu_diff = np.diff(mu_value,axis=0)
print(mu_diff)
print(len(mu_diff))
sum_mu_diff=sum(mu_diff)
print(f"{sum_mu_diff}MU")
MU_rate=sum_mu_diff/1.296
print(f"{MU_rate} MU/min 선량이 매분 전달되었다")# 매분 20MU의 선량이 전달되었다.

mu_to_gy_conversion_factor=0.01

print(f"Conversion factor: {mu_to_gy_conversion_factor}")
sum_gy=sum_mu_diff*mu_to_gy_conversion_factor
print(f"MU to Gy: {sum_gy}Gy")


mu_expected=tlog.axis_data.mu.expected
print(f"{max(mu_expected)}MU")

print("Expected - Actual: ", max(mu_expected)-sum_mu_diff)


