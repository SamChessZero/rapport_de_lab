from pandas import DataFrame
from numpy import pi, inf, log10
from scipy.optimize import curve_fit
from scipy.stats import linregress
from données import Données


class ConductivitéHydraulique:
    def __init__(self) -> None:

        def calculer_Ks_moyen(débits_Q: list):
            surface = pi * (échantillon.diamètre / 2) ** 2
            Ks_moyen = (
                (débits_Q.mean()) / surface * échantillon.longueur / échantillon.delta_H
            )
            return Ks_moyen

        def obtenir_Ks_de_chaque_équipe():
            Ks = []
            for i in range(28):
                Ks.append(calculer_Ks_moyen(échantillon.débit_H2O[i]))
            return Ks

        self.Ks = DataFrame(
            obtenir_Ks_de_chaque_équipe(), index=range(1, 29), columns=["Ks (cm/s)"]
        )


class CourbeDeRétention:
    def __init__(self) -> None:

        paramètres_optimaux = [
            curve_fit(
                van_Genuchten,
                échantillon.potentiel_matriciel,
                échantillon.teneur_en_eau[i],
                bounds=(1e-8, inf),
            )[0]
            for i in range(28)
        ]
        self.paramètres_optimaux = DataFrame(
            paramètres_optimaux,
            index=range(1, 29),
            columns=["theta_r", "theta_s", "alpha", "m", "n"],
        )
        capacité_au_champ = [
            van_Genuchten(convertir_kiloPascals_en_cm_H2O(33), *paramètres_optimaux[i])
            for i in range(28)
        ]
        self.capacité_au_champ = DataFrame(
            capacité_au_champ, index=range(1, 29), columns=["theta_c"]
        )


class LimiteDeLiquidité:
    def __init__(self) -> None:
        linregress_result = [
            linregress(
                échantillon.teneur_en_eau_massique[i],
                log10(échantillon.nombre_de_coups[i]),
            )
            for i in range(28)
        ]
        df = DataFrame(
            linregress_result,
            index=range(1, 29),
        )
        df["R^2"] = df["rvalue"] ** 2
        self.régression_linéaire = df.drop(columns=["rvalue", "pvalue", "stderr"])
        self.teneur_en_eau_limite = DataFrame(
            [
                (log10(25) - linregress_result[i][1]) / linregress_result[i][0] / 100
                for i in range(28)
            ],
            index=range(1, 29),
            columns=["teneur en eau limite"],
        )


def van_Genuchten(h, qr, qs, a, m, n):
    teneur_en_eau = qr + (qs - qr) / (1 + (a * h) ** n) ** m
    return teneur_en_eau


def droite_de_liquidation(m, w, b):
    log10_nombre_de_coups = m * w + b
    return log10_nombre_de_coups


def convertir_kiloPascals_en_cm_H2O(pression):
    accélération_gravitationnelle = 9.81  # mètres par secondes^2
    Pascals = 1000  # Pascals par kiloPascal
    masse_volumique_H2O = 1000  # kilogramme par mètre^3
    conversion_cm = 100  # centimètres par mètre
    hauteur_H2O = (
        pression
        * Pascals
        * conversion_cm
        / masse_volumique_H2O
        / accélération_gravitationnelle
    )
    return hauteur_H2O


échantillon = Données()
