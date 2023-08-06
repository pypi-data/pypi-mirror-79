#!/usr/bin/env python3

# coding: utf-8

""" Collection of function to monitor a simulation in real time.
"""

import time
import os

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from os_command_py import os_command


# Autorship information
__author__ = "Samuel Murail"
__copyright__ = "Copyright 2020, RPBS"
__credits__ = ["Samuel Murail"]
__license__ = "GNU General Public License v2.0"
__maintainer__ = "Samuel Murail"
__email__ = "samuel.murail@u-paris.fr"
__status__ = "Production"

# Test folder path
MONITOR_LIB_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_PATH = os.path.abspath(os.path.join(MONITOR_LIB_DIR, "../test_files/"))


def isnotebook():
    """ Return if the command is launch from a notebook or not
    Taken from:
    https://stackoverflow.com/questions/15411967/\
    how-can-i-check-if-code-is-executed-in-the-ipython-notebook

    :Example:

    >>> isnotebook()
    False
    """

    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter


def read_xvg(xvg_file, x_axis='time'):
    """ Read a `.xvg` file and return a pandas dataframe.

    :param xvg_file: path of the xvg file
    :type xvg_file: string

    :param x_axis: name of first column
    :type xvg_file: string (Default: 'time')

    :Example:

    >>> xvg_file = os.path.join(TEST_PATH, 'volume.xvg')
    >>> vol_df = read_xvg(xvg_file)
    >>> vol_df.head()
       time      Volume
    0   0.0  171.237213
    1   5.0  135.081039
    2  10.0   94.224792
    3  15.0   59.942383
    4  20.0   58.125397
    """

    y_label_list = []

    # Get first line without command in output file:
    with open(xvg_file, 'r') as file_in:
        for first_line, line in enumerate(file_in):
            if line.startswith("@ s"):
                y_label_list.append(line.split("\"")[1])
            if not line.startswith(("#", "@")):
                break

    ener_pd = pd.read_csv(xvg_file, comment='#',
                          skiprows=first_line,
                          sep=r'\s+',
                          names=[x_axis] + y_label_list)
    return(ener_pd)


