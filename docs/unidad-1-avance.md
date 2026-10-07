# Unidad 1 — Registro de avance (Acts. 1–41)

Módulo `real_estate`: modelos, vistas, menús y seguridad. Entorno Odoo 19
sobre Doodba (la guía pide Odoo 18; acá puertos `19xxx`).

## Act. 1 — Entorno

- Se verificó la instancia: 7 contenedores en `Up` (`odoo`, `db`, `proxy`,
  `pgweb`, `smtp`, `wdb`, `net_setup`) y login `admin/admin` en `:19069`.
- Puertos: Odoo `19069`, pgweb `19081`, MailHog `19025`, wdb `19984`.
- Lo discutido: la guía referencia Odoo 18 / puertos `18xxx`; todo se traslada
  tal cual a 19 / `19xxx`.

## Act. 2 — Módulo `real_estate`

- Se generó el esqueleto con scaffold dentro del contenedor y se ubicó en
  `addons/real_estate`, expuesto a Odoo vía symlink en `private/` (Doodba solo
  lee addons desde ahí).
- Lo challengeado: el scaffold trae de más (`controllers`, `demo`, vistas,
  csv apuntando a un modelo inexistente, import de `controllers`) y eso rompe
  el install. Se recortó al mínimo de la guía: `__init__.py` + `__manifest__.py`.
- Instalación por UI: el `Update Apps List` exige modo debug (`?debug=1`; en
  19 el backend es `/odoo`) y hay que sacar la pastilla `Apps` del buscador
  para que aparezca el módulo.
