class Papier(object):
    def __init__(self, nazov, typ, cesta, cisla = None):
        pom_typ = ''
        if typ == 1:
            pom_typ = 'WK'
        elif typ == 2:
            pom_typ = 'PREVOD'
        elif typ == 3:
            pom_typ = 'OP'
        elif typ == 4:
            pom_typ = 'TP'
        elif typ == 5:
            pom_typ = 'PZ'
        elif typ == 6:
            pom_typ = 'CP'
        elif typ == 7:
            pom_typ = 'VP'
        elif typ == 8:
            pom_typ = 'EXC'
        elif typ == 9:
            pom_typ = 'WH'
        self.typ = pom_typ
        self.nazov = nazov
        self.cesta = cesta
        self.cisla = cisla = list()

    def typ_update(self, typ):
        pom_typ = ''
        if typ == 1:
            pom_typ = 'WK'
        elif typ == 2:
            pom_typ = 'PREVOD'
        elif typ == 3:
            pom_typ = 'OP'
        elif typ == 4:
            pom_typ = 'TP'
        elif typ == 5:
            pom_typ = 'PZ'
        elif typ == 6:
            pom_typ = 'CP'
        elif typ == 7:
            pom_typ = 'VP'
        elif typ == 8:
            pom_typ = 'EXC'
        elif typ == 9:
            pom_typ = 'WH'
        self.typ = pom_typ

    def pridaj_cisla(self, zoznam):
        if type(zoznam) == list:
            for cislo in zoznam:
                if cislo not in self.cisla:
                    self.cisla.append(cislo)
            return
        self.cisla.append(zoznam)
            

    def __repr__(self):
        if len(self.cisla) == 0:
            return self.nazov + ' (' + self.typ + ')'
        printni = str(self.cisla).replace('[','').replace(']','')
        return self.nazov + ' (' + self.typ + ') ' + '- ' + printni
