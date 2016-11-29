# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2016- Vizucom Oy (http://www.vizucom.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Zip Multiple Reports',
    'category': 'Utilities',
    'version': '1.0',
    'author': 'Vizucom Oy',
    'website': 'http://www.vizucom.com',
    'depends': ['report'],
    'description': """
Zip Multiple Reports
====================
* Creates a generic wizard for selecting multiple records, rendering their PDF reports and placing them inside a single ZIP file for the user to download
* Does not directly add the functionality to any Odoo object, so you will need to inherit this module to add the wizard to e.g. Purchase Orders or Invoices.
* Works also with Aeroo reports

Usage
-----
* In your custom module, inherit this module and create a new action to a model of your choice, e.g.::

    <act_window id="action_account_invoice_zip"
                multi="True" key2="client_action_multi" name="Create ZIP file"
                res_model="report.zip.wizard" src_model="account.invoice"
                view_mode="form" target="new" view_type="form"
                context="{'default_source_model': context.get('active_model') }" />

* Check the boxes in your object's treeview, and click More --> Create ZIP file to launch the wizard.
""",
    'data': [
        'views/report_zip_wizard.xml',
    ],
}
