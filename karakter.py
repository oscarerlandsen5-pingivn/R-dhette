import random

class Tilbehor:
    """
    Attributter:
        navn (str): Navnet på tilbehøret.
        beskyttelse (int): Hvor mye skade som reduseres.
        skade (int): Ekstra skade tilbehøret gir.
        gull (int): Ekstra gull tilbehøret gir.
        venn_med_hekser (bool): Sjekker om heksene er vennlige.
    """
    def __init__(self, navn, skade=0, beskyttelse=0, gull=0, venn_med_hekser=False):
        self._navn = navn
        self._skade = skade
        self._beskyttelse = beskyttelse
        self._gull = gull
        self._venn_med_hekser = venn_med_hekser

    def hent_navn(self):
        return self._navn

    def hent_skade(self):
        return self._skade

    def hent_beskyttelse(self):
        return self._beskyttelse

    def hent_gull(self):
        return self._gull

    def er_venn_med_hekser(self):
        return self._venn_med_hekser

class Karakter:
    """
    Attributter:
        navn (str): Navnet på karakteren.
        liv (int): Karakterens nåværende liv.
        maks_liv (int): Karakterens maksimale liv.
        skade (int): Hvor mye skade karakteren gjør.
    """
    def __init__(self, navn, liv, skade):
        self._navn = navn
        self._liv = liv
        self._maks_liv = liv
        self._skade = skade

    def angrip(self, motstander, bonus=0):
        skade = max(1, self._skade + bonus + random.randint(-2,2))

        print(f"\n{self._navn} angriper!")
        print(f"Angrepet gjør {skade} skade.")

        motstander.ta_skade(skade)

    def ta_skade(self, skade):
        self._liv = max(0, self._liv - skade)
        print(f"{self._navn} har {self._liv} liv igjen.")

    def er_i_live(self):
        return self._liv > 0

    def hent_liv(self):
        return self._liv

    def hent_maks_liv(self):
        return self._maks_liv

    def hent_navn(self):
        return self._navn


class Spiller(Karakter):
    """
    Attributter:
        tilbehor (Tilbehor): Tilbehøret spilleren har valgt.
        gull (int): Hvor mye gull spilleren har.
        helsedrikker (int): Antall helsedrikker spilleren har.
    """

    def __init__(self, navn, tilbehor):
        super().__init__(navn, 100, 15)

        self._tilbehor = tilbehor
        self._gull = 5
        self._helsedrikker = 2

    def angrip(self, motstander):
        bonus = self._tilbehor.hent_skade()
        super().angrip(motstander, bonus)

    def ta_skade(self, skade):
        reduksjon = self._tilbehor.hent_beskyttelse()
        faktisk_skade = max(0, skade - reduksjon)

        self._liv = max(0, self._liv - faktisk_skade)

        print(f"{self._navn} mister {faktisk_skade} liv.")
        print(f"Liv igjen: {self._liv}")

    def helbred(self, mengde):
        gammelt_liv = self._liv
        self._liv = min(self._maks_liv, self._liv + mengde)

        print(f"Du fikk {self._liv - gammelt_liv} liv tilbake.")

    def hent_tilbehor(self):
        return self._tilbehor

    def legg_til_gull(self, mengde):
        self._gull += mengde

    def bruk_gull(self, mengde):

        if self._gull >= mengde:
            self._gull -= mengde
            return True

        return False

    def hent_helsedrikker(self):
        return self._helsedrikker

    def legg_til_helsedrikk(self):
        self._helsedrikker += 1

    def bruk_helsedrikk(self):

        if self._helsedrikker > 0:
            self._helsedrikker -= 1
            self.helbred(30)
            return True
        print("Du har ingen helsedrikker igjen!")
        return False

    def vis_status(self):

        print("\n========== STATUS ==========")
        print(f"Navn: {self._navn}")
        print(f"Liv: {self._liv}/{self._maks_liv}")
        print(f"Gull: {self._gull}")
        print(f"Helsedrikker: {self._helsedrikker}")
        print(f"Tilbehør: {self._tilbehor.hent_navn()}")
        print("============================")


class Fiende(Karakter):
    class Fiende(Karakter):
    """
    Representerer fiendene spilleren møter i spillet.
    Klassen arver egenskaper og metoder fra Karakter.
    """
    pass
