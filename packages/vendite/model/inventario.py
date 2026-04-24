#!/usr/bin/env python
# encoding: utf-8

class Table(object):
    def config_db(self, pkg):
        tbl = pkg.table('inventario', pkey='id',
                        name_long='!![it]Movimento inventario',
                        name_plural='!![it]Movimenti inventario',
                        caption_field='isbn')
        self.sysFields(tbl)
        tbl.column('titolo_id', size='22', group='_',
                   name_long='!![it]Titolo').relation('cedi.titolo.id',
                                                      relation_name='inventario',
                                                      mode='foreignkey',
                                                      onDelete='setnull')
        tbl.column('isbn', size=':20', name_long='!![it]ISBN')
        tbl.column('data', dtype='D', name_long='!![it]Data',
                   validate_notnull=True)
        tbl.column('quantita', dtype='L', name_long='!![it]Quantita')
        tbl.column('ricavo', dtype='money', name_long='!![it]Ricavo')
        tbl.column('tipo', size=':20', name_long='!![it]Tipo',
                   values='CONCORSO:Concorso,FIERA:Fiera,ECOMMERCE:Ecommerce,OMAGGIO:Omaggio,RESO:Reso')
        tbl.column('note', dtype='X', name_long='!![it]Note')
