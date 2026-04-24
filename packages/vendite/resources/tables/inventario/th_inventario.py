#!/usr/bin/python
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent

class View(BaseComponent):
    def th_struct(self, struct):
        r = struct.view().rows()
        r.fieldcell('data', width='8em')
        r.fieldcell('isbn', width='12em')
        r.fieldcell('titolo_id', width='15em', zoom=True)
        r.fieldcell('quantita', width='6em')
        r.fieldcell('ricavo', width='8em')
        r.fieldcell('tipo', width='8em')
        r.fieldcell('note', width='15em')

    def th_order(self):
        return 'data DESC'

    def th_query(self):
        return dict(column='isbn', op='contains', val='')

class Form(BaseComponent):
    def th_form(self, form):
        pane = form.record
        fb = pane.formlet(cols=2, border_spacing='4px')
        fb.field('data')
        fb.field('isbn')
        fb.field('titolo_id')
        fb.field('quantita')
        fb.field('ricavo')
        fb.field('tipo')
        fb.field('note', colspan=2, tag='simpleTextArea', height='80px')

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
