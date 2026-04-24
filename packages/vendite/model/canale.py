#!/usr/bin/env python
# encoding: utf-8

class Table(object):
    def config_db(self, pkg):
        tbl = pkg.table('canale', pkey='codice',
                        name_long='!![it]Canale',
                        name_plural='!![it]Canali',
                        caption_field='descrizione',
                        lookup=True)
        self.sysFields(tbl, id=False)
        tbl.column('codice', size=':10', name_long='!![it]Codice')
        tbl.column('descrizione', name_long='!![it]Descrizione')
