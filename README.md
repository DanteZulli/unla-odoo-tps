# Trabajos prácticos — Programación de Sistemas ERP con Odoo

Repositorio de código de la materia **Programación de Sistemas (ERP con Odoo)**,
Licenciatura en Sistemas, UNLa. Cátedra: Gustavo Siciliano, Javier Vescio.
Guía de TPs + programa (v20250927b) en `docs/`.

Acá se trackea el desarrollo de los módulos de cada unidad y la evidencia de lo
probado en el entorno del alumno.

## Entorno utilizado

Odoo 19 sobre Doodba, que es la configuración pedida por la cátedra
("Odoo 18 o superior"):

- Doodba Copier Template: https://github.com/Tecnativa/doodba-copier-template
- Imagen base Doodba: https://github.com/Tecnativa/doodba

La guía referencia Odoo 18 (puertos `18xxx`); este entorno corre Odoo 19,
por lo que los puertos son `19xxx`: Odoo en `19069`, pgweb en `19081`,
MailHog en `19025` y wdb en `19984`.

## Cómo se vincula este repo con Odoo

Los módulos viven en `addons/` de este repo y se exponen al Odoo local
mediante enlaces simbólicos en la carpeta `private` del proyecto Doodba:

```
unla-odoo-tps/addons/<modulo>
  └─ symlink ─> odoo19-doodba/odoo/custom/src/private/<modulo>
```

Doodba detecta automáticamente los addons de `private`, así que todo lo que
se desarrolla acá se instala y prueba en el Odoo local sin duplicar código.
El proyecto Doodba local (`odoo19-doodba`) no se versiona acá: es solo el
entorno de ejecución.

## Contenido

- `docs/` — guía de TPs, programa y evidencia (`docs/evidencia/`) con
  capturas de lo probado en el entorno.
- `addons/real_estate` — Unidad 1: inmobiliaria (modelos, vistas, menús,
  seguridad, relaciones).
- `addons/estate_account` — Unidad 2: facturación de ventas de propiedades
  (hereda de `real_estate` y `account`).
