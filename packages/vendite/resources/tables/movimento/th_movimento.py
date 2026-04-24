#!/usr/bin/python
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent

class View(BaseComponent):
    def th_struct(self, struct):
        r = struct.view().rows()
        r.fieldcell('canale_codice', width='10em')
        r.fieldcell('tipo_movimento', width='8em')
        r.fieldcell('periodo_da', width='8em')
        r.fieldcell('periodo_a', width='8em')
        r.fieldcell('descrizione', width='20em')
        r.fieldcell('valuta', width='4em')
        r.fieldcell('totale_importo', width='10em')
        r.fieldcell('totale_quantita', width='8em')
        r.fieldcell('n_righe', width='6em')
        r.fieldcell('data_importazione', width='12em')

    def th_order(self):
        return 'periodo_da DESC'

    def th_query(self):
        return dict(column='canale_codice', op='contains', val='')

class Form(BaseComponent):
    def th_form(self, form):
        bc = form.center.borderContainer()
        self.datiMovimento(bc.roundedGroupFrame(title='Dati movimento',
                                                 region='top',
                                                 datapath='.record',
                                                 height='23em'))
        tc = bc.tabContainer(region='center', margin='2px')
        self.righeMovimento(tc.contentPane(title='Righe'))
        self.noteMovimento(tc.contentPane(title='Note', datapath='.record'))

    def datiMovimento(self, pane):
        fb = pane.div(margin_left='3em', margin_right='5em').formlet(
            cols=2, border_spacing='4px')
        fb.field('canale_codice')
        fb.field('tipo_movimento')
        fb.field('periodo_da')
        fb.field('periodo_a')
        fb.field('descrizione', colspan=2)
        fb.field('valuta')
        fb.field('totale_importo')
        fb.field('totale_quantita')
        fb.field('data_importazione')
        fb.field('file_sorgente', colspan=2, readOnly=True)

    def righeMovimento(self, pane):
        pane.plainTableHandler(relation='@righe',
                               viewResource='ViewFromMovimento')

    def noteMovimento(self, pane):
        pane.simpleTextArea(value='^.note', editor=True)

    def th_options(self):
        return dict(dialog_height='47em', dialog_width='56em')
