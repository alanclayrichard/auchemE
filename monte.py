import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from tqdm import tqdm

# simulation parameters
x_min = 0
y_min = 0
x_max = 100
y_max = 100
n_steps = 1000*x_max
trials = 1
step_size = np.sqrt(2)/2
closeness = 1
n_pred = 1
n_prey = 1
n_berries = 1

# Initialize position arrays
pred_start = [0.8*x_max,0.8*y_max]
prey_start = [x_max-0.8*x_max,y_max-0.8*y_max]
pred = np.zeros([n_steps,2])
pred[0,:] = pred_start
prey = np.zeros([n_steps,2])
prey[0,:] = prey_start
berry = np.zeros([n_steps,2])
berry_loc = [0,0]
berry[0,:] = berry_loc
berry_bool = False
berries_eaten = 0

# Define Event Probabilities
# pred perfect step
a = .01
# spawn a berry
b = .005
# prey step toward berry
c = .5

# Simulate
i = 1
for j in tqdm(range(0,trials)):
    while i < n_steps:

        # current location of pred and prey and berry 
        x1 = pred[i-1,0]
        y1 = pred[i-1,1]
        x2 = prey[i-1,0]
        y2 = prey[i-1,1]
        berry_x = berry[i-1,0]
        berry_y = berry[i-1,1]

        # create random number for chance events
        event_chance = np.random.uniform(0,1)

        # create random number for steps if no event
        pred_x_step = np.random.uniform(-step_size, step_size)
        pred_y_step = np.random.uniform(-step_size, step_size)
        prey_x_step = np.random.uniform(-step_size, step_size)
        prey_y_step = np.random.uniform(-step_size, step_size)

        # calculate direction of prey from pred
        opt_x_pred = (x2 - x1)/np.sqrt(x1**2 + x2**2)
        opt_y_pred = (y2 - y1)/np.sqrt(y1**2 + y2**2)

        # calculate direction of pred from prey
        opt_x_prey = (x1 - x2)/np.sqrt(x1**2 + x2**2)
        opt_y_prey = (y1 - y2)/np.sqrt(y1**2 + y2**2)

        # calculate direction of berry from prey
        opt_x_berry = (berry_x - x2)/np.sqrt(berry_x**2 + x2**2)
        opt_y_berry = (berry_y - y2)/np.sqrt(berry_y**2 + y2**2)

        #Events:
        # a% chance predator takes a perfect step
        if 0 <= event_chance <= a:
            pred_x_step = opt_x_pred
            pred_y_step = opt_y_pred

        # b% chance to spawn a berry (if no berry spawned)
        elif a<event_chance<=a+b and berry_bool==False:
            berry_bool = True
            berry_loc = [np.random.randint(0,x_max), np.random.randint(0,y_max)]

        # c% chance prey takes step towards berry (if there is a berry spawned)
        elif a+b<event_chance<=a+b+c and berry_bool==True:
            prey_x_step = opt_x_berry
            prey_y_step = opt_y_berry
            
        # take steps
        # pred steps (ensure within boundaries)
        if x1 + pred_x_step < x_min or x1+ pred_x_step > x_max:
            x1 += -pred_x_step
        if y1 + pred_y_step > y_max or y1+ pred_y_step <y_min: 
            y1 += -pred_y_step
        else: 
            x1 += pred_x_step
            y1 += pred_y_step
        # prey steps (ensure within boundaries)
        if x2 + prey_x_step < x_min or x2+ prey_x_step > x_max:
            x2 += -prey_x_step
        if y2 + prey_y_step > y_max or y2+ prey_y_step <y_min: 
            y2 += -prey_y_step
        else: 
            x2 += prey_x_step
            y2 += prey_y_step

        # calculate proximity to evaluate whether to stop/not stop or eat berry
        pp_proximity = np.sqrt((x2-x1)**2+(y2-y1)**2)
        pb_proximity = np.sqrt((x2-berry_x)**2+(y2-berry_y)**2)

        # pred catches prey
        if pp_proximity < closeness:
            print('caught after '+ str(i) +' steps')
            print('berries eaten: ' + str(berries_eaten))
            break

        # prey eats berry
        if pb_proximity < closeness:
            print('ate berry at step: ' + str(i))
            berry_bool = False
            berries_eaten+=1

        # record locations
        pred[i,:] = [x1,y1]
        prey[i,:] = [x2,y2]
        if berry_bool == True:
            berry[i,:] = berry_loc
        else:
            berry[i,:] = [0,0]

        # increment
        i+=1

# if not caught i will equal the max # of steps
if i == n_steps:
    print('not caught')
    print('berries eaten: ' + str(berries_eaten))

# PLAY MOVIE
fig = plt.figure()
plt.xlim([x_min,x_max])
plt.ylim([y_min,y_max])
frame, = plt.plot([],[],'o')
def animate(j):
    frame.set_data(np.array([pred[j,0],prey[j,0],berry[j,0]]),np.array([pred[j,1],prey[j,1],berry[j,1]]))
    plt.title('steps: '+ str(j))
    return frame
ani = FuncAnimation(fig, animate, frames=i, interval=1, repeat=False)
plt.show()

# # PLOT TRAJECTORIES OF PRED/PREY
# plt.scatter(pred[:,0],pred[:,1],s=3)
# plt.scatter(prey[:,0],prey[:,1],s=3)
# plt.scatter(pred[i-1,0],pred[i-1,1],color='black',s=60)
# plt.scatter(prey[i-1,0],prey[i-1,1],color='yellow',s=5)
# plt.xlim([x_min,x_max])
# plt.ylim([y_min,y_max])
# plt.show()
