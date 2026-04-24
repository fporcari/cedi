#!/usr/bin/env python
# encoding: utf-8

class Table(object):
    def config_db(self, pkg):
        tbl = pkg.table('titolo_autore', pkey='id',
                        name_long='!![it]Titolo - Autore',
                        name_plural='!![it]Titoli - Autori')
        self.sysFields(tbl, counter='titolo_id')
        tbl.column('titolo_id', size='22', group='_',
                   name_long='!![it]Titolo').relation('titolo.id',
                                                      relation_name='autori_titolo',
                                                      mode='foreignkey',
                                                      onDelete='cascade')
        tbl.column('autore_id', size='22', group='_',
                   name_long='!![it]Autore').relation('autore.id',
                                                      relation_name='titoli_autore',
                                                      mode='foreignkey',
                                                      onDelete='raise')
        tbl.column('quota_percentuale', dtype='percent',
                   name_long='!![it]Quota %')
        tbl.column('ruolo', size=':30', name_long='!![it]Ruolo')
        tbl.column('note', dtype='X', name_long='!![it]Note')

    def defaultValues(self):
        return dict(quota_percentuale=100)
