#!/usr/bin/python
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent

class View(BaseComponent):
    def th_struct(self, struct):
        r = struct.view().rows()
        r.fieldcell('titolo_id', width='15em', zoom=True)
        r.fieldcell('autore_id', width='15em', zoom=True)
        r.fieldcell('ruolo', width='10em')
        r.fieldcell('quota_percentuale', width='8em', name='Quota %')

    def th_order(self):
        return 'titolo_id'

    def th_query(self):
        return dict(column='autore_id', op='contains', val='')

class ViewFromTitolo(BaseComponent):
    def th_struct(self, struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, hidden=True)
        r.fieldcell('autore_id', edit=dict(validate_notnull=True),
                    width='15em', zoom=True)
        r.fieldcell('ruolo', edit=True, width='10em')
        r.fieldcell('quota_percentuale', edit=True, width='8em', name='Quota %')

    def th_order(self):
        return 'autore_id'

class ViewFromAutore(BaseComponent):
    def th_struct(self, struct):
        r = struct.view().rows()
        r.fieldcell('titolo_id', width='15em', zoom=True)
        r.fieldcell('ruolo', width='10em')
        r.fieldcell('quota_percentuale', width='8em', name='Quota %')

    def th_order(self):
        return 'titolo_id'

class Form(BaseComponent):
    def th_form(self, form):
        pane = form.record
        fb = pane.formlet(cols=2, border_spacing='4px')
        fb.field('titolo_id', validate_notnull=True)
        fb.field('autore_id', validate_notnull=True)
        fb.field('ruolo')
        fb.field('quota_percentuale')
        fb.field('note', colspan=2, tag='simpleTextArea', height='80px')

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
