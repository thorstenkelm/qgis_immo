import pandas as pd
import numpy as np

from dfply import *
import matplotlib.pyplot as plt  # To visualize
import seaborn as sns
import statsmodels.formula.api as smf

dat = pd.read_csv("C:/Users/Kelm/Desktop/Daten/Mieten_Essen_Export.csv", sep=",", na_values=0)

df = dat >> select(X.Parkplaetze, X.Kaltmiete, X.AnzZimmer, X.Quartier, X.Wohnflaeche) >> \
     filter_by(X.Parkplaetze > 0, X.Kaltmiete > 0, X.AnzZimmer > 0)

df['Quartier'] = pd.Categorical(df.Quartier)

est = smf.ols(formula="Kaltmiete ~ Quartier + AnzZimmer + Wohnflaeche", data=df).fit()
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
