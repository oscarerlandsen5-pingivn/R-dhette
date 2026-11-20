class NPC:
    """
    Attributter:
        navn (str): Navnet på personen.
        dialog (str): Dialogen til personen.
    """
    def __init__(self, navn, dialog):
        self._navn = navn
        self._dialog = dialog

    def snakk(self):
        print(f"\n{self._navn}:")
        print(f'"{self._dialog}"')
