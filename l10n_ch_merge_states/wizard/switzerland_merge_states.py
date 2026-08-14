# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade
from psycopg2 import sql

from odoo import fields, models

states = {
    "zurich": {
        "multi": "state_ch_zh",
        "ge": "state_ch_zh",
        "it": "state_ch_zh_it",
        "fr": "state_ch_zh_fr",
    },
    "bern": {
        "multi": "state_ch_be",
        "ge": "state_ch_be",
        "it": "state_ch_be_it",
        "fr": "state_ch_be_fr",
    },
    "luzern": {
        "multi": "state_ch_lu",
        "ge": "state_ch_lu",
        "it": "state_ch_lu_it",
        "fr": "state_ch_lu_fr",
    },
    "schwyz": {
        "multi": "state_ch_sz",
        "ge": "state_ch_sz",
        "it": "state_ch_sz_it",
        "fr": "state_ch_sz",
    },
    "obwalden": {
        "multi": "state_ch_ow",
        "ge": "state_ch_ow",
        "it": "state_ch_ow_it",
        "fr": "state_ch_ow_fr",
    },
    "nidwalden": {
        "multi": "state_ch_nw",
        "ge": "state_ch_nw",
        "it": "state_ch_nw_it",
        "fr": "state_ch_nw_fr",
    },
    "glarus": {
        "multi": "state_ch_gl",
        "ge": "state_ch_gl",
        "it": "state_ch_gl_it",
        "fr": "state_ch_gl_fr",
    },
    "zug": {
        "multi": "state_ch_zg",
        "ge": "state_ch_zg",
        "it": "state_ch_zg_it",
        "fr": "state_ch_zg_fr",
    },
    "freiburg": {
        "multi": "state_ch_fr_fr",
        "ge": "state_ch_fr",
        "it": "state_ch_fr_it",
        "fr": "state_ch_fr_fr",
    },
    "solothurn": {
        "multi": "state_ch_so",
        "ge": "state_ch_so",
        "it": "state_ch_so_it",
        "fr": "state_ch_so_fr",
    },
    "basels": {
        "multi": "state_ch_bs",
        "ge": "state_ch_bs",
        "it": "state_ch_bs_it",
        "fr": "state_ch_bs_fr",
    },
    "basell": {
        "multi": "state_ch_bl",
        "ge": "state_ch_bl",
        "it": "state_ch_bl_it",
        "fr": "state_ch_bl_fr",
    },
    "schaffhausen": {
        "multi": "state_ch_sh",
        "ge": "state_ch_sh",
        "it": "state_ch_sh_it",
        "fr": "state_ch_sh_fr",
    },
    "Appenzella": {
        "multi": "state_ch_ar",
        "ge": "state_ch_ar",
        "it": "state_ch_ar_it",
        "fr": "state_ch_ar_fr",
    },
    "Appenzelli": {
        "multi": "state_ch_ai",
        "ge": "state_ch_ai",
        "it": "state_ch_ai_it",
        "fr": "state_ch_ai_fr",
    },
    "stgallen": {
        "multi": "state_ch_sg",
        "ge": "state_ch_sg",
        "it": "state_ch_sg_it",
        "fr": "state_ch_sg_fr",
    },
    "graubunden": {
        "multi": "state_ch_gr",
        "ge": "state_ch_gr",
        "it": "state_ch_gr_it",
        "fr": "state_ch_gr_fr",
    },
    "aargau": {
        "multi": "state_ch_ag",
        "ge": "state_ch_ag",
        "it": "state_ch_ag_it",
        "fr": "state_ch_ag_fr",
    },
    "thurgau": {
        "multi": "state_ch_tg",
        "ge": "state_ch_tg",
        "it": "state_ch_tg_it",
        "fr": "state_ch_tg_fr",
    },
    "ticino": {
        "multi": "state_ch_ti_it",
        "ge": "state_ch_ti",
        "it": "state_ch_ti_it",
        "fr": "state_ch_ti",
    },
    "waadt": {
        "multi": "state_ch_vd_fr",
        "ge": "state_ch_vd",
        "it": "state_ch_vd_fr",
        "fr": "state_ch_vd_fr",
    },
    "wallis": {
        "multi": "state_ch_vs_fr",
        "ge": "state_ch_vs",
        "it": "state_ch_vs_it",
        "fr": "state_ch_vs_fr",
    },
    "neuenburg": {
        "multi": "state_ch_ne_fr",
        "ge": "state_ch_ne",
        "it": "state_ch_ne_fr",
        "fr": "state_ch_ne_fr",
    },
    "genf": {
        "multi": "state_ch_ge_fr",
        "ge": "state_ch_ge",
        "it": "state_ch_ge_it",
        "fr": "state_ch_ge_fr",
    },
    "jura": {
        "multi": "state_ch_ju",
        "ge": "state_ch_ju",
        "it": "state_ch_ju_it",
        "fr": "state_ch_ju",
    },
}


