#!/usr/bin/python
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent

class View(BaseComponent):
    def th_struct(self, struct):
        r = struct.view().rows()
        r.fieldcell('cognome', width='12em')
        r.fieldcell('nome', width='12em')
        r.fieldcell('codice_fiscale', width='12em')
        r.fieldcell('partita_iva', width='10em')
        r.fieldcell('regime_fiscale_codice', width='8em')
        r.fieldcell('email', width='15em')
        r.fieldcell('n_titoli', width='6em')

    def th_order(self):
        return 'cognome'

    def th_query(self):
        return dict(column='cognome', op='contains', val='')

class Form(BaseComponent):
    def th_form(self, form):
        bc = form.center.borderContainer()
        self.datiAutore(bc.roundedGroupFrame(title='Anagrafica autore',
                                             region='top',
                                             datapath='.record',
                                             height='21em'))
        tc = bc.tabContainer(region='center', margin='2px')
        self.datiFiscali(tc.contentPane(title='Dati fiscali', datapath='.record'))
        self.titoliAutore(tc.contentPane(title='Titoli'))
        self.noteAutore(tc.contentPane(title='Note', datapath='.record'))

    def datiAutore(self, pane):
        fb = pane.div(margin_left='3em', margin_right='5em').formlet(
            cols=2, border_spacing='4px')
        fb.field('cognome', validate_notnull=True)
        fb.field('nome', validate_notnull=True)
        fb.field('email', validate_email=True)
        fb.field('telefono')
        fb.field('indirizzo', colspan=2)
        fb.field('provincia')
        fb.field('comune_id', condition='$sigla_provincia=:provincia',
                 condition_provincia='^.provincia')

    def datiFiscali(self, pane):
        fb = pane.div(margin='0.6em').formlet(
            cols=2, border_spacing='4px')
        fb.field('codice_fiscale')
        fb.field('partita_iva')
        fb.field('regime_fiscale_codice')
        fb.field('ritenuta_acconto')
        fb.field('iban', colspan=2)
        fb.field('data_contratto')

    def titoliAutore(self, pane):
        pane.dialogTableHandler(relation='@titoli_autore',
                                viewResource='ViewFromAutore')

    def noteAutore(self, pane):
        pane.simpleTextArea(value='^.note', editor=True)

    def th_options(self):
        return dict(dialog_height='43em', dialog_width='53em')
