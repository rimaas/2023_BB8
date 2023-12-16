import numpy as np
import SYSxCONST as constants

if constants.SystemConstants().SIM_MODE:
    import matplotlib.pyplot as plt


# 3th order setpoint
def setpoint_3th_order(start, final):
    sample_time = 1 / constants.SystemConstants().sample_rate

    delta_pos = final - start

    va = pow(constants.SystemConstants().acceleration, 2) / constants.SystemConstants().jerk

    if constants.SystemConstants().velocity < va:
        selection = [1, 3, 4]
    else:
        selection = [2, 5, 6]

    sa = (2 * pow(constants.SystemConstants().acceleration, 3)) / pow(constants.SystemConstants().jerk, 2)

    if delta_pos < sa:
        selection = list(set(selection).intersection([2, 3, 4]))
    else:
        selection = list(set(selection).intersection([1, 5, 6]))

    if np.shape(selection)[0] > 1:
        if constants.SystemConstants().velocity * constants.SystemConstants().jerk < \
                pow(constants.SystemConstants().acceleration, 2):
            m = 1
            n = 0
        else:
            m = 0
            n = 1

        a = 2 * np.sqrt(constants.SystemConstants().velocity / constants.SystemConstants().jerk)
        b = constants.SystemConstants().velocity / constants.SystemConstants().acceleration
        c = constants.SystemConstants().acceleration / constants.SystemConstants().jerk

        sv = constants.SystemConstants().velocity * (m * a + n * (b + c))

        if delta_pos < sv:
            selection = list(set(selection).intersection([4, 6]))
        else:
            selection = list(set(selection).intersection([3, 5]))

    if selection[0] == 1:
        tj = np.sqrt(constants.SystemConstants().velocity / constants.SystemConstants().jerk)
        ta = tj
        tv = delta_pos / constants.SystemConstants().velocity

    elif selection[0] == 2:
        tj = pow((delta_pos / (2 * constants.SystemConstants().jerk)), 1 / 3)
        ta = tj
        tv = 2 * tj

    elif selection[0] == 3:

        tj = np.sqrt(constants.SystemConstants().velocity / constants.SystemConstants().jerk)
        ta = tj
        tv = delta_pos / constants.SystemConstants().velocity

    elif selection[0] == 4:
        tj = pow(delta_pos / (2 * constants.SystemConstants().jerk), 1 / 3)
        ta = tj
        tv = 2 * tj

    elif selection[0] == 5:
        tj = constants.SystemConstants().acceleration / constants.SystemConstants().jerk
        ta = constants.SystemConstants().velocity / constants.SystemConstants().acceleration
        tv = delta_pos / constants.SystemConstants().velocity

    elif selection[0] == 6:
        a = 4 * delta_pos * pow(constants.SystemConstants().jerk, 2) + pow(constants.SystemConstants().acceleration, 3)
        b = constants.SystemConstants().acceleration * pow(constants.SystemConstants().jerk, 2)

        tj = constants.SystemConstants().acceleration / constants.SystemConstants().jerk
        ta = 0.5 * (np.sqrt(a / b) - tj)
        tv = ta + tj

    else:
        tj = 1
        ta = 1
        tv = 1

    tj = round_to_sample(tj, sample_time)
    ta = round_to_sample(ta, sample_time)
    tv = round_to_sample(tv, sample_time)

    t0 = 0
    t1 = tj
    t2 = ta
    t3 = ta + tj
    t4 = tv
    t5 = tv + tj
    t6 = tv + ta
    t7 = tv + tj + ta

    time_signal = []
    pos_signal = []
    vel_signal = []
    acc_signal = []
    jer_signal = []

    # interval A
    time_interval = np.arange(t0, t1, sample_time)
    jer_interval = np.zeros(time_interval.shape[0])
    acc_interval = np.zeros(time_interval.shape[0])
    vel_interval = np.zeros(time_interval.shape[0])
    pos_interval = np.zeros(time_interval.shape[0])

    for idx in range(time_interval.shape[0]):
        delta_t = time_interval[idx] - t0

        jer_interval[idx] = constants.SystemConstants().jerk
        acc_interval[idx] = constants.SystemConstants().jerk * delta_t
        vel_interval[idx] = 0.5 * constants.SystemConstants().jerk * pow(delta_t, 2)
        pos_interval[idx] = 1 / 6 * constants.SystemConstants().jerk * pow(delta_t, 3)

    time_signal = np.append(time_signal, time_interval)
    pos_signal = np.append(pos_signal, pos_interval)
    vel_signal = np.append(vel_signal, vel_interval)
    acc_signal = np.append(acc_signal, acc_interval)
    jer_signal = np.append(jer_signal, jer_interval)

    # interval B
    time_interval = np.arange(t1 + sample_time, t2, sample_time)
    jer_interval = np.zeros(time_interval.shape[0])
    acc_interval = np.zeros(time_interval.shape[0])
    vel_interval = np.zeros(time_interval.shape[0])
    pos_interval = np.zeros(time_interval.shape[0])

    for idx in range(time_interval.shape[0]):
        delta_t = time_interval[idx] - t1

        jer_interval[idx] = 0
        acc_interval[idx] = acc_signal[-1]
        vel_interval[idx] = vel_signal[-1] + acc_signal[-1] * delta_t
        pos_interval[idx] = pos_signal[-1] + vel_signal[-1] * delta_t + 0.5 * acc_signal[-1] * pow(delta_t, 2)

    time_signal = np.append(time_signal, time_interval)
    pos_signal = np.append(pos_signal, pos_interval)
    vel_signal = np.append(vel_signal, vel_interval)
    acc_signal = np.append(acc_signal, acc_interval)
    jer_signal = np.append(jer_signal, jer_interval)

    # interval C
    time_interval = np.arange(t2 + sample_time, t3, sample_time)
    jer_interval = np.zeros(time_interval.shape[0])
    acc_interval = np.zeros(time_interval.shape[0])
    vel_interval = np.zeros(time_interval.shape[0])
    pos_interval = np.zeros(time_interval.shape[0])

    for idx in range(time_interval.shape[0]):
        delta_t = time_interval[idx] - t2

        jer_interval[idx] = -constants.SystemConstants().jerk
        acc_interval[idx] = acc_signal[-1] - constants.SystemConstants().jerk * delta_t
        vel_interval[idx] = vel_signal[-1] + acc_signal[-1] * delta_t - \
                            0.5 * constants.SystemConstants().jerk * pow(delta_t, 2)
        pos_interval[idx] = pos_signal[-1] + vel_signal[-1] * delta_t + 0.5 * acc_signal[-1] * pow(delta_t, 2) - \
                            1 / 6 * constants.SystemConstants().jerk * pow(delta_t, 3)

    time_signal = np.append(time_signal, time_interval)
    pos_signal = np.append(pos_signal, pos_interval)
    vel_signal = np.append(vel_signal, vel_interval)
    acc_signal = np.append(acc_signal, acc_interval)
    jer_signal = np.append(jer_signal, jer_interval)

    # interval D
    time_interval = np.arange(t3 + sample_time, t4, sample_time)
    jer_interval = np.zeros(time_interval.shape[0])
    acc_interval = np.zeros(time_interval.shape[0])
    vel_interval = np.zeros(time_interval.shape[0])
    pos_interval = np.zeros(time_interval.shape[0])

    for idx in range(time_interval.shape[0]):
        delta_t = time_interval[idx] - t3

        jer_interval[idx] = 0
        acc_interval[idx] = 0
        vel_interval[idx] = vel_signal[-1]
        pos_interval[idx] = pos_signal[-1] + vel_signal[-1] * delta_t

    time_signal = np.append(time_signal, time_interval)
    pos_signal = np.append(pos_signal, pos_interval)
    vel_signal = np.append(vel_signal, vel_interval)
    acc_signal = np.append(acc_signal, acc_interval)
    jer_signal = np.append(jer_signal, jer_interval)

    # interval E
    time_interval = np.arange(t4 + sample_time, t5, sample_time)
    jer_interval = np.zeros(time_interval.shape[0])
    acc_interval = np.zeros(time_interval.shape[0])
    vel_interval = np.zeros(time_interval.shape[0])
    pos_interval = np.zeros(time_interval.shape[0])

    for idx in range(time_interval.shape[0]):
        delta_t = time_interval[idx] - t4

        jer_interval[idx] = -constants.SystemConstants().jerk
        acc_interval[idx] = -constants.SystemConstants().jerk * delta_t
        vel_interval[idx] = vel_signal[-1] - 0.5 * constants.SystemConstants().jerk * pow(delta_t, 2)
        pos_interval[idx] = pos_signal[-1] + vel_signal[-1] * delta_t - \
                            1 / 6 * constants.SystemConstants().jerk * pow(delta_t, 3)

    time_signal = np.append(time_signal, time_interval)
    pos_signal = np.append(pos_signal, pos_interval)
    vel_signal = np.append(vel_signal, vel_interval)
    acc_signal = np.append(acc_signal, acc_interval)
    jer_signal = np.append(jer_signal, jer_interval)

    # interval F
    time_interval = np.arange(t5 + sample_time, t6, sample_time)
    jer_interval = np.zeros(time_interval.shape[0])
    acc_interval = np.zeros(time_interval.shape[0])
    vel_interval = np.zeros(time_interval.shape[0])
    pos_interval = np.zeros(time_interval.shape[0])

    for idx in range(time_interval.shape[0]):
        delta_t = time_interval[idx] - t5

        jer_interval[idx] = 0
        acc_interval[idx] = acc_signal[-1]
        vel_interval[idx] = vel_signal[-1] - constants.SystemConstants().acceleration * delta_t
        pos_interval[idx] = pos_signal[-1] + vel_signal[-1] * delta_t - \
                            0.5 * constants.SystemConstants().acceleration * pow(delta_t, 2)

    time_signal = np.append(time_signal, time_interval)
    pos_signal = np.append(pos_signal, pos_interval)
    vel_signal = np.append(vel_signal, vel_interval)
    acc_signal = np.append(acc_signal, acc_interval)
    jer_signal = np.append(jer_signal, jer_interval)

    # interval G
    time_interval = np.arange(t6 + sample_time, t7, sample_time)
    jer_interval = np.zeros(time_interval.shape[0])
    acc_interval = np.zeros(time_interval.shape[0])
    vel_interval = np.zeros(time_interval.shape[0])
    pos_interval = np.zeros(time_interval.shape[0])

    for idx in range(time_interval.shape[0]):
        delta_t = time_interval[idx] - t6

        jer_interval[idx] = constants.SystemConstants().jerk
        acc_interval[idx] = acc_signal[-1] + constants.SystemConstants().jerk * delta_t
        vel_interval[idx] = vel_signal[-1] + acc_signal[-1] * delta_t + \
                            0.5 * constants.SystemConstants().jerk * pow(delta_t, 2)
        pos_interval[idx] = pos_signal[-1] + vel_signal[-1] * delta_t + 0.5 * acc_signal[-1] * pow(delta_t, 2) + \
                            1 / 6 * constants.SystemConstants().jerk * pow(delta_t, 3)

    time_signal = np.append(time_signal, time_interval)
    pos_signal = np.append(pos_signal, pos_interval)
    vel_signal = np.append(vel_signal, vel_interval)
    acc_signal = np.append(acc_signal, acc_interval)
    jer_signal = np.append(jer_signal, jer_interval)

    if constants.SystemConstants().SIM_MODE:
        plot_results(time_signal, pos_signal, vel_signal, acc_signal, jer_signal)

    return time_signal, pos_signal, vel_signal, acc_signal, jer_signal


