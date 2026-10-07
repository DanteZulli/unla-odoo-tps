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

## Act. 9 — Validez y fecha límite

- En `estate.property.offer`: `validity` Integer default 7 + `date_deadline`
  Date, ambos agregados a la lista de ofertas.
- ([e6be7e2](https://github.com/DanteZulli/unla-odoo-tps/commit/e6be7e2))

## Act. 10 — Cómputo con inverso

- `date_deadline = create_date + validity` (`compute`), pero si el usuario
  carga la fecha se recalcula la validez (`inverse`). Sin registro creado
  aún (`create_date` vacío) se usa hoy como base. Con `inverse=` el
  computado deja de ser readonly (ver material teórico).
- ([e6be7e2](https://github.com/DanteZulli/unla-odoo-tps/commit/e6be7e2))

## Act. 11 — Related almacenado

- `property_type_id` related a `property_id.property_type_id` con
  `store=True`: trae el tipo sin duplicar datos y al estar almacenado
  permite buscar y agrupar por él.
- ([7c938f9](https://github.com/DanteZulli/unla-odoo-tps/commit/7c938f9))

## Act. 12 — Formulario y menú de ofertas

- Form de oferta (precio, ofertante, propiedad, tipo + validez, límite,
  estado) + acción "Ofertas" (`list,form`) con menú bajo Anuncios.
- ¿Se pueden agrupar por tipo? Sí: el related está almacenado, así que
  `group_by` sobre `property_type_id` funciona en la lista.
- ([5fdf952](https://github.com/DanteZulli/unla-odoo-tps/commit/5fdf952))

## Act. 13 — Onchange de jardín

- `@api.onchange("garden")`: al tildar, `garden_area = 10`; al destildar,
  `= 0`. Solo corre en el form sin guardar (UX, no validación).
- ([11a02af](https://github.com/DanteZulli/unla-odoo-tps/commit/11a02af))

## Act. 14 — Onchange no bloqueante de precio

- `@api.onchange("expected_price")`: si < 10000 devuelve `warning` (no
  bloquea el guardado, solo avisa posible error de tipeo). Se puede
  depurar con `wdb.set_trace()` y verlo en el wdb de Doodba (`:19984`).
- ([11a02af](https://github.com/DanteZulli/unla-odoo-tps/commit/11a02af))

## Act. 15 — Botones Cancelar / Vendida

- `action_cancel` y `action_sold` en el header, con `invisible` por estado
  (frontend) + `UserError` en backend si se vende una cancelada o se
  cancela una vendida. Al vender, ribbon "Vendida" (`web_ribbon` visible
  solo en `sold`).
- ([b696f14](https://github.com/DanteZulli/unla-odoo-tps/commit/b696f14))

## Act. 16 — Aceptar oferta

- `action_accept` en la lista de ofertas: marca Aceptada, carga comprador
  y precio en la propiedad, la pasa a "oferta aceptada" y rechaza las
  demás (`offer_ids - offer`).
- ([3749784](https://github.com/DanteZulli/unla-odoo-tps/commit/3749784))

## Act. 17 — Nombres únicos

- `UNIQUE(name)` en tipos y etiquetas. Si hay duplicados en base, el
  Upgrade falla: hay que limpiarlos desde la UI antes.
- ([23e140e](https://github.com/DanteZulli/unla-odoo-tps/commit/23e140e))

## Act. 18 — Oferta única por partner/propiedad

- `UNIQUE(partner_id, property_id)` en ofertas (limpiar duplicados antes
  desde la UI).
- ([23e140e](https://github.com/DanteZulli/unla-odoo-tps/commit/23e140e))

## Act. 19 — `offer_partner_ids`

- Many2many computado con todos los ofertantes
  (`offer_ids.partner_id`, depends en `offer_ids.partner_id`).
- ¿Serviría un related? No: el related sigue un único camino M2O; acá hay
  que juntar los partners de N ofertas, eso pide cómputo.
- ([a1a4625](https://github.com/DanteZulli/unla-odoo-tps/commit/a1a4625))

## Act. 20 — Oferta automática

- Botón en la página Ofertas: precio = esperado ±30% (`random.uniform`),
  ofertante al azar entre contactos activos que aún no ofertaron
  (`random.choice` + `not in`); `UserError` si no hay precio o no quedan
  candidatos.
- ([a690d63](https://github.com/DanteZulli/unla-odoo-tps/commit/a690d63))

## Act. 21 — Botones de etiquetas

- "Sacar etiquetas" (`Command.clear`), "Cargar todas las etiquetas"
  (`Command.set`) y "A estrenar" (crea+vincula con `Command.link` si no
  existe). Comandos relacionales sin escribir la tabla intermedia a mano.
- ([a690d63](https://github.com/DanteZulli/unla-odoo-tps/commit/a690d63))
