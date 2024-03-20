import calculs
import numpy as np
import matplotlib.pyplot as plt
from pandas import ExcelWriter
from données import Données

équipe = 8


# Ks Graphique de points et diagramme en boîte
def figure_1():
    """graphique de points et diagramme en boite"""
    Ks_unique, counts = np.unique(
        calculs.ConductivitéHydraulique().Ks["Ks (cm/s)"], return_counts=True
    )
    medianprops = dict(linestyle="-", linewidth=2.5, color="crimson")

    boxprops = dict(color="midnightblue", facecolor="powderblue")
    whiskerprops = dict(color="midnightblue")

    fig1, ax = plt.subplots(2, figsize=(9, 6), sharex=True)
    ax[0].scatter(Ks_unique, counts, 50, color="powderblue", edgecolor="darkblue")
    ax[0].set_ybound(0, 5)
    ax[0].set_ylabel("frequence", fontsize=14)
    ax[0].set_title("Labo 1 partie 1 \nDistribution des différents Ks", fontsize=14)

    ax[1].boxplot(
        calculs.ConductivitéHydraulique().Ks,
        vert=False,
        patch_artist=True,
        medianprops=medianprops,
        boxprops=boxprops,
        whiskerprops=whiskerprops,
    )
    ax[1].set_xlabel("Ks (cm/s)", fontsize=14)
    ax[1].get_yaxis().set_visible(False)
    plt.savefig("figures/fig1.png")


# Ks diagramme en barres Ks
def figure_2():
    """Diagramme à barres"""
    Ks = calculs.ConductivitéHydraulique().Ks["Ks (cm/s)"]
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.bar(
        np.arange(1, len(Ks) + 1), Ks, color="powderblue", edgecolor="cornflowerblue"
    )
    ax.bar(
        équipe,
        Ks[équipe],
        color="crimson",
        label="K$_s$ = {0:0.4f} cm/s".format(Ks[équipe]),
    )
    ax.set_title(
        "Labo 1 partie 1 \nConstante de conductivité hydraulique à saturation (K$_s$)",
        fontsize=14,
    )
    ax.set_xlabel("équipe", fontsize=14)
    ax.set_xticks(np.arange(1, len(Ks) + 1))
    ax.tick_params(axis="x", which="both", labelsize="small")
    ax.set_ylabel("$K_s$" + " (cm/s)", fontsize=14)
    ax.set_ylim(bottom=0.005, top=0.022)
    ax.axhline(0.0157, linestyle="--", color="cornflowerblue", label="moyenne")
    ax.legend(loc="upper left", frameon=False, fontsize=12)
    line_break = dict(
        marker=[(-1, -0.5), (1, 0.5)],
        markersize=12,
        linestyle="none",
        color="k",
        mec="k",
        mew=1,
        clip_on=False,
    )
    ax.plot([0.02], transform=ax.transAxes, **line_break)
    ax.plot([0.03], transform=ax.transAxes, **line_break)
    plt.savefig("figures/fig2.png")


# courbe de rétention simple
def figure_3a():
    fig, ax = plt.subplots(figsize=(9, 6))
    x = np.logspace(-0.2, 4.8, 200)
    y = calculs.van_Genuchten(
        x, *(calculs.CourbeDeRétention().paramètres_optimaux.loc[équipe])
    )
    ax.semilogx(x, y)
    ax.semilogx(Données().potentiel_matriciel, Données().teneur_en_eau[équipe - 1], ".")
    ax.set_title(
        "Labo 1 partie 2\n" + f"Courbe de rétention équipe {équipe}", fontsize=14
    )
    ax.set_xlabel(r"potentiel matriciel $\psi$  (cm $H_2O$)", fontsize=14)
    ax.set_ylabel("\n" + r"teneur en eau $\theta$", fontsize=14)
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
    ax.semilogx(x, y(équipe))
    ax.semilogx(h, theta[équipe - 1], ".")
    ax.set_title(
        "Labo 1 partie 2\n" + f"Courbe de rétention équipe {équipe}, comparée",
        fontsize=14,
    )
    ax.set_xlabel(r"potentiel matriciel $\psi$  (cm $H_2O$)", fontsize=14)
    ax.set_ylabel("\n" + r"teneur en eau $\theta$", fontsize=14)
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
    x = np.linspace(
        w[3] - 1,
        w[0] + 1,
        100,
    )
    fig, ax = plt.subplots()
    ax.plot(
        w,
        np.log10(Données().nombre_de_coups[équipe - 1]),
        "o",
    )
    ax.plot(
        x,
        calculs.droite_de_liquidation(m, w, b),
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


def tableaux_excel():
    with ExcelWriter("tableaux/tableaux.xlsx") as writer:
        calculs.ConductivitéHydraulique().Ks.to_excel(writer, sheet_name="Ks")
        calculs.ConductivitéHydraulique().Ks.describe().to_excel(
            writer, sheet_name="Ks stats"
        )
        calculs.CourbeDeRétention().paramètres_optimaux.join(
            calculs.CourbeDeRétention().capacité_au_champ
        ).to_excel(writer, sheet_name="paramètres courbe rétention")
        calculs.LimiteDeLiquidité().régression_linéaire.to_excel(
            writer, sheet_name="droite régression"
        )
        calculs.LimiteDeLiquidité().teneur_en_eau_limite.to_excel(
            writer, sheet_name="teneur eau limite"
        )


# tableaux_excel()
figures_png()