def round_to_sample(time_signal, sample_time):
    rounded_time = np.ceil(time_signal / sample_time) * sample_time

    return rounded_time


def plot_results(time_signal, pos_signal, vel_signal, acc_signal, jer_signal):
    fig, axs = plt.subplots(4)
    fig.suptitle('Generated Setpoints')
    axs[0].plot(time_signal, pos_signal)
    axs[0].set_ylabel('Pos [m]')

    axs[1].plot(time_signal, vel_signal)
    axs[1].plot(time_signal, np.ones(time_signal.shape[0]) * constants.SystemConstants().velocity, 'r')
    axs[1].plot(time_signal, np.ones(time_signal.shape[0]) * -constants.SystemConstants().velocity, 'r')
    axs[1].set_ylabel('Vel [m/s]')

    axs[2].plot(time_signal, acc_signal)
    axs[2].plot(time_signal, np.ones(time_signal.shape[0]) * constants.SystemConstants().acceleration, 'r')
    axs[2].plot(time_signal, np.ones(time_signal.shape[0]) * -constants.SystemConstants().acceleration, 'r')
    axs[2].set_ylabel('Acc [m/sˆ2]')

    axs[3].plot(time_signal, jer_signal)
    axs[3].plot(time_signal, np.ones(time_signal.shape[0]) * constants.SystemConstants().jerk, 'r')
    axs[3].plot(time_signal, np.ones(time_signal.shape[0]) * -constants.SystemConstants().jerk, 'r')
    axs[3].set_ylabel('Jerk [m/sˆ3]')
    axs[3].set_xlabel('Time [s]')

    plt.show()
