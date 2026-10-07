from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Propiedad"

    name = fields.Char(string="Título", required=True)
    description = fields.Text(string="Descripción")
    postcode = fields.Char(string="Código Postal")
    date_availability = fields.Date(
        string="Fecha disponibilidad",
        copy=False,
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(string="Precio esperado")
    selling_price = fields.Float(string="Precio de venta", copy=False)
    bedrooms = fields.Integer(string="Habitaciones", default=2)
    living_area = fields.Integer(string="Superficie cubierta")
    facades = fields.Integer(string="Fachadas")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Jardín")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "Norte"),
            ("south", "Sur"),
            ("east", "Este"),
            ("west", "Oeste"),
        ],
        default="north",
        string="Orientación del jardín",
    )
    garden_area = fields.Integer(string="Superficie jardín")
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type", string="Tipo Propiedad"
    )
    buyer_id = fields.Many2one(comodel_name="res.partner", string="Comprador")
    salesman_id = fields.Many2one(
        comodel_name="res.users",
        string="Vendedor",
        copy=False,
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many(
        comodel_name="estate.property.tag", string="Etiquetas"
    )
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
        string="Ofertas",
    )
    total_area = fields.Float(
        string="Superficie total",
        compute="_compute_total_area",
        store=True,
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_offer = fields.Float(
        string="Mejor oferta", compute="_compute_best_offer"
    )

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(
                record.offer_ids.mapped("price"), default=0
            )

    offer_partner_ids = fields.Many2many(
        comodel_name="res.partner",
        compute="_compute_offer_partner_ids",
        string="Ofertantes",
    )

    @api.depends("offer_ids.partner_id")
    def _compute_offer_partner_ids(self):
        for record in self:
            record.offer_partner_ids = record.offer_ids.partner_id

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
        else:
            self.garden_area = 0

    @api.onchange("expected_price")
    def _onchange_expected_price(self):
        if self.expected_price and self.expected_price < 10000:
            return {
                "warning": {
                    "title": "Precio bajo",
                    "message": (
                        "El precio esperado es menor a 10000, "
                        "posible error de tipeo."
                    ),
                }
            }

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError(
                    "No se puede cancelar una propiedad vendida."
                )
            record.state = "canceled"

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError(
                    "No se puede vender una propiedad cancelada."
                )
            record.state = "sold"
    state = fields.Selection(
        selection=[
            ("new", "Nuevo"),
            ("offer_received", "Oferta recibida"),
            ("offer_accepted", "Oferta aceptada"),
            ("sold", "Vendido"),
            ("canceled", "Cancelado"),
        ],
        string="Estado",
        required=True,
        default="new",
        copy=False,
    )
