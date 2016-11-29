# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp import report as odoo_report
import base64
import zipfile
import StringIO


class ReportZipWizard(models.TransientModel):

    _name = 'report.zip.wizard'

    @api.one
    def _get_zip_file_name(self):
        self.zip_file_name = 'reports.zip'

    def get_report_filename(self, source_model, record_id, report_name):
        ''' A generif function for naming individual report files inside
        the ZIP archive. Override and customize this function as necessary. '''

        report_prefix = report_name.lower().replace(' ', '_')
        # Remove slashes to avoid creating subdirs inside zip. Use object ID
        # as a fallback in case there is no name defined
        active_object = self.env[source_model].browse(record_id)
        object_name = active_object.name and active_object.name.replace('/', '-') or str(active_object.id)
        filetype_suffix = 'pdf'

        return '{}_{}.{}'.format(report_prefix, object_name, filetype_suffix)

    @api.multi
    def create_zip(self):

        report_name = self.report_id.name
        report_service = self.report_id.report_name

        in_memory_zip = StringIO.StringIO()

        with zipfile.ZipFile(in_memory_zip, 'w') as report_zip:

            ''' Iterate through all the checkmarked records and generate the PDF reports '''
            for record_id in self._context.get('active_ids', []):

                if self.report_id.report_type in ['qweb-html', 'qweb-pdf']:
                    result, format = self.pool['report'].get_pdf(self._cr, self._uid, [record_id], report_service, context=self._context), 'pdf'
                else:
                    render_options = {
                        'model': self.source_model
                    }
                    result, format = odoo_report.render_report(self._cr, self._uid, [record_id], report_service, render_options, context=self._context)

                report_filename = self.get_report_filename(self.source_model, record_id, report_name)
                report_zip.writestr(report_filename, result)

        ''' Attach the ready zip file to the wizard '''
        self.zip_file = base64.b64encode(in_memory_zip.getvalue())

        ''' Update the wizard's state and relaunch it, now showing the download link '''
        self.state = 'step_results'

        return {
            'type': 'ir.actions.act_window',
            'name': _('Zip multiple reports'),
            'res_model': 'report.zip.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }

    name = fields.Char('Name')
    report_id = fields.Many2one('ir.actions.report.xml', 'Report')
    state = fields.Selection([('step_selection', 'Selection'),('step_results', 'Results')], 'State', default='step_selection')
    source_model = fields.Char('Source model')
    zip_file = fields.Binary('Zip file')
    zip_file_name = fields.Char(compute=_get_zip_file_name, string='Filename')
