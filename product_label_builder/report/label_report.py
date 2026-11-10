from odoo import api, models

SHEET_SIZE = 24      # A4 sheet: 3 columns x 8 rows
SHEET_COLUMNS = 3


class ProductLabelBuilderReport(models.AbstractModel):
    """Turns the wizard's [product id, quantity] pairs into the list of labels to print."""
    _name = 'report.product_label_builder.report_label_base'
    _description = 'Product Label Builder - labels'

    @api.model
    def _get_report_values(self, docids, data=None):
        data = data or {}
        products = self.env['product.product']
        labels = []
        for product_id, quantity in data.get('lines', []):
            product = products.browse(int(product_id)).exists()
            if product:
                labels.extend([product] * max(int(quantity), 0))
        sheets = []
        for start in range(0, len(labels), SHEET_SIZE):
            sheet = labels[start:start + SHEET_SIZE]
            sheets.append([sheet[i:i + SHEET_COLUMNS] for i in range(0, len(sheet), SHEET_COLUMNS)])
        return {
            'labels': labels,
            'sheets': sheets,
            'show_price': data.get('show_price', True),
            'show_code': data.get('show_code', True),
            'show_barcode': data.get('show_barcode', True),
            'scale': float(data.get('scale') or 1.0),
            'extra_text': (data.get('extra_text') or '')[:40],
        }


class ProductLabelBuilderReport50x25(models.AbstractModel):
    _name = 'report.product_label_builder.report_label_50x25'
    _inherit = 'report.product_label_builder.report_label_base'
    _description = 'Product Label Builder - 50 x 25 mm'


class ProductLabelBuilderReport60x40(models.AbstractModel):
    _name = 'report.product_label_builder.report_label_60x40'
    _inherit = 'report.product_label_builder.report_label_base'
    _description = 'Product Label Builder - 60 x 40 mm'


class ProductLabelBuilderReportA4(models.AbstractModel):
    _name = 'report.product_label_builder.report_label_a4_3x8'
    _inherit = 'report.product_label_builder.report_label_base'
    _description = 'Product Label Builder - A4 3 x 8'
