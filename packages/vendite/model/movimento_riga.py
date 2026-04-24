#!/usr/bin/env python
# encoding: utf-8

class Table(object):
    def config_db(self, pkg):
        tbl = pkg.table('movimento_riga', pkey='id',
                        name_long='!![it]Riga movimento',
                        name_plural='!![it]Righe movimento',
                        caption_field='descrizione_titolo')
        self.sysFields(tbl, counter='movimento_id')
        tbl.column('movimento_id', size='22', group='_',
                   name_long='!![it]Movimento').relation('movimento.id',
                                                         relation_name='righe',
                                                         mode='foreignkey',
                                                         onDelete='cascade')
        tbl.column('titolo_id', size='22', group='_',
                   name_long='!![it]Titolo').relation('cedi.titolo.id',
                                                      relation_name='movimenti',
                                                      mode='foreignkey',
                                                      onDelete='setnull')
        tbl.column('isbn', size=':20', name_long='!![it]ISBN/ASIN')
        tbl.column('descrizione_titolo', name_long='!![it]Titolo (da file)')
        tbl.column('autore', name_long='!![it]Autore (da file)')
        tbl.column('quantita', dtype='L', name_long='!![it]Quantita')
        tbl.column('prezzo_unitario', dtype='money', name_long='!![it]Prezzo unitario')
        tbl.column('importo_lordo', dtype='money', name_long='!![it]Importo lordo')
        tbl.column('importo_netto', dtype='money', name_long='!![it]Importo netto')
        tbl.column('royalty', dtype='money', name_long='!![it]Royalty')
        tbl.column('valuta', size=':3', name_long='!![it]Valuta')
        tbl.column('tasso_cambio', dtype='N', name_long='!![it]Tasso cambio')
        tbl.column('paese', size=':20', name_long='!![it]Paese')
        tbl.column('store', name_long='!![it]Store/Piattaforma')
        tbl.column('tipo_prodotto', size=':15', name_long='!![it]Tipo prodotto',
                   values='EBOOK:Ebook,CARTACEO:Cartaceo,AUDIOLIBRO:Audiolibro')
        tbl.column('sconto_percentuale', dtype='percent',
                   name_long='!![it]Sconto %')
        tbl.column('aliquota_iva', dtype='percent',
                   name_long='!![it]Aliquota IVA')
        tbl.column('note', dtype='X', name_long='!![it]Note')
