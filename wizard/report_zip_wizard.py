# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
import base64


class ReportZipWizard(models.TransientModel):

    _name = 'report.zip.wizard'

    @api.multi
    def create_zip(self):

        report_service = self.report_id.report_name

        for id in self._context.get('active_ids', []):

            result = self.pool['report'].get_pdf(self._cr, self._uid, [id], report_service)
            b64result = base64.b64encode(result)
            self.zip_file = b64result
            break


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
