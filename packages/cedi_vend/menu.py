# encoding: utf-8
class Menu(object):
    def config(self, root, **kwargs):
        movimenti = root.branch("Movimenti", tags="")
        movimenti.thpage("Movimenti", table="cedi_vend.movimento", tags="")
        movimenti.thpage("Dettaglio Righe", table="cedi_vend.movimento_riga", tags="")
        movimenti.thpage("Inventario", table="cedi_vend.inventario", tags="")
        movimenti.lookupBranch("Tabelle Ausiliarie", pkg="cedi_vend")
