# Unidad 1 — Registro de avance (Acts. 1–16)

Módulo `real_estate`: modelos, vistas, menús y seguridad. Entorno Odoo 19
sobre Doodba (la guía pide 18; puertos `19xxx`).

- Act. 1: entorno levantado y verificado — 7 contenedores en `Up`, login
  `admin/admin` en `:19069`. Odoo `19069`, pgweb `19081`, MailHog `19025`.
- Act. 2: esqueleto `real_estate` + symlink en `private/` e instalación. El
  scaffold trae de más (`controllers`, `demo`, vistas, csv huérfano) y rompe
  el install: se recorta a `__init__.py` + `__manifest__.py`. ([a6408dd](https://github.com/DanteZulli/unla-odoo-tps/commit/a6408dd6c0c9bdf60e6883385a951fa6a5fed9c7))
- Act. 3: modelo `estate.property` con los 13 campos de la guía. No hay
  generador: se escribe a mano con el ORM y se cablea en `models/__init__.py`. ([242bd4b](https://github.com/DanteZulli/unla-odoo-tps/commit/242bd4b5193ecf45824ac308caa20efde1803d88))
- Act. 4: pgweb confirma la tabla `estate_property`; Odoo agrega `id`,
  `create_date`/`create_uid`, `write_date`/`write_uid` (los "mágicos").
- Act. 5: acción `ir.actions.act_window` "Propiedades" (`list,form`). Sin
  vistas propias, Odoo usa las genéricas. ([c75c725](https://github.com/DanteZulli/unla-odoo-tps/commit/c75c72517d1514505ff1f1bd7c476109f4dac43f))
- Act. 6: menús `Inmobiliaria → Anuncios → Propiedades`. El orden en `data`
  importa: la acción debe definirse antes que el menú que la referencia. ([4ced331](https://github.com/DanteZulli/unla-odoo-tps/commit/4ced3312e0d26b43100c0080b8dc1ea3216c71d5))
- Act. 7: sin accesos los menús no se ven; se verifican con debug
  (`?debug=1`, icono bug) + *Become Superuser* (salir = logout).
- Act. 8: solo `list` no abre formulario, solo `form` no lista; se deja
  `list,form`.
- Act. 9: tipos Interno (`base.group_user`), Portal, Público, más Superuser
  (`__system__`, saltea todos los accesos).
- Act. 10: `ir.model.access.csv` con solo lectura para `base.group_user`
  (= usuario interno); el csv va primero en `data`. ([db60dc8](https://github.com/DanteZulli/unla-odoo-tps/commit/db60dc8cd0fcbefb0468c71067a72e11d48dbb16))
- Act. 11: grupo "Manager de Propiedades" por UI con las 4 tildes + prueba
  de crear/modificar/eliminar. Rápido para prototipar, pero no se versiona.
- Act. 12: grupo Manager formalizado en `security/real_estate_res_groups.xml`.
  UI vs módulo: rápido y efímero vs versionado y desplegable. ([dd5b9f0](https://github.com/DanteZulli/unla-odoo-tps/commit/dd5b9f0727a2a0819cb90bec14d8b1c9d667aeba))
- Act. 13: grupo "Vendedor de Propiedades" en el mismo xml. ([dd5b9f0](https://github.com/DanteZulli/unla-odoo-tps/commit/dd5b9f0727a2a0819cb90bec14d8b1c9d667aeba))
- Act. 14: Manager full (`1,1,1,1`) y Vendedor solo lectura; se elimina la
  línea de `base.group_user`. ([652c27c](https://github.com/DanteZulli/unla-odoo-tps/commit/652c27c714bd9bc740532383e352f39d81cb5194))
- Act. 15: usuario sin grupos = denegado total (`AccessError`, menús ocultos),
  verificado con usuario de prueba.
- Act. 16: categoría `Inmobiliaria` (`ir.module.category`) con ambos grupos
  para ubicarlos juntos. ([1bcd20e](https://github.com/DanteZulli/unla-odoo-tps/commit/1bcd20ed8e09e8c25da088a3fbf5f30ee51c9af9))
