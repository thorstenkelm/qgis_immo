import pandas as pd
import numpy as np

from dfply import *
import matplotlib.pyplot as plt  # To visualize
import seaborn as sns
import statsmodels.formula.api as smf
# Tool for training and test splitting
from sklearn.model_selection import train_test_split

dat = pd.read_csv("C:/Users/Kelm/Desktop/Daten/Mieten_Essen_Export.csv", sep=",", na_values=0)

df = dat >> select(X.Parkplaetze, X.Kaltmiete, X.AnzZimmer, X.Quartier, X.Wohnflaeche) >> \
     filter_by(X.Parkplaetze > 0, X.Kaltmiete > 0, X.AnzZimmer > 0)

df['Quartier'] = pd.Categorical(df.Quartier)

#training and test split, random_State makes the training and test split reproducible
df_train, df_test = train_test_split(df,test_size=0.2,random_state=24, shuffle=True)

est = smf.ols(formula="Kaltmiete ~ Quartier + AnzZimmer + Wohnflaeche", data=df_train).fit()
print(est.summary())

# model values
model_fitted_y = est.fittedvalues
# model residuals
model_residuals = est.resid
# normalized residuals
model_norm_residuals = est.get_influence().resid_studentized_internal
# absolute squared normalized residuals
model_norm_residuals_abs_sqrt = np.sqrt(np.abs(model_norm_residuals))
# absolute residuals
model_abs_resid = np.abs(model_residuals)
# leverage, from statsmodels internals
model_leverage = est.get_influence().hat_matrix_diag
# cook's distance, from statsmodels internals
model_cooks = est.get_influence().cooks_distance[0]

# Plot
plot_lm_1 = plt.figure()
plot_lm_1.axes[0] = sns.residplot(model_fitted_y, model_residuals,
                                  lowess=True,
                                  scatter_kws={'alpha': 0.5},
                                  line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})

plot_lm_1.axes[0].set_title('Residuals vs Fitted')
plot_lm_1.axes[0].set_xlabel('Fitted values')
plot_lm_1.axes[0].set_ylabel('Residuals')
plot_lm_1.show()


# Model validation on the test data (df_test)
def rmse(predictions, targets):
    diff = predictions - targets
    diff_squared = diff ** 2
    mean_of_diff_squared = diff_squared.mean()
    rmse_val = np.sqrt(mean_of_diff_squared)

    return rmse_val

print("RMSE of the training dataset:" + str(rmse(predictions=est.predict(df_train), targets=df_train["Kaltmiete"])))
print("RMSE of the test dataset:" + str(rmse(predictions=est.predict(df_test), targets=df_test["Kaltmiete"])))

