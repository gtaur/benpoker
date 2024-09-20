
class Giocatore:
    def __init__(self, nome,cognome, pg,loss,paypal,cash,podi,masterL,alias,battlecry,pic_dir,punti=0,):
        self.nome = nome
        self.punti = punti
        self.posizione = None  # Può essere aggiornata man mano che le partite si svolgono
        self.pg = pg
        self.cognome = cognome
        self.paypal = paypal
        self.loss = loss
        self.cash = cash
        self.podi = podi
        self.masterL = masterL
        self.alias = alias
        self.battlecry = battlecry
        self.pic_dir = pic_dir

    
    def aggiungi_punti(self, punti):
        """Aggiungi punti al giocatore dopo una partita."""
        self.punti += punti
    def presente(self,pg):
        """Incrementa il numero di partite giocate"""
        self.pg = pg+1
    def guadagno (self,cash):
        self.cash = cash

    def __str__(self):
        return f"{self.nome} - {self.punti} punti"

class Partita:
    def __init__(self, giocatori, data,giornata):
        self.giocatori = giocatori  # Lista di istanze di Giocatore
        self.data = data
        self.giornata = giornata
    
    def registra_risultati(self, risultati):
        """Aggiorna i punti dei giocatori in base ai risultati della partita."""
        for nome, punti in risultati.items():
            for giocatore in self.giocatori:
                if giocatore.nome == nome:
                    giocatore.aggiungi_punti(punti)
                    break

class Torneo:
    def __init__(self, nome):
        self.nome = nome
        self.partite = []  # Elenco delle partite
        self.giocatori = []  # Elenco delle istanze di Giocatore
    
    def aggiungi_giocatore(self, giocatore):
        self.giocatori.append(giocatore)
    
    def aggiungi_partita(self, partita):
        self.partite.append(partita)
        partita.registra_risultati(partita.risultati)
    
    def aggiorna_classifica(self):
        """Ordina i giocatori in base ai punti."""
        self.giocatori.sort(key=lambda x: x.punti, reverse=True)
    
    def mostra_classifica(self):
        """Mostra la classifica aggiornata dei giocatori."""
        self.aggiorna_classifica()
        for posizione, giocatore in enumerate(self.giocatori, 1):
            giocatore.posizione = posizione
            print(f"{posizione}. {giocatore.nome} - {giocatore.punti} punti")
