import résultats
import matplotlib.pyplot as plt
from données import Données
from numpy import log10, linspace


def afficher_résultats():
    res = résultats.CourbeDeRétention().paramètres_optimaux
    print(
        "\nÉchantillon équipe 8 : "
        + "\nConductivité hydraulique à saturation = {0:0.4f} cm/s.".format(
            résultats.ConductivitéHydraulique().Ks[7]
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
            résultats.CourbeDeRétention().capacité_au_champ[7]
        )
    )


droite = résultats.LimiteDeLiquidité().paramètres_optimaux
droite["R^2"] = droite["rvalue"] ** 2
droite = droite.drop(columns=["rvalue", "pvalue", "stderr"])
print(droite)


def plot_liquidité():
    m = droite.loc[8][0]
    b = droite.loc[8][1]
    x = linspace(64, 72, 100)
    y = m * x + b
    plt.plot(
        Données().teneur_en_eau_massique[7], log10(Données().nombre_de_coups[7]), "o"
    )
    plt.plot(
        x,
        y,
        label="$y = {0:0.4f} x + {1:0.4f}$ \n $R^2 = {2:0.6f}$".format(
            droite.loc[8][0], droite.loc[8][1], droite.loc[8][2]
        ),
    )
    plt.legend()
    plt.title("labo 2 limite de liquidité")
    plt.xlabel("teneur en eau massique (%)")
    plt.ylabel("log(#coups)")
    plt.show()


# plot_liquidité()
