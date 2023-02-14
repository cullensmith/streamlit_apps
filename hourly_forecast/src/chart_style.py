import matplotlib as plt

def set_style(fig):
    plt.pyplot.grid(True)
    plt.pyplot.rcParams.update({'grid.color': '#eeeeee'})
    # plt.pyplot.rcParams.update({'font.family': 'sans=serif'})
    plt.pyplot.rcParams.update({'font.size': 8})
    plt.pyplot.rcParams.update({'axes.labelcolor': 'red'})
    plt.pyplot.rcParams.update({'axes.edgecolor': '#b4b4b4'})
    plt.pyplot.rcParams.update({'axes.titlecolor': 'yellow'})
    plt.pyplot.rcParams.update({'axes.facecolor': 'white'})
    plt.pyplot.rcParams.update({'axes.spines.left':   True})
    plt.pyplot.rcParams.update({'axes.spines.bottom':   True})
    plt.pyplot.rcParams.update({'axes.spines.top':   False})
    plt.pyplot.rcParams.update({'axes.spines.right':   False})
    plt.pyplot.rcParams.update({'xtick.labelcolor': '#9b9b9b'})
    plt.pyplot.rcParams.update({'ytick.labelcolor': '#7b7b7b'})
    plt.pyplot.rcParams.update({'xtick.color': '#9b9b9b'})
    plt.pyplot.rcParams.update({'ytick.color': '#9b9b9b'})
    plt.pyplot.rcParams.update({'ytick.color': '#9b9b9b'})

# set_style()