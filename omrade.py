class Omrade:
    """
    Attributter:
        navn (str): Navnet på området.
        beskrivelse (str): Beskrivelsen av området.
    """
    def __init__(self, navn, beskrivelse):
        self._navn = navn
        self._beskrivelse = beskrivelse

    def vis_beskrivelse(self):
        print("\n================================")
        print(self._navn.upper())
        print("================================")
        print(self._beskrivelse)