def simulation_plot(proc, func_input_dict, refresh_time=1.0):
    """ This function is used for monitoring a simulation in real time.
    Function can be excecuted by the gromacs.tools.os_command.run_background()
    function.
    The function monitors a trajectory file, and launch the analysis if the
    file has been modified.
    It can plot as function of time an analysis of a simulation.
    Analysis is passed as input function.

    .. warning::
        Need to add the following lines to be run in jupyter notebook:

        * ``%matplotlib notebook``

    Example:

    >>> TEST_OUT = str(getfixture('tmpdir'))
    >>> import sys
    >>> # print(os.path.abspath(os.path.join(MONITOR_LIB_DIR, \
'../..')))
    >>> sys.path.insert(0, os.path.abspath(os.path.join(MONITOR_LIB_DIR, \
'../..')))
    >>> from gromacs_py import gmx #doctest: +ELLIPSIS
    >>> prot = gmx.GmxSys(name='1y0m', coor_file=TEST_PATH+'/1y0m.pdb')
    >>> ###################################
    >>> ####   Create the topologie:   ###
    >>> ###################################
    >>> prot.prepare_top(out_folder=os.path.join(TEST_OUT, 'top_SH3'), \
vsite='hydrogens') #doctest: +ELLIPSIS
    pdb2pqr... --ff CHARMM --ffout CHARMM --chain --ph-calc-method=propka \
tmp_pdb2pqr.pdb 00_1y0m.pqr
    gmx pdb2gmx -f 01_1y0m_good_his.pdb -o 1y0m_pdb2gmx.pdb -p \
1y0m_pdb2gmx.top -i 1y0m_posre.itp -water tip3p -ff charmm36-jul2017 -ignh \
-vsite hydrogens
    >>> ######################################
    >>> ### Monitor an energy minimisation ###
    >>> ######################################
    >>> monitor = {'function': simulation_plot,\
           'extract_func': [{'func': extract_log_dict,\
                             'term': 'Potential'},\
                           {'func': extract_log_dict,\
                             'term': 'Temperature'}],\
           'file_check_ext':'log'}
    >>> prot.em(out_folder=os.path.join(TEST_OUT, 'em_SH3'), nsteps=100,\
    constraints='none', create_box_flag=True, monitor=monitor, nstlog=10)\
    #doctest: +ELLIPSIS
    gmx editconf -f ...top_SH3/1y0m_pdb2gmx.pdb -o \
...top_SH3/1y0m_pdb2gmx_box.pdb -bt dodecahedron -d 1.0
    gmx grompp -f 1y0m.mdp -c .../top_SH3/1y0m_pdb2gmx_box.pdb \
-r .../top_SH3/1y0m_pdb2gmx_box.pdb -p .../top_SH3/1y0m_pdb2gmx.top \
-po out_1y0m.mdp -o 1y0m.tpr -maxwarn 1
    gmx mdrun -s 1y0m.tpr -deffnm 1y0m -nt 0 -ntmpi 0 -nsteps -2 -nocopyright

    """

    file_to_check = func_input_dict[func_input_dict['file_check_ext']]
    function_list = func_input_dict['extract_func']
    time_modif = None
    file_time = None
    count = 1
    x_list = []
    y_list = []
    notebook = isnotebook()

    ###################
    # Set up the plot #
    ###################

    # Remove the matplotlib window buttons:
    matplotlib.rcParams['toolbar'] = 'None'
    # Create the plot in interactive mode
    plt.ion()
    # fig = plt.figure()
    fig, axarr = plt.subplots(len(function_list), sharex=True)

    for i, function in enumerate(function_list):
        y_list.append([])
        x_list.append([])
        axarr[i].set_xlabel('time (ps)')
        axarr[i].set_ylabel(function['term'])
        axarr[i].plot(x_list[i], y_list[i],
                      'ko-', markersize=2,
                      linewidth=0.5,
                      color='blue')
    # show the window
    # figure will be in foreground, but the user may move it to background
    if not notebook:
        fig.show()
    fig.canvas.set_window_title(file_to_check[:-4])

    while proc.poll() is None:

        time.sleep(refresh_time)
        count += 1

        if os_command.check_file_exist(file_to_check):
            file_time = os.stat(file_to_check).st_mtime

        if time_modif != file_time:

            time_modif = file_time

            for i, function in enumerate(function_list):
                anal = function['func'](func_input_dict)
                # print(anal)

                if 'time' in anal and function['term'] in anal:
                    x_list[i].append(anal['time'])
                    y_list[i].append(anal[function['term']])

                    # set plot data
                    axarr[i].lines[0].set_data(x_list[i], y_list[i])
                    # recompute the data limits
                    axarr[i].relim()
                    # automatic axis scaling
                    axarr[i].autoscale_view()
                # except KeyError:
                # print('Energy could not be extract,
                # simulation is probably finished.')

            # Update the plot and take care of window events
            # (like resizing etc.)
            fig.canvas.flush_events()
            if notebook:
                # Needed when launched in notebook
                fig.canvas.draw()


def extract_log_dict(func_input_dict, tail_line_num=20):
    """ Read the last lines of a gromacs ``.log`` file and return a dictionnary
    containing ``time``,  ``step`` and all energetic terms.
    """

    log_to_check = func_input_dict['log']
    tail_text = os.popen('tail -n {} {}'.format(tail_line_num,
                                                log_to_check)).read()

    split_text = tail_text.split('\n')
    log_dict = {}
    time_read = False
    ener_read = False
    ener_done = False
    field_len = 15

    i = 0
    while i < len(split_text) and not ener_done:
        line = split_text[i]
        # Find Step Time line:
        if line.strip().startswith('Step'):
            line_split = split_text[i + 1].split()
            log_dict['step'] = int(line_split[0])
            log_dict['time'] = float(line_split[1])
            time_read = True
            # Skip next line (already extracted with time and step)
            i += 2
            continue
        elif time_read and line.strip().startswith('Energies'):
            ener_read = True
        elif ener_read and len(line) == 0:
            ener_done = True
        elif ener_read:
            next_line = split_text[i + 1]
            for j in range(5):
                field = line[field_len * j:field_len * (j + 1)].\
                    strip().replace(" ", "_")
                if len(field) > 0:
                    value = float(
                        next_line[field_len * j:field_len * (j + 1)].strip())
                    log_dict[field] = value
            i += 2
            continue
        i += 1

    return(log_dict)


