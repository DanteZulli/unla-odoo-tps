from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Etiqueta de propiedad"

    _sql_constraints = [
        (
            "name_uniq",
            "UNIQUE(name)",
            "El nombre de la etiqueta debe ser único.",
        ),
    ]

    name = fields.Char(string="Nombre", required=True)
