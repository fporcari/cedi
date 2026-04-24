#!/usr/bin/python
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent

class View(BaseComponent):
    def th_struct(self, struct):
        r = struct.view().rows()
        r.fieldcell('isbn', width='12em')
        r.fieldcell('titolo', width='20em')
        r.fieldcell('collana_codice', width='8em')
        r.fieldcell('formato_codice', width='8em')
        r.fieldcell('genere_codice', width='8em')
        r.fieldcell('n_autori', width='6em')
        r.fieldcell('n_codifiche', width='6em')
        r.fieldcell('data_pubblicazione', width='8em')
        r.fieldcell('attivo', width='5em')

    def th_order(self):
        return 'titolo'

    def th_query(self):
        return dict(column='titolo', op='contains', val='')

class Form(BaseComponent):
    def th_form(self, form):
        bc = form.center.borderContainer()
        self.datiTitolo(bc.roundedGroupFrame(title='Dati titolo',
                                             region='top',
                                             datapath='.record',
                                             height='180px'))
        tc = bc.tabContainer(region='center', margin='2px')
        self.codificheTitolo(tc.contentPane(title='Codifiche'))
        self.autoriTitolo(tc.contentPane(title='Autori'))
        self.noteTitolo(tc.contentPane(title='Note', datapath='.record'))

    def datiTitolo(self, pane):
        fb = pane.div(margin_left='50px', margin_right='80px').formlet(
            cols=2, border_spacing='4px')
        fb.field('isbn')
        fb.field('collana_codice')
        fb.field('titolo', colspan=2, validate_notnull=True)
        fb.field('sottotitolo', colspan=2)
        fb.field('formato_codice')
        fb.field('genere_codice')
        fb.field('data_pubblicazione')
        fb.field('aliquota_iva')
        fb.field('attivo')

    def codificheTitolo(self, pane):
        pane.inlineTableHandler(relation='@codifiche',
                                viewResource='ViewFromTitolo')

    def autoriTitolo(self, pane):
        pane.inlineTableHandler(relation='@autori_titolo',
                                viewResource='ViewFromTitolo')

    def noteTitolo(self, pane):
        pane.simpleTextArea(value='^.note', editor=True)

    def th_options(self):
        return dict(dialog_height='550px', dialog_width='850px')
