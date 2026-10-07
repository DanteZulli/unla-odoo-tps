# Unidad 2 — Registro de avance

Campos computados, `@api.depends`, `@api.onchange`, related, ORM/CRUD,
constraints, comandos relacionales, herencia, wdb. Módulo `estate_account`.

## Act. 1–2 — `total_area` computado

- `total_area = fields.Float(compute="_compute_total_area")` en
  `estate.property` + `total_area` en la página "Descripción" del form.
  Sin `store`, se calcula en memoria cada vez que se muestra.
- ([340989c](https://github.com/DanteZulli/unla-odoo-tps/commit/340989c))

## Act. 3 — pgweb y campos no almacenados

- En pgweb la tabla `estate_property` no tiene columna `total_area`:
  sin `store=True` no hay columna, Odoo lo computa al vuelo y por eso sí
  aparece en la vista. Solo UI, sin código.

## Act. 4 — `store=True` sin depends

- Con `store=True` aparece la columna y el valor se guarda, pero deja de
  recomputarse al cambiar living/garden: Odoo no sabe cuándo invalidar
  el cache porque falta `@api.depends`. Se verifica cambiando ambos
  campos tras el Upgrade.
- (incluido en
  [340989c](https://github.com/DanteZulli/unla-odoo-tps/commit/340989c))

## Act. 5 — `@api.depends`

- `@api.depends("living_area", "garden_area")` declara las dependencias:
  Odoo invalida y recalcula el almacenado ante cada cambio. Estado final:
  `store=True` + depends.
- (incluido en
  [340989c](https://github.com/DanteZulli/unla-odoo-tps/commit/340989c))

## Act. 6 — Dos ofertas de prueba

- Solo UI: cargar dos ofertas con distinto precio en una propiedad para
  probar el Act. 7.

## Act. 7 — `best_offer`

- `best_offer` Float computado = `max(offer_ids.mapped("price"), default=0)`,
  con `@api.depends("offer_ids.price")`, mostrado bajo el precio de venta.
- ¿Almacenarlo? No: es un agregado barato sobre pocas ofertas y así nunca
  queda desactualizado; con `store=True` habría que mantener depends sobre
  la relación y solo convendría si se busca/ordena por ese campo en listas.
- ([1dfe4de](https://github.com/DanteZulli/unla-odoo-tps/commit/1dfe4de))

## Act. 8 — Ofertas desde formulario

- Se sacó `editable="top"` de la lista de ofertas: ahora se crean desde su
  formulario (abre paso a validez/límite del Act. 9+).
- ([1dfe4de](https://github.com/DanteZulli/unla-odoo-tps/commit/1dfe4de))
