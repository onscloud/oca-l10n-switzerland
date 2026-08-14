# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    "name": "Switzerland Merge States",
    "category": "Tools",
    "version": "18.0.1.0.0",
    "author": "Odoo Community Association (OCA)",
    "maintainers": ["jguenat"],
    "website": "https://github.com/OCA/l10n-switzerland",
    "license": "AGPL-3",
    "depends": ["base"],
    "external_dependencies": {
        "python": [
            "openupgradelib",
        ]
    },
    "data": [
        "wizard/switzerland_merge_states.xml",
        "security/ir.model.access.csv",
    ],
}
