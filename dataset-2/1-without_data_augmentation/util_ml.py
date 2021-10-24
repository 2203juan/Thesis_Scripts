import matplotlib.pyplot as plt
from sklearn import metrics
import pandas as pd
import numpy as np

def plot_roc(predictions, y_test, names):
    fpr = list()
    tpr = list()
    auc = list()

    for i in range(len(predictions)):
        fpr_, tpr_,_= metrics.roc_curve(y_test,predictions[i])
        fpr.append(fpr_); tpr.append(tpr_)
        auc_ = metrics.roc_auc_score(y_test,predictions[i])
        auc.append(auc_)
        



    result_table = pd.DataFrame(columns = ['classifiers', 'fpr','tpr','auc'])

    for i in range(len(predictions)):
        result_table = result_table.append({'classifiers':names[i],
                                                'fpr':fpr[i], 
                                                'tpr':tpr[i], 
                                                'auc':auc[i]}, ignore_index = True)

    # Set name of the classifiers as index labels
    result_table.set_index('classifiers', inplace=True)

    fig = plt.figure(figsize=(7,7))

    for i in result_table.index:
        plt.rcParams['axes.facecolor'] = '#ececec'
        plt.plot(result_table.loc[i]['fpr'], 
                result_table.loc[i]['tpr'], 
                label = "{},\nAUC={:.3f}".format(i, result_table.loc[i]['auc']))

        
    plt.plot([0,1], [0,1], color='#0288d1', linestyle='--')

    plt.xticks(np.arange(0.0, 1.1, step=0.1))
    plt.xlabel("False Positive Rate", fontsize=15)

    plt.yticks(np.arange(0.0, 1.1, step=0.1))
    plt.ylabel("True Positive Rate", fontsize=15)

    plt.title('ROC Curve Analysis\n', fontweight='bold', fontsize=15)
    plt.legend(prop={'size':13}, loc='lower right')

    plt.show()