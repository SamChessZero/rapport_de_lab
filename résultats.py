import calculs
import matplotlib.pyplot as plt
from données import Données
from numpy import log10, linspace, unique, arange


def tableau_1():
    print(
        "\nTableau 1. Constantes de conductivité hydraulique à saturation"
        + " des 28 équipes au laboratoire 1\n",
        calculs.ConductivitéHydraulique().Ks,
    )


def tableau_2():
    print(
        "\nTableau 2: statistiques de base relatives aux valeurs de "
        + "conductivité hydraulique\n",
        calculs.ConductivitéHydraulique().Ks.describe(),
    )


def figure_1():
    """graphique de points et diagramme en boite"""
    Ks_unique, counts = unique(
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
    plt.show()


def figure_2():
    """Diagramme à barres"""
    Ks = calculs.ConductivitéHydraulique().Ks["Ks (cm/s)"]
    team = 8
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.bar(arange(1, len(Ks) + 1), Ks, color="powderblue", edgecolor="cornflowerblue")
    ax.bar(
        team, Ks[team], color="crimson", label="K$_s$ = {0:0.4f} cm/s".format(Ks[team])
    )
    ax.set_title(
        "Labo 1 partie 1 \nConstante de conductivité hydraulique à saturation (K$_s$)",
        fontsize=14,
    )
    ax.set_xlabel("équipe", fontsize=14)
    ax.set_xticks(arange(1, len(Ks) + 1))
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
    plt.show()


def afficher_résultats():
    res = calculs.CourbeDeRétention().paramètres_optimaux
    print(
        "\nÉchantillon équipe 8 : "
        + "\nConductivité hydraulique à saturation = {0:0.4f} cm/s.".format(
            calculs.ConductivitéHydraulique().Ks[7]
        )
    )
    print(
        "teneur en eau résiduelle = {0:0.5f}".format(res[7][0])
        + "\nteneur en eau à saturation = {0:0.5f}".format(res[7][1])
        + "\na = {0:0.5f}".format(res[7][2])
        + "\nm = {0:0.5f}".format(res[7][3])
        + "\nn = {0:0.5f}".format(res[7][4])
    )
    print(
        "capacité au champ = {0:0.5f}".format(
            calculs.CourbeDeRétention().capacité_au_champ[7]
        )
    )


droite = calculs.LimiteDeLiquidité().paramètres_optimaux
droite["R^2"] = droite["rvalue"] ** 2
droite = droite.drop(columns=["rvalue", "pvalue", "stderr"])


def plot_liquidité():
    m = droite.loc[8].iloc[0]
    b = droite.loc[8].iloc[1]
    r2 = droite.loc[8].iloc[2]
    w = linspace(64, 72, 100)
    plt.plot(
        Données().teneur_en_eau_massique[7], log10(Données().nombre_de_coups[7]), "o"
    )
    plt.plot(
        w,
        calculs.droite_de_liquidation(m, w, b),
        label="$y = {0:0.4f} x + {1:0.4f}$ \n $R^2 = {2:0.6f}$".format(m, b, r2),
    )
    plt.legend()
    plt.title("labo 2 limite de liquidité")
    plt.xlabel("teneur en eau massique (%)")
    plt.ylabel("log(#coups)")
    plt.show()


# tableau_1()
# tableau_2()
# figure_1()
figure_2()
# print(droite)
# plot_liquidité()
