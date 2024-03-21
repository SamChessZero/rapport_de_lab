import calculs
import numpy as np
import matplotlib.pyplot as plt
from pandas import ExcelWriter
from données import Données

équipe = 8


def tableaux_excel():
    with ExcelWriter("tableaux/tableaux.xlsx") as writer:
        calculs.ConductivitéHydraulique().Ks.to_excel(writer, sheet_name="Ks")
        calculs.ConductivitéHydraulique().Ks.describe().to_excel(
            writer, sheet_name="Ks stats"
        )
        calculs.CourbeDeRétention().paramètres_optimaux.to_excel(
            writer, sheet_name="paramètres courbe rétention"
        )
        calculs.CourbeDeRétention().capacité_au_champ.to_excel(
            writer, sheet_name="capacité au champ"
        )
        calculs.LimiteDeLiquidité().régression_linéaire.to_excel(
            writer, sheet_name="droite régression"
        )
        calculs.LimiteDeLiquidité().teneur_en_eau_limite.to_excel(
            writer, sheet_name="teneur eau limite"
        )


# Distribution des Ks des 28 échantillons
def figure_1():
    Ks = calculs.ConductivitéHydraulique().Ks
    Ks_unique, counts = np.unique(Ks["Ks (mm/s)"], return_counts=True)
    medianprops = dict(linestyle="-", linewidth=2, color="midnightblue")
    boxprops = dict(color="midnightblue", facecolor="powderblue")
    whiskerprops = dict(color="midnightblue")
    fig, ax = plt.subplots(2, figsize=(9, 6), sharex=True)
    ax[0].scatter(Ks_unique, counts, 50, color="powderblue", edgecolor="darkblue")
    ax[0].scatter(
        Ks.loc[8],
        1,
        50,
        color="crimson",
        edgecolor="darkred",
    )
    ax[0].set_ybound(0, 5)
    ax[0].set_ylabel("Fréquence", fontsize=12)
    ax[0].set_title(
        "Distribution des $K_s$ des 28 échantillons\n",
        fontsize=14,
    )
    ax[1].boxplot(
        Ks,
        vert=False,
        patch_artist=True,
        medianprops=medianprops,
        boxprops=boxprops,
        whiskerprops=whiskerprops,
    )
    ax[1].set_xlabel(
        "Conductivité hydraulique à saturation $K_s$ $(mm/s)$", fontsize=12
    )
    ax[1].get_yaxis().set_visible(False)
    plt.savefig("figures/fig1.png")


# Valeurs de Ks des 28 échantillons
def figure_2():
    Ks = calculs.ConductivitéHydraulique().Ks["Ks (mm/s)"]
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.bar(
        np.arange(1, len(Ks) + 1), Ks, color="powderblue", edgecolor="cornflowerblue"
    )
    ax.bar(
        équipe,
        Ks[équipe],
        color="crimson",
        edgecolor="darkred",
        label="K$_s$ = {0:0.3f} mm/s".format(Ks[équipe]),
    )
    ax.set_title(
        "Valeurs de $K_s$ des 28 échantillons",
        fontsize=14,
    )
    ax.set_xlabel("Échantillon", fontsize=12)
    ax.set_xticks(np.arange(1, len(Ks) + 1))
    ax.tick_params(axis="x", which="both", labelsize="small")
    ax.set_ylabel("Conductivité hydraulique à saturation $K_s$ $(mm/s)$", fontsize=12)
    ax.legend(loc="upper left", frameon=False, fontsize=12)
    ax.set_ylim(bottom=0.00, top=0.25)
    plt.savefig("figures/fig2.png")


# courbe de rétention simple
def figure_3a():
    fig, ax = plt.subplots(figsize=(9, 6))
    x = np.logspace(-0.2, 4.8, 200)
    y = calculs.van_Genuchten(
        x, *(calculs.CourbeDeRétention().paramètres_optimaux.loc[équipe])
    )
    ax.semilogx(Données().potentiel_matriciel, Données().teneur_en_eau[équipe - 1], ".")
    ax.semilogx(x, y, color="crimson")
    ax.set_title(f"Courbe de rétention d'eau de l'échantillon {équipe}", fontsize=14)
    ax.set_xlabel(r"Potentiel matriciel $\Psi$  ($cm$ $H_2O$)", fontsize=12)
    ax.set_ylabel("\n" + r"Teneur en eau $\theta$ ($cm^3/cm^3$)", fontsize=12)
    ax.set_ylim(bottom=-0.02, top=0.51)
    plt.savefig("figures/fig3a.png")


# courbe de rétention comparée
def figure_3b():
    fig, ax = plt.subplots(figsize=(9, 6))
    h = Données().potentiel_matriciel
    theta = Données().teneur_en_eau
    x = np.logspace(-0.2, 4.8, 200)

    def y(équipe):
        y = calculs.van_Genuchten(x, *(popt.loc[équipe]))
        return y

    popt = calculs.CourbeDeRétention().paramètres_optimaux
    for i in range(1, 29):
        ax.semilogx(
            h,
            theta[i - 1],
            ".",
            color="cornflowerblue",
            markersize=0.75,
        )
        ax.semilogx(x, y(i), color="powderblue", linewidth=0.75)
    ax.semilogx(h, theta[équipe - 1], ".")
    ax.semilogx(x, y(équipe), color="crimson")
    ax.set_title(
        f"Courbe de rétention d'eau de l'échantillon {équipe}, comparée",
        fontsize=14,
    )
    ax.set_xlabel(r"Potentiel matriciel $\Psi$  ($cm$ $H_2O$)", fontsize=12)
    ax.set_ylabel("\n" + r"Teneur en eau $\theta$ ($cm^3/cm^3$)", fontsize=12)
    ax.set_ylim(bottom=-0.02, top=0.51)
    plt.savefig("figures/fig3b.png")


# graphique nombre de coups Casagrande
def figure_4():
    fig, ax = plt.subplots()
    ax.plot(
        Données().teneur_en_eau_massique[équipe - 1],
        Données().nombre_de_coups[équipe - 1],
        "o",
    )
    ax.set_title(f"Labo 2 limite de liquidité équipe {équipe}")
    ax.set_xlabel("teneur en eau massique (kg/kg)")
    ax.set_ylabel("nombre de coups")
    plt.savefig("figures/fig4.png")


# graphique log(nombre de coups) Casagrande
def figure_5():
    droite = calculs.LimiteDeLiquidité().régression_linéaire
    w = Données().teneur_en_eau_massique[équipe - 1]
    m = droite.loc[équipe].iloc[0]
    b = droite.loc[équipe].iloc[1]
    r2 = droite.loc[équipe].iloc[2]
    x = np.linspace(w[3] - 1, w[0] + 1, 100)
    fig, ax = plt.subplots()
    ax.plot(
        w,
        np.log10(Données().nombre_de_coups[équipe - 1]),
        "o",
    )
    ax.plot(
        x,
        calculs.droite_de_liquidation(m, x, b),
        label="$y = {0:0.4f} x + {1:0.4f}$ \n $R^2 = {2:0.6f}$".format(m, b, r2),
    )
    ax.legend()
    ax.set_title("labo 2 limite de liquidité")
    ax.set_xlabel("teneur en eau massique (%)")
    ax.set_ylabel("log(#coups)")
    plt.savefig("figures/fig5.png")


def figures_png():
    figure_1()
    figure_2()
    figure_3a()
    figure_3b()
    figure_4()
    figure_5()


tableaux_excel()
figures_png()
