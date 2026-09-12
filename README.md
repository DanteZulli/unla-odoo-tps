# UNLa · Lic. en Sistemas · Programación de Sistemas ERP con Odoo

Trabajos prácticos de la materia (guía v20250927b en `docs/`).

## Estructura

- `docs/` — guía de TPs + programa de la materia.
- `addons/` — módulos propios (`real_estate`, `estate_account`, ...).

Los módulos viven acá y se linkean en el entorno Doodba:

```
~/Repositories/unla-odoo-tps/addons/<modulo>
  -> symlink -> ~/Repositories/odoo19-doodba/odoo/custom/src/private/<modulo>
```

## Entorno

Odoo 19 (vale por "18 o superior") con Doodba en `../odoo19-doodba`.

- Odoo: http://localhost:19069 (usuario `admin`, clave `admin`, DB `devel`)
- Pgweb: http://localhost:19081 · MailHog: http://localhost:19025 · wdb: http://localhost:19984

La guía menciona puertos `18xxx` (Odoo 18); acá es `19xxx` (Odoo 19).

## Flujo de trabajo

```bash
cd ../odoo19-doodba
just run                        # levantar entorno
just scaffold <modulo> --path /tmp/scaff   # o crear directo en addons/
# mover el módulo a ../unla-erp-tps/addons/ y symblinkearlo en private/
just install <modulo>           # instalar/actualizar en DB devel
just test <modulo>              # correr sus tests
just logs odoo                  # ver logs
```

## Unidades

- **U1**: módulo `real_estate` (modelos, vistas, menús, seguridad, relaciones).
- **U2**: computados, onchange, ORM, constraints, herencia, `estate_account`.
- **U3**: wizards, QWeb/reportes, cron, MailHog, pytest, traducciones.