def print_log_file(proc, func_input_dict, tail_line_num=20):
    """ Monitor ``.log`` file information.
    The ``func_input_dict`` should contains several keys:

    * `terms`: list of energetic terms to extract, eg. ['Potential',
        'Temperature']
    * `log`: path of the log file (Defined in ``os_command.run_background()``)
    * `refresh_time`: time interval to refresh log extract (default=1.0 s)

    :param proc: running subprocess
    :type proc: subprocess object

    :param func_input_dict: dictionnary containing parameters for log extract
    :type func_input_dict: dict

    :param tail_line_num: number of line to read at the end of ``.log`` file
    :type tail_line_num: int, default=20


    Example:

    >>> TEST_OUT = str(getfixture('tmpdir'))
    >>> import sys
    >>> sys.path.insert(0, os.path.abspath(os.path.join(MONITOR_LIB_DIR, \
'../..')))
    >>> from gromacs_py import gmx #doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
    <BLANKLINE>
    ...
    >>> prot = gmx.GmxSys(name='1y0m', coor_file=TEST_PATH+'/1y0m.pdb')
    >>> ###################################
    >>> ####   Create the topologie:   ###
    >>> ###################################
    >>> prot.prepare_top(out_folder=os.path.join(TEST_OUT, 'top_SH3'), \
vsite='hydrogens') #doctest: +ELLIPSIS
    pdb2pqr... --ff CHARMM --ffout CHARMM --chain --ph-calc-method=propka \
tmp_pdb2pqr.pdb 00_1y0m.pqr
    gmx pdb2gmx -f 01_1y0m_good_his.pdb -o 1y0m_pdb2gmx.pdb -p \
1y0m_pdb2gmx.top -i 1y0m_posre.itp -water tip3p -ff charmm36-jul2017 -ignh \
-vsite hydrogens
    >>> ######################################
    >>> ### Monitor an energy minimisation ###
    >>> ######################################
    >>> monitor = {'function': print_log_file,\
           'terms':['Potential'],\
           'file_check_ext':'log'}
    >>> prot.em(out_folder=os.path.join(TEST_OUT, 'em_SH3'), nsteps=100,\
    constraints='none', create_box_flag=True, monitor=monitor, nstlog=10)\
    #doctest: +ELLIPSIS
    gmx editconf -f .../top_SH3/1y0m_pdb2gmx.pdb -o \
.../top_SH3/1y0m_pdb2gmx_box.pdb -bt dodecahedron -d 1.0
    gmx grompp -f 1y0m.mdp -c ../top_SH3/1y0m_pdb2gmx_box.pdb -r \
../top_SH3/1y0m_pdb2gmx_box.pdb -p ../top_SH3/1y0m_pdb2gmx.top -po \
out_1y0m.mdp -o 1y0m.tpr -maxwarn 1
    gmx mdrun -s 1y0m.tpr -deffnm 1y0m -nt 0 -ntmpi 0 -nsteps -2 \
-nocopyright...

    """

    log_to_check = func_input_dict['log']
    time_modif = None
    file_time = None
    count = 1
    if 'refresh_time' in func_input_dict:
        refresh_time = func_input_dict['refresh_time']
    else:
        refresh_time = 1.0

    while proc.poll() is None:

        time.sleep(refresh_time)
        count += 1

        if os_command.check_file_exist(log_to_check):
            file_time = os.stat(log_to_check).st_mtime

        if time_modif != file_time:

            time_modif = file_time

            log_dict = extract_log_dict(func_input_dict)
            if 'time' in log_dict:
                print("time = {:6.1f} ".format(log_dict['time']), end='')
                for keys in func_input_dict['terms']:
                    if keys in log_dict:
                        print("  {} = {:5.1f} ".format(keys, log_dict[keys]),
                              end='')
                print()


