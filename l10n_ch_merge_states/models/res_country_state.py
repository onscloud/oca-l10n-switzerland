# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCountryState(models.Model):
    _inherit = "res.country.state"

    active = fields.Boolean(default=True)
