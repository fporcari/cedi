#!/usr/bin/env python
# encoding: utf-8

class Table(object):
    def config_db(self, pkg):
        tbl = pkg.table('titolo_codifica', pkey='id',
                        name_long='!![it]Codifica titolo',
                        name_plural='!![it]Codifiche titolo',
                        caption_field='codice')
        self.sysFields(tbl, counter='titolo_id')
        tbl.column('titolo_id', size='22', group='_',
                   name_long='!![it]Titolo').relation('titolo.id',
                                                      relation_name='codifiche',
                                                      mode='foreignkey',
                                                      onDelete='cascade')
        tbl.column('codice', size=':20', name_long='!![it]Codice',
                   validate_notnull=True)
        tbl.column('tipo_codice', size=':15', name_long='!![it]Tipo codice',
                   values='ISBN:ISBN,ASIN:ASIN,ISBN_STORYTEL:ISBN Storytel')
        tbl.column('tipo_prodotto', size=':15', name_long='!![it]Tipo prodotto',
                   values='EBOOK:Ebook,CARTACEO:Cartaceo,AUDIOLIBRO:Audiolibro')
        tbl.column('tipo_stampa', size=':15', name_long='!![it]Tipo stampa',
                   values='POD:POD,SELF:Self,TIRATURA:Tiratura')
        tbl.column('prezzo', dtype='money', name_long='!![it]Prezzo')
        tbl.column('royalty_percentuale', dtype='percent',
                   name_long='!![it]Royalty %')
        tbl.column('data_uscita', dtype='D', name_long='!![it]Data uscita')
        tbl.column('note', dtype='T', name_long='!![it]Note')
