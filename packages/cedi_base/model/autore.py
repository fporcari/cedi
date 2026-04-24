#!/usr/bin/env python
# encoding: utf-8

class Table(object):
    def config_db(self, pkg):
        tbl = pkg.table('autore', pkey='id',
                        name_long='!![it]Autore',
                        name_plural='!![it]Autori',
                        caption_field='denominazione')
        self.sysFields(tbl)
        tbl.column('cognome', size=':60', name_long='!![it]Cognome',
                   validate_notnull=True)
        tbl.column('nome', size=':60', name_long='!![it]Nome',
                   validate_notnull=True)
        tbl.column('codice_fiscale', size=':16',
                   name_long='!![it]Codice fiscale', name_short='!![it]C.F.')
        tbl.column('partita_iva', size=':11',
                   name_long='!![it]Partita IVA', name_short='!![it]P.IVA')
        tbl.column('regime_fiscale_codice', size=':5',
                   name_long='!![it]Regime fiscale').relation('regime_fiscale.codice',
                                                              relation_name='autori',
                                                              mode='foreignkey',
                                                              onDelete='raise')
        tbl.column('ritenuta_acconto', dtype='percent',
                   name_long='!![it]Ritenuta acconto %')
        tbl.column('iban', size=':34', name_long='!![it]IBAN')
        tbl.column('email', name_long='!![it]Email')
        tbl.column('telefono', size=':20', name_long='!![it]Telefono')
        tbl.column('indirizzo', name_long='!![it]Indirizzo')
        tbl.column('provincia', size='2',
                   name_long='!![it]Provincia',
                   name_short='!![it]Pr.').relation('glbl.provincia.sigla',
                                                     relation_name='autori',
                                                     mode='foreignkey',
                                                     onDelete='raise')
        tbl.column('comune_id', size='22', group='_',
                   name_long='!![it]Comune').relation('glbl.comune.id',
                                                      relation_name='autori',
                                                      mode='foreignkey',
                                                      onDelete='raise')
        tbl.column('data_contratto', dtype='D',
                   name_long='!![it]Data contratto')
        tbl.column('note', dtype='X', name_long='!![it]Note')

        tbl.formulaColumn('denominazione',
                          "$cognome || ' ' || $nome",
                          name_long='!![it]Denominazione')

        tbl.formulaColumn('n_titoli',
                          select=dict(table='cedi_base.titolo_autore',
                                      columns='COUNT(*)',
                                      where='$autore_id=#THIS.id'),
                          dtype='L',
                          name_long='!![it]N. Titoli')
