'''
===============
Plot Metric Sum
===============
'''


from matplotlib import pyplot as plt
import numpy as np


AGENTS_PATH = ('agents',)


def get_timepoint_metric_sum(path_from_agent, timepoint_data):
    agents_data = get_in(timepoint_data, AGENTS_PATH)
    return np.sum([
        get_in(agent_data, path_from_agent)
        for agent_data in agents_data.values()
    ])


def plot_metric_sum(name_data_map, config):
    metric_name = config['metric_name']
    path_from_agent = config['path_from_agent']
    x_label = config.get('x_label', 'time (s)')
    y_label = config.get('y_label', metric_name)
    title = config.get('title', 'Total {} Over Time'.format(metric_name))

    fig, ax = plt.subplots()
    if x_label is not None:
        ax.set_xlabel(x_label)
    if y_label is not None:
        ax.set_ylabel(y_label)
    if title is not None:
        ax.set_title(title)

    for exp_name, data in name_data_map.items():
        metric_sums = [
            get_timepoint_metric_sum(path_from_agent, data[time])
            for time in sorted(data.keys())
        ]
        ax.plot(metric_sums, label=exp_name)

    return fig
