import random
from karakter import Spiller, Fiende, Tilbehor
from npc import NPC
from omrade import Omrade


class Spill:
    """
    Attributter:
        spiller (Spiller): Spilleren i spillet.
        fortsetter (bool): Sjekker om spillet skal fortsette.
        omrade (str): Området spilleren befinner seg i.
        har_ringoppdrag (bool): Om ringoppdraget er aktivt.
        har_funnet_ring (bool): Om spilleren har funnet ringen.
        har_beseiret_ulven (bool): Om ulven er beseiret.
        omrader (dict): Områdene i spillet.
        marta (NPC): NPC-en Marta.
        heksa (NPC): NPC-en Heksen.
    """

    def __init__(self):
        # Oppretter variabler som holder oversikt over spillet
        self._spiller = None
        self._fortsetter = True
        self._omrade = "Landsbyen"

        # Holder oversikt over fremdriften i oppdragene
        self._har_ringoppdrag = False
        self._har_funnet_ring = False
        self._har_beseiret_ulven = False

        # Oppretter områdene spilleren kan besøke
        self._omrader = {
            "Landsbyen": Omrade(
                "Landsbyen",
                "Du befinner deg i en liten landsby.\n"
                "Folk virker bekymret for skogen."
            ),
            "Skogen": Omrade(
                "Den mørke skogen",
                "Trærne står tett rundt deg.\n"
                "Du hører merkelige lyder."
            ),
            "Bekken": Omrade(
                "Den gamle bekken",
                "En liten bekk renner gjennom skogen.\n"
                "Noe glitrer mellom steinene."
            ),
            "Bestemors hus": Omrade(
                "Bestemors hus",
                "Du har kommet frem til bestemors hus.\n"
                "Men noe virker galt."
            )
        }

        # Oppretter NPC-ene som spilleren kan snakke med
        self._marta = NPC(
            "Marta",
            "Jeg har mistet en ring i skogen. "
            "Den betyr svært mye for meg."
        )

        self._heksa = NPC(
            "Heksen",
            "Hva gjør du i skogen min, fremmede?"
        )

    # MENY
    def velg(self, alternativer):
        """
        Viser en meny og lar spilleren velge et alternativ.

        Kontrollerer at spilleren skriver inn et gyldig tall.
        """
        while True:
            print()

            # Skriver ut alternativene med nummer
            for teller, alternativ in enumerate(alternativer, start=1):
                print(f"{teller}. {alternativ}")

            try:
                valg = int(input("\nVelg: "))

                if 1 <= valg <= len(alternativer):
                    return valg

                print("Ugyldig valg!")

            except ValueError:
                print("Du må skrive et tall.")

    # START
    def start(self):
        """
        Starter spillet og viser introduksjonen.

        Spilleren skriver inn navn og velger tilbehør
        før hovedmenyen starter.
        """
        print("""
========================================
                 RØDHETTE
             SKOGENS HEMMELIGHET
========================================

Det var en gang en jente som alle
kalte Rødhette.

En morgen ba moren henne om å levere
en kurv med mat til sin syke bestemor.

Bestemor bodde på den andre siden
av en stor og mystisk skog.

Moren hadde bare én advarsel:

"Ikke stol på alt du møter i skogen."
""")

        # Ber spilleren skrive inn et navn
        navn = input("\nHva heter du? ").strip()

        while navn == "":
            navn = input("Du må skrive et navn: ").strip()

        # Lar spilleren velge tilbehør
        self.velg_tilbehor()
        self._spiller = Spiller(navn, self._tilbehor)

        print(f"\nVelkommen, {navn}!")
        print("Du er klar for reisen.")

        # Starter hovedmenyen
        self.hovedmeny()

    def velg_tilbehor(self):
        """
        Lar spilleren velge ett av tre tilbehør.

        Hvert tilbehør gir spilleren forskjellige fordeler.
        """
        print("\nVelg ett tilbehør:")

        valg = self.velg([
            "Rød kappe - reduserer skade",
            "Heksehatt - gir ekstra skade",
            "Gullamulett - gir ekstra gull"
        ])

        if valg == 1:
            self._tilbehor = Tilbehor(
                "Rød kappe",
                beskyttelse=4
            )

        elif valg == 2:
            self._tilbehor = Tilbehor(
                "Heksehatt",
                skade=5,
                venn_med_hekser=True
            )

        else:
            self._tilbehor = Tilbehor(
                "Gullamulett",
                gull=10
            )

        print(f"\nDu valgte {self._tilbehor.hent_navn()}!")

    # HOVEDMENY
    def hovedmeny(self):
        """
        Styrer spillets hovedmeny.

        Spilleren kan bevege seg mellom områdene
        så lenge spillet fortsetter og spilleren lever.
        """
        while self._fortsetter and self._spiller.er_i_live():

            if self._omrade == "Landsbyen":
                self.landsbyen()

            elif self._omrade == "Skogen":
                self.skogen()

            elif self._omrade == "Bekken":
                self.bekken()

            elif self._omrade == "Bestemors hus":
                self.bestemors_hus()

        # Viser melding hvis spilleren mister alt livet
        if not self._spiller.er_i_live():
            print("\nDu har blitt beseiret. Spillet er over.")

    # LANDSBYEN
    def landsbyen(self):
        """
        Viser landsbyen og alternativene spilleren kan velge.

        Spilleren kan snakke med Marta, reise til skogen
        eller se sin egen status.
        """
        self._omrader["Landsbyen"].vis_beskrivelse()

        valg = self.velg([
            "Snakk med Marta",
            "Gå til skogen",
            "Se status"
        ])

        if valg == 1:
            self._marta.snakk()

            # Sjekker om spilleren allerede har funnet ringen
            if self._har_funnet_ring:
                print("\nMarta takker deg for at du fant ringen.")

            # Sjekker om spilleren allerede har fått oppdraget
            elif self._har_ringoppdrag:
                print("\nMarta håper du finner ringen snart.")

            else:
                svar = self.velg([
                    "Ja, jeg skal lete etter ringen",
                    "Nei, jeg har ikke tid"
                ])

                if svar == 1:
                    self._har_ringoppdrag = True
                    print("\nMarta takker deg for hjelpen!")

        elif valg == 2:
            self._omrade = "Skogen"

        else:
            self._spiller.vis_status()

    # SKOGEN
    def skogen(self):
        """
        Viser skogen og lar spilleren velge hva
        han eller hun ønsker å gjøre.
        """
        self._omrader["Skogen"].vis_beskrivelse()

        valg = self.velg([
            "Utforsk skogen",
            "Gå til bekken",
            "Gå til bestemors hus",
            "Gå tilbake til landsbyen",
            "Se status"
        ])

        if valg == 1:
            self.utforsk_skogen()

        elif valg == 2:
            self._omrade = "Bekken"

        elif valg == 3:
            self._omrade = "Bestemors hus"

        elif valg == 4:
            self._omrade = "Landsbyen"

        else:
            self._spiller.vis_status()

    def utforsk_skogen(self):
        """
        Utforsker skogen og velger en tilfeldig hendelse.

        Spilleren kan møte en ulv, møte heksen
        eller finne en skattekiste.
        """
        print("\nDu går dypere inn i skogen...")

        # Velger et tilfeldig tall mellom 1 og 100
        hendelse = random.randint(1, 100)

        if hendelse <= 50:
            print("\nEn ulv hopper frem fra buskene!")

            fiende = Fiende("Skogsulv", 50, 12)
            resultat = self.kamp(fiende)

            # Gir gull hvis spilleren vinner kampen
            if resultat == "vunnet":
                gull = random.randint(5, 10)
                self._spiller.legg_til_gull(gull)
                print(f"Du finner {gull} gull!")

        elif hendelse <= 75:
            self.mot_hekse()

        else:
            print("\nDu finner en skattekiste!")
            print("Du finner en helsedrikk.")
            self._spiller.legg_til_helsedrikk()

    # HEKS
    def mot_hekse(self):
        """
        Starter et møte med heksen.

        Hvis spilleren har heksehatt, får spilleren
        en helsedrikk. Ellers starter en kamp.
        """
        print("\nDu kommer til en liten lysning.")
        self._heksa.snakk()

        # Henter spillerens valgte tilbehør
        tilbehor = self._spiller.hent_tilbehor()

        if tilbehor.er_venn_med_hekser():
            print("""
Heksen ser på hatten din.

"Du bærer en av våre hatter!

Du er velkommen her!"
""")

            self._spiller.legg_til_helsedrikk()
            print("Heksen gir deg en helsedrikk.")

        else:
            print("\nHeksen blir sint og angriper!")

            fiende = Fiende("Skogheks", 45, 14)
            self.kamp(fiende)

    # BEKKEN OG RINGOPPDRAG
    def bekken(self):
        """
        Viser bekken og lar spilleren undersøke steinene,
        gå tilbake til skogen eller reise til landsbyen.
        """
        self._omrader["Bekken"].vis_beskrivelse()

        valg = self.velg([
            "Undersøk steinene",
            "Gå tilbake til skogen",
            "Gå til landsbyen",
            "Se status"
        ])

        if valg == 1:
            self.finn_ring()

        elif valg == 2:
            self._omrade = "Skogen"

        elif valg == 3:
            self._omrade = "Landsbyen"

        else:
            self._spiller.vis_status()

    def finn_ring(self):
        """
        Undersøker steinene ved bekken.

        Spilleren finner ringen hvis ringoppdraget
        fra Marta er aktivt, og mottar gull som belønning.
        """
        print("\nDu leter mellom steinene...")

        if self._har_funnet_ring:
            print("Du har allerede funnet ringen.")

        elif not self._har_ringoppdrag:
            print("Du finner noen gamle mynter, men ingen ring.")

        else:
            print("\nDu finner ringen mellom steinene!")

            # Oppdaterer statusen til ringoppdraget
            self._har_funnet_ring = True
            self._har_ringoppdrag = False

            # Regner ut belønningen basert på tilbehøret
            bonus = self._spiller.hent_tilbehor().hent_gull()
            belonning = 20 + bonus

            self._spiller.legg_til_gull(belonning)
            print(f"Marta belønner deg med {belonning} gull!")

    # KAMPSYSTEM
    def kamp(self, fiende):
        """
        Styrer kampene mellom spilleren og fienden.

        Spilleren kan angripe, bruke helsedrikk,
        forsøke å flykte eller se sin egen status.

        Returnerer resultatet av kampen.
        """
        print(f"\nEn kamp starter mot {fiende.hent_navn()}!")

        # Kampen fortsetter så lenge begge lever
        while self._spiller.er_i_live() and fiende.er_i_live():
            print("\n========== KAMP ==========")

            # Viser spillerens liv
            print(
                f"{self._spiller.hent_navn()}: "
                f"{self._spiller.hent_liv()}/"
                f"{self._spiller.hent_maks_liv()} liv"
            )

            # Viser fiendens liv
            print(
                f"{fiende.hent_navn()}: "
                f"{fiende.hent_liv()}/"
                f"{fiende.hent_maks_liv()} liv"
            )

            valg = self.velg([
                "Angrip",
                "Bruk helsedrikk",
                "Forsøk å flykte",
                "Se status"
            ])

            if valg == 1:
                self._spiller.angrip(fiende)

            elif valg == 2:
                if not self._spiller.bruk_helsedrikk():
                    continue

            elif valg == 3:
                print("\nDu prøver å flykte...")

                # Spilleren har 50 prosent sjanse for å flykte
                if random.random() < 0.5:
                    print("Du klarte å flykte!")
                    return "flykt"

                print("Du klarte ikke å flykte!")

            else:
                self._spiller.vis_status()
                continue

            # Fienden angriper hvis den fortsatt lever
            if fiende.er_i_live():
                fiende.angrip(self._spiller)

        # Sjekker om spilleren har tapt kampen
        if not self._spiller.er_i_live():
            return "tapt"

        print(f"\nDu beseiret {fiende.hent_navn()}!")
        return "vunnet"

    # BESTEMORS HUS
    def bestemors_hus(self):
        """
        Viser bestemors hus og starter hovedoppgjøret
        mot den store ulven.
        """
        self._omrader["Bestemors hus"].vis_beskrivelse()

        # Sjekker om ulven allerede er beseiret
        if self._har_beseiret_ulven:
            self.avslutning()
            return

        print("""
Du går forsiktig inn i huset.

Bestemor ligger i sengen.

Hun ser annerledes ut enn vanlig.

Plutselig oppdager du store poter
under dynen.

DET ER ULVEN!
""")

        valg = self.velg([
            "Angrip ulven",
            "Undersøk rommet",
            "Forsøk å flykte"
        ])

        if valg == 1:
            self.bosskamp()

        elif valg == 2:
            print("\nDu finner en stekepanne!")
            print("Du får et overraskelsesangrep.")
            self.bosskamp(10)

        else:
            print("\nDu løper tilbake til skogen.")
            self._omrade = "Skogen"

    def bosskamp(self, bonus=0):
        """
        Starter sjefskampen mot den store ulven.

        Spilleren kan få et ekstra angrep hvis
        han eller hun finner stekepannen.
        """
        ulv = Fiende("Den store ulven", 100, 18)

        # Gir ulven ekstra skade før kampen starter
        if bonus > 0:
            print("\nDu slår ulven med stekepannen!")
            ulv.ta_skade(bonus)

        resultat = self.kamp(ulv)

        if resultat == "vunnet":
            self._har_beseiret_ulven = True

            print("""
Ulven faller om.

Du finner bestemor gjemt i skapet
og hjelper henne ut.

"Jeg visste du ville komme!"

sier bestemor.
""")

            self.avslutning()

        elif resultat == "flykt":
            print("\nDu løper tilbake til skogen.")
            self._omrade = "Skogen"

    # AVSLUTNING
    def avslutning(self):
        """
        Avslutter spillet etter at ulven er beseiret.

        Viser gratulasjonsmelding, spillerens status
        og om sideoppdraget til Marta er fullført.
        """
        self._fortsetter = False

        print("""
========================================
              GRATULERER!
========================================

Du har beseiret ulven og reddet bestemor.

Skogen er endelig trygg igjen!

Takk for at du spilte Rødhette!
""")

        # Viser spillerens endelige status
        self._spiller.vis_status()

        # Sjekker om spilleren har fullført sideoppdraget
        if self._har_funnet_ring:
            print("Du fullførte sideoppdraget til Marta!")

        else:
            print("Du fullførte ikke sideoppdraget til Marta.")
