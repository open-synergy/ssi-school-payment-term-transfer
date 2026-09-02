import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-ssi-school-payment-term-transfer",
    description="Meta package for open-synergy-ssi-school-payment-term-transfer Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_school_payment_term_transfer',
        'odoo14-addon-ssi_school_payment_term_transfer_admission',
        'odoo14-addon-ssi_school_payment_term_transfer_operating_unit',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
