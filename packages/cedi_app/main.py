#!/usr/bin/env python
# encoding: utf-8
from gnr.app.gnrdbo import GnrDboTable, GnrDboPackage

class Package(GnrDboPackage):
    def config_attributes(self):
        return dict(comment='Applicativo Casa Editrice',
                    sqlschema='cedi_app',
                    language='it',
                    name_short='CEDI',
                    name_long='Casa Editrice',
                    name_full='Gestionale Casa Editrice')

    def config_db(self, pkg):
        pass

class Table(GnrDboTable):
    pass
