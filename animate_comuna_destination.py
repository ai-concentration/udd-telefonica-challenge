import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

print('loading csv')
df_trip = pd.read_csv('./data/trips2.csv')

trip_num = len(df_trip)

comuna_list = df_trip['destination'].unique().tolist()
len(comuna_list)

print('process data')
#Set time interval
all_day_seconds = 24 * 60 * 60
time_num = 24
time_interval = all_day_seconds / time_num

#set top N comuna to display
top_num = 10
display_comunas = list(df_trip['destination'].value_counts().head(top_num).to_dict().keys())

#create the matrix to save the count of trip for each comuna and each hour
dict_comuna_trip_temp = {}
list_comuna_trip = []

#create count for each comuna
for comuna in display_comunas:
    dict_comuna_trip_temp[comuna] = 0

#create count for each hour
for count in range(time_num):
    list_comuna_trip.append(dict_comuna_trip_temp.copy())

#convert to list to be easier to handle
time_list = df_trip['end_time'].tolist()
comuna_list = df_trip['destination'].tolist()

#create the matrix
for count in range(trip_num):
    comuna = comuna_list[count]

    if(comuna in display_comunas):
        time = time_list[count]
        time_index = int(time // time_interval)
        (list_comuna_trip[time_index])[comuna] += 1

#for animation
labels = list(list_comuna_trip[0].keys())

# create the figure and axes objects
fig, ax = plt.subplots(figsize=(10,10))

def animate(count):
    global ax
    global labels
    values = list(list_comuna_trip[count].values())
    ax.clear()


    ax.set_title(str(count) + 'hour')
    #cmap = plt.get_cmap('tab20c')
    #colors = cmap(np.linspace(0, 1, len(labels)))

    #ax.pie(values, labels=labels, colors=colors)
    ax.pie(values, labels=labels )
    #plt.legend(title = "Comunas:", loc='lower center', ncols=4, bbox_to_anchor = (0.5,-0.5))

# run the animation
print('Generate Animation')
ani = FuncAnimation(fig, animate, frames=24, interval=1000, repeat=True)
ani.save('animate.gif')
plt.show()      