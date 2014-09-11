# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Cyril Sester. Copyright Compassion CH
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import re
import time
from os.path import dirname

from openerp import addons
from openerp.report import report_sxw
from openerp.osv import orm

from openerp.tools import mod10r
from openerp.tools.translate import _

import logging
logger = logging.getLogger(__name__)


class three_bvr_per_page(report_sxw.rml_parse):
    ''' Report that output three BVR from partners. '''

    def __init__(self, cr, uid, name, context):
        super(three_bvr_per_page, self).__init__(cr, uid, name,
                                                 context=context)

        # Setup vars passed to template file
        bank_obj = self.pool.get('res.partner.bank')
        self.localcontext.update({
            'police_absolute_path': self.police_absolute_path,
            'account': bank_obj.browse(cr, uid, context.get('account_id')),
            'get_bvrs_data': self._get_bvrs_data,
            '_space': self._space,
        })

        #Setup internal vars
        self.fund = None
        if context.get('fund_id'):
            self.fund = self.pool.get('product.product').browse(cr, uid, context.get('fund_id'))
        self.gifts = context.get('gift')

    def set_context(self, objects, data, ids, report_type=None):
        objects = self.pool.get('res.partner').browse(
            self.cr, self.uid, ids)

        return super(three_bvr_per_page, self).set_context(
            objects,
            data,
            ids,
            report_type='webkit'
            )

    def _get_bvrs_data(self, partner):
        data = []
        i = 0  # Used for numpole in gift ref
        for sponsorship in partner.contracts_paid + partner.contracts_fully_managed:
            i += 1
            if sponsorship.state not in ['active', 'waiting']:
                continue
            for gift_id, checked in self.gifts.iteritems():
                if not checked:
                    continue
                data.append([self._compute_gift_ref(gift_id, partner, i,
                                                    sponsorship),
                             False, self._get_gift_com(gift_id, sponsorship)])
        if self.fund:
            data.append([self._compute_fund_ref(self.fund, partner), 
                         False, self._get_fund_com(self.fund)])
        
        return data

    def _compute_fund_ref(self, fund, partner):
        ''' Compute fund ref with fund-id and partner codega '''
        ref = partner.ref + '0'*5 + '6' + str(fund.gp_fund_id).zfill(5)
        return mod10r(ref)

    def _get_fund_com(self, fund):
        ''' Generate a comment for fund '''
        return fund.name

    def _compute_gift_ref(self, gift_id, partner, numpole, sponsorship):
        ''' Compute gift bvr ref '''
        ref = partner.ref + str(numpole).zfill(5) + gift_id + '0'*4
        return mod10r(ref)

    def _get_gift_com(self, gift_id, sponsorship):
        ''' Generate a comment for gift (if needed) '''
        child = sponsorship.child_id
        comment = child.name + ' (' + child.code + ')<br />'
        gift_names = {'1': _('Birthday'), '2': _('General'), '3': _('Family'),
                      '4': _('Project'), '5': _('Graduation')}
        comment += _('%s gift') % gift_names[gift_id] + '<br />'
        if gift_id == '1' and sponsorship.child_id.birthdate:
            comment += _('Birthdate: %s') % sponsorship.child_id.birthdate
        return comment

    @staticmethod
    def _space(nbr, nbrspc=5):
        """Spaces * 5.

        Example:
            AccountInvoice._space('123456789012345')
            '12 34567 89012 345'
        """
        l = len(str(nbr))
        return ''.join([' '[(l-i) % nbrspc:] + c for i, c in enumerate(nbr)])

    def police_absolute_path(self, inner_path):
        """Will get the ocrb police absolute path"""
        path = addons.get_module_resource(
            'l10n_ch_payment_slip',
            'report',
            inner_path
        )
        return path

# The dirname function is an hack, we should find a better solution...
report_sxw.report_sxw('report.three_bvr_per_page',
                      'res.partner',
                      dirname(__file__) + '/three_bvr_per_page.mako',
                      parser=three_bvr_per_page)
