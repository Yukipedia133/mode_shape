from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt 
import sys
sys.path.append("../modules")

def plot(data,num_md,damage_loc):

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_xlabel("length(x)")
    ax.set_ylabel("disppacement(m)")
    ax.plot(data)
    ax.set_title("difference of {} mode shape (damage at {}) ".format(num_md,damage_loc))
    ax.axhline(y=0,color='green')
    fig.savefig("../result/disp/{}disp{}.png".format(damage_loc,num_md))
    plt.show


def plot_angle(data,num_md,damage_loc):

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_xlabel("length(x)")
    ax.set_ylabel("angle")
    ax.plot(data)
    ax.set_title("difference of {} mode shape angle(damage at {}) ".format(num_md,damage_loc))
    ax.axhline(y=0,color='green')
    fig.savefig("../result/angle/{}angle{}.png".format(damage_loc,num_md))
    plt.show

def plot_curvature(data,num_md,damage_loc):

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_xlabel("length(x)")
    ax.set_ylabel("curvature(1/m)")
    ax.plot(data)
    ax.set_title("difference of {} mode shape carvature(damage at {}) ".format(num_md,damage_loc))
    ax.axhline(y=0,color='green')
    fig.savefig("../result/curvature/{}curvature{}.png".format(damage_loc,num_md))
    plt.show