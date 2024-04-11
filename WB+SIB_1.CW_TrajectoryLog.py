from pylinac import (TrajectoryLog)
from pylinac import Dynalog
import numpy as np
import matplotlib.pyplot as plt
from pylinac.log_analyzer import MachineLogs

log_file_path1='/home/bi/LOG/log/data/WB+SIB_1.CW_20230603113548/WB+SIB_1.CW_20230603113548.bin'

print("##############################################################")

tlog=TrajectoryLog('/home/bi/LOG/log/data/Lt.breast_1.RAO_20230420160142/Lt.breast_4.LAO_20230420160036.bin' )
print(f"header:{tlog.header.header}")
print(f"header_size:{tlog.header.header_size}")
print(f"version:{tlog.header.version}")
print(f"sampling interval:{tlog.header.sampling_interval}ms")
print(f"number of axes:{tlog.header.num_axes}")
print(f"axis enumarate:{tlog.header.axis_enum}")
print(f"samples/axis:{tlog.header.samples_per_axis}")
print(f"number of MLC Leaves:{tlog.header.num_mlc_leaves}")
print(f"axis scale:{tlog.header.axis_scale}")
print(f"number of subbeams:{tlog.header.num_subbeams}")
print(f"Is truncated?:{tlog.header.is_truncated}")
print(f"MLC Model:{tlog.header.mlc_model}")
print(f"number of snapshots:{tlog.header.num_snapshots}")
print(f"Number of control points: {len(tlog.axis_data.control_point.actual)}")
print("##############################################################")

# total_MU_per_control_point=[]
mu_value=tlog.axis_data.mu.actual


for i, mu in enumerate(mu_value, start=1):
    print(f"제어점:{i}: 실제 MU={mu}")
print("##############################################################")


gantry_position=tlog.axis_data.gantry.actual
for i, gantry_position in enumerate(gantry_position, start=1):
    print(f"제어점:{i}: 실제 POSITION={gantry_position}")
print("##############################################################")


control_points=tlog.axis_data.control_point.actual
for i, control_points in enumerate(control_points, start=1):
    print(f"제어점:{i}: 실제 Control point={control_points}")
print("##############################################################")

mu_diff=np.diff(tlog.axis_data.mu.actual)
x=(len(tlog.axis_data.control_point.actual)*tlog.header.sampling_interval)/60000
MU_rate=mu_diff/x #snapshot: 60000=20*60*(1/0.02)
print("************************************************************")
print(mu_diff)
print(MU_rate)




total_MU_rate_per_control_point=[]
total_MU_rate_per_control_point=[sum(MU_rate[:i+1]) for i in range(len(MU_rate))]
total_MU_per_control_point=[]
total_MU_per_control_point=[sum(MU_rate[:i+1])/x for i in range(len(MU_rate))]



plt.plot(total_MU_rate_per_control_point, color='black', linestyle='--')
plt.title('MU rate sum Graph', fontsize=15)
plt.xlabel('Control Points')
plt.ylabel('Sum MU rate')
plt.grid(color='gray', linestyle='--', linewidth=0.3)
plt.savefig('MU_rate_sum', dpi=300)
plt.show()

plt.plot(mu_diff)
plt.title('MU: WB+SIB_1.CW TrajectoryLog', fontsize=15)
plt.xlabel('Control points')
plt.ylabel('MU')
plt.grid(color='gray', linestyle='--', linewidth=0.3)
plt.savefig('MU_graph', dpi=300)
plt.show()

tlog.axis_data.mu.plot_actual()
tlog.axis_data.mu.plot_difference()

print(total_MU_per_control_point)

plt.plot(total_MU_per_control_point, color='red', linestyle='--')
plt.title('MU sum Graph', fontsize=15)
plt.xlabel('Control Points')
plt.ylabel('Sum MU')
plt.grid(color='gray', linestyle='--', linewidth=0.3)
plt.savefig('MU_sum', dpi=300)
plt.show()

print(tlog.axis_data.mu.actual.sum(axis=0)/3000)
print(mu_value.sum(axis=0))
print(MU_rate.sum(axis=0))

for i, total_MU_per_control_point in enumerate(total_MU_per_control_point, start=1):
    print(f"제어점:{i}: 실제 MU SUM={total_MU_per_control_point}")