def progress_bar(proc, func_input_dict, tail_line_num=20):
    """ Monitor ``.log`` file timestep.
    The ``func_input_dict`` should contains several keys:

    * `nsteps`: Total number of steps during the simulation
    * `log`: path of the log file (Defined in ``os_command.run_background()``)
    * `refresh_time`: time interval to refresh log extract (default=1.0 s)

    :param proc: running subprocess
    :type proc: subprocess object

    :param func_input_dict: dictionnary containing parameters for log extract
    :type func_input_dict: dict

    :param tail_line_num: number of line to read at the end of ``.log`` file
    :type tail_line_num: int, default=20


    Example:

    >>> TEST_OUT = str(getfixture('tmpdir'))
    >>> import sys
    >>> sys.path.insert(0, os.path.abspath(os.path.join(MONITOR_LIB_DIR, \
'../..')))
    >>> from gromacs_py import gmx #doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
    <BLANKLINE>
    ...
    >>> prot = gmx.GmxSys(name='1y0m', coor_file=TEST_PATH+'/1y0m.pdb')
    >>> ###################################
    >>> ####   Create the topologie:   ###
    >>> ###################################
    >>> prot.prepare_top(out_folder=os.path.join(TEST_OUT, 'top_SH3'), \
vsite='hydrogens') #doctest: +ELLIPSIS
    pdb2pqr... --ff CHARMM --ffout CHARMM --chain --ph-calc-method=propka \
tmp_pdb2pqr.pdb 00_1y0m.pqr
    gmx pdb2gmx -f 01_1y0m_good_his.pdb -o 1y0m_pdb2gmx.pdb -p \
1y0m_pdb2gmx.top -i 1y0m_posre.itp -water tip3p -ff charmm36-jul2017 -ignh \
-vsite hydrogens
    >>> ######################################
    >>> ### Monitor an energy minimisation ###
    >>> ######################################
    >>> monitor = PROGRESS_BAR
    >>> prot.em(out_folder=os.path.join(TEST_OUT, 'em_SH3'), nsteps=100,\
    constraints='none', create_box_flag=True, monitor=monitor, nstlog=10)\
    #doctest: +ELLIPSIS
    gmx editconf -f .../top_SH3/1y0m_pdb2gmx.pdb -o \
.../top_SH3/1y0m_pdb2gmx_box.pdb -bt dodecahedron -d 1.0
    gmx grompp -f 1y0m.mdp -c ../top_SH3/1y0m_pdb2gmx_box.pdb -r \
../top_SH3/1y0m_pdb2gmx_box.pdb -p ../top_SH3/1y0m_pdb2gmx.top -po \
out_1y0m.mdp -o 1y0m.tpr -maxwarn 1
    gmx mdrun -s 1y0m.tpr -deffnm 1y0m -nt 0 -ntmpi 0 -nsteps -2 \
-nocopyright

    """

    if isnotebook():
        from tqdm.notebook import tqdm
    else:
        from tqdm import tqdm

    log_to_check = func_input_dict['log']
    time_modif = None
    file_time = None
    count = 1
    if 'refresh_time' in func_input_dict:
        refresh_time = func_input_dict['refresh_time']
    else:
        refresh_time = 1.0

    pbar = tqdm(total=func_input_dict['nsteps'])
    last_time = 0

    while proc.poll() is None:

        time.sleep(refresh_time)
        count += 1

        if os_command.check_file_exist(log_to_check):
            file_time = os.stat(log_to_check).st_mtime

        if time_modif != file_time:

            time_modif = file_time

            log_dict = extract_log_dict(func_input_dict)
            if 'step' in log_dict:
                pbar.update(log_dict['step'] - last_time)
                last_time = log_dict['step']

    pbar.update(func_input_dict['nsteps'] - last_time)
    pbar.close()


PROGRESS_BAR = {'function': progress_bar,
                'file_check_ext': 'log'}


if __name__ == "__main__":

    import doctest
    import shutil

    TEST_DIR = 'gromacs_py_test_out'
    TEST_OUT = os.path.join(TEST_DIR, 'monitor')

    def getfixture(*args):
        return TEST_OUT

    print("-Test os_command module:")

    print("monitor:  \t", doctest.testmod())
    # Erase all test files
    shutil.rmtree(TEST_DIR, ignore_errors=True)