class SwitzerlandMergeStates(models.TransientModel):
    _name = "switzerland.merge.states"
    _description = "Switzerland Merge States"

    lang = fields.Selection(
        [
            ("multi", "Multilingual"),
            ("ge", "German"),
            ("fr", "French"),
            ("it", "Italian"),
        ],
        string="Language",
        required=True,
    )

    def _process_state(self, state, lang):
        state_xml_ids = list(set(states[state].values()))
        target_xml_id = states[state][lang]
        duplicate_xml_ids = [
            xml_id for xml_id in state_xml_ids if xml_id != target_xml_id
        ]
        target = duplicates = self.env["res.country.state"]

        target = self.env.ref(f"base.{target_xml_id}", raise_if_not_found=False)
        for duplicate_xml_id in duplicate_xml_ids:
            duplicate = self.env.ref(
                f"base.{duplicate_xml_id}", raise_if_not_found=False
            )
            duplicates |= duplicate if duplicate else duplicates

        if not target or not duplicates:
            return False
        self._change_many2one_state(duplicates, target)
        self._change_many2many_state(duplicates, target)
        self._archive(duplicates, target)
        return True

    def _change_many2one_state(self, duplicates, target):
        man2one_state_fields = self.env["ir.model.fields"].search(
            [
                ("ttype", "=", "many2one"),
                ("relation", "=", "res.country.state"),
                ("store", "=", True),
            ]
        )
        for field in man2one_state_fields:
            model = self.env[field.model_id.model]
            if not model._auto:
                continue
            table = model._table
            column = field.name
            self._query_many2one(table, column, duplicates, target)
        return True

    def _change_many2many_state(self, duplicates, target):
        man2many_state_fields = self.env["ir.model.fields"].search(
            [
                ("ttype", "=", "many2many"),
                ("relation", "=", "res.country.state"),
                ("store", "=", True),
            ]
        )
        for field in man2many_state_fields:
            model = self.env[field.model_id.model]
            if not model._auto:
                continue
            table = model._fields[field.name].relation
            column1 = model._fields[field.name].column1
            column2 = model._fields[field.name].column2
            self._query_many2many(table, column1, column2, duplicates, target)
        return True

    def _query_many2one(self, table, column, duplicates, target):
        sql_query = sql.SQL(
            """
            UPDATE {table}
            SET {column} = %(target)s
            WHERE {column} in %(duplicates)s
            """
        ).format(
            table=sql.Identifier(table),
            column=sql.Identifier(column),
        )
        openupgrade.logged_query(
            self.env.cr,
            sql_query,
            {
                "target": target.id,
                "duplicates": tuple(duplicates.ids),
            },
            skip_no_result=True,
        )
        return True

    def _query_many2many(self, table, column1, column2, duplicates, target):
        # avoid unique key value contraint : it is possible the target state
        # is already there.
        sql_query = sql.SQL(
            """
            UPDATE {table}
            SET {column2} = %(target)s
            WHERE {column2} IN %(duplicates)s
              AND NOT EXISTS (
                  SELECT 1
                  FROM {table} t2
                  WHERE t2.{column1} = {table}.{column1}
                    AND t2.{column2} = %(target)s
              )
            """
        ).format(
            table=sql.Identifier(table),
            column1=sql.Identifier(column1),
            column2=sql.Identifier(column2),
        )
        openupgrade.logged_query(
            self.env.cr,
            sql_query,
            {
                "target": target.id,
                "duplicates": tuple(duplicates.ids),
            },
            skip_no_result=True,
        )
        return True

    def _archive(self, duplicates, target):
        target.write({"active": True})
        duplicates.write({"active": False})
        return True

    def merge_states(self):
        for state in states:
            self._process_state(state, self.lang)
        return True
