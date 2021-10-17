import numpy as np
import pandas as pd
import sklearn as sk
import seaborn as sns
import matplotlib.pyplot as plt
import random

##### Exploración ####
def color_negative_red(val):
    """
    Función para visualizar dataframe con colores
    """
    try:
        color = 'red' if val > 0.85 else 'blue'
    except:
        color = 'blue'
    return 'color: %s' % color


def show_correlated(dataset, threshold):
    """
    Función para visualizar en un dataframe las parejas de variables cuya correlación es mayor al threshold
    """
    corr_matrix = dataset.corr()
    n = len(corr_matrix.columns)
    correlated = list()
    to_delete = list()
    
    for i in range(n):
        for j in range(n):
            fila, columna, valor = corr_matrix.columns[i], corr_matrix.columns[j], corr_matrix.iloc[i, j]
            if ( valor >= threshold and i!=j and (columna, fila, valor) not in correlated):
                correlated.append((fila,columna, valor))
    #print(correlated)
    return pd.DataFrame(correlated, columns=['VAR_1', 'VAR_2', 'CORR']).style.applymap(color_negative_red)
   
def plot_class_distr(target_data):
    """
    Función para visualizar la distribución de clases de la variable objetivo
    """
    sns.set(rc={'figure.figsize':(15,7)})
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
