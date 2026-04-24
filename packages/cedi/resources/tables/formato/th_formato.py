#!/usr/bin/python
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent

class View(BaseComponent):
    def th_struct(self, struct):
        r = struct.view().rows()
        r.fieldcell('codice')
        r.fieldcell('descrizione')

    def th_order(self):
        return 'codice'

    def th_query(self):
        return dict(column='codice', op='contains', val='')

class Form(BaseComponent):
    def th_form(self, form):
        pane = form.record
        fb = pane.formlet(cols=2, border_spacing='4px')
        fb.field('codice')
        fb.field('descrizione')

    def th_options(self):
        return dict(dialog_height='15em', dialog_width='25em')
