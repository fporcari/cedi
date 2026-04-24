#!/usr/bin/env python
# encoding: utf-8

class Table(object):
    def config_db(self, pkg):
        tbl = pkg.table('titolo', pkey='id',
                        name_long='!![it]Titolo',
                        name_plural='!![it]Titoli',
                        caption_field='titolo')
        self.sysFields(tbl)
        tbl.column('isbn', size=':17', name_long='!![it]ISBN',
                   unique=True, indexed=True)
        tbl.column('titolo', size=':200', name_long='!![it]Titolo',
                   validate_notnull=True)
        tbl.column('sottotitolo', size=':200', name_long='!![it]Sottotitolo')
        tbl.column('collana_codice', size=':5',
                   name_long='!![it]Collana').relation('collana.codice',
                                                       relation_name='titoli',
                                                       mode='foreignkey',
                                                       onDelete='raise')
        tbl.column('formato_codice', size=':5',
                   name_long='!![it]Formato').relation('formato.codice',
                                                       relation_name='titoli',
                                                       mode='foreignkey',
                                                       onDelete='raise')
        tbl.column('genere_codice', size=':5',
                   name_long='!![it]Genere').relation('genere.codice',
                                                      relation_name='titoli',
                                                      mode='foreignkey',
                                                      onDelete='raise')
        tbl.column('aliquota_iva', dtype='percent',
                   name_long='!![it]Aliquota IVA')
        tbl.column('data_pubblicazione', dtype='D',
                   name_long='!![it]Data pubblicazione')
        tbl.column('attivo', dtype='B', name_long='!![it]Attivo')
        tbl.column('note', dtype='X', name_long='!![it]Note')

        tbl.formulaColumn('n_autori',
                          select=dict(table='cedi_base.titolo_autore',
                                      columns='COUNT(*)',
                                      where='$titolo_id=#THIS.id'),
                          dtype='L',
                          name_long='!![it]N. Autori')

        tbl.formulaColumn('n_codifiche',
                          select=dict(table='cedi_base.titolo_codifica',
                                      columns='COUNT(*)',
                                      where='$titolo_id=#THIS.id'),
                          dtype='L',
                          name_long='!![it]N. Codifiche')

    def defaultValues(self):
        return dict(attivo=True)
