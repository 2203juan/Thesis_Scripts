#### Pre-procesamiento ####
import numpy as np
import pandas as pd
import sklearn as sk
import seaborn as sns
import matplotlib.pyplot as plt
import random
from sklearn.linear_model import LinearRegression

def clean_by_correlation(dataset, to_delete):
    for elem in to_delete:
        del dataset[elem]
    return dataset

def plot_class_distr(target_data):
    """
    Función para visualizar la distribución de clases de la variable objetivo
    """
    sns.set(rc={'figure.figsize':(5,5)})
    sns.set(font_scale = 1.25)
    chart = sns.barplot(x = "Result", y = "Count", data = target_data)
    chart.set_title('Treatment Results')
    chart.set_xticklabels(chart.get_xticklabels())
    # annotation here
    for p in chart.patches:
                 chart.annotate("%.0f" % p.get_height(), (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                     textcoords='offset points')
    plt.show()

def replace_by_lr(peso,dosis):
    missing_labels = list()
    x,y = list(),list()

    for i in range(len(peso)):
        if str(dosis[i]) == "nan":
            missing_labels.append(peso[i])
        else:
            x.append(peso[i])
            y.append(dosis[i])

    x = np.array(x)
    y = np.array(y)
    missing_labels = np.array(missing_labels)
    model = LinearRegression()
    model.fit(x.reshape(-1, 1), y.reshape(-1, 1))
    y_pred = model.predict(missing_labels.reshape(-1, 1))

    peso =list(peso)
    dosis = list(dosis)

    x = list(x)
    y = list(y)
    for i in range(len(peso)):
        if str(dosis[i]) == "nan":
            pred = model.predict(peso[i].reshape(-1, 1))
            dosis[i] = pred.tolist()[0][0]
        else:
            x.append(peso[i])
            y.append(dosis[i])
    return peso, dosis