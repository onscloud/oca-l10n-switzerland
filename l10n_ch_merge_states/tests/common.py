# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from contextlib import contextmanager

import odoo
from odoo.tests import common

ADMIN_USER_ID = common.ADMIN_USER_ID


@contextmanager
def environment():
    """Return an environment with a new cursor for the current database; this
    is required to run sql query with the same cursor. Need to be carful and
    cleanup with tearDownClass.
    """
    registry = odoo.modules.registry.Registry(common.get_db_name())
    with registry.cursor() as cr:
        yield odoo.api.Environment(cr, ADMIN_USER_ID, {})
