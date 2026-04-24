#!/usr/bin/env python
# encoding: utf-8

class Table(object):
    def config_db(self, pkg):
        tbl = pkg.table('movimento', pkey='id',
                        name_long='!![it]Movimento',
                        name_plural='!![it]Movimenti',
                        caption_field='descrizione')
        self.sysFields(tbl)
        tbl.column('canale_codice', size=':10',
                   name_long='!![it]Canale').relation('canale.codice',
                                                      relation_name='movimenti',
                                                      mode='foreignkey',
                                                      onDelete='raise')
        tbl.column('periodo_da', dtype='D', name_long='!![it]Periodo da',
                   validate_notnull=True)
        tbl.column('periodo_a', dtype='D', name_long='!![it]Periodo a',
                   validate_notnull=True)
        tbl.column('descrizione', name_long='!![it]Descrizione')
        tbl.column('file_sorgente', name_long='!![it]File sorgente')
        tbl.column('data_importazione', dtype='DH',
                   name_long='!![it]Data importazione')
        tbl.column('tipo_movimento', size=':15', name_long='!![it]Tipo',
                   values='VENDITA:Vendita,RESO:Reso,ROYALTY:Royalty,PAGAMENTO:Pagamento')
        tbl.column('valuta', size=':3', name_long='!![it]Valuta')
        tbl.column('totale_importo', dtype='money', name_long='!![it]Totale importo')
        tbl.column('totale_quantita', dtype='L', name_long='!![it]Totale quantita')
        tbl.column('note', dtype='X', name_long='!![it]Note')

        tbl.formulaColumn('n_righe',
                          select=dict(table='vendite.movimento_riga',
                                      columns='COUNT(*)',
                                      where='$movimento_id=#THIS.id'),
                          dtype='L',
                          name_long='!![it]N. Righe')
