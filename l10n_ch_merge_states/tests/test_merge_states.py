# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import BaseCase, tagged

from .common import environment


@tagged("post_install", "-at_install")
class TestMergeState(BaseCase):
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        with environment() as env:
            self.model_name = "x_merge.states.test.model"
            self.field_name = "x_merge_states_m2m_test_field"
            self.partner_name = "test_partner"
            # create a model
            self.model = env["ir.model"].create(
                {
                    "name": "Merge states test model",
                    "model": self.model_name,
                }
            )
            # create a many2many field
            self.field = env["ir.model.fields"].create(
                {
                    "name": self.field_name,
                    "model_id": self.model.id,
                    "field_description": "Merge states test field",
                    "ttype": "many2many",
                    "relation": "res.country.state",
                }
            )
            # create a record with the many2many field
            self.test_model_record = env[self.model_name].create(
                {
                    self.field_name: [(6, 0, [env.ref("base.state_ch_zh_fr").id])],
                }
            )
            # create a partner
            self.partner = env["res.partner"].create(
                {
                    "name": self.partner_name,
                    "state_id": env.ref("base.state_ch_zh_fr").id,
                }
            )

    def test_reassign_state(self):
        with environment() as env:
            wizard = env["switzerland.merge.states"].create({"lang": "multi"})
            wizard.merge_states()
            state_m2m = (
                env[self.model_name]
                .browse(self.test_model_record.id)
                .x_merge_states_m2m_test_field
            )
            self.assertEqual(
                state_m2m, env.ref("base.state_ch_zh"), "m2m state was not reassigned"
            )
            state_m2o = (
                env["res.partner"].search([("name", "=", self.partner_name)]).state_id
            )
            self.assertEqual(
                state_m2o, env.ref("base.state_ch_zh"), "m2o state was not reassigned"
            )
            active = env.ref("base.state_ch_zh_fr").active
            self.assertFalse(active)

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()
        with environment() as env:
            test_record = env[self.model_name].search(
                [("id", "=", self.test_model_record.id)]
            )
            if test_record:
                test_record.unlink()
            field = env["ir.model.fields"].search([("name", "=", self.field_name)])
            if field:
                field.unlink()
            model = env["ir.model"].search([("model", "=", self.model_name)])
            if model:
                model.unlink()
            partner = env["res.partner"].search([("name", "=", self.partner_name)])
            if partner:
                partner.unlink()