- ([a6408dd](https://github.com/DanteZulli/unla-odoo-tps/commit/a6408dd6c0c9bdf60e6883385a951fa6a5fed9c7))

## Act. 3 — Modelo `estate.property`

- Se creó `models/estate_property.py` con los 13 campos de la guía
  (`Char`, `Text`, `Date`, `Float`, `Integer`, `Boolean`, `Selection` con sus
  `string`, `required`, `default`) y se cableó en `models/__init__.py`.
- Lo aprendido: no hay comando que genere el modelo con sus campos; el
  scaffold solo deja un ejemplo comentado. El modelo se escribe a mano con el
  ORM (`_name`, `_description`, `fields.*`).
- ([242bd4b](https://github.com/DanteZulli/unla-odoo-tps/commit/242bd4b5193ecf45824ac308caa20efde1803d88))

## Act. 4 — pgweb

- pgweb (`:19081`) ya entra conectado a la base `devel`; se buscó la tabla
  `estate_property` (Odoo convierte los puntos en guion bajo).
- Además de los 13 campos, Odoo crea `id`, `create_date`, `create_uid`,
  `write_date` y `write_uid`: los campos "mágicos" de auditoría.

## Act. 5 — Acción

- Se definió `ir.actions.act_window` "Propiedades" (`list,form`) en
  `views/estate_property_views.xml` y se incluyó en el manifest.
- Sin vistas propias, Odoo renderiza lista y formulario genéricos (solo el
  nombre), lo que motiva el Act. 22 más adelante.
- ([c75c725](https://github.com/DanteZulli/unla-odoo-tps/commit/c75c72517d1514505ff1f1bd7c476109f4dac43f))

## Act. 6 — Menús

- Tres niveles en `views/real_estate_menuitem.xml`:
  `Inmobiliaria` (raíz) → `Anuncios` → `Propiedades` (acción del Act. 5).
- Lo discutido: el orden en `data` importa — el menú referencia la acción,
  así que el archivo de vistas va primero; invertido, el update falla con
  `external ID not found`.
- ([4ced331](https://github.com/DanteZulli/unla-odoo-tps/commit/4ced3312e0d26b43100c0080b8dc1ea3216c71d5))

## Act. 7 — Menús invisibles y superuser

- Tras el Upgrade los menús no se veían. Causa: sin `ir.model.access.csv` el
  usuario no tiene ningún permiso y Odoo oculta los menús sin acceso.
- Se verificó con debug + *Become Superuser* (el icono bug indica debug
  activo; puede estar bajo el bug o el avatar según versión; salir = logout).

## Act. 8 — `view_mode`

- Solo `list`: no hay formulario de detalle/creación. Solo `form`: se abre el
  formulario directo, sin lista. Se deja `list,form`. Sin cambios de código.

## Act. 9 — Tipos de usuario

- Interno (`base.group_user`, empleados con backend), Portal
  (`base.group_portal`, contactos externos), Público (`base.group_public`,
  anónimos) y Superuser (`__system__`, saltea todos los accesos).

## Act. 10 — `ir.model.access.csv`

- Se creó `security/ir.model.access.csv` con solo lectura para
  `base.group_user` (= usuario interno). Para dar crear/modificar/eliminar
  bastaría poner `1` en `perm_create`/`perm_write`/`perm_unlink`.
- El csv va primero en `data`: la seguridad se carga antes que vistas y menús.
- ([db60dc8](https://github.com/DanteZulli/unla-odoo-tps/commit/db60dc8cd0fcbefb0468c71067a72e11d48dbb16))

## Act. 11 — Grupo por UI

- Se creó "Manager de Propiedades" desde Settings → Groups, con el usuario
  asignado y las 4 tildes (lectura/creación/escritura/borrado); al principio
  faltaban Crear y Borrar y se corrigió.
- Se probó crear, modificar y eliminar propiedades. Lo aprendido: por UI es
  inmediato para prototipar, pero no se versiona ni se despliega.

## Act. 12 — Grupo Manager en el módulo

- Se formalizó el grupo en `security/real_estate_res_groups.xml`.
- UI vs módulo: rápido y efímero contra versionado, reproducible e instalable
  en cualquier base a cambio de requerir Upgrade por cambio.
- Detalle: al upgradear conviven el grupo de UI y el del módulo (con external
  id `real_estate.group_estate_manager`); se borra el de UI.
- ([dd5b9f0](https://github.com/DanteZulli/unla-odoo-tps/commit/dd5b9f0727a2a0819cb90bec14d8b1c9d667aeba))

## Act. 13 — Grupo Vendedor en el módulo

- "Vendedor de Propiedades" en el mismo xml (mismo commit que Act. 12).

## Act. 14 — Permisos Manager/Vendedor

- Manager con full (`1,1,1,1`) y Vendedor con solo lectura; se eliminó la
  línea de `base.group_user`, que queda sin accesos.
- ([652c27c](https://github.com/DanteZulli/unla-odoo-tps/commit/652c27c714bd9bc740532383e352f39d81cb5194))

## Act. 15 — Usuario sin grupos

- Sin pertenecer a ningún grupo: denegado total (`AccessError` si entra
  directo, menús ocultos). Verificado con un usuario de prueba.

## Act. 16 — Categoría

- Categoría `Inmobiliaria` (`ir.module.category`) con ambos grupos para
  ubicarlos juntos.
- Desvío Odoo 19 (guía = Odoo 18): `res.groups` ya no tiene `category_id` y
  el install fallaba con `Invalid field 'category_id'`. Se adaptó al modelo
  nuevo: privilegio `Inmobiliaria` (`res.groups.privilege` bajo la categoría)
  + `privilege_id` en ambos grupos, con Manager implicando a Vendedor (mismo
  patrón que Contabilidad en `account`).
- ([1bcd20e](https://github.com/DanteZulli/unla-odoo-tps/commit/1bcd20ed8e09e8c25da088a3fbf5f30ee51c9af9),
  [a96c19f](https://github.com/DanteZulli/unla-odoo-tps/commit/a96c19f))

## Act. 17 — Vista search

- Search en `views/estate_property_views.xml`: busca por `name`, `postcode`,
  `expected_price`, `bedrooms`, `living_area` y `facades`.
- Filtro `Mis propiedades` (`create_uid = uid`) y agrupar por creador, mes de
  creación (`create_date:month`) y código postal. Odoo la levanta sola por
  modelo, sin tocar la acción.
- ([7d9303f](https://github.com/DanteZulli/unla-odoo-tps/commit/7d9303f))

## Act. 18 — Duplicar

- Solo UI: crear un registro y desde la lista Acción → Duplicar. Por defecto
  copia todos los campos (incluye fecha y precio de venta), lo que motiva el
  Act. 19.

## Act. 19 — `copy=False`

- `date_availability` y `selling_price` con `copy=False`: al duplicar, esos
  dos quedan vacíos y el resto se copia. Se verifica duplicando antes y
  después del cambio (requiere Upgrade).
- ([8dea7b4](https://github.com/DanteZulli/unla-odoo-tps/commit/8dea7b4))

## Act. 20 — Fecha por defecto

- `date_availability` por defecto = hoy + 3 meses, con
  `default=lambda self: fields.Date.add(fields.Date.today(), months=3)`.
  Se verifica creando un registro: la fecha ya viene cargada.
- ([b3bdbdf](https://github.com/DanteZulli/unla-odoo-tps/commit/b3bdbdf))

## Act. 21 — Campo `state`

- `state` (Selection, requerido, default `new`, `copy=False`): Nuevo, Oferta
  recibida, Oferta aceptada, Vendido, Cancelado. Al duplicar, vuelve a Nuevo.
- ([b3bdbdf](https://github.com/DanteZulli/unla-odoo-tps/commit/b3bdbdf))

## Act. 22 — Lista custom

- Vista `list` propia con `name`, `postcode`, `bedrooms`, `living_area`,
  `expected_price`, `selling_price` y `date_availability`. Antes Odoo
  mostraba solo el nombre.
- ([645caeb](https://github.com/DanteZulli/unla-odoo-tps/commit/645caeb))

## Act. 23 — Formulario custom

- Form con `state` en el header (`statusbar`), `name` en H1 con placeholder
  "Nombre propiedad", dos grupos de dos campos (postal/disponibilidad y
  esperado/venta) y notebook "Descripción" con `description` + dos subgrupos
  (interior: habitaciones/superficie/fachadas/garage; jardín: jardín/área/
  orientación).
- ([64baf46](https://github.com/DanteZulli/unla-odoo-tps/commit/64baf46))

## Act. 24 — Search: disponibles y por estado

- Filtro `Disponibles` (`state` en Nuevo u Oferta recibida) + agrupar por
  estado.
- Desvío Odoo 19: el `<group expand="0" string="...">` no pasa la validación
  RNG (`Invalid view ... search definition`); la referencia oficial usa
  `<group>` pelado. Validado en local contra `search_view.rng`.
- ([64baf46](https://github.com/DanteZulli/unla-odoo-tps/commit/64baf46),
  [46277af](https://github.com/DanteZulli/unla-odoo-tps/commit/46277af))

## Act. 25 — Modelo `estate.property.type`

- `models/estate_property_type.py` con `name` Char requerido + import en
  `models/__init__.py`. Solo el modelo: sin vistas todavía Odoo genera
  lista/form automáticos.
- ([8662f6a](https://github.com/DanteZulli/unla-odoo-tps/commit/8662f6a))

## Act. 26 — Accesos sobre tipos

- Manager full (`1,1,1,1`), Vendedor solo lectura, mismo esquema que
  `estate.property`.
- ([c8c4bc3](https://github.com/DanteZulli/unla-odoo-tps/commit/c8c4bc3))

## Act. 27 — Acción de tipos

- `views/estate_property_type_views.xml` con `ir.actions.act_window`
  "Tipos de propiedad" (`list,form`). Sin vistas propias al principio;
  después se agregó lista explícita (ver Act. 33).
- ([99bce12](https://github.com/DanteZulli/unla-odoo-tps/commit/99bce12))

## Act. 28 — Menú Ajustes

- Primer nivel "Ajustes" bajo "Inmobiliaria" + submenú "Tipos de propiedad"
  a la acción. El xml de tipos va antes del menú en el manifest (orden
  `data` por dependencias, como en Act. 6).
- Nota de debugging: etiquetas (`list` solo) andaba, tipos (`list,form`)
  colgaba el browser: la diferencia era el formulario autogenerado, que el
  cliente genera al abrir tipos aunque muestre la lista. Con lista + form
  explícitos se estabilizó.
- ([99bce12](https://github.com/DanteZulli/unla-odoo-tps/commit/99bce12),
  [c2777e4](https://github.com/DanteZulli/unla-odoo-tps/commit/c2777e4))
- Actualización: el form explícito NO lo resolvió. Tipos abre pero no recibe
  clicks (solo se sale con Tab); etiquetas anda joya con el mismo patrón de
  vistas. Se parkea: queda como issue de entorno/browser, no del módulo.

## Act. 29 — Many2one en propiedad

- `property_type_id` a `estate.property.type` ("Tipo Propiedad"),
  `buyer_id` a `res.partner` ("Comprador"), `salesman_id` a `res.users`
  ("Vendedor", `copy=False`, `default=lambda self: self.env.user`).
- Lo aprendido: el Many2one guarda el id del relacionado y Odoo muestra su
  `display_name`; `default` con `env.user` deja al logueado como vendedor.
- ([7ee5da0](https://github.com/DanteZulli/unla-odoo-tps/commit/7ee5da0))

## Act. 30 — Formulario con relaciones

- `property_type_id` en el primer grupo sobre el código postal; nueva
  notebook "Más info." con Comprador y Vendedor.
- ([7ee5da0](https://github.com/DanteZulli/unla-odoo-tps/commit/7ee5da0))

## Act. 31 — Modelo `estate.property.tag`

- `models/estate_property_tag.py` con `name` requerido,
  `_description` "Etiqueta de propiedad"; se normalizó `_description` en
  los otros dos ("Propiedad", "Tipo de propiedad"). Sirve para el
  display name en errores y vistas genéricas.
- ([72f1897](https://github.com/DanteZulli/unla-odoo-tps/commit/72f1897))

## Act. 32 — Accesos sobre etiquetas

- Manager full, Vendedor lectura (mismo patrón tipos/ofertas).
- ([11a1728](https://github.com/DanteZulli/unla-odoo-tps/commit/11a1728))

## Act. 33 — Listas editables

- `views/estate_property_tag_views.xml`: acción "Etiquetas de propiedad"
  solo `list` + lista con `name` y `editable="top"` (alta rápida sin form).
- `editable="top"` también en la lista de tipos: crear tipos desde la
  lista sin formulario.
- ([84316a1](https://github.com/DanteZulli/unla-odoo-tps/commit/84316a1))

## Act. 34 — Menú de etiquetas

- Submenú "Etiquetas de propiedad" bajo Ajustes a la acción de etiquetas;
  xml de etiquetas antes del menú en el manifest.
- ([84316a1](https://github.com/DanteZulli/unla-odoo-tps/commit/84316a1))

## Act. 35 — `tag_ids` Many2many

- `tag_ids = fields.Many2many("estate.property.tag", string="Etiquetas")`
  en `estate.property`.
- ¿Por qué many2many y no many2one/one2many? Una propiedad lleva varias
  etiquetas y una etiqueta marca muchas propiedades (N a N). Con Many2one
  solo habría una etiqueta por propiedad; con One2many haría falta un FK
  inverso en la etiqueta apuntando a una sola propiedad. El M2M crea la
  tabla intermedia solo.
- ([e980901](https://github.com/DanteZulli/unla-odoo-tps/commit/e980901))

## Act. 36 — Etiquetas en vistas

- `tag_ids` debajo del `name` en el form y como columna en la lista, con
  `widget="many2many_tags"`. Sin widget se ve como lista cruda/cantidad;
  con widget, pills clickeables.
- ([e980901](https://github.com/DanteZulli/unla-odoo-tps/commit/e980901))

## Act. 37 — Modelo `estate.property.offer`

- `models/estate_property_offer.py` (`_description` "Oferta sobre propiedad"):
  `price` Float requerido, `status` Selection Aceptada/Rechazada,
  `partner_id` M2O a `res.partner` requerido, `property_id` M2O a
  `estate.property` requerido.
- ([3c613aa](https://github.com/DanteZulli/unla-odoo-tps/commit/3c613aa))

## Act. 38 — Accesos sobre ofertas

- Manager full, Vendedor lectura.
- ([75bdd64](https://github.com/DanteZulli/unla-odoo-tps/commit/75bdd64))

## Act. 39 — `offer_ids` One2many

- `offer_ids = fields.One2many("estate.property.offer", "property_id",
  string="Ofertas")` en propiedad.
- ¿Por qué el `inverse_name`? La One2many no tiene columna propia: lee las
  ofertas cuyo `property_id` apunta a esta propiedad; `inverse_name` dice
  cuál es ese FK. Es virtual: no crea columna, es la vista inversa del M2O.
- ([75bdd64](https://github.com/DanteZulli/unla-odoo-tps/commit/75bdd64))

## Act. 40 — Lista de ofertas sin acción

- `views/estate_property_offer_views.xml` con lista `editable="top"`
  (price, partner_id, status), sin `ir.actions.act_window` ni menú.
- ¿Por qué no hace falta acción? La lista solo se usa embebida dentro del
  form de propiedad (Act. 41); no hay entrada de menú propia. El menú de
  todas las ofertas recién llega en Unidad 2 Act. 12.
- ([ca377f0](https://github.com/DanteZulli/unla-odoo-tps/commit/ca377f0))

## Act. 41 — Página Ofertas

- Página "Ofertas" en el form de propiedad con `<field name="offer_ids" />`,
  que levanta la lista del Act. 40. Cierre de Unidad 1: modelo relacional
  completo tipo–propiedad–etiquetas–ofertas.
- ([ca377f0](https://github.com/DanteZulli/unla-odoo-tps/commit/ca377f0))
