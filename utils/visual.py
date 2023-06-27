plt.figure(figsize=(8, 6))
# 画出depot
depot_coor = data['display_data'][depot_index + 1]
plt.plot(depot_coor[0], depot_coor[1], 'r*', markersize=11)
# 路径可视化
for i, j in zip(visiting_sequence, visiting_sequence[1:]):
    start_coor = data['display_data'][i]
    end_coor = data['display_data'][j]
    plt.arrow(start_coor[0], start_coor[1], end_coor[0] - start_coor[0], end_coor[1] - start_coor[1])
plt.xlabel("X coordinate", fontsize = 14)
plt.ylabel("Y coordinate", fontsize = 14)
plt.title("TSP path for {}".format(fname), fontsize = 16)
