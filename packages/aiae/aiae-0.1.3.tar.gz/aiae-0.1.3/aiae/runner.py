import os

import PySimpleGUI
import numpy as np
import pandas as pd
from aihelper import aifile
from aithermal import ms_runner
from scipy import integrate
from netz.parser import Parse
import matplotlib.pyplot as plt
from typing import Dict
from scipy import stats

plt.style.use("ggplot")

ACS = "Alpha Cumulative Sum"
TIME = "Time/min"
TEMP = "Temp./°C"
QMID = lambda x: f"QMID(m:{x})/A"
GAS_CONSTANT = 8.3144598
EPS = 1
N = 1000
K = 273.15
KK = 1000


def main():
    calculated_data, conversion_data, path, plot = load()
    if plot:
        PE_Write(calculated_data, conversion_data, path)
    else:
        write_set(calculated_data, path, str(conversion_data))


def write_set(set, path, name):
    print("Saving Data")
    try:
        set.to_csv(
            os.path.join(path, f"{name}.csv"), sep=";", index=True
        )
    except PermissionError:
        print(f"Permission denied to write {name}")


def PE_Write(calculated_data, conversion_data, path):
    write_set(calculated_data, path, 'calculated data')
    write_set(conversion_data, path, 'conversion data')
    i = 0
    print("Plotting Graphs")
    for n in range(len(calculated_data.columns) // 5):
        oo = calculated_data.iloc[:, i: i + 5].replace("", np.nan).dropna()
        oo.set_index("Temperature (K)", inplace=True)
        ax = oo.plot.area(stacked=False)
        for conv in np.arange(0.2, 0.7, 0.2):
            conv = conv.round(1)
            conv_temp = int(oo[oo >= conv].idxmin()[ACS].round(0))
            ax.annotate(
                f"Conversion\n {conv}",
                xy=(conv_temp, conv),
                xycoords="data",
                xytext=(-100, 60),
                textcoords="offset points",
                size=8,
                arrowprops=dict(
                    arrowstyle="fancy",
                    fc="red",
                    ec="none",
                    connectionstyle="angle3,angleA=0,angleB=-90",
                ),
            )
        plt.legend(frameon=False)
        plt.legend(framealpha=0.0)
        plt.savefig(os.path.join(path, f"Gradient - {conversion_data.iloc[:, n].name}"))
        i += 5
        print(f"Gradient Plot {conversion_data.iloc[:, n].name} Finished")


def load():
    layout = [
        [PySimpleGUI.Text("Ion to Calculate"), PySimpleGUI.InputText(key="ion")],
        [
            PySimpleGUI.Text("MS Offset (Default 30)"),
            PySimpleGUI.InputText(key="offset"),
        ],
        [
            PySimpleGUI.Text("Directory for data"),
            PySimpleGUI.InputText(key="browse"),
            PySimpleGUI.FolderBrowse(),
        ],
        [
            PySimpleGUI.Text("Instrument"),
            PySimpleGUI.Checkbox(text="Netzsch", key="netzsch"),
        ],
        [PySimpleGUI.Submit()],
    ]

    PySimpleGUI.ChangeLookAndFeel("TealMono")
    window = PySimpleGUI.Window("Tools", layout)
    event, result = window.Read()
    window.Close()

    path = result.get("browse")
    ion = result.get("ion")
    offset = result.get("offset", 30)
    netzsch = result.get("netzsch")
    plot = not netzsch
    if netzsch:
        data, meta = load_netz(path, ion)
        return data, meta, path, plot

    else:
        calculated_data, conversion_data = load_data(path, ion, offset)
        return calculated_data, conversion_data, path, plot


def load_netz(path, ion):

    ms_data = {}
    meta = {}
    for file in os.listdir(path):
        keys = [f"QMID(m:{ion})/A", "Time/min", "Temp./°C"]
        absolute_file = os.path.join(path, file)
        parser = Parse(absolute_file)
        meta = parser.meta()
        try:
            xy = {key: parser.xy()[key] for key in keys}
        except KeyError:
            import re
            keys = ["Time/min", "Temp./°C"]
            ion_current = list(filter(lambda x: re.search(str(ion), x), list(parser.xy().keys())))[0]
            keys.append(ion_current)
            xy = {key: parser.xy()[key] for key in keys}
            xy[QMID(ion)] = xy.pop(ion_current)
        xy_df = pd.DataFrame(xy)
        ms_data[float(parser.meta()["RANGE"][1].replace(",", "."))] = xy_df
    return do_netz(ms_data, ion), meta.get('SAMPLE')


def load_data(path, ion, offset):
    files = aifile.activation_energy(path, ion)
    ms_data = {a: ms_runner(f, offset) for a, f in files.items()}
    calculated_data, conversion_data = do_the_work(ms_data)
    return calculated_data, conversion_data


def lineparams(frame):
    time = frame.get(TIME).astype(float)
    temp = frame.get(TEMP).astype(float)
    if len(time) == len(temp):
        X = sum(time)
        Y = sum(temp)
        XX = sum(map(lambda x: x * x, time))
        XY = sum(map(lambda time_temp: time_temp[0] * time_temp[1], zip(time, temp)))
        beta = (XY * len(time) - X * Y) / (len(time) * XX - X * X)
        temp_zero = (Y - beta * X) / (len(time))
        dt = time.diff().mean()
        temp_start = temp[0]
        temp_end = temp[temp.last_valid_index()]
        return beta, temp_zero, dt, temp_start, temp_end
    else:
        return 0


def function(frame: dict, E: float, beta: Dict[float, float], alpha: float):
    S = 0
    for i in beta.keys():
        for j in beta.keys():
            if i is not j:
                T1 = getAl(alpha, frame[i])
                T2 = getAl(alpha, frame[j])
                S += (I(T1, E) * beta[j]) / (I(T2, E) * beta[i])
    return S


def getAl(alpha, frame):
    b = frame.loc[frame[frame.index < alpha].idxmax()]["T"]
    c = frame.loc[frame[frame.index > alpha].idxmin()]["T"]
    alpha_temp = pd.concat([b, c]).mean()
    return alpha_temp


def nonlinearinterpol(alpha, frame):
    x0 = frame.loc[frame[frame.index < alpha].idxmax()].index[0]
    y0 = frame.loc[frame[frame.index < alpha].idxmax()]["T"].values[0]
    x1 = frame.loc[frame[frame.index > alpha].idxmin()].index[0]
    y1 = frame.loc[frame[frame.index > alpha].idxmin()]["T"].values[0]
    return ((alpha - x0) / (x1 - x0) * (y1 - y0) + y0)


def I(T, E):
    return E * pp(T, E) / GAS_CONSTANT


def pp(T, E):
    x = E / (GAS_CONSTANT * T)
    return (
            np.exp(-x)
            * (x ** 3 + 18 * x ** 2 + 88 * x + 96)
            / (x * (x ** 4 + 20 * x ** 3 + 120) * x ** 2 + 240 * x + 120)
    )


def do_netz(data: dict, ion: int):
    """
       :param ion: the ion to be extracted for integration
       :param data: Dictionary containing Gradient: Frame data pairs
       :return: tuple with calculated data and conversion data
       """
    frameDict = {}
    betadict = {}
    for gradient, frame in data.items():
        workFrame = pd.DataFrame()
        beta, temp_zero, dt, temp_start, temp_end = lineparams(frame)
        frame = frame.applymap(lambda x: x.strip()).replace('', '0').applymap(lambda x: float(x))
        frame["T"] = frame.get(TIME).mul(beta).add(K + temp_start)
        workFrame["PreAlpha"] = frame.get(QMID(ion))
        workFrame["PreAlpha"].index = frame.get("T")
        workFrame["T"] = frame.get("T")
        workFrame = workFrame.set_index("T")
        integral = workFrame.apply(lambda g: integrate.simps(g, x=g.index))
        pre_alpha = workFrame.rolling(2).apply(lambda g: integrate.simps(g, x=g.index))
        workFrame["Alpha"] = pre_alpha.div(integral).cumsum().fillna(0)
        finalFrame = workFrame.drop(columns="PreAlpha").reset_index().set_index("Alpha")
        frameDict[gradient] = finalFrame
        betadict[gradient] = beta
    return Oakwood(frameDict, betadict, 0.8, 0.2)


def Oakwood(frame, beta, alpha_max, alpha_min):
    area = np.arange(alpha_min, alpha_max, 0.01)

    X = []
    Y = []
    for alpha in area:
        x = [alpha]
        y = [alpha]
        for b in beta.keys():
            temp = nonlinearinterpol(alpha, frame[b])
            x.append((1 / temp) * 1000)
            y.append(np.log(beta[b] / np.power(float(temp), 2)))
        X.append(x)
        Y.append(y)
    DATASETS = {}
    for i in range(0, len(X)):
        slope, intercept, r_value, p_value, std_err = stats.linregress(X[i][1:], Y[i][1:])
        E = -(slope * GAS_CONSTANT)
        A = intercept
        DATASETS[X[i][0]] = [E, A, r_value, p_value, std_err]
    r = pd.DataFrame.from_dict(DATASETS)
    r.index = ["Activation Energy", "Pre Exponential", "R", "P", "std_err"]
    return r


def OzawaFlynnWall(frame, beta, alpha_max, alpha_min):
    X = []
    Y = []
    n = len(beta.keys())
    longest = frame[
        [
            l
            for l in frame.keys()
            if len(frame[l]) == max([len(l) for l in frame.values()])
        ][0]
    ]
    for alpha in [i for i in longest.index if alpha_min < i < alpha_max]:
        x = [alpha]
        y = [alpha]
        for i in beta.keys():
            y.append(np.log(i * getAl(alpha, frame[i]) ** 1.92))
            x.append(1 / getAl(alpha, frame[i]))
        X.append(x)
        Y.append(y)

    OzawaE0 = 0
    Al = []
    E = []
    R = []
    for i in np.arange(len(X)):
        Sxy = 0
        Sx = 0
        Sy = 0
        Sx2 = 0
        for j in np.arange(1, len(X[0])):
            Sxy += X[i][j] * Y[i][j]
            Sx += X[i][j]
            Sy += Y[i][j]
            Sx2 += X[i][j] * X[i][j]
        B = (n * Sxy - Sx * Sy) / (n * Sx2 - (Sx * Sx));
        A = (Sy - B * Sx) / n
        R.append(A)
        Al.append(X[i][0])
        E.append(-B * GAS_CONSTANT / 1.0008 / N)
        OzawaE0 += (-B * GAS_CONSTANT / 1.0008)
    OzawaE0 = (E / len(X)) / N


def Vyazovkin(betadict, frameDict):
    energy = pd.DataFrame()
    e_zero = 0
    longest = frameDict[
        [
            l
            for l in frameDict.keys()
            if len(frameDict[l]) == max([len(l) for l in frameDict.values()])
        ][0]
    ]
    n = 0
    for alpha in [i for i in longest.index if 0.2 < i < 0.8]:
        A = 0
        B = 100000
        while abs(B - A) > EPS:
            x = (A + B) / 2
            step = (B - A) / 100.0
            f1 = function(frame=frameDict, E=x - step, beta=betadict, alpha=alpha)
            f2 = function(frame=frameDict, E=x + step, beta=betadict, alpha=alpha)
            if f1 > f2:
                A = x
            else:
                B = x
        energy = energy.append(
            pd.DataFrame.from_dict(
                {"Alpha": [alpha], "Energy": [((A + B) / 2.0) / 1000]}
            ),
            ignore_index=True,
        )
        e_zero += (A + B) / 2.0
    return e_zero


def do_the_work(data: dict):
    """

    :param data: Dictionary containing Gradient: Frame data pairs
    :return: tuple with calculated data and conversion data
    """
    calculated_frames = {}
    for gradient, frame in data.items():
        frame = frame.applymap(lambda x: float(x))
        normalized_frame = frame.div(frame.max())
        normalized_frame.index = (
                                         normalized_frame.index.astype(float) * float(gradient) + 30
                                 ) + 273.15
        rolling_integral = normalized_frame.rolling(2).apply(
            lambda g: integrate.simps(g, x=g.index)
        )
        sums = normalized_frame.apply(lambda g: integrate.simps(g, x=g.index))
        alpha = rolling_integral.div(sums)
        alphacs = alpha.cumsum()
        alphacs.columns = [ACS]
        rolling_integral.columns = [f"Rolling Integral"]
        alpha.columns = [f"Alpha"]
        df = pd.concat([normalized_frame, rolling_integral, alpha, alphacs], axis=1)
        df.index.name = "Temperature (K)"
        calculated_frames[gradient] = df
    conversion_values = {}
    conversion = np.arange(0.1, 1.1, 0.1)
    for gradient, frame in calculated_frames.items():
        conversion_values[gradient] = {}
        for conv in conversion:
            conv = round(conv, 1)
            conv_value = frame[ACS][frame[ACS] < conv].idxmax()
            if conversion_values.get(gradient):
                conversion_values[gradient][conv] = conv_value
            else:
                conversion_values[gradient] = {conv: conv_value}
    unique_index_calculated_frame = [
        a.reset_index() for a in calculated_frames.values()
    ]

    calculated_data = pd.concat(unique_index_calculated_frame, axis=1).fillna("")
    conversion_factor = pd.DataFrame.from_dict(conversion_values)
    conversion_factor.index.name = "Conversion Factor"
    return calculated_data, conversion_factor


if __name__ == "__main__":
    main()
