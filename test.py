import pandas as pd
import matplotlib.cm as cm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="darkgrid") 

redeemed_sales = [90668.54, 133346.80]
non_redeemed_sales = [503407.53, 455860.56]
redeemed_transactions = [304, 496]
non_redeemed_transactions = [1905, 2025]
redeemed_sales_quantity = [369, 544]
non_redeemed_sales_quantity = [2308, 2474]
redeemed_customers = [171, 278]
non_redeemed_customers = [1260, 1291]

np1 = np.array([[90668.54, 133346.80], [503407.53, 455860.56]])

def plot_clustered_stacked(dfall, labels=None, title="multiple stacked bar plot",  H="/", **kwargs):
    """Given a list of dataframes, with identical columns and index, create a clustered stacked bar plot. 
labels is a list of the names of the dataframe, used for the legend
title is a string for the title of the plot
H is the hatch used for identification of the different dataframe"""

    n_df = len(dfall)
    n_col = len(dfall[0].columns) 
    n_ind = len(dfall[0].index)
    axe = plt.subplot(111)

    for df in dfall : # for each data frame
        axe = df.plot(kind="bar",
                      linewidth=0,
                      stacked=True,
                      ax=axe,
                      legend=False,
                      grid=False,
                      **kwargs)  # make bar plots

    h,l = axe.get_legend_handles_labels() # get the handles we want to modify
    for i in range(0, n_df * n_col, n_col): # len(h) = n_col * n_df
        for j, pa in enumerate(h[i:i+n_col]):
            for rect in pa.patches: # for each index
                rect.set_x(rect.get_x() + 1 / float(n_df + 1) * i / float(n_col))
                rect.set_hatch(H * int(i / n_col)) #edited part     
                rect.set_width(1 / float(n_df + 1))

    axe.set_xticks((np.arange(0, 2 * n_ind, 2) + 1 / float(n_df + 1)) / 2.)
    axe.set_xticklabels(df.index, rotation = 0)
    axe.set_title(title)

    # Add invisible data to add another legend
    n=[]        
    for i in range(n_df):
        n.append(axe.bar(0, 0, color="gray", hatch=H * i))

    l1 = axe.legend(h[:n_col], l[:n_col], loc=[1.01, 0.5])
    if labels is not None:
        l2 = plt.legend(n, labels, loc=[1.01, 0.1]) 
    axe.add_artist(l1)
    return axe

a_sales = 100*np.array([90668.54, 503407.53])/(90668.54+503407.53)
b_sales = 100*np.array([133346.80, 455860.56])/(133346.80+455860.56)

a_transactions = 100*np.array([304, 1905])/(304+1905)
b_transactions = 100*np.array([496, 2025])/(496+2025)

a_quantity = 100*np.array([369, 2308])/(369+2308)
b_quantity = 100*np.array([544, 2474])/(544+2474)

a_customers = 100*np.array([171, 1260])/(171+1260)
b_customers = 100*np.array([278, 1291])/(278+1291)

# create fake dataframes
sales = pd.DataFrame(np.array([a_sales, b_sales]),
                   index=["TargetA", "TargetB"],
                   columns=["Redeemed", "Not Redeemed"])
transactions = pd.DataFrame(np.array([a_transactions, b_transactions]),
                   index=["TargetA", "TargetB"],
                   columns=["Redeemed", "Not Redeemed"])
quantity = pd.DataFrame(np.array([a_quantity, b_quantity]),
                   index=["TargetA", "TargetB"],
                   columns=["Redeemed", "Not Redeemed"])
customers = pd.DataFrame(np.array([a_customers, b_customers]),
                   index=["TargetA", "TargetB"],
                   columns=["Redeemed", "Not Redeemed"])

# Then, just call :
plot_clustered_stacked([sales, quantity, transactions, customers],["Sales Value", "Quantity", "Transactions", "Customers"])
plt.title('Redeemed vs Not Redeemed')
plt.ylabel('Percentage (%)')
plt.xlabel('Group')
plt.show()
    