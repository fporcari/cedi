#!/usr/bin/python
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent

class View(BaseComponent):
    def th_struct(self, struct):
        r = struct.view().rows()
        r.fieldcell('movimento_id', width='12em', zoom=True)
        r.fieldcell('isbn', width='12em')
        r.fieldcell('descrizione_titolo', width='18em')
        r.fieldcell('autore', width='12em')
        r.fieldcell('quantita', width='6em')
        r.fieldcell('prezzo_unitario', width='8em')
        r.fieldcell('importo_lordo', width='8em')
        r.fieldcell('importo_netto', width='8em')
        r.fieldcell('royalty', width='8em')
        r.fieldcell('paese', width='4em')
        r.fieldcell('store', width='10em')

    def th_order(self):
        return 'movimento_id'

    def th_query(self):
        return dict(column='isbn', op='contains', val='')

class ViewFromMovimento(BaseComponent):
    def th_struct(self, struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, hidden=True)
        r.fieldcell('isbn', width='12em')
        r.fieldcell('descrizione_titolo', width='18em')
        r.fieldcell('autore', width='12em')
        r.fieldcell('titolo_id', width='12em', zoom=True)
        r.fieldcell('quantita', width='6em')
        r.fieldcell('prezzo_unitario', width='8em')
        r.fieldcell('importo_lordo', width='8em')
        r.fieldcell('importo_netto', width='8em')
        r.fieldcell('royalty', width='8em')
        r.fieldcell('valuta', width='4em')
        r.fieldcell('paese', width='4em')
        r.fieldcell('store', width='10em')

    def th_order(self):
        return 'isbn'

class Form(BaseComponent):
    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('movimento_id')
        fb.field('titolo_id')
        fb.field('isbn')
        fb.field('descrizione_titolo')
        fb.field('autore')
        fb.field('quantita')
        fb.field('prezzo_unitario')
        fb.field('importo_lordo')
        fb.field('importo_netto')
        fb.field('royalty')
        fb.field('valuta')
        fb.field('tasso_cambio')
        fb.field('paese')
        fb.field('store')
        fb.field('tipo_prodotto')
        fb.field('sconto_percentuale')
        fb.field('aliquota_iva')
        fb.field('note', colspan=2, tag='simpleTextArea', height='80px')

    def th_options(self):
        return dict(dialog_height='500px', dialog_width='700px')
