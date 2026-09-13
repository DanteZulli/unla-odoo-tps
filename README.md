# Trabajos prácticos — Programación de Sistemas ERP con Odoo

Repositorio de código de la materia **Programación de Sistemas (ERP con Odoo)**,
Licenciatura en Sistemas, UNLa. Cátedra: Gustavo Siciliano, Javier Vescio.
Guía de TPs + programa (v20250927b) en `docs/`.

## Entorno utilizado

Odoo 19 sobre Doodba:

- Doodba Copier Template: https://github.com/Tecnativa/doodba-copier-template
- Imagen base Doodba: https://github.com/Tecnativa/doodba

La guía referencia Odoo 18 (puertos `18xxx`); este entorno corre Odoo 19,
por lo que los puertos son `19xxx`: Odoo en `19069`, pgweb en `19081`,
MailHog en `19025` y wdb en `19984`.

## Cómo se vincula este repo con mi instancia de Odoo

Los módulos viven en `addons/` de este repo y se exponen al Odoo local
mediante enlaces simbólicos en la carpeta `private` del proyecto Doodba:

```
unla-odoo-tps/addons/<modulo>
  └─ symlink ─> odoo19-doodba/odoo/custom/src/private/<modulo>
```

Doodba detecta automáticamente los addons de `private`, así que todo lo que
se desarrolla acá se instala y prueba en el Odoo local sin duplicar código,
mientras desarrollo. El proyecto Doodba local (`odoo19-doodba`) no se
versiona acá: es solo mi entorno de ejecución.

## Cómo cargar estos módulos en tu propio Doodba

Vale para cualquier proyecto generado con el Doodba Copier Template en una
versión de Odoo compatible con los módulos (19.x). Copiá cada carpeta de
`addons/` dentro de `odoo/custom/src/private/`:

```bash
cp -r addons/real_estate addons/estate_account <tu-doodba>/odoo/custom/src/private/
```

Después, en tu Doodba: Apps → Update Apps List, e instalá `real_estate`
(o por consola con `addons init -w real_estate`). `estate_account`
requiere tener instalados `real_estate` y `account`.

## Contenido

- `docs/` — guía de TPs, programa y evidencia (`docs/evidencia/`) con
  capturas de lo probado en el entorno.
- `addons/real_estate` — Unidad 1: inmobiliaria (modelos, vistas, menús,
  seguridad, relaciones).
- `addons/estate_account` — Unidad 2: facturación de ventas de propiedades
  (hereda de `real_estate` y `account`).

## Registro de avance — Unidad 1 (Acts. 1–16)

- Act. 1: entorno Odoo 19 levantado (`:19069`, login `admin/admin` OK).
- Act. 2: esqueleto `real_estate` (`__init__.py` + `__manifest__.py`) + symlink en `private/` e instalación. ([a6408dd](https://github.com/DanteZulli/unla-odoo-tps/commit/a6408dd6c0c9bdf60e6883385a951fa6a5fed9c7))
- Act. 3: modelo `estate.property` con los 13 campos de la guía. ([242bd4b](https://github.com/DanteZulli/unla-odoo-tps/commit/242bd4b5193ecf45824ac308caa20efde1803d88))
- Act. 4: en pgweb la tabla trae además `id`, `create_date`, `create_uid`, `write_date`, `write_uid`.
- Act. 5: acción `ir.actions.act_window` "Propiedades" (`list,form`). ([c75c725](https://github.com/DanteZulli/unla-odoo-tps/commit/c75c72517d1514505ff1f1bd7c476109f4dac43f))
- Act. 6: menús `Inmobiliaria → Anuncios → Propiedades`; el menú va después de la acción en el manifest o falla. ([4ced331](https://github.com/DanteZulli/unla-odoo-tps/commit/4ced3312e0d26b43100c0080b8dc1ea3216c71d5))
- Act. 7: sin accesos los menús no se ven; se verifican con debug + superuser (salir = logout).
- Act. 8: solo `list` no abre formulario, solo `form` no lista; queda `list,form`.
- Act. 9: tipos Interno (`base.group_user`), Portal, Público, más Superuser.
- Act. 10: `ir.model.access.csv` con solo lectura para `base.group_user` (usuario interno). ([db60dc8](https://github.com/DanteZulli/unla-odoo-tps/commit/db60dc8cd0fcbefb0468c71067a72e11d48dbb16))
- Act. 11: grupo "Manager de Propiedades" por UI con lectura/creación/escritura/borrado + prueba CRUD.
- Acts. 12–13: grupos Manager y Vendedor formalizados en `security/real_estate_res_groups.xml` (UI = prototipo no versionado). ([dd5b9f0](https://github.com/DanteZulli/unla-odoo-tps/commit/dd5b9f0727a2a0819cb90bec14d8b1c9d667aeba))
- Act. 14: Manager full + Vendedor solo lectura; sale `base.group_user`. ([652c27c](https://github.com/DanteZulli/unla-odoo-tps/commit/652c27c714bd9bc740532383e352f39d81cb5194))
- Act. 15: sin ningún grupo → denegado total (`AccessError`, menús ocultos).
- Act. 16: categoría `Inmobiliaria` (`ir.module.category`) con ambos grupos. ([1bcd20e](https://github.com/DanteZulli/unla-odoo-tps/commit/1bcd20ed8e09e8c25da088a3fbf5f30ee51c9af9))
