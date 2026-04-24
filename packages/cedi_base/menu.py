# encoding: utf-8
class Menu(object):
    def config(self, root, **kwargs):
        catalogo = root.branch("Catalogo", tags="")
        catalogo.thpage("Titoli", table="cedi_base.titolo", tags="")
        catalogo.thpage("Autori", table="cedi_base.autore", tags="")
        catalogo.thpage("Titoli - Autori", table="cedi_base.titolo_autore", tags="")
        catalogo.thpage("Codifiche Titoli", table="cedi_base.titolo_codifica", tags="")
        catalogo.lookupBranch("Tabelle Ausiliarie", pkg="cedi_base")
