{
    'name': 'Odoo Product Label Builder – Free | Barcode & Price Labels (PDF)',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Free product label builder for Odoo: print barcode labels, price tags and A4 label sheets as PDF '
               'from the product list. Choose products, quantities and a layout - no setup, no extra libraries.',
    'description': """
Product Label Builder - Free
============================
Print product labels as PDF straight from the product list or form:

- barcode label 50 x 25 mm, price tag 60 x 40 mm, A4 sheet with 24 labels (3 x 8)
- product name, internal reference, sales price and barcode (EAN-13 / Code 128, chosen automatically)
- quantity per product, any printer

Need your own label layouts, price-list offers or direct printing to Zebra (ZPL) and TSC / Rongta
(TSPL) label printers? See Odoo Product Label Builder PRO (label_studio_pro).
    """,
    'author': 'NexMosaic Technologies',
    'maintainer': 'NexMosaic Technologies',
    'support': 'support@nexmosaictechnologies.com',
    'depends': ['product'],
    'data': [
        'security/ir.model.access.csv',
        'report/label_reports.xml',
        'report/label_templates.xml',
        'wizard/label_builder_wizard_views.xml',
        'views/menu_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
