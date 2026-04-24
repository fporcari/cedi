#!/usr/bin/env python
# encoding: utf-8
from gnr.app.gnrdbo import GnrDboTable, GnrDboPackage

class Package(GnrDboPackage):
    def config_attributes(self):
        return dict(comment='Vendite e movimenti casa editrice',
                    sqlschema='cedi_vend',
                    language='it',
                    name_short='Vendite',
                    name_long='Vendite',
                    name_full='Vendite e Movimenti')

    def config_db(self, pkg):
        pass

    def custom_type_money(self):
        return dict(dtype='N', format='#,###.00')

    def custom_type_percent(self):
        return dict(dtype='N', format='##.00')

class Table(GnrDboTable):
    pass
