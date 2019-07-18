import pandas as pd
import numpy as np
from dfply import *
import seaborn as sns
import statsmodels.formula.api as smf
# To visualize
import matplotlib.pyplot as plt
import scipy.stats as stats
import math

#Einlesen der Mieten aus Essen als csv und return als dataframe
dat = pd.read_csv("C:/Users/Tim/Desktop/Sommersemester 2019/GI Projekt Immobilien/Regressionsanalyse/Mieten_Essen_Export.csv", sep=",", na_values="0")


#Selektion mithilfe der Bibliothek dfply, einer Vereinfachung der Datenseletion
df = dat >> select(X.Parkplaetze, X.Kaltmiete, X.AnzZimmer, X.Quartier, X.Wohnflaeche) >> \
            filter_by(X.Parkplaetze > 0, X.Kaltmiete > 0, X.AnzZimmer > 0)


# For schleife ueber den Inhalt und die Spaltenueberschriften und Prüfung auf numerische Typen
# Wenn das zutrifft kann die Normalverteilung der Spalten bestimmt werden
for label, content in df.iteritems():
    if(content.dtype != object):
        k2, p = stats.normaltest(content, nan_policy="omit")
        alpha = 0.05
        print("p = {:g}".format(p) + " k2: " + str(k2))
        if p < alpha:  # null hypothesis: x comes from a normal distribution
            print("The null hypothesis can be rejected")
        else:
            print("The null hypothesis cannot be rejected")

# For schleife ueber den Inhalt und die Spaltenueberschriften und Prüfung auf numerische Typen
# Wenn das zutrifft, kann eine logartihmierung der Spalte stattfinden, falls die Splate nicht Normalverteilt sein sollte
for label, content in df.iteritems():
    if(content.dtype != object):
        for i in content:
            if(i != 0):
                content[i] = math.log(i,10.0)
            else:
                pass

        k2, p = stats.normaltest(content, nan_policy="omit")
        if p < alpha:
            print("Auch das Logarithmieren  hat nichts gebracht!")
            print("p = {:g}".format(p) + " k2: " + str(k2))
        else:
            print("Das Logarithmieren  hats gebracht!")
            print("p = {:g}".format(p) + " k2: " + str(k2))

#print(content)

df['Quartier'] = pd.Categorical(df.Quartier)

#print(df['Quartier'])

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

# Plotten Beispielhaft der Spalte Kaltmiete
# Bilden von Subplots
plot, ax = plt.subplots(1, 1)

# Diagramm im Stil 'seaborn plotten'
plt.style.use('seaborn')

# Bestimmung des Mittelwertes aus der Kalttmiete
mean_value = df["Kaltmiete"].mean(axis=0)
#Bestimmung der Variance aus der Kaltmiete
variance = df["Kaltmiete"].var(axis=0)
sigma = math.sqrt(variance)
# Plot between mu - 3*sigma and mu + 3*sigma with 0.001 steps.
x_axis = np.arange(mean_value - 3*sigma, mean_value + 3*sigma, 0.001)
# Erzeugen eines Histogrammes, das die Preise für die Mieten darstellt
ax.hist(df["Kaltmiete"],color='green', density=True, alpha=0.2, label="Kaltmiete")
# Plotten der dichtefunktion als Kurve
ax.plot(x_axis, stats.norm.pdf(x_axis, mean_value, sigma), alpha=0.6, label='norm pdf')

# Betitelung
plt.title("Kaltmiete normalverteilt")
plt.xlabel("Kaltmiete")
plt.ylabel("Wahrscheinlichkeit")
plt.legend(loc='best', frameon=False)

plt.show()