from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        res = super().action_sold()
        for record in self:
            if record.buyer_id and record.selling_price:
                self.env["account.move"].create(
                    {
                        "move_type": "out_invoice",
                        "partner_id": record.buyer_id.id,
                        "invoice_line_ids": [
                            Command.create(
                                {
                                    "name": record.name,
                                    "quantity": 1,
                                    "price_unit": record.selling_price,
                                }
                            ),
                            Command.create(
                                {
                                    "name": "Gastos administrativos",
                                    "quantity": 1,
                                    "price_unit": 100,
                                }
                            ),
                        ],
                    }
                )
        return res
