from numpy import loadtxt, array


class Données:
    def __init__(self) -> None:
        self.delta_H = 8  # cm
        self.longueur = 5  # cm
        self.diamètre = 5  # cm
        self.débit_H2O = loadtxt(
            "data/conductivité_hydraulique.csv",
            dtype=float,
            skiprows=1,
            delimiter=";",
            unpack=True,
        )
        self.teneur_en_eau = loadtxt(
            "data/courbe_de_rétention.csv",
            dtype=float,
            skiprows=2,
            usecols=range(1, 29),
            delimiter=";",
            unpack=True,
        )
        self.potentiel_matriciel = loadtxt(
            "data/courbe_de_rétention.csv",
            dtype=float,
            skiprows=2,
            usecols=0,
            delimiter=";",
            unpack=True,
        )
        cisaillement = loadtxt(
            "data/tension_de_cisaillement.csv",
            dtype=float,
            skiprows=2,
            delimiter=";",
            unpack=True,
        )
        self.cisaillement = array(
            [[cisaillement[2 * x], cisaillement[2 * x + 1]] for x in range(28)]
        )
        compression = loadtxt(
            "data/résistance_à_la_compression.csv",
            dtype=float,
            skiprows=2,
            delimiter=";",
            unpack=True,
        )
        self.compression = array(
            [[compression[2 * x], compression[2 * x + 1]] for x in range(28)]
        )
        liquidation = loadtxt(
            "data/limite_de_liquidité.csv",
            dtype=float,
            skiprows=2,
            delimiter=";",
            unpack=True,
        )
        self.nombre_de_coups = array([liquidation[2 * x] for x in range(28)])
        self.teneur_en_eau_massique = array([liquidation[2 * x + 1] for x in range(28)])
