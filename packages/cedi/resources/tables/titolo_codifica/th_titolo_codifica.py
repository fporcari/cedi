#!/usr/bin/python
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent

class View(BaseComponent):
    def th_struct(self, struct):
        r = struct.view().rows()
        r.fieldcell('titolo_id', width='15em', zoom=True)
        r.fieldcell('codice', width='12em')
        r.fieldcell('tipo_codice', width='10em')
        r.fieldcell('tipo_prodotto', width='10em')
        r.fieldcell('tipo_stampa', width='8em')
        r.fieldcell('prezzo', width='8em')
        r.fieldcell('royalty_percentuale', width='7em', name='Royalty %')
        r.fieldcell('data_uscita', width='8em')

    def th_order(self):
        return 'titolo_id'

    def th_query(self):
        return dict(column='codice', op='contains', val='')

class ViewFromTitolo(BaseComponent):
    def th_struct(self, struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, hidden=True)
        r.fieldcell('codice', edit=dict(validate_notnull=True), width='12em')
        r.fieldcell('tipo_codice', edit=True, width='10em')
        r.fieldcell('tipo_prodotto', edit=True, width='10em')
        r.fieldcell('tipo_stampa', edit=True, width='8em')
        r.fieldcell('prezzo', edit=True, width='8em')
        r.fieldcell('royalty_percentuale', edit=True, width='7em', name='Royalty %')
        r.fieldcell('data_uscita', edit=True, width='8em')

    def th_order(self):
        return 'tipo_codice'

class Form(BaseComponent):
    def th_form(self, form):
        pane = form.record
        fb = pane.formlet(cols=2, border_spacing='4px')
        fb.field('titolo_id', validate_notnull=True)
        fb.field('codice', validate_notnull=True)
        fb.field('tipo_codice')
        fb.field('tipo_prodotto')
        fb.field('tipo_stampa')
        fb.field('prezzo')
        fb.field('royalty_percentuale')
        fb.field('data_uscita')
        fb.field('note', colspan=2, tag='simpleTextArea', height='5em')

    def th_options(self):
        return dict(dialog_height='38em', dialog_width='38em')
