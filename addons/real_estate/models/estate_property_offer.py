from datetime import timedelta

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Oferta sobre propiedad"

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
