# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Compassion CH (http://www.compassion.ch)
#    Releasing children from poverty in Jesus' name
#    @author: David Coninckx
#
#    The licence is in the file __openerp__.py
#
##############################################################################
from openerp.osv import orm


class recurring_contract(orm.TransientModel):
    _name = "install.contract.compassion"

    def install(self, cr, uid, ids=None, context=None):

        # Modify old ir_model_data to change module name
        cr.execute(
            """
        UPDATE ir_model_data
        SET module='contract_compassion'
        WHERE module='sponsorship_compassion' AND
        model='product.product'
        """
        )

        # Modify old ir_model_data to change module name
        cr.execute(
            """
        UPDATE ir_model_data
        SET module='contract_compassion'
        WHERE module='sponsorship_compassion' AND
        model IN ('workflow.activity','workflow.transition')
        """
        )
        # Set the contract type
        cr.execute(
            '''
        UPDATE recurring_contract
        SET type = 'S'
        WHERE child_id IS NOT NULL
        AND type IN ('ChildSponsorship') OR type IS NULL
        '''
        )
        cr.execute(
            '''
        UPDATE recurring_contract
        SET type = 'O'
        WHERE child_id IS NULL
        AND type IN ('ChildSponsorship') OR type IS NULL
        '''
        )

        cr.execute(
            """
        UPDATE ir_model_data
        SET module= 'contract_compassion'
        WHERE module = 'sponsorship_compassion' AND
        name IN ('view_recurring_contract_form_compassion',
        'view_contract_group_form_compassion') AND
        model = 'ir.ui.view'
        """
        )