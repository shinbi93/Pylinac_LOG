from pylinac import (TrajectoryLog)
from pylinac import Dynalog
import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
from pylinac.log_analyzer import MachineLogs

log_file_path1='/home/bi/LOG/log/data/WB+SIB_1.CW_20230603113548/WB+SIB_1.CW_20230603113548.bin'
tlog=TrajectoryLog(log_file_path1)


#number of control point
cp=tlog.axis_data.control_point.actual
print(tlog.axis_data.control_point.actual)
print(f"number of control point: {len(cp)}")
# for i in range(0,len(cp)):
#     print(f"제어점:{i}: 실제 Control point={tlog.axis_data.control_point.actual[i]}")

#Monitor Unit and Dose Rate Set
mu_actual=np.diff(tlog.axis_data.mu.actual)
print(f"MU value: {sum(mu_actual)}MU")
print(f"Dose Rate value: {sum(mu_actual)/20}MU/min")
print(f"Dose Rate value: {sum(mu_actual)/60}MU/sec")

#Monitor Unit at CP

# for i in range(0,len(cp)):
#     print(f"제어점:{i}: 실제 Control point의 MU={tlog.axis_data.mu.actual[i]}MU")

num_leaf=tlog.axis_data.mlc.leaf_axes
# for i in range(1,len(num_leaf)+1):
#      print(f"제어점:{i}: 실제 Control point={tlog.axis_data.mlc.leaf_axes[i].actual}cm")


#1부터 120까지 가지는 배열: num_leaf
#1부터 3888까지 가지는 배열: tlog.axis_data.control_point
#120*3888의 배열을 만들어 데이터를 삽입하는 방법
mlc_cp_position=np.zeros((120,3888))
print(mlc_cp_position)

for i in range(len(tlog.axis_data.mlc.leaf_axes)):
    mlc_cp_position[i,:]=tlog.axis_data.mlc.leaf_axes[i+1].actual

print(mlc_cp_position)

#field size
field_size=np.zeros(3888)


for cp in range(mlc_cp_position.shape[1]):
    left_position=mlc_cp_position[:60,cp]
    right_position=mlc_cp_position[60:,cp]
    print("*******************************************************")
    print(left_position)
    # print(left_position)
    x_axis=np.zeros(3888)
    x_axis=(left_position[cp]-right_position[cp])
    field_size[cp]=x_axis
    # x_axis=mlc_cp_position[60:, cp]-mlc_cp_position[:60, cp]
    # print(f"{cp} => {x_axis[cp]}")
    # x_axis=(mlc_cp_position[60:, cp])-(mlc_cp_position[:60, cp])
    # field_size[cp] = x_axis
    # print(f"Field size {cp}: {field_size[cp]}")

#
# print(np.min(x_axis))
# print(np.argmin(x_axis))
# x_min_index=np.argmin(x_axis)
# print(np.max(x_axis))
# print(np.argmax(x_axis))
# x_max_index=np.argmax(x_axis)
#
# for cp in range(mlc_cp_position.shape[1]):
#     y_axis=mlc_cp_position[:60, cp]-mlc_cp_position[60:, cp]




# for cp in range(mlc_cp_position.shape[1]):
#     left_most_leaf_position=np.min(mlc_cp_position[:60, cp])
#     left_most_leaf_position1=np.argmin(mlc_cp_position[:60, cp])
#     right_most_leaf_position=np.max(mlc_cp_position[60:, cp])
#     right_most_leaf_position1 = np.argmin(mlc_cp_position[60:, cp])
#     print(f"{cp} => Left: {left_most_leaf_position}, Right: {right_most_leaf_position}")
#     field_width=right_most_leaf_position[cp]-left_most_leaf_position[cp]
#     field_size[cp]=field_width
#     print(f"Field size {cp}: {field_size[cp]}")
#     min_field_size=np.min(field_size)
    # min_field_index=np.argmin(field_size)
    # min_array=np.unravel_index(min_field_index,field_size.shape)
    # max_field_size=np.max(field_size)
    # max_field_index=np.argmax(field_size)


# print(f"Minimum field size: {min_field_size}")
# print(f"Maximum field size: {max_field_size}")
# print(max_field_index)
# print(min_field_index)
# print(min_array)














# print(min_field_size, min_index_position)
# print("Field size of the Last control point:",field_size[3887])
# print("Field size of the First control point:",field_size[0])
# print(f"Field size : {field_size[0]}*{field_size[3887]}cm^2")
# print(mlc_cp_position.shape[0])
# print(mlc_cp_position[:,1])
# print(mlc_cp_position[:,2])
# print(mlc_cp_position[:,1]-mlc_cp_position[:,2])
# for cp in range(mlc_cp_position.shape[1]):
#     left_most_leaf_position=np.min(mlc_cp_position[:60, cp])
#     right_most_leaf_position = np.max(mlc_cp_position[60:, cp])
#     print(left_most_leaf_position,right_most_leaf_position)


# multipliers=np.ones(120)
# multipliers[10:49] = 0.5
# multipliers[60:99] = 0.5
# adjusted_mlc_cp_position= mlc_cp_position*multipliers[:,None]
# print(adjusted_mlc_cp_position[1])
# print(mlc_cp_position[1])
# print(adjusted_mlc_cp_position[20])
# print(mlc_cp_position[20])
#
# for cp in range(3888):
#     left_most_leaf_position=np.max(adjusted_mlc_cp_position[:60, cp])
#     right_most_leaf_position = np.min(adjusted_mlc_cp_position[60:, cp])
#     y_value_comparison=left_most_leaf_position-right_most_leaf_position
#     y_value_comparison_min=np.min(y_value_comparison)
#     min_index=np.argmin(y_value_comparison_min)
#
#
# print(y_value_comparison_min)
# print(min_index)

for cp in range(mlc_cp_position.shape[1]):
    left_most_leaf_position=np.min(mlc_cp_position[:60, cp])
    right_most_leaf_position=np.max(mlc_cp_position[60:, cp])
    field_width=right_most_leaf_position-left_most_leaf_position
    field_size[cp]=field_width




# field_sizes=np.zeros(mlc_cp_position.shape[1])
#
# for cp in range(mlc_cp_position.shape[1]):
#     min_pos=np.min(mlc_cp_position[:,cp])
#     max_pos=np.max(mlc_cp_position[:,cp])
#     field_size= max_pos-min_pos
#     field_sizes[cp]=field_size
#     print(f"field size at the {cp} point: {field_sizes[cp]}")