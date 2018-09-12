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

def graph_read(file_input, file_output,readers):
    lines = [line.rstrip('\n') for line in open('read/' + file_input)]
    del lines[0]
    times = []
    nb_elt = []
    timeperchunk = []
    for line in lines:
        items = line.split(";")
        nb_elt.append(int(items[2]))
        times.append(float(items[4]))
        timeperchunk.append(float(items[3]))

    X = nb_elt
    Y = times
    Y2 = timeperchunk
    ax = plt.axes()
    ax2 = ax.twinx()
    ax.plot(X, Y, color='tab:blue')
    ax2.plot(X, Y2, color='tab:red')
    # plt.locator_params(nbins=8)
    # ticks = range(0, 170,10)
    # ticks = ['0.001', '0.01', '0.1', '1', '10', '100', '1000']
    # ax.set_xticklabels(ticks)
    ax2.set_yticklabels(['0.05', '0.1', '0.15', '0.2', '0.25', '0.3', '0.35', '0.4'])
    # ax.set_xticklabels(ticks)
    # major_ticks = np.arange(0, 1135515, 100000)
    # minor_ticks = np.arange(0, 22000, 1095)
    mean = np.mean(Y2)
    total = '%.3f' % Y[len(Y) - 1]
    mean = '%.3f' % mean
    # ax.set_xticks(major_ticks)
    # ax.set_xticks(minor_ticks, minor=True)
    plt.xticks(rotation=45)
    plt.tick_params(labelsize='6')
    plt.grid()
    plt.title('PRECO2 data extract duration with DynamoDb with %s readers ' % readers)
    ax.set_xlabel('items extracted from db', color='tab:blue')
    ax.set_ylabel('time in seconds (total = %ss)' % total, color='tab:blue')
    ax.tick_params(axis='y', labelcolor='tab:blue')
    ax2.set_ylabel('time to extract 1095 items in seconds (mean = %ss)' % mean, color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')
    # plt.ylabel('time in seconds')
    # plt.xlabel('K elements extracted db')
    # ax.text(700000,110, "moyenne=%s" %mean, fontsize=15, color='tab:red')
    plt.savefig("read/plots/" + file_output)


if __name__ == '__main__':

    graph_read("80_readers_chunk_1095.log","80_dynamodb_read.png", 80)
    #graph_variable_size("60_writers_variable_size.txt", "test_60_writers_variable_size_bar.png")
    #graph_read_half_db("5_Reader_limit_10.txt","test_5_readers_limit_10.png")


