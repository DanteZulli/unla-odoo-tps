# Unidad 1 — Registro de avance (Acts. 1–16)

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

- Categoría `Inmobiliaria` (`ir.module.category`) referenciada por
  `category_id` en ambos grupos: quedan agrupados en la vista de grupos.
- ([1bcd20e](https://github.com/DanteZulli/unla-odoo-tps/commit/1bcd20ed8e09e8c25da088a3fbf5f30ee51c9af9))
