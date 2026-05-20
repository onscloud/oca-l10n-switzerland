Since Odoo 16.0 states are no longer translatable. Odoo's solution was to
create additional states to cover the 3 main switzerland languages
for each state.

This module aims to go back to how it was while mitigating the loss of
state translation feature. It does it by adding archiving feature to the 
state model and by allowing the erp manager to choose between four options
(each time archiving the other states).

- Keep only states in german.
- Keep only states in italian.
- Keep only states in french.
- Use the main regional language for each state e.g. Genève for GE and 
Graubunden for GR.

The discarded states are archived and the wizard will reassign every related
Many2one and Many2many fields to the chosen state so that logic relying on states is
not lost (e.g. fiscal positions, Geonames Zips, Public holidays (OCA) ...)

This module will not work for manually created states or if the states external
IDs have been messed with. It is *strongly* encourged to try the wizard on a test
database before running it in production.
