from pylinac import (TrajectoryLog)
from pylinac import Dynalog
import numpy as np
import csv
import pandas as pd
from pylinac import load_log
import matplotlib.pyplot as plt
from pylinac.log_analyzer import MachineLogs
from pylinac.log_analyzer import FluenceBase

log_file_path1='/home/bi/LOG/log/data/Lt.breast_1.RAO_20230420160142/Lt.breast_1.RAO_20230420160142.bin'
log_file_path2='/home/bi/LOG/log/data/WB+SIB_1.CW_20230603113548/WB+SIB_1.CW_20230603113548.bin'

print("##############################################################")


tlog=TrajectoryLog(log_file_path1)
tlog2=TrajectoryLog(log_file_path2)


cp=tlog2.axis_data.control_point.actual
print(tlog2.axis_data.control_point.actual)
print(f"number of control point: {len(cp)}")

num_leaf=tlog2.axis_data.mlc.leaf_axes
print(tlog2.axis_data.mlc.leaf_axes)
print(f"number of mlc leaf: {len(num_leaf)}")

mlc_cp=np.zeros((120,3888))
print(mlc_cp)

for i in range(len(tlog2.axis_data.mlc.leaf_axes)):
    mlc_cp[i,:]=tlog2.axis_data.mlc.leaf_axes[i+1].actual

print(mlc_cp)
print(mlc_cp.shape)
