from datetime import datetime

import numpy as np
import facilities.FAxCONST as constants

import os


data = [0]


def collect_data(new_samples):
    global data

    if np.shape(data)[0] == 1:
        data = new_samples
    else:
        data = np.vstack([data, new_samples])

    if np.shape(np.shape(data))[0] > 1:
        if np.shape(data)[0] >= constants.Tracing().max_samples_per_file:
            store_trace(data)
            data = [0]


def store_trace(dataset):

    print('saving data')

    date_time_now = datetime.now().strftime('%Y%m%d_%H%M%S')

    directory = os.getcwd() + '/facilities/data_trace_' + str(datetime.now().strftime('%Y%m%d') + '/')
    file_name = 'data_trace_' + date_time_now + '.txt'

    if not os.path.exists(directory):
        os.mkdir(directory)

    path = os.path.join(directory, file_name)

    f = open(path, 'w')

    f.write('---------------------------------------------------------------------------\n')
    f.write(' \n')
    f.write('Filename:                 ' + file_name + '\n')
    f.write('Date / Time:              ' + str(datetime.now()) + '\n')
    f.write(' \n')
    f.write('Number of traced signals: ' + str(np.shape(dataset)[1]) + '\n')
    f.write('Number of traced samples: ' + str(np.shape(dataset)[0]) + '\n')
    f.write(' \n')
    f.write('---------------------------------------------------------------------------\n')
    f.write(' \n')
    f.write(' \n')

    for row in range(np.shape(dataset)[0]):
        data_str = str(row) + ', '
        for column in range(np.shape(dataset)[1]):
            data_str += str(dataset[row][column]) + ', '
        data_str += '\n'

        f.write(data_str)

    f.close()
