# encoding: utf-8
class Menu(object):
    def config(self, root, **kwargs):
        movimenti = root.branch("Movimenti", tags="")
        movimenti.thpage("Movimenti", table="vendite.movimento", tags="")
        movimenti.thpage("Dettaglio Righe", table="vendite.movimento_riga", tags="")
        movimenti.thpage("Inventario", table="vendite.inventario", tags="")
        movimenti.lookupBranch("Tabelle Ausiliarie", pkg="vendite")
