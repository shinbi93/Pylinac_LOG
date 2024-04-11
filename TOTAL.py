from pylinac import TrajectoryLog
from pylinac import Dynalog
#from pylinac import JawStruct
import numpy as np
import matplotlib.pyplot as plt
from pylinac.log_analyzer import MachineLogs

log_file_path1='/home/bi/LOG/log/data/WB+SIB_1.CW_20230603113548/WB+SIB_1.CW_20230603113548.bin'
tlog=TrajectoryLog(log_file_path1)

print("##############################################################")
print(f"Loaded log file: {log_file_path1}")
print(f"header:{tlog.header.header}")
print(f"header_size:{tlog.header.header_size}")
print(f"version:{tlog.header.version}")
print(f"sampling interval:{tlog.header.sampling_interval}ms")
print(f"number of axes:{tlog.header.num_axes}")
print(f"axis enumarate:{tlog.header.axis_enum}")
print(f"samples/axis:{tlog.header.samples_per_axis}")
print(f"axis scale:{tlog.header.axis_scale}")
print(f"number of subbeams:{tlog.header.num_subbeams}")
print(f"Is truncated?:{tlog.header.is_truncated}")

print(f"MLC Model:{tlog.header.mlc_model}")
print(f"number of MLC Leaves:{tlog.header.num_mlc_leaves}")
print(f"number of snapshots:{tlog.header.num_snapshots}")
print(f"Number of control points: {len(tlog.axis_data.control_point.actual)}")
print("##############################################################")


#MU
mu_value=tlog.axis_data.mu.actual
# for i, mu in enumerate(mu_value, start=1):
#     print(f"제어점:{i}: 실제 MU={mu}")
#
# print("##############################################################")

#control point
control_points=tlog.axis_data.control_point.actual
# for i, control_points in enumerate(control_points, start=1):
#     print(f"제어점:{i}: 실제 Control point={control_points}")
# print("##############################################################")

#MU and Dose_rate[MU/min]
mu_diff=np.diff(tlog.axis_data.mu.actual)
x=(len(tlog.axis_data.control_point.actual)*tlog.header.sampling_interval)/60000
MU_rate=mu_diff/x
total_MU=mu_diff.sum(axis=0)
total_MU_rate=MU_rate.sum(axis=0)
print("MU:",total_MU)
print("min:", x)
print("Dose_rate[MU/min]", total_MU_rate)
print("##############################################################")

#MU plot
plt.plot(mu_diff)
plt.title('MU: WB+SIB_1.CW TrajectoryLog', fontsize=15)
plt.xlabel('Control points')
plt.ylabel('MU')
plt.grid(color='gray', linestyle='--', linewidth=0.3)
plt.savefig('MU_graph', dpi=300)
plt.show()

#Dose rate[MU/min] plot
plt.plot(MU_rate)
plt.title('MU: WB+SIB_1.CW TrajectoryLog', fontsize=15)
plt.xlabel('Control points')
plt.ylabel('MU/min')
plt.grid(color='gray', linestyle='--', linewidth=0.3)
plt.savefig('MU_graph', dpi=300)
plt.text(3500, 0.14, 'min=1.296', fontsize=8, ha='center', va='center')
plt.show()

#Fluence map plot
fluence_map=tlog.fluence.actual.calc_map()
fluence_map_plot=tlog.fluence.actual.plot_map()

#Jaws and field size defined by jaws
jawx1=tlog.axis_data.jaws.x1.actual
jawx2=tlog.axis_data.jaws.x2.actual
jawy1=tlog.axis_data.jaws.y1.actual
jawy2=tlog.axis_data.jaws.y2.actual

field_size=np.zeros(len(control_points))
jaw_x=np.zeros(len(control_points))
jaw_y=np.zeros(len(control_points))

for i, control_points in enumerate(control_points, start=0):
    #print(f"x1_{i}:{jawx1[i]}, x2_{i}:{jawx2[i]}, y1_{i}:{jawy1[i]}, y2_{i}:{jawy2[i]}")
    jaw_x_value=abs(jawx2[i]-jawx1[i])
    jaw_x[i]=jaw_x_value
    jaw_y_value=abs(jawy2[i]-jawy1[i])
    jaw_y[i]=jaw_y_value
    field_size_jaw=jaw_x_value*jaw_y_value
    field_size[i]=field_size_jaw
    # print(f"field size_{i}:{field_size_jaw}cm^2")

min_field_value=np.argmin(field_size)
max_field_value=np.argmax(field_size)

print("Field size defined by Jaw value")
print(f"Max field size: {np.max(field_size)}cm^2")
print(f"Max field size [x value: {jaw_x[max_field_value]}cm, y value: {jaw_y[max_field_value]}cm]")
print(f"Max field size control points: {np.argmax(field_size)}")
print(f"Max field size x1: {jawx1[max_field_value]}cm, x2: {jawx2[max_field_value]}cm, y1: {jawy1[max_field_value]}cm, y2: {jawy2[max_field_value]}cm")

print(f"Min field size: {np.min(field_size)}cm^2")
print(f"Min field size [x value: {jaw_x[min_field_value]}cm, y value: {jaw_y[min_field_value]}cm]")
print(f"Min field size control points: {np.argmin(field_size)}")
print(f"Min field size x1: {jawx1[min_field_value]}cm, x2: {jawx2[min_field_value]}cm, y1: {jawy1[min_field_value]}cm, y2: {jawy2[min_field_value]}cm")


#Field_width defined by MLC leaf

mlc_cp=np.zeros((120,3888))

for i in range(len(tlog.axis_data.mlc.leaf_axes)):
    mlc_cp[i,:]=tlog.axis_data.mlc.leaf_axes[i+1].actual


left_leaf_position=mlc_cp[:60,]
right_leaf_position=mlc_cp[60:,]
field_width=np.zeros((60,3888))
right_left=np.zeros((60,3888))

for i in range(len(left_leaf_position)):
    # right_left = abs(right_leaf_position[i] - (left_leaf_position[i]))
    right_left=mlc_cp[0:60]-mlc_cp[60:120]
    field_width=np.max(right_left, axis=0)

print(f"Max Field Width for control points:{max(field_width)}cm")

