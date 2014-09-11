from openerp.osv import orm, fields
from openerp.tools.translate import _

class compassion_bvr_wizard(orm.Model):
    _name = 'compassion.bvr.wizard'
    
    _columns = {
        'dest_account_id': fields.many2one(
            'res.partner.bank', _('Destination account'),
            required=True, domain=[('state', '=', 'bvr')]),
        'print_birthday': fields.boolean(_('Birthday')),
        'print_family': fields.boolean(_('Family')),
        'print_general': fields.boolean(_('General')),
        'print_project': fields.boolean(_('Project')),
        'print_graduation': fields.boolean(_('Graduation')),
        'fund_id': fields.many2one(
            'product.product', _('Fund'),
            domain=[('categ_id.name', '=', 'Fund')]),
    }
    
    def launch_report(self, cr, uid, ids, context=None):
        datas = {}
        if context is None:
            context = {}
        data = self.read(cr, uid, ids)[0]
        form = self.browse(cr, uid, ids)[0]
        account_id = form.dest_account_id.id
        fund_id = form.fund_id
        datas = {
                     'ids': context.get('active_ids', []),
                     'model': 'res.partner',
        }
        context['account_id'] = account_id
        if fund_id:
            context['fund_id'] = fund_id.id
        context['gift'] = {
            '1': form.print_birthday,
            '2': form.print_general,
            '3': form.print_family,
            '4': form.print_project,
            '5': form.print_graduation
        }
        return {'type': 'ir.actions.report.xml', 'report_name': 'three_bvr_per_page', 'datas': datas, 'context': context}