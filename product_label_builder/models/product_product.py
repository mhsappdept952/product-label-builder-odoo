from odoo import _, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def action_open_label_builder(self):
        """Print Labels button of the Product Labels app: opens the print window for the selected
        products (or an empty one to add products to, when nothing is selected)."""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Print Product Labels'),
            'res_model': 'product.label.builder.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_model': 'product.product', 'active_ids': self.ids},
        }
