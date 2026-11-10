from odoo import Command, _, api, fields, models
from odoo.exceptions import UserError

# layout -> report action (xml id)
LAYOUT_REPORTS = {
    'barcode_50x25': 'product_label_builder.action_report_label_50x25',
    'price_60x40': 'product_label_builder.action_report_label_60x40',
    'sheet_a4_3x8': 'product_label_builder.action_report_label_a4_3x8',
}
MAX_LABELS = 1000
EXTRA_TEXT_MAX = 40
TEXT_SCALE = {'small': 0.85, 'medium': 1.0, 'large': 1.2}


class ProductLabelBuilderWizard(models.TransientModel):
    _name = 'product.label.builder.wizard'
    _description = 'Product Label Builder'

    layout = fields.Selection([
        ('barcode_50x25', 'Barcode label 50 × 25 mm'),
        ('price_60x40', 'Price tag 60 × 40 mm'),
        ('sheet_a4_3x8', 'A4 sheet - 24 labels (3 × 8)'),
    ], string='Layout', required=True, default='barcode_50x25')
    show_price = fields.Boolean(string='Sales price', default=True)
    show_code = fields.Boolean(string='Internal reference', default=True)
    show_barcode = fields.Boolean(string='Barcode', default=True)
    text_size = fields.Selection([
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ], string='Text size', required=True, default='medium')
    extra_text = fields.Char(string='Extra text line', size=EXTRA_TEXT_MAX,
                             help='Printed on every label, e.g. your shop name or "Made in Pakistan".')
    line_ids = fields.One2many('product.label.builder.line', 'wizard_id', string='Products')
    label_count = fields.Integer(string='Labels', compute='_compute_label_count')

    @api.depends('line_ids.quantity')
    def _compute_label_count(self):
        for wizard in self:
            wizard.label_count = sum(max(q, 0) for q in wizard.line_ids.mapped('quantity'))

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'line_ids' in fields_list and not res.get('line_ids'):
            model = self.env.context.get('active_model')
            ids = self.env.context.get('active_ids') or []
            products = self.env['product.product']
            if model == 'product.template':
                products = self.env['product.template'].browse(ids).product_variant_ids
            elif model == 'product.product':
                products = self.env['product.product'].browse(ids)
            res['line_ids'] = [Command.create({'product_id': p.id, 'quantity': 1}) for p in products]
        return res

    def action_print(self):
        self.ensure_one()
        lines = self.line_ids.filtered(lambda line: line.product_id and line.quantity > 0)
        if not lines:
            raise UserError(_('Add at least one product with a quantity above 0.'))
        if self.label_count > MAX_LABELS:
            raise UserError(_(
                'The free version prints up to %(max)s labels at a time (you asked for %(count)s). '
                'Print in smaller batches, or use Odoo Product Label Builder PRO for up to 10,000 labels per print.',
                max=MAX_LABELS, count=self.label_count))
        extra_text = (self.extra_text or '').strip()
        if len(extra_text) > EXTRA_TEXT_MAX:
            raise UserError(_('The extra text line can have up to %(max)s characters.', max=EXTRA_TEXT_MAX))
        data = {
            'lines': [[line.product_id.id, line.quantity] for line in lines],
            'show_price': self.show_price,
            'show_code': self.show_code,
            'show_barcode': self.show_barcode,
            'scale': TEXT_SCALE[self.text_size],
            'extra_text': extra_text,
        }
        # config=False: labels have no letterhead, so never stop at the "document layout" setup screen
        return self.env.ref(LAYOUT_REPORTS[self.layout]).report_action(None, data=data, config=False)


class ProductLabelBuilderLine(models.TransientModel):
    _name = 'product.label.builder.line'
    _description = 'Product Label Builder - Product'

    wizard_id = fields.Many2one('product.label.builder.wizard', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    barcode = fields.Char(related='product_id.barcode', string='Barcode')
    quantity = fields.Integer(string='Labels', default=1)
