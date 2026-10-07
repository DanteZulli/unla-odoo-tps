from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Oferta sobre propiedad"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            prop = self.env["estate.property"].browse(vals["property_id"])
            if prop.state not in ("new", "offer_received"):
                raise UserError(
                    "Solo se puede ofertar en propiedades Nuevas u "
                    "Ofertas recibidas."
                )
            if vals["price"] <= prop.best_offer:
                raise UserError(
                    "La oferta debe superar la mejor oferta actual."
                )
        records = super().create(vals_list)
        records.property_id.write({"state": "offer_received"})
        return records

    price = fields.Float(string="Precio", required=True)
    status = fields.Selection(
        selection=[
            ("accepted", "Aceptada"),
            ("refused", "Rechazada"),
        ],
        string="Estado",
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Ofertante", required=True
    )
    property_id = fields.Many2one(
        comodel_name="estate.property", string="Propiedad", required=True
    )
    validity = fields.Integer(string="Validez (días)", default=7)
    date_deadline = fields.Date(
        string="Fecha límite",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        string="Tipo de propiedad",
        store=True,
    )

    _sql_constraints = [
        (
            "partner_property_uniq",
            "UNIQUE(partner_id, property_id)",
            "Un ofertante no puede ofertar dos veces por la misma propiedad.",
        ),
    ]

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                base = offer.create_date.date()
            else:
                base = fields.Date.today()
            offer.date_deadline = base + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                base = offer.create_date.date()
                offer.validity = (offer.date_deadline - base).days

    def action_accept(self):
        for offer in self:
            offer.status = "accepted"
            offer.property_id.write(
                {
                    "buyer_id": offer.partner_id.id,
                    "selling_price": offer.price,
                    "state": "offer_accepted",
                }
            )
            (offer.property_id.offer_ids - offer).write(
                {"status": "refused"}
            )
