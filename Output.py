from pylinac import (TrajectoryLog)
from pylinac import Dynalog
import numpy as np
import matplotlib.pyplot as plt
from pylinac.log_analyzer import MachineLogs

log_file_path1='/home/bi/LOG/log/data/WB+SIB_1.CW_20230603113548/WB+SIB_1.CW_20230603113548.bin'

print("##############################################################")

tlog=TrajectoryLog('/home/bi/LOG/log/data/WB+SIB_1.CW_20230603113548/WB+SIB_1.CW_20230603113548.bin')

control_point=tlog.axis_data.control_point.actual
print(control_point)
leaves=np.zeros((120,3888))
print(tlog.axis_data.mlc.num_leaves)
for i in range(tlog.axis_data.mlc.num_leaves):
    leaves_list=tlog.axis_data.mlc.leaf_axes[i+1].actual
    leaves[i]=leaves_list

print(leaves)
print(leaves.shape)
print(tlog.axis_data.mlc.num_moving_leaves)

# MLC의 위치 값
mlc_positions = leaves[:,100]
print(mlc_positions)

# 왼쪽 리프와 오른쪽 리프의 위치 분리
left_data = mlc_positions[:60]
right_data = mlc_positions[60:]

y_values_left = np.arange(0, 60)
y_values_right = np.arange(61, 121)

# 새로운 그림과 축을 생성합니다.
fig, ax1 = plt.subplots()

for i in range(len(left_data)):
    height = 0.8 if i < 10 or i >= 50 else 1.5  # 특정 범위의 인덱스에 대해 막대의 두께를 조정
    ax1.barh(i+1, left_data[i], color='blue', height=height)

# 오른쪽 y축을 만들고 오른쪽 데이터에 대한 막대 그래프를 그립니다.
ax2 = ax1.twinx()
for i in range(len(right_data)):
    height = 0.8 if i < 10 or i >= 50 else 1.5
    ax2.barh(i+1, right_data[i], color='red', height=height, zorder=10)


ax1.set_xlabel('Value')
ax1.set_ylabel('Index (1-60)')
ax1.set_xlim(-10, 10)
ax1.invert_yaxis()  # y축의 순서를 뒤집습니다.
ax1.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)


ax2.set_ylim(ax1.get_ylim())  # 오른쪽 y축의 범위를 왼쪽 y축과 동일하게 설정
ax2.set_ylabel('Index (61-120)')
ax2.grid(True, which='both', axis='x', linestyle='--', linewidth=0.5)



plt.title('Beam\'s Eye View (BEV) with Variable Thickness')
plt.show()
