import matplotlib
import matplotlib.ticker as ticker
import numpy as np
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def graph_read_half_db(file_input, file_output):
    lines = [line.rstrip('\n') for line in open('read/' + file_input)]
    del lines[0]
    times = []
    nb_elt = []
    for line in lines:
        items = line.split(" ")
        nb_elt.append(int(items[1]))
        times.append(float(items[0]))

    n_groups = 5

    fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.4
    error_config = {'ecolor': '0.3'}

    rects1 = ax.bar(index, times, bar_width,
                    alpha=opacity, color='b',
                    error_kw=error_config,
                    )



    ax.set_xlabel('Table size in items')
    ax.set_ylabel('Time in seconds')
    ax.set_title('Time to extract 10 items of a table with 5 readers')

    ax.set_xticklabels(('10', '100', '1000', '10000', '100000', '1000000'))
    ax.legend()
    #fig.tight_layout()
    plt.show()
    plt.savefig("write/plots/" + file_output)


def graph_variable_size(file_input, file_output):
    lines = [line.rstrip('\n') for line in open('write/' + file_input)]
    del lines[0]
    times = []
    nb_elt = []

    for line in lines:
        items = line.split(";")
        nb_elt.append(int(items[2]))
        times.append(float(items[0]))


    n_groups = 6
    fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.4
    error_config = {'ecolor': '0.3'}

    rects1 = ax.bar(index, times, bar_width,
                    alpha=opacity, color='b',
                    error_kw=error_config,
                    )
    ticks = ['0', '10', '100', '1000', '10000', '100000','1000000']
    ax.set_xticklabels(ticks)
    print(times[0])
    print(times[1])
    for i in [0,1,2,3,4,5]:
        ax.text(i, times[i]-0.5, round(times[i],2), color='blue', fontweight='bold')

    plt.grid()
    plt.title('insertion of x items in an empty Dynamodb table with 60 writers')
    plt.ylabel('time in seconds')
    plt.xlabel('elements inserted')
    plt.savefig("write/plots/" + file_output)

def graph(file_input, file_output):
    lines = [line.rstrip('\n') for line in open('write/' + file_input)]
    del lines[0]
    times = []
    nb_elt = []
    for line in lines:
        items = line.split(";")
        nb_elt.append(int(items[3]))
        times.append(float(items[0]))

    X = nb_elt
    Y = times

    ax = plt.axes()
    plt.plot(X, Y)

    ticks = ['0.001', '0.01', '0.1', '1', '10', '100','1000']
    ax.set_xticklabels(ticks)
    #major_ticks = np.arange(0, 1135515, 100000)
    #minor_ticks = np.arange(0, 22000, 1095)

    #ax.set_xticks(major_ticks)
    #ax.set_xticks(minor_ticks, minor=True)
    plt.xticks(rotation=90)
    plt.tick_params(labelsize='6')
    plt.grid()
    plt.title('Duration of insertion of 1095 items in Dynamodb')
    plt.ylabel('time in seconds')
    plt.xlabel('K elements in db')
    plt.savefig("write/plots/" + file_output)

if __name__ == '__main__':

    graph("20_writers_PRECO2_model_data.txt","20_writers_PRECO2_model_data.png")
    #graph_variable_size("60_writers_variable_size.txt", "test_60_writers_variable_size_bar.png")
    #graph_read_half_db("5_Reader_limit_10.txt","test_5_readers_limit_10.png")


