# Resumen de teoría — Programación de Sistemas ERP con Odoo

**Alcance:** contenido hasta la Guía 2 (Unidad 1, Unidad 2, Material Teórico y Programa).
La Unidad 3 (asistentes/wizards, QWeb, reportes, cron, MailHog, pytest, traducciones) queda
**fuera del examen**.

**Formato de examen:** multiple choice, marcar la **única** opción correcta. Puede venir teoría
pura o ejemplos de los prácticos (mismo formato).

> **Nota de versión:** la guía está armada sobre **Odoo 18** (puertos `18xxx`). Tu entorno local
> corre **Odoo 19** (puertos `19xxx`), por eso hay un par de diferencias señaladas con el sello
> **⚠ Odoo 19**. En el examen, respondé pensando en **Odoo 18**.

---

## Índice de temas

1. [ERP y Odoo: fundamentos](#tema-1--erp-y-odoo-fundamentos)
2. [Anatomía de un módulo y estructura de carpetas](#tema-2--anatomía-de-un-módulo-y-estructura-de-carpetas)
3. [Entorno de desarrollo: Doodba, pgweb, wdb, debug](#tema-3--entorno-de-desarrollo-doodba-pgweb-wdb-debug)
4. [Modelos y campos](#tema-4--modelos-y-campos)
5. [Seguridad: usuarios, grupos y reglas de acceso](#tema-5--seguridad-usuarios-grupos-y-reglas-de-acceso)
6. [Relaciones: Many2one, One2many, Many2many](#tema-6--relaciones-many2one-one2many-many2many)
7. [Vistas, acciones y menús](#tema-7--vistas-acciones-y-menús)
8. [Campos computados, related, depends, inverse, store](#tema-8--campos-computados-related-depends-inverse-store)
9. [onchange y validaciones](#tema-9--onchange-y-validaciones)
10. [ORM y CRUD](#tema-10--orm-y-crud)
11. [Comandos relacionales](#tema-11--comandos-relacionales)
12. [Constraints](#tema-12--constraints)
13. [Herencia (modelos, métodos, vistas, módulos)](#tema-13--herencia-modelos-métodos-vistas-módulos)
14. [Lógica de negocio: botones, UserError, ondelete, create](#tema-14--lógica-de-negocio-botones-usererror-ondelete-create)
15. [Respuestas a los "¿por qué?" de la guía](#tema-15--respuestas-a-los-por-qué-de-la-guía)
16. [Trampas típicas de multiple choice](#tema-16--trampas-típicas-de-multiple-choice)
17. [Simulacro: 25 preguntas tipo examen con respuestas](#tema-17--simulacro-25-preguntas-tipo-examen-con-respuestas)
18. [Simulacro de código: snippets y qué pasa](#tema-18--simulacro-de-código-snippets-y-qué-pasa)
19. [Checklist final](#tema-19--checklist-final)
20. [Anexo — Hoja de ruta: repaso de 1 página](#anexo--hoja-de-ruta-repaso-de-1-página)

---

## Tema 1 — ERP y Odoo: fundamentos

### ¿Qué es un ERP?

- **ERP** = *Enterprise Resource Planning* (Sistema de Planificación de Recursos empresariales).
- Es un sistema que gestiona **todas las áreas de la empresa de forma integral**.
- **Información centralizada en una única base de datos**: no hay islas de información.
- Las aplicaciones **no funcionan aisladas, se comunican entre sí**: al registrar una venta en
  Ventas, Odoo puede actualizar el inventario y generar la factura en Contabilidad
  automáticamente. Esa integración es la diferencia clave frente a tener sistemas separados.
- Eslogan de Odoo: *"todo tu negocio en una sola plataforma"*.

### ¿Qué es Odoo?

- ERP de **código abierto** (open source), escrito principalmente en **Python** → curva de
  aprendizaje razonable para desarrollar.
- Se puede desplegar en la **nube** o en **servidores propios** (on-premise).
- **Una versión mayor por año**, con mejoras de usabilidad, apps y procesos.
- Enfoque en **PyMEs**, a diferencia de **SAP**, que se usa en grandes corporaciones con
  necesidades complejas.
- **Altamente configurable**: se pueden modificar procesos funcionales fácilmente.
- **Modular y extensible**: apps desde el App Store de Odoo, apps de terceros o desarrollo
  propio; miles de apps de la comunidad + de la empresa creadora.

### Community vs Enterprise

| | Community | Enterprise |
|---|---|---|
| Costo | Gratuito | Licencia de pago (suscripción) |
| Código | Abierto | Propietario sobre la base Community |
| Contenido | Módulos core (Ventas, Compras, Contabilidad, Inventario, ...) | + apps extra (Studio, reportes avanzados, IoT, ...) y hosting Odoo.sh |
| Soporte | Comunidad | Soporte oficial |

> La materia trabaja sobre la versión **Community**.

### Tecnologías de Odoo (para preguntas "¿con qué está hecho?")

- **Python** (lenguaje principal), **PostgreSQL** (base de datos), **XML** (vistas/acciones/menús),
  **JS/OWL** (frontend), **QWeb** (motor de plantillas para reportes/web), **Docker** (entornos
  con Doodba).
- La materia: enseña **personalización y desarrollo de módulos** sobre Odoo, complementando
  bases de datos, POO y sistemas/organizaciones de la carrera.
- Objetivo del curso: decidir **configuración vs desarrollo**, modelar con el **ORM**,
  implementar **vistas, lógica y reportes**, y levantar Odoo con **Doodba** en contenedores.

---

## Tema 2 — Anatomía de un módulo y estructura de carpetas

### La pieza básica: el módulo

Odoo es **modular**: toda funcionalidad (una app o un feature) vive en un módulo. Un módulo
custom mínimo necesita **dos archivos raíz**:

- `__init__.py`: hace los imports de Python del paquete (para un módulo simple puede estar
  vacío; si hay `models/`, debe hacer `from . import models`).
- `__manifest__.py`: diccionario con los **metadatos** del módulo.

### Estructura de carpetas de un módulo completo

```
real_estate/
├── __init__.py              # import de subpaquetes: from . import models
├── __manifest__.py          # metadatos: name, depends, data, license...
├── models/                  # modelos (clases Python que definen tablas)
│   ├── __init__.py          # from . import estate_property, estate_property_offer, ...
│   ├── estate_property.py
│   └── ...
├── views/                   # XML: vistas (list/form/search), acciones y menús
│   ├── estate_property_views.xml
│   └── real_estate_menuitem.xml
├── security/                # grupos (res.groups) y reglas de acceso (ACL)
│   ├── real_estate_res_groups.xml
│   └── ir.model.access.csv
├── data/                    # datos que se cargan al instalar (plantillas, cron...)
├── demo/                    # datos de demostración (solo si se instala con demo)
├── reports/                 # reportes (QWeb)      [se usa en Unidad 3]
├── wizard/                  # asistentes/wizards   [se usa en Unidad 3]
├── static/                  # imágenes, CSS, JS (web assets)
└── i18n/                    # traducciones (.po/.pot) [se usa en Unidad 3]
```

**Preguntas típicas de examen:**

- ¿Dónde van los modelos? → `models/`, e **incluyendo el archivo en `models/__init__.py`**
  y ese paquete en el `__init__.py` del módulo. Si olvidás el import, Python no llega a
  definir la clase y el modelo **no existe**.
- ¿Dónde van las vistas? → `views/`. ¿La seguridad? → `security/`.
- ¿Qué pasa si creo `estate_property.py` pero no lo importo? → el modelo no se registra en
  Odoo (pgweb no lo muestra).

### El `__manifest__.py`

```python
{
    "name": "Real Estate",
    "summary": "Real estate ads",
    "author": "UNLa",
    "category": "Uncategorized",
    "version": "1.0",
    "depends": ["base"],                 # módulos de los que depende
    "data": [                            # XML/CSV cargados al instalar/actualizar
        "security/real_estate_res_groups.xml",
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/real_estate_menuitem.xml",   # SIEMPRE al final
    ],
    "demo": [],
    "license": "LGPL-3",
    "installable": True,
    "application": True,
}
```

Claves importantes:

- **`depends`**: lista de módulos que deben estar instalados antes. Si dependés de `account`
  y de `real_estate`, poner ambos; Odoo instala las dependencias solo. Ej.: `estate_account`
  depende de `["real_estate", "account"]`.
- **`data`**: archivos que Odoo carga **en orden** al instalar o **actualizar** (`-u`).
  - ⚠ **El orden importa**: si `real_estate_menuitem.xml` referencia por `ref` una acción
    definida en `estate_property_views.xml`, el menú debe venir **después** en la lista;
    al revés, Odoo falla con *"External ID not found"* (no existe el XML ID de la acción).
  - Seguridad primero: los grupos (XML) **antes** que `ir.model.access.csv`, porque el CSV
    referencia los XML ID de los grupos.
- **`demo`**: datos de prueba, solo se cargan si se instala con datos de demostración.
- **`application=True`**: aparece como app en el menú de aplicaciones (no es lo mismo que
  `installable`, que solo dice que se puede instalar).
- **`license`**: LGPL-3 (Community).

### Actualizar vs instalar

- **Instalar**: crea el módulo, carga todo, ejecuta su lógica inicial.
- **Actualizar** (`-u módulo` o botón *"Actualizar módulo"* en Apps): **relee `data`** y
  actualiza vistas/registros XML. Los cambios en **modelos** (nuevos campos) requieren
  actualizar módulo; los cambios en XML también. Si no ves cambios de menús/vistas:
  actualizá desde Odoo y, en último caso, borrá la caché del navegador.

### XML ID (identificador externo)

Cada registro creado desde XML tiene un **XML ID** con forma `modulo.prefijo_nombre`
(por ejemplo `real_estate.action_estate_property`). Con `ref="..."` se referencian otros
registros. Odoo genera automáticamente, para cada modelo, el XML ID `model_<nombre_con_guiones_bajos>`
(p. ej. `model_estate_property`), que es el que se usa en `ir.model.access.csv`.

---

## Tema 3 — Entorno de desarrollo: Doodba, pgweb, wdb, debug

### Doodba

- **Doodba Copier Template** (de Tecnativa): plantilla basada en **Copier** para levantar
  entornos de Odoo en **contenedores Docker** con buenas prácticas (estructura, backups,
  herramientas de desarrollo).
- El objetivo de la materia: *"tener una instancia Odoo en cualquier versión con contenedores
  Docker usando Doodba"*.
- Trae incluidas herramientas: **pgweb**, **wdb**, **MailHog** (Unidad 3).

### Puertos (guía = Odoo 18, `18xxx`; tu entorno = Odoo 19, `19xxx`)

| Servicio | Guía (Odoo 18) | Tu entorno (Odoo 19) |
|---|---|---|
| Odoo (web) | 18069 | 19069 |
| pgweb | 18081 | 19081 |
| wdb (depurador) | 18984 | 19984 |
| MailHog | 18025 | 19025 |

### pgweb

- Interfaz web para navegar la **base de datos PostgreSQL** (ver tablas, filas, correr SQL).
- Uso en la materia: **verificar si un campo existe como columna en la tabla**.
  - Ejemplo clave: un campo computado **sin `store=True` NO aparece en la tabla** en pgweb,
    pero **sí se ve en la vista formulario** (se calcula en memoria al renderizar).
  - Con `store=True`, la columna **sí existe**.
- También sirve para ver los **campos automáticos** que Odoo agrega a toda tabla
  (`id`, `create_uid`, `create_date`, `write_uid`, `write_date`).

### wdb — depuración

- Depurador interactivo que trae Doodba (interfaz web en el puerto `18984`/`19984`).
- Uso: en un método (p. ej. un `@api.onchange`) poner:

```python
import wdb
wdb.set_trace()
```

- Al ejecutarse ese método, la ejecución **se interrumpe** en el `set_trace()`, entrás a wdb,
  hacés clic en el **hash de la sesión** y podés: ver el código, inspeccionar/modificar
  variables y hasta usar funciones del ORM en la consola.

### Modo debug y SuperUsuario

- **Modo debug** (developer mode): muestra menús técnicos (modelos, vistas, campos, XML ID,
  estructura de datos...). Se activa desde Configuración → Activar modo desarrollador.
- **SuperUsuario** (admin): usuario **dueño de la base (id=1)** que **ignora las reglas de
  acceso**: ve y hace todo. Sirve para probar sin depender de ACLs.
  - Para **salir** del modo SuperUsuario: **cerrar sesión y volver a identificarte**
    (la guía lo aclara expresamente).
- ⚠ Los permisos de SuperUsuario enmascaran errores de seguridad: si algo "no se ve",
  conviene primero preguntar *"¿será que no tengo permisos?"* antes de asumir bug.

---

## Tema 4 — Modelos y campos

### Definir un modelo

```python
from odoo import api, fields, models

class EstateProperty(models.Model):
    _name = "estate.property"          # nombre técnico = tabla en PostgreSQL
    _description = "Propiedad"         # descripción humana (recomendada siempre)
```

- `_name` con **puntos**; la tabla en BD se llama igual con **guiones bajos**
  (`estate.property` → tabla `estate_property`).
- `_description` es recomendable: lo usan UI, logs y avisos de Odoo ("Fields `...` have no
  patch description"). La guía lo pide explícitamente para los 4 modelos.
- Atributos de clase menos usados pero posibles: `_order` (orden por defecto), `_rec_name`
  (campo que Odoo muestra como nombre/display_name).

### Tipos de campos (guía de elección)

| Tipo | Uso | Ejemplo |
|---|---|---|
| `Char` | texto corto (una línea) | `name`, `postcode` |
| `Text` | texto largo (varias líneas) | `description` |
| `Integer` | entero | `bedrooms`, `living_area` |
| `Float` | decimal | `expected_price`, `selling_price` |
| `Monetary` | dinero con moneda (requiere `currency_field`) | (no usado en la guía) |
| `Boolean` | sí/no | `garage`, `garden` |
| `Date` | fecha | `date_availability` |
| `Datetime` | fecha y hora | `create_date` |
| `Selection` | conjunto fijo de opciones (clave → etiqueta) | `garden_orientation`, `state`, `status` |
| `Binary` | archivos | adjuntos |
| `Many2one` | muchos de este modelo → uno de otro | `buyer_id`, `salesman_id` |
| `One2many` | uno de este modelo → muchos de otro | `offer_ids` |
| `Many2many` | muchos ↔ muchos | `tag_ids` |

### Atributos comunes de un campo

```python
name = fields.Char(string="Título", required=True)
bedrooms = fields.Integer(string="Habitaciones", default=2)
date_availability = fields.Date(
    string="Fecha disponibilidad",
    copy=False,
    default=lambda self: fields.Date.add(fields.Date.today(), months=3),
)
```

- **`string`**: etiqueta visible en la UI.
- **`required=True`**: obligatorio en UI **y** genera `NOT NULL` en la tabla.
- **`default`**: valor inicial. Puede ser literal (`default=2`, `default="north"`) o
  **función/lambdas** `lambda self: ...` (se evalúa con el `self`/env actual → para el
  usuario logueado: `default=lambda self: self.env.user`; para fecha+3 meses:
  `fields.Date.add(fields.Date.today(), months=3)`).
- **`copy=False`**: el campo **NO se copia al duplicar** (Acción → Duplicar).
  - La guía lo usa en `date_availability`, `selling_price`, `state` y `salesman_id`:
    un duplicado no debe heredar precio de venta, estado ni vendedor.
  - Los campos computados **no almacenados** tampoco se copian (no tienen valor propio).
- **`readonly=True`**: solo lectura (además de los que lo son por naturaleza).
- **`help`**: tooltip; **`index=True`**: índice en BD (búsquedas más rápidas).
- **`selection=[('clave', 'Etiqueta'), ...]`**: las claves ('north') son lo que se guarda en
  BD; las etiquetas ('Norte') se muestran.

### Campo `state` (caso especial)

- **`state` es un campo "reservado"/convencional** de tipo Selection en Odoo: por convención
  representa el flujo del registro y se muestra con **`widget="statusbar"`** en el header.
- La guía lo pide con: requerido, `default="new"` y `copy=False`, con opciones
  Nuevo / Oferta recibida / Oferta aceptada / Vendido / Cancelado.

### Campos automáticos (lo que "aparece solo" en pgweb)

Además de tus campos, Odoo crea en **toda** tabla:

- `id` (clave primaria),
- `create_uid`, `create_date` (quién y cuándo creó),
- `write_uid`, `write_date` (quién y cuándo modificó por última vez),
- más `display_name` (calculado, en general el `name`).

Esto responde al ejercicio 4 de la Unidad 1: esos son los campos adicionales que vas a ver.

### Convenciones de nombres (importante para MC)

- Many2one → sufijo **`_id`** (`buyer_id`).
- One2many y Many2many → sufijo **`_ids`** (`offer_ids`, `tag_ids`).
- Métodos de cómputo → prefijo **`_compute_*`** (`_compute_total_area`) — buena práctica
  pedida por la guía.
- Nombres técnicos en inglés snake_case; `string` en español (el idioma de la etiqueta).

---

## Tema 5 — Seguridad: usuarios, grupos y reglas de acceso

### ¿Qué tipos de usuario existen en Odoo?

Tres tipos, según cómo entran y qué alcance tienen:

| Tipo | Grupo | Quién es |
|---|---|---|
| **Usuario interno** (backend) | `base.group_user` | Empleados que usan la interfaz de Odoo con permisos por grupo. **`base.group_user` = usuario interno** (la respuesta esperada en la guía, ejercicio 9/10) |
| **Portal** | `base.group_portal` | Usuarios externos (clientes/proveedores) con acceso limitado vía enlaces (portal de facturas, pedidos...) |
| **Público** | `base.group_public` | Visitantes sin login (web pública) |

Además: **SuperUsuario/admin** = el dueño de la base (id=1), ignora ACLs; y hay otros grupos
funcionales (Contabilidad, Ventas...) que combinan permisos.

### Grupos (`res.groups`)

- Un **grupo** agrupa permisos (ACLs, reglas de registro, visibilidad de menús/campos).
- Se pueden crear **desde Odoo** (Ajustes → Usuarios → Grupos → Nuevo) o **desde el módulo**
  (XML en `security/`):

```xml
<record id="group_estate_salesman" model="res.groups">
    <field name="name">Vendedor de Propiedades</field>
    <field name="category_id" ref="module_category_real_estate"/>
</record>
<record id="group_estate_manager" model="res.groups">
    <field name="name">Manager de Propiedades</field>
    <field name="category_id" ref="module_category_real_estate"/>
</record>
```

- **⚠ Odoo 19:** tu repo usa `privilege_id` + modelo `res.groups.privilege`. En **Odoo 18
  (examen)** el campo es **`category_id`** apuntando a `ir.module.category`. Aprendete la
  forma de Odoo 18 para el examen y la de tu entorno para codear.
- **`implied_ids`** (grupo implícito): si el Manager *implica* al Vendedor, todo Manager es
  automáticamente también Vendedor (`eval="[(4, ref('group_estate_salesman'))]"`).

**¿Ventajas/desventajas de crear el grupo desde Odoo vs desde el módulo?**

| Desde Odoo (UI) | Desde el módulo (XML) |
|---|---|
| Rápido, inmediato, bueno para probar | **Reproducible y versionable** (git) |
| Se pierde al reinstalar/recrear la BD | Se carga automáticamente al instalar/actualizar el módulo |
| No se lleva a otros entornos (dev/prod) | Mismo resultado en cualquier entorno |
| Cambios "sucios" no rastreables | Requiere actualizar el módulo; IDs fijos |

→ Lo correcto para producción es **formalizar desde el módulo** (así lo hizo la guía en el
ejercicio 12).

### Categorías de grupo (`ir.module.category`)

- Sirven para **agrupar los grupos del módulo** en la vista de Grupos, para que no se
  "pierdan" entre los grupos nativos.
- Ej.: categoría **"Inmobiliaria"** → buscándola en la vista de grupos aparecen
  "Vendedor de Propiedades" y "Manager de Propiedades".
- En la UI, la categoría es el desplegable "Aplicación" del formulario de grupo.

### ACL: `ir.model.access.csv`

Archivo en `security/`, **incluido en el manifest**, con columnas:

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_estate_property_manager,estate.property.manager,model_estate_property,real_estate.group_estate_manager,1,1,1,1
access_estate_property_salesman,estate.property.salesman,model_estate_property,real_estate.group_estate_salesman,1,0,0,0
```

- `model_id:id` → XML ID del modelo: **`model_` + nombre del modelo con `_`** en vez de `.`
  (`estate.property` → `model_estate_property`). Se genera solo.
- `group_id:id` → a qué grupo aplican estos permisos (XML ID del grupo, con o sin prefijo
  del módulo).
- `perm_read / perm_write / perm_create / perm_unlink` → `1` o `0` (CRUD: R-U-C-D).
- **Reglas por fila, permisos en acumulativo**: un usuario puede tener varias filas
  (por varios grupos) y se **suma** lo permitido.

**Casos típicos de examen:**

1. *¿A qué tipo de usuario representa `base.group_user`?* → **Usuario interno** (empleado).
2. *¿Cómo le das crear/modificar/eliminar además de leer?* → cambiar los `0` por `1` en las
   columnas `perm_write`, `perm_create`, `perm_unlink` de su fila (o agregar filas nuevas).
3. *¿Qué pasa si un usuario NO pertenece ni al grupo Vendedor ni al Manager?* → **no tiene
   ningún permiso sobre `estate.property`**: al intentar leer Odoo lanza **AccessError**
   ("no tienes permisos de acceso"), no ve ni puede usar los menús/acciones de ese modelo.
4. *¿Y si la fila del CSV queda **sin `group_id`**?* → los permisos aplican a **TODOS** los
   usuarios (incluidos portal/público). ¡Peligro típico!
5. *La guía pide "solo lectura" para Vendedor en tipos/etiquetas/ofertas* → fila con
   `perm_read=1` y el resto `0`.

### Otras capas de seguridad (para no confundir)

- **ACL (`ir.model.access.csv`)**: permisos por **modelo** (¿puede leer/escribir `estate.property`?).
- **Reglas de registro (`ir.rule`)**: filas visibles dentro del modelo (dominio por usuario/
  compañía). *No aparece en los prácticos de esta guía, pero puede salir como distractor.*
- **Visibilidad en vistas**: atributo `groups="real_estate.group_estate_manager"` sobre
  menús, botones o campos → **oculta** el elemento a quien no está en el grupo (es UX, no
  reemplaza la validación en backend).

---

## Tema 6 — Relaciones: Many2one, One2many, Many2many

### Many2one (muchos de este modelo → uno de otro)

```python
buyer_id = fields.Many2one(comodel_name="res.partner", string="Comprador")
salesman_id = fields.Many2one(
    comodel_name="res.users", string="Vendedor",
    copy=False, default=lambda self: self.env.user,
)
property_type_id = fields.Many2one(
    comodel_name="estate.property.type", string="Tipo Propiedad",
)
```

- Guarda **la foreign key** en **esta** tabla (columna `salesman_id` → `res_users.id`).
- **`comodel_name`**: modelo destino. Nombre en BD del campo = nombre del campo.
- Es **la relación "por defecto"** cuando cada registro apunta a **un solo** registro del
  otro modelo.
- Casos de la guía: tipo de propiedad (uno), comprador (uno), vendedor (uno, el usuario
  logueado).

### One2many (uno de este modelo → muchos de otro)

```python
offer_ids = fields.One2many(
    comodel_name="estate.property.offer",
    inverse_name="property_id",
    string="Ofertas",
)
```

- **No existe columna propia**: es **virtual**. Odoo la resuelve buscando en el modelo hijo
  todos los registros cuyo Many2one `property_id` apunte a este registro.
- Por eso hay que pasar **`inverse_name`**: es el nombre del campo **Many2one** del modelo
  hijo que "vuelve" hacia acá. Sin él Odoo no sabe qué campo filtrar.
- La información "vive" en la tabla del hijo (`estate_property_offer.property_id`).
- Forma abreviada (lo pide la guía): `fields.One2many("estate.property.offer", "property_id", string="Ofertas")`.
  (La guía escribe `estate_property_offer`; el valor correcto es con **puntos**.)

**¿Por qué la One2many es virtual?** → porque solo es "la vista inversa" del Many2one
hijo→padre; no agrega tabla ni columna. Consecuencia práctica: **no podés asignarla con
`create()`/`write()` un registro directamente "creando hijos" sin pasar por comandos
relacionales** y conviene mostrarla en el formulario como lista embebida.

### Many2many (muchos ↔ muchos)

```python
tag_ids = fields.Many2many(comodel_name="estate.property.tag", string="Etiquetas")
```

- **Tabla intermedia** (relación) generada por Odoo: guarda pares `(propiedad, etiqueta)`.
- **Ambos lados pueden tener muchos**: una propiedad tiene muchas etiquetas y una etiqueta
  puede estar en muchas propiedades.

**¿Por qué `tag_ids` es Many2many y no Many2one ni One2many?** (pregunta fija de examen)

- **Many2one no sirve**: solo permitiría **una etiqueta por propiedad** (necesitamos muchas).
- **One2many no sirve** (desde `estate.property`): implicaría que la FK está en el lado de la
  etiqueta, o sea que **cada etiqueta pertenece a una sola propiedad** (imposible: "luminosa"
  debe poder usarse en varias propiedades). Además habría que poner el campo en `tag`.
- **Many2many** modela exactamente la relación **N:N** de la realidad.

### Resumen de elección (tabla para el examen)

| Situación | Relación | Se guarda en... |
|---|---|---|
| Cada registro apunta a **1** de otro modelo | Many2one | columna FK en **esta** tabla |
| Un registro tiene **muchos** de otro modelo y la FK va en el hijo | One2many | en la tabla del **hijo** (vista inversa de un m2o) |
| **Muchos ↔ muchos** | Many2many | **tabla intermedia** |

- Caso de la guía: ofertas → `estate.property` tiene `offer_ids` (One2many inverso de
  `property_id`, que es Many2one). Es el dúo clásico: **el mismo par de campos se declara
  m2o en el hijo y o2m en el padre**.

### Vincular en vistas

- En formulario y lista se puede mostrar cualquier relación. Con
  `widget="many2many_tags"` las etiquetas se ven como "chips" (probá con y sin widget).
- En listas de ofertas `editable="top"` permite editar/crear **en línea** desde la lista.

---

## Tema 7 — Vistas, acciones y menús

### Tipos de vistas

| Tipo | Tag XML | Para qué |
|---|---|---|
| Lista | `<list>` (antes `<tree>`) | columnas, orden, edición en línea |
| Formulario | `<form>` | alta/edición de un registro |
| Búsqueda | `<search>` | buscar, filtrar, agrupar |
| Kanban, etc. | `<kanban>` | tarjetas (no usado en la guía) |

- Odoo elige la **primera vista del `view_mode`** como inicial. Si no definís vista lista
  propia para el modelo, **Odoo muestra una lista por defecto con solo el nombre** del
  registro. Al definir una lista propia, **se toma automáticamente como principal**.

### Acción (`ir.actions.act_window`)

```xml
<record id="action_estate_property" model="ir.actions.act_window">
    <field name="name">Propiedades</field>
    <field name="res_model">estate.property</field>
    <field name="view_mode">list,form</field>
</record>
```

- La acción es el **puente menú/modelo**: dice *qué modelo abrir* y *con qué vistas*.
- **`view_mode`**: lista ordenada de vistas disponibles.
  - `"list, form"` → abre la lista; desde la lista se entra al formulario.
  - Solo `"list"` → **no se puede abrir el detalle** de un registro (no hay form).
  - Solo `"form"` → la acción abre **directamente el formulario** (no hay listado previo).
  - El **orden** define qué vista se muestra primero.
- Otras claves útiles: `domain` (filtro por defecto), `context`, `views` (especificar vistas
  concretas), `target` (`current`, `new` = ventana emergente).

### Menús (`ir.ui.menu`)

```xml
<menuitem id="menu_estate_root" name="Inmobiliaria"/>
<menuitem id="menu_estate_ads" name="Anuncios" parent="menu_estate_root"/>
<menuitem id="menu_estate_property"
          name="Propiedades"
          parent="menu_estate_ads"
          action="action_estate_property"/>
```

- Estructura de **3 niveles**: raíz (barra superior) → primer nivel (desplegable) → menú de
  **acción** (con `action="xml_id_de_la_accion"`).
- Un menú de acción **sin `action` no hace nada** al clickearlo.
- **Jerarquía de padres:** los `parent=` deben apuntar a menús ya definidos; y en el
  **manifest**, el archivo de menús va **después** del archivo de acciones/vistas (orden de
  carga en `data`).
- **Visibilidad:** si un menú/acción apunta a un modelo al que el usuario **no tiene ACL**,
  Odoo **oculta** el menú. Por eso en la guía, recién creado el módulo **no se ven los
  menús** y se pide entrar en **modo debug y convertirse en SuperUsuario** para verlos
  (SuperUsuario ignora permisos). También puede influir falta de actualización/caché.
- `groups="..."` en un menú lo restringe a miembros de ese grupo.

### Vista lista

```xml
<record id="view_estate_property_list" model="ir.ui.view">
    <field name="name">estate.property.list</field>
    <field name="model">estate.property</field>
    <field name="arch" type="xml">
        <list>
            <field name="name"/>
            <field name="postcode"/>
            <field name="tag_ids" widget="many2many_tags"/>
        </list>
    </field>
</record>
```

- **`editable="top"`** (o `"bottom"`): edición **en línea** desde la lista → permite crear
  registros **sin abrir el formulario**. Práctico cuando el modelo tiene **uno o pocos
  campos** (la guía lo usa en etiquetas, tipos y ofertas).
- La guía manda **quitar** `editable="top"` de la lista de ofertas cuando la carga se vuelve
  más compleja (onchange, validaciones) → se pasa a crear desde el formulario.
- Sin acción asociada, una vista lista igual se usa: cuando se embebe en otro formulario
  (ver "ofertas" abajo).

### Vista formulario

Estructura típica (la que pide la guía, ejercicio 23 U1):

```xml
<form>
    <header>
        <button name="action_cancel" string="Cancelar" type="object"
                invisible="state not in ['new', 'offer_received']"/>
        <button name="action_sold" string="Marcar como vendida" type="object"
                invisible="state in ['sold', 'canceled']"/>
        <field name="state" widget="statusbar"/>
    </header>
    <sheet>
        <widget name="web_ribbon" title="Vendida" bg_color="bg-success"
                invisible="state != 'sold'"/>
        <h1><field name="name" placeholder="Nombre propiedad"/></h1>
        <field name="tag_ids" widget="many2many_tags"/>
        <group>                <!-- dos <group> = dos columnas -->
            <group> ... columna 1 ... </group>
            <group> ... columna 2 ... </group>
        </group>
        <notebook>
            <page string="Descripción"> ... </page>
            <page string="Ofertas"> <field name="offer_ids"/> </page>
        </notebook>
    </sheet>
</form>
```

- **`<header>`**: botones de acciones y el `state` con **`widget="statusbar"`**.
- **`<sheet>`**: "el papel" del formulario; ahí va el título (`<h1>`), grupos, notebook y el
  ribbon.
- **`<group>`**: agrupa campos **en columnas**; dos `<group>` hermanos = dos columnas.
- **`<notebook>` / `<page>`**: pestañas.
- **`placeholder`**: texto de ayuda dentro del campo vacío.
- **Ribbon** (cinta esquina superior derecha): `<widget name="web_ribbon" title="Vendida" .../>`
  con `bg_color` (p. ej. `bg-success`, `bg-warning`).
- **Botones**: `type="object"` llama a un **método del modelo** (`name="action_sold"`);
  `type="action"` dispara otra acción; también hay `type="object"` con `confirm` etc.
- **`invisible="..."`**: expresión estilo Python (Odoo 17+). En el examen pensá en Odoo 18 →
  esta sintaxis, **no** el viejo `attrs="{'invisible': [...]}"`.
  - Ideal: **validación en backend** (`raise UserError`) **+ visibilidad en frontend**
    (esconder el botón según estado): la guía lo pide así (ej. 15 U2).
- **`groups="grupo"`** en un campo/botón/menú: lo muestra solo a ese grupo.

### Vista search

```xml
<search>
    <field name="name"/>
    <field name="postcode"/>
    <filter name="my_properties" string="Mis propiedades"
            domain="[('create_uid', '=', uid)]"/>
    <filter name="available" string="Disponibles"
            domain="[('state', 'in', ['new', 'offer_received'])]"/>
    <group>
        <filter name="groupby_state" string="Estado"
                context="{'group_by': 'state'}"/>
        <filter name="groupby_month" string="Mes de creación"
                context="{'group_by': 'create_date:month'}"/>
    </group>
</search>
```

- `<field>` simple → agrega ese campo a los **términos de búsqueda** del search bar.
- `<filter domain="...">` → **filtro guardado** (chips) con un dominio.
  - "Lo creado por el usuario actual": `[('create_uid', '=', uid)]` (`uid` está disponible
    en el contexto de la vista).
  - "Disponibles": `[('state', 'in', ['new', 'offer_received'])]`.
- `<filter context="{'group_by': 'campo'}">` → **agrupación**. Se anidan en `<group>` para
  que aparezcan en el menú "Agrupar por". Añadí `:month` para agrupar por mes
  (`create_date:month`).
- **Solo se puede agrupar/buscar por campos "almacenables"**: un campo computado **sin
  `store=True` no se puede usar para agrupar ni buscar** (en BD no existe columna).

### Herencia de vistas (extender sin romper)

```xml
<record id="res_users_view_form" model="ir.ui.view">
    <field name="name">res.users.form (real_estate)</field>
    <field name="model">res.users</field>
    <field name="inherit_id" ref="base.view_users_form"/>
    <field name="arch" type="xml">
        <xpath expr="//notebook" position="inside">
            <page string="Propiedades">
                <field name="property_ids" readonly="1"/>
            </page>
        </xpath>
    </field>
</record>
```

- `inherit_id` → vista base (nativa u otra). `position` → `inside`, `after`, `before`,
  `replace`, `attributes`, `rename`... o directamente sobre un `<field name="...">`
  (Odoo infiere `position="inside"` para etiquetas conocidas).
- Ventaja: **no modificás la vista original**; si el módulo nativo cambia, tu extensión
  sigue aplicándose. Así trabajan los módulos entre sí (y así se agregó la pestaña
  "Propiedades" a `res.users` en el ejercicio 25 U2).

### ¿Por qué la lista de ofertas NO necesita acción? (ej. 40 U1)

Porque esa lista **no se abre desde un menú**: se muestra **embebida** dentro del formulario
de la propiedad, en la página "Ofertas", como vista de los registros de `offer_ids`. Una
**vista** (record `ir.ui.view`) es un plantilla reutilizable; la **acción** solo hace falta
cuando querés **abrir un modelo de forma independiente** (menú propio). Por eso recién en el
ejercicio 12 U2 ("vista formulario + menú de **todas** las ofertas") sí se pide acción y
menú. (Y ahí sí se puede agrupar por tipo, porque `property_type_id` es related **`store=True`**.)

---

## Tema 8 — Campos computados, related, depends, inverse, store

> **Tema estrella del examen.** La guía dice literalmente *"campos computados"* como ejemplo
> de tema suelto. Dominá esta sección.

### Campo computado

Un campo cuyo valor **surge de hacer una operación**, ejecutando un **método de cómputo**:

```python
total_area = fields.Float(
    string="Superficie total",
    compute="_compute_total_area",
    # store=True,   ← sin esto, NO se guarda en BD
)

@api.depends("living_area", "garden_area")
def _compute_total_area(self):
    for record in self:
        record.total_area = record.living_area + record.garden_area
```

Reglas:

- El método se llama por `compute="nombre_del_metodo"`; convención: prefijo **`_compute_`**.
- El método **siempre itera `for record in self`**: `self` es un **recordset** que puede traer
  muchos registros (una vista lista muestra decenas a la vez). En un formulario `self` tiene
  1 registro.
- **Campo computado = de solo lectura** por defecto (la UI no deja escribirlo), salvo que
  tenga **`inverse`** (ver más abajo).

### ¿Dónde se guarda? `store` — la pregunta del millón

| | **Sin `store`** (default) | **Con `store=True`** |
|---|---|---|
| ¿Existe columna en la tabla (pgweb)? | **No** | **Sí** |
| ¿Cuándo se calcula? | **Cada vez que una vista lo necesita** (en memoria) | **Una vez**, al crearse/modificarse lo que depende; después Odoo **lee de la BD** |
| Costo | cálculo repetido en cada render | ahorra cómputo, usa espacio en BD |
| ¿Se puede buscar/gruppear/sortear por él? | **No** (no hay columna) — salvo que implementes `_search` | **Sí** |
| Caso de la guía | Ej. 1: se ve en formulario pero **no en pgweb** | Ej. 4: aparece la columna, pero **ya no se recalcula** solo |

Analogía de la guía: con `store=True` guardás *"el valor ya calculado, así la próxima vez
no tengo que volver a calcular, simplemente leo la base y me ahorro el costo"*.

### `@api.depends` — cuándo recomputar

- Con **`store=True` y SIN `@api.depends`**: Odoo calcula **una vez** (al crear el registro)
  y **no sabe que debe recalcular** → al modificar `living_area`, `total_area` queda
  **desactualizado** (ej. 4 U2: "ya no se recomputa. ¿Por qué?").
- Agregando **`@api.depends('living_area', 'garden_area')`**: Odoo **registra la dependencia**
  y, al escribir en esos campos, **vuelve a disparar el cómputo** (ej. 5 U2: "vuelve a
  computarse").
- `depends` también sirve para campos **no store**: mantiene frescos los valores ya cargados
  en la vista.
- Se pueden indicar **rutas**: `@api.depends("offer_ids.price")` (best_offer),
  `@api.depends("offer_ids.partner_id")` (offer_partner_ids).

**Pregunta clásica:** *"¿Por qué con `store=True` solo no recalcula y con `depends` sí?"*
→ Porque `store` decide **dónde** vive el valor y `depends` define **las dependencias que
Odoo debe vigilar** para reprogramar el cálculo al escribir en ellas. Son atributos
independientes que trabajan juntos.

### ⚠ Rendimiento: el peligro de `depends` cruzado

Si el cómputo almacenado depende de **un campo de otro modelo** (p. ej.
`@api.depends("partner_id.name")` con `store=True`), al cambiar **un** partner Odoo tendría
que **recomputar todos los registros** que lo referencian → miles de recomputos y caída de
rendimiento. Ejemplo clásico: capítulo 8 del tutorial *Server Framework 101*
(`description = fields.Char(compute=..., store=True)` + `@api.depends("partner_id.name")`).

### ¿Almacenar o no almacenar? (criterios de la guía)

- Solo se muestra en **formulario** → **no hace falta** almacenar.
- Querés **buscar** por el campo → o lo **almacenás**, o definís un método **`_search`**
  (si el rendimiento no importa, almacená).
- Se muestra en **vista de lista** (pueden verse cientos de registros) → **considerá
  almacenarlo**.
- **`best_offer`** (ej. 7 U2, "¿lo almacenarías?"): conviene **no** almacenarlo → se muestra
  en el formulario de un registro y depende de las ofertas (otro modelo): con `store` cada
  nueva oferta dispararía recomputos encadenados. Respuesta esperada: **no, con no store es
  suficiente**.

### Campo related

```python
partner_id = fields.Many2one("res.partner", string="Ofertante")
email = fields.Char(related="partner_id.email")
# en la oferta:
property_type_id = fields.Many2one(
    related="property_id.property_type_id", store=True, string="Tipo de propiedad",
)
```

- Toma el valor de **otro campo siguiendo una cadena de relaciones**
  (`property_id.property_type_id`).
- **Por defecto: NO se almacena** y **es de solo lectura**; con `store=True` se guarda
  (y entonces **se puede buscar/gruppear** por él — por eso en el ejercicio 12 U2 se pide
  el related **almacenado**: para poder **agrupar las ofertas por tipo**).
- El **tipo de dato debe coincidir** con el del campo original.
- **Un related es "un tipo especial y simplificado de campo computado"** (la guía lo dice
  así). Reemplaza un `compute` trivial como `_compute_email`.

**¿Se puede usar related en `offer_partner_ids`?** (ej. 19 U2) → **No conviene.** Un related
refleja **un campo puntual siguiendo un camino fijo**; acá necesitás **agregar** los partners
de **todas** las ofertas (muchos → muchos). Eso se resuelve con un **campo computado** que
hace `record.offer_ids.partner_id` / `.mapped('partner_id')`.

### Cómputo inverso (`inverse=`)

```python
numero = fields.Integer(string="Número")
doble_de_numero = fields.Integer(
    string="Doble de número",
    compute="_compute_doble_de_numero",
    inverse="_inverse_doble_de_numero",      # ← hace el campo escribible
)

def _compute_doble_de_numero(self):
    for rec in self:
        rec.doble_de_numero = rec.numero * 2

def _inverse_doble_de_numero(self):
    for rec in self:
        rec.numero = rec.doble_de_numero / 2
```

- **La sola presencia de `inverse=` hace que el computado deje de ser solo lectura**: cuando
  el usuario escribe en el campo, Odoo llama al método inverso para "devolver" el valor.
- Caso práctico de la guía (ej. 10 U2): `date_deadline = create_date + validity`; pero si el
  usuario ingresa la **fecha** a mano, el inverso recalcula
  `validity = date_deadline - create_date`.

### Tabla comparativa final (memorizá esta)

| | related | compute (no store) | compute + store | compute + store + depends | compute + inverse |
|---|---|---|---|---|---|
| Se guarda en BD | no (salvo `store=True`) | no | sí | sí | no (salvo store) |
| Se recalcula solo al modificar origen | sí (en render) | sí (en render) | **no** | **sí** | sí |
| Se puede buscar/gruppear | solo con store | no | sí | sí | no |
| Escritura desde UI | no (readonly) | no | no | no | **sí** |

---

## Tema 9 — onchange y validaciones

### `@api.onchange`

```python
@api.onchange("garden")
def _onchange_garden(self):
    if self.garden:
        self.garden_area = 10
    else:
        self.garden_area = 0
```

- Se dispara **en el cliente**, **al editar el formulario** (antes de guardar), cuando cambia
  uno de los campos indicados.
- Permite **modificar campos del "registro en pantalla"** y devolver avisos.
- **No persiste nada por sí solo**: si el usuario cancela, los cambios se descartan; **tampoco
  se ejecuta** si el registro se escribe desde código (XML-RPC, otro método, imports).
  → Por eso **no sirve como validación de seguridad/regla de negocio**; es **UX**.
- Funciona con `self` de un solo registro (formularios).

**Aviso no bloqueante** (ej. 14 U2): el onchange puede devolver un diccionario con `warning`:

```python
@api.onchange("expected_price")
def _onchange_expected_price(self):
    if self.expected_price and self.expected_price < 10000:
        return {
            "warning": {
                "title": "Precio bajo",
                "message": "El precio esperado es menor a 10000, posible error de tipeo.",
            }
        }
```

- **No bloquea** el guardado: solo informa (mensaje emergente). Se puede depurar con
  `wdb.set_trace()`.

### ¿Qué mecanismo elijo según el objetivo?

| Objetivo | Mecanismo | ¿Bloquea? | Cuándo corre |
|---|---|---|---|
| Sugerir/auto-completar valores mientras se edita | `@api.onchange` | no | en el form, al editar |
| Avisar "ojo, posible error de tipeo" sin frenar | `onchange` que devuelve `warning` | no | en el form |
| **Impedir** una operación (regla de negocio) | `raise UserError(...)` en método de botón/`create`/`write` | **sí** | en el servidor |
| Validar campos al **crear/modificar vía ORM** | `@api.constrains('campo')` + `ValidationError` | **sí** | en el servidor (create/write) |
| Integridad dura (únicos, rangos) | `_sql_constraints` (SQL) | **sí** | siempre, hasta en SQL directo |

- **`UserError`** (de `odoo.exceptions`): la guía lo usa para botones "Cancelar"/"Marcar como
  vendida" y para `@api.ondelete` → Odoo muestra un diálogo de error al usuario.
- Patrón pedido en el ej. 15 U2: **validación en backend con `UserError`** (obligatoria) **+
  visibilidad frontend** de los botones según `state` (mejora UX). Al vender: **ribbon
  "Vendida"**.

---

## Tema 10 — ORM y CRUD

### El ORM

- Odoo expone una capa de **ORM (Object-Relational Mapping)** en Python: los modelos son
  clases, los registros son **objetos/recordsets**, y las operaciones CRUD se hacen en Python
  **sin escribir SQL** (el ORM traduce a SQL sobre PostgreSQL).
- Todo acceso pasa por el **environment (`env`)**.

### `env` y recordsets

```python
self.env["estate.property"]                 # modelo vía env (recordset vacío)
self.env["res.partner"].search([...])       # búsqueda → recordset
self.env.user                                # usuario actual
self.env.uid                                 # id del usuario actual
self.env.context                             # contexto (dict)
self.env.su                                  # modo superusuario (sudo)
```

- **Recordset**: colección **inmutable** de registros (cero, uno o muchos). Siempre hay que
  **iterar** (`for record in self`) antes de asignar campos.
- Atributos de un recordset: `rec.id` (si es de a uno), `rec.ids` (lista de ids),
  `rec.display_name`. Se puede recorrer, y con `ensure_one()` exigir que sea exactamente uno.
- Métodos útiles: `mapped('campo')` (lista de valores/records), `filtered(lambda/campo)`,
  `sorted(...)`, `browse(ids)`, `copy()`, `exists()`. Operadores de recordsets:
  `rs1 + rs2`, `rs1 - rs2` (diferencia — usado en `action_accept`: `offer_ids - offer`).

### CRUD

```python
# CREATE
prop = self.env["estate.property"].create({"name": "Casa", "bedrooms": 3})
self.env["estate.property.offer"].create({          # lista para varios
    "price": 100000, "partner_id": p.id, "property_id": prop.id,
})

# READ / SEARCH (dominios)
recs = self.env["estate.property"].search(
    [("state", "=", "new"), ("expected_price", ">", 100000)],
    limit=10, offset=0, order="expected_price desc",
)
one = self.env["estate.property"].browse(5)
self.env["estate.property"].search_count([...])     # cantidad

# UPDATE (write modifica TODOS los registros del recordset con el MISMO dict)
recs.write({"state": "canceled"})
prop.write({"buyer_id": partner.id, "selling_price": 95000})

# DELETE
prop.unlink()
```

**Dominios**: lista de tuplas `(campo, operador, valor)` combinadas con **Y lógico** por
defecto; operadores de prefijo `&` (Y), `|` (O), `!` (NO).

- Operadores: `=`, `!=`, `<`, `<=`, `>`, `>=`, `like`, `ilike`, `in`, `not in`, `child_of`,
  `=like`, `=ilike`.
- Ejemplos de la guía:
  - creados por mí: `[('create_uid', '=', uid)]`
  - disponibles: `[('state', 'in', ['new', 'offer_received'])]`
  - contactos activos sin ofertar: `[('active', '=', True), ('id', 'not in', offered_ids)]`

**Sobre `create()` redefinido:** en versiones modernas `create` recibe **una lista de
diccionarios** (creación en lote) y se decora con **`@api.model_create_multi`**; dentro se
valida cada `vals` y al final **siempre se llama a `super().create(vals_list)`** y se devuelve
lo que devuelve `super`:

```python
@api.model_create_multi
def create(self, vals_list):
    for vals in vals_list:
        ...validaciones que lancen UserError...
    records = super().create(vals_list)
    records.property_id.write({"state": "offer_received"})
    return records
```

**Sobre `write()` redefinido**: misma idea — validar y llamar `super().write(vals)`.

**`unlink()`**: borrado; ver por qué conviene `@api.ondelete` en el Tema 14.

---

## Tema 11 — Comandos relacionales

### Qué son

Para **manipular los registros de campos One2many y Many2many** no se asignan ids "a mano":
se usa una **lista de comandos relacionales**. Internamente cada comando es una **tupla de
tres elementos**:

1. número entero que identifica el comando,
2. id del registro (si aplica),
3. diccionario con los datos a cargar/actualizar (si aplica).

### Los 7 comandos (tabla obligatoria de memorizar)

| N° | Nombre | Tupla | Qué hace |
|---|---|---|---|
| **0** | CREATE | `(0, 0, valores)` | **crea y vincula** un registro nuevo con `valores` |
| **1** | UPDATE | `(1, id, valores)` | **actualiza** los campos de un registro ya vinculado (el registro sigue vinculado) |
| **2** | DELETE | `(2, id, 0)` | **borra el registro de la BD** y rompe el vínculo |
| **3** | UNLINK | `(3, id, 0)` | **solo desvincula**; el registro **sigue existiendo** |
| **4** | LINK | `(4, id, 0)` | **vincula** un registro ya existente |
| **5** | CLEAR | `(5, 0, 0)` | **desvincula todos** (vacía la relación) |
| **6** | SET | `(6, 0, ids)` | **reemplaza** la relación por la lista `ids` exactamente |

### Helpers `Command` (forma recomendada)

```python
from odoo import Command

Command.create({values})   # (0, 0, {values})
Command.update(id, {values})  # (1, id, {values})
Command.delete(id)         # (2, id, 0)
Command.unlink(id)         # (3, id, 0)
Command.link(id)           # (4, id, 0)
Command.clear()            # (5, 0, 0)
Command.set([ids])         # (6, 0, ids)
```

- Odoo **recomienda** los helpers por legibilidad; las tuplas siguen siendo válidas.
- Uso típico: `record.tag_ids = [Command.create({'name': 'A estrenar'})]` → crea la etiqueta
  **y** la vincula. Equivale a `[(0, 0, {'name': 'A estrenar'})]`.

### delete vs unlink y clear vs set (la pregunta trampa)

- `Command.unlink(id)` → la etiqueta **desaparece de la propiedad pero sigue existiendo**
  en `estate.property.tag`. `Command.delete(id)` → además de romper el vínculo, **borra el
  registro** de la tabla.
- `Command.clear()` → **todos** los vínculos afuera (la propiedad queda sin etiquetas).
  `Command.set([ids])` → deja vinculados **exactamente** los de la lista (también desvincula
  los que no estén).

### Ejemplos de la guía (ej. 21 U2) mapeados

| Botón | Comando |
|---|---|
| "Sacar etiquetas" (desvincular todas) | `record.tag_ids = [Command.clear()]` |
| "Cargar todas las etiquetas" | `record.tag_ids = [Command.set(all_tags.ids)]` |
| "A estrenar" (crear si no existe y vincular) | `search` → si no existe `create`, luego `record.tag_ids = [Command.link(tag.id)]` |
| Factura con 2 líneas (`account.move.line`) | `line_ids = [Command.create({...}), Command.create({...})]` |

> Nota: los comandos funcionan igual para **One2many** (p. ej. `Command.create` en `line_ids`
> crea hijos con la FK puesta automáticamente por el `inverse_name`).

---

## Tema 12 — Constraints

### `_sql_constraints` (restricciones a nivel de base de datos)

Atributo de clase: **lista de tuplas `(nombre, definición_SQL, mensaje_de_error)`**:

```python
_sql_constraints = [
    ("unique_tag_name", "UNIQUE(name)", "El nombre de la etiqueta debe ser único"),
    ("partner_property_uniq",
     "UNIQUE(partner_id, property_id)",
     "Un ofertante no puede ofertar dos veces por la misma propiedad."),
]
```

- **`UNIQUE(columna)`** → unicidad de una columna (etiquetas, tipos de propiedad).
- **`UNIQUE(col1, col2)`** → unicidad **compuesta**: la **combinación** se repite; por sí
  sola cada columna puede repetirse. Caso de la guía: un mismo partner puede ofertar en
  propiedades distintas, pero **no dos veces en la misma**.
- **`CHECK(expresión)`** → condición arbitraria (no usado en la guía, pero entra como opción).
- El motor es **PostgreSQL**: la restricción **siempre** se cumple, incluso si alguien escribe
  con SQL directo o desde otro módulo. Si se viola, Odoo muestra el **mensaje** de la tercera
  posición.
- ⚠ **Antes de agregar un `UNIQUE` hay que limpiar los duplicados existentes** si no, la
  actualización del módulo falla (la guía lo advierte en los ej. 17 y 18 U2).

### `@api.constrains` (restricciones en Python)

```python
@api.constrains("price")
def _check_price(self):
    for rec in self:
        if rec.price < 0:
            raise ValidationError("El precio no puede ser negativo.")
```

- Se ejecutan en el **servidor** cuando el registro se crea o modifica **vía ORM**
  (`create`/`write` de Odoo).
- Permiten lógica que SQL no puede expresar fácilmente (llamar a otros modelos, reglas
  complejas).
- Lanzan **`ValidationError`** (de `odoo.exceptions`).
- **No se ejecutan** si el cambio se hace con SQL directo (por eso se combinan con SQL
  constraints cuando la regla es dura).
- **Diferencia clave con onchange**: el onchange solo "avisa" en el formulario; el
  `@api.constrains` **bloquea el guardado** venga por donde venga la escritura desde Odoo.

### Resumen de validaciones (fórmula para el examen)

`onchange` (UX, no bloquea) < `@api.constrains` (bloquea en ORM, Python) <
`_sql_constraints` (bloquea siempre, SQL). Y `UserError` para botones/lógica de negocio.

---

## Tema 13 — Herencia (modelos, métodos, vistas, módulos)

### 1) Herencia de modelos: `_inherit`

**Extender un modelo existente** (agregar campos/métodos **sin crear tabla nueva**):

```python
class ResUsers(models.Model):
    _inherit = "res.users"                      # sin _name → mismo modelo, misma tabla

    property_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="salesman_id",
        string="Propiedades",
    )
```

- `_inherit = "modelo"` **sin `_name`** → herencia **prototipo**: la clase se **fusiona** en
  `res.users`; los campos nuevos se agregan **a la misma tabla** `res_users`.
- **`_name` + `_inherit` juntos** → creás un modelo **nuevo** que copia campos/métodos del
  padre (es otra tabla/otro modelo).
- **`_inherits = {'padre': 'campo_m2o'}`** → herencia por **delegación**: el hijo "presta"
  los campos del padre a través de un Many2one (no confundir con `_inherit`; es el patrón de
  `res.partner` en usuarios). No usado en los prácticos, pero puede salir en MC.

**¿Hace falta `ir.model.access.csv` para el modelo que hereda `res.users`?**
→ **NO.** Al usar `_inherit` sin `_name` **no se crea un modelo nuevo ni una tabla nueva**:
sigue siendo `res.users`, que **ya tiene sus reglas de acceso**. Sí haría falta si creara un
modelo nuevo con `_name`.

### 2) Herencia de métodos: `super()`

```python
def action_sold(self):
    res = super().action_sold()          # ejecuta la lógica original primero
    # ... lógica nueva: generar la factura ...
    return res
```

- Redefinís el método en la clase hija y llamás a **`super()`** para no perder el
  comportamiento original (clave: los módulos se apilan sin pisarse).
- Caso `estate_account` (ej. 27 U2): hereda `estate.property` y **redefine "Marcar como
  vendida"** para, además de lo original, crear un `account.move`.

### 3) Herencia de vistas

Ya vista en el Tema 7: `inherit_id` + `xpath`/`position` → **agregás** (no reescribís) una
página, campo o botón a una vista existente (nativa o de otro módulo).

### 4) Herencia/dependencia entre módulos

```python
# estate_account/__manifest__.py
{
    "name": "Estate Account",
    "depends": ["real_estate", "account"],
    ...
}
```

- **`depends`**: para instalar `estate_account` se instalan antes `real_estate` y `account`;
  el módulo nuevo puede **extender** los modelos de sus dependencias (mismo patrón de la
  arquitectura modular de Odoo: los addons extienden a otros addons).
- La factura usará comandos relacionales en `line_ids`:

```python
self.env["account.move"].create({
    "partner_id": record.buyer_id.id,
    "move_type": "out_invoice",     # factura a cliente (venta)
    "line_ids": [
        Command.create({"name": record.name, "quantity": 1,
                        "price_unit": record.selling_price}),
        Command.create({"name": "Gastos administrativos", "quantity": 1,
                        "price_unit": 100}),
    ],
})
```

- `move_type = "out_invoice"` = factura de venta a cliente; `out_refund` sería nota de
  crédito, `in_invoice` factura de compra (proveedor).

---

## Tema 14 — Lógica de negocio: botones, UserError, ondelete, create

### Métodos de botones

- En la vista: `<button name="action_sold" string="Marcar como vendida" type="object"/>`
  → llama al método `def action_sold(self)` del modelo, pasándole el/los registro(s)
  seleccionados.
- Convención: devuelven a veces un `ir.actions.act_window` (abrir wizard/form) o `None`.
- Validación **siempre en backend** además de esconder el botón en frontend.

### `UserError`

```python
from odoo.exceptions import UserError

def action_cancel(self):
    for record in self:
        if record.state == "sold":
            raise UserError("No se puede cancelar una propiedad vendida.")
        record.state = "canceled"
```

- `raise UserError(...)` → diálogo de error para el usuario; **aborta** la operación.
- Casos guía: cancelar una vendida / vender una cancelada (ej. 15 U2); condiciones de
  `create()` de ofertas (ej. 23 U2); borrado con `ondelete`.

### `@api.ondelete` en vez de redefinir `unlink()`

```python
@api.ondelete(at_uninstall=False)
def _unlink_if_new_or_cancelled(self):
    for record in self:
        if record.state not in ("new", "canceled"):
            raise UserError("Solo se pueden borrar propiedades Nuevas o Canceladas.")
```

**¿Por qué es conveniente `ondelete` antes que redefinir `unlink()`?** (pregunta de la
guía, ej. 22 U2)

1. **No tenés que reimplementar la lógica de borrado**: el método **solo valida y lanza**;
   no hay riesgo de olvidar `super().unlink()` o romper el borrado real.
2. **Es el mecanismo recomendado por Odoo** para proteger registros: el framework llama a los
   métodos `ondelete` como chequeo previo y maneja él el resto (borrados en lote, borrados
   internos del framework, etc.).
3. **`at_uninstall=False`**: al **desinstalar** el módulo Odoo necesita poder borrar sus
   registros; un `unlink()` redefinido que siempre bloquea **rompería la desinstalación**,
   mientras `ondelete` puede saltarse el chequeo.
4. Si redefinís `unlink()`, tus validaciones corren **para todo** el borrado de ese modelo,
   incluso flujos internos que esperan poder borrar (p. ej. borrado en cascada de registros
   temporales) — los invalidás sin querer.

### Redefinir `create()` (ej. 23 U2) — flujo completo

En `estate.property.offer`:

1. Recorrer `vals_list` y validar **antes** de crear:
   - `price` debe superar `best_offer` de la propiedad → si no, `UserError`.
   - `state` de la propiedad debe ser "Nuevo" u "Oferta recibida" → si no, `UserError`.
2. `records = super().create(vals_list)`.
3. Después de crear: `records.property_id.write({"state": "offer_received"})`.
4. `return records`.

### Aceptar oferta (ej. 16 U2) — qué pasa en cascade

Botón en la lista de ofertas → al aceptar una:

- `property.buyer_id = offer.partner_id` y `property.selling_price = offer.price`,
- `property.state = "offer_accepted"`,
- **todas las demás** ofertas → `status = "refused"` (en el repo:
  `(offer.property_id.offer_ids - offer).write({"status": "refused"})`).

### Ribbon y estados en vista

- `<widget name="web_ribbon" title="Vendida" bg_color="bg-success"
  invisible="state != 'sold'"/>` dentro de `<sheet>`.

---

## Tema 15 — Respuestas a los "¿por qué?" de la guía

> Cada "¿por qué?"/"¿qué pasa si...?" de la guía es un candidato directo a multiple choice.
> Acá están todos, en orden.

### Unidad 1

**4. ¿Qué campos adicionales aparecieron en pgweb?**
`id`, `create_uid`, `create_date`, `write_uid`, `write_date` (más `display_name`). Son los
campos técnicos/auditoría que Odoo agrega a toda tabla.

**6. ¿Qué pasa si el archivo de menús va ANTES de las vistas/acciones en el manifest?**
Falla la actualización: el menú hace `ref` a la acción (XML ID) que **todavía no existe**
(*External ID not found*). El orden de `data` es el orden de carga → **primero las acciones
y vistas, después los menús**.

**7. ¿Por qué todavía no se ven los menús?**
Los menús de acción apuntan a un modelo para el que **aún no hay reglas de acceso**
(`ir.model.access.csv` se crea recién en el ej. 10); sin permisos, Odoo oculta el menú.
Se pide entrar en **modo debug y convertirse en SuperUsuario** porque este **ignora las ACL**.
(Secundario: falta de actualización/caché del navegador — lo aclara la guía en el ej. 28.)

**8. `view_mode` solo `list` / solo `form`**
- Solo `list`: entrás a la lista pero **no podés abrir el detalle** de un registro (no hay
  formulario).
- Solo `form`: la acción abre **directamente el formulario**, sin listado previo.
- `"list, form"`: lista primero, y desde ahí se navega al formulario (lo correcto).

**9. ¿Qué tipos de usuario existen?**
Usuario **interno** (backend, `base.group_user`), **portal** y **público** (+ SuperUsuario).

**10. ¿A qué representa `base.group_user`? ¿Cómo dar C/U/D?**
Representa al **usuario interno**. Para dar crear/modificar/eliminar: poner `1` en las
columnas `perm_create`, `perm_write`, `perm_unlink` de su fila en `ir.model.access.csv`.

**12. ¿Ventajas/desventajas de cambiar desde Odoo vs desde el módulo?**
Desde Odoo: rápido para probar, pero **se pierde** al recrear la BD, **no se versiona** ni
se lleva a otros entornos. Desde el módulo: **reproducible, versionable (git), automático en
cualquier entorno**, pero requiere actualizar el módulo.

**15. ¿Qué pasa si un usuario no pertenece a ningún grupo con permisos?**
**No tiene ningún acceso** al modelo: Odoo lanza **AccessError** y no puede leer ni operar
con `estate.property` (no le sirven menús ni acciones).

**35. ¿Por qué `tag_ids` Many2many y no Many2one ni One2many?**
Porque la relación real es **N:N**: cada propiedad tiene **muchas** etiquetas y cada etiqueta
puede estar en **muchas** propiedades. Un Many2one solo admitiría una etiqueta por propiedad;
un One2many pondría la FK en la etiqueta (una sola propiedad por etiqueta).

**39. ¿Por qué hay que especificar `inverse_name`? ¿Qué implica que la One2many sea virtual?**
- `inverse_name`: es el nombre del **Many2one** del modelo hijo
  (`property_id`) mediante el cual Odoo **resuelve la relación inversa**; sin él no sabe qué
  campo buscar en `estate.property.offer`.
- **Virtual**: la One2many **no tiene columna ni tabla propia**; es "la vista inversa" de un
  Many2one que ya existe en el hijo (la FK vive en `estate_property_offer.property_id`).

**40. ¿Por qué la lista de ofertas no necesita acción?**
Porque **no se abre como modelo independiente**: se muestra **dentro del formulario** de la
propiedad (página "Ofertas") como vista embebida de `offer_ids`. La acción solo es necesaria
para abrir el modelo desde un menú (como en el ej. 12 U2: "todas las ofertas").

### Unidad 2

**3. ¿Por qué `total_area` no está en la tabla pero sí en la vista?**
Porque **no tiene `store=True`**: no hay columna en la BD; Odoo lo **calcula en memoria**
cada vez que la vista lo necesita.

**4. ¿Por qué con `store=True` solo ya no se recalcula?**
`store` hace que el valor se **lea de la base**, pero **sin `@api.depends`** Odoo **no conoce
las dependencias**, así que al modificar `living_area`/`garden_area` no dispara ningún
recomputo → el valor queda desactualizado.

**5. ¿Por qué agregando `@api.depends` vuelve a computarse?**
Porque el decorador **registra qué campos, al cambiar, deben re-disparar el cómputo**: Odoo
programa el recomputo del campo almacenado cuando se escribe en `living_area` o `garden_area`.

**7. ¿Almacenarías `best_offer`?**
No hace falta: se muestra en el formulario de un registro y depende de `offer_ids` (otro
modelo); con `store` cada nueva oferta generaría recomputos encadenados. Con **no store**
suficiente (solo se recomputa al mostrar).

**35/36 (U1) relacionados**: ver arriba.

**10. `date_deadline` con función inversa**
Se computa `create_date + validity`; al definir `inverse`, si el usuario ingresa la fecha,
Odoo llama al inverso y recalcula `validity = fecha - create_date`. Además `inverse` hace que
el computado **deje de ser solo lectura**.

**12. ¿Se pueden agrupar las ofertas por tipo?**
**Sí**, porque `property_type_id` es un related **`store=True`**: solo los campos con columna
en BD se pueden usar para agrupar/buscar.

**19. ¿Serviría un related para `offer_partner_ids`?**
**No**: un related refleja **un campo puntual siguiendo una cadena fija**; acá hay que
**agregar los partners de muchas ofertas** (relación N:M) → se resuelve con un **campo
computado** (`record.offer_ids.partner_id` / `mapped`).

**22. ¿Por qué `@api.ondelete` y no redefinir `unlink()`?**
Ver el detalle en el [Tema 14](#tema-14--lógica-de-negocio-botones-usererror-ondelete-create):
ondelete solo valida y lanza (sin reimplementar borrado ni `super`), es la forma recomendada
y no rompe la desinstalación (`at_uninstall=False`) ni borrados internos del framework.

**24. ¿Hace falta `ir.model.access.csv` para el modelo que hereda `res.users`?**
**No**: `_inherit` sin `_name` **no crea modelo ni tabla nuevos**; sigue siendo `res.users`,
que **ya tiene sus permisos**.

---

## Tema 16 — Trampas típicas de multiple choice

### No confundir

| Tema | Opción correcta | Trampas habituales |
|---|---|---|
| `base.group_user` | Usuario **interno** (empleado/backend) | "portal", "público", "superusuario" |
| ACL CSV sin `group_id` | Aplica a **todos** los usuarios | "a nadie", "solo a admin" |
| Usuario sin grupo con ACL | **AccessError**, cero acceso | "solo lectura por defecto" |
| Campo **no store** | **No** existe en la tabla; se calcula al mostrar | "se guarda al final del día" |
| `store=True` sin `depends` | Se guarda pero **no se recalcula** | "se recalcula solo siempre" |
| `@api.depends` | Define **qué cambios disparan** el recomputo | "define el tipo del campo" |
| `related` default | **No store** y **readonly** | "se guarda y es editable" |
| `related` + `store=True` | Se guarda → **permite buscar/agrupar** | "related nunca se guarda" |
| `inverse=` | Hace el computado **editable** y calcula al revés | "hace store automático" |
| One2many `inverse_name` | Campo **m2o del hijo** por el que se resuelve | "es la primary key" |
| One2many | **Virtual**: sin tabla/columna propia | "crea una columna en el padre" |
| Many2many | **Tabla intermedia** | "FK en el padre" |
| `unlink` relacional (3) vs `delete` (2) | unlink = **desvincula**; delete = **borra el registro** | al revés |
| `Command.clear()` | Desvincula **todos** | "borra todos los registros" |
| `Command.set([ids])` | Reemplaza por **exactamente** esos ids | "agrega los ids" |
| `onchange` | Solo **cliente/UX**, **no bloquea**, no corre al escribir desde código | "valida en backend" |
| `@api.constrains` | Corre en **create/write del ORM**, bloquea | "corre al abrir el form" |
| `_sql_constraints` | Motor **PostgreSQL**, siempre activo | "es Python" |
| `UserError` | Botones/lógica de negocio (servidor) | "es un warning de onchange" |
| `@api.ondelete` | Valida borrado; **no reimplementa** `unlink` | "es lo mismo que unlink" |
| `_inherit` sin `_name` | **Mismo modelo/tabla** (extiende), **no necesita ACL nueva** | "crea tabla nueva" |
| `_inherit` con `_name` | Modelo nuevo copiando al padre | "es delegación" |
| `_inherits` | **Delegación** vía Many2one al padre | "mezcla de tablas" |
| `super()` en método | Ejecuta la **versión original** y sigue | "no hace falta" |
| `data` en manifest | **Orden importa**; menús después de acciones | "orden alfabético libre" |
| `depends` en manifest | Módulos que deben estar **instalados antes** | "campos que observa el cómputo" |
| Vista por defecto sin lista propia | Muestra **solo el nombre** | "todas las columnas" |
| `editable="top"` | Editar/crear **en línea** en la lista | "abre el formulario" |
| Agrupar/buscar por campo | Solo si tiene **columna** (store o related store) | "cualquier campo" |
| `view_mode="form"` solo | Abre **directamente el form** | "no abre nada" |
| `view_mode="list"` solo | **No permite** abrir el detalle | "abre la lista y ya" |
| `copy=False` | No se copia **al duplicar** | "no se puede guardar" |
| `required=True` | UI obligatorio **y NOT NULL en BD** | "solo UI" |
| Duplicar (Acción → Duplicar) | Llama a `copy()`; aplica `copy=False` | "crea registro vacío" |
| `default` con lambda | Se evalúa **por registro/env** (usuario actual) | "se evalúa al importar" |
| `store=True` + `depends` cruzado a otro modelo | **Riesgo de rendimiento** (recomputa miles) | "nunca hay riesgo" |

### Sintaxis que puede salir en ejemplos de código

- Orden correcto: grupos (XML) **antes** que `ir.model.access.csv`; vistas/acciones **antes**
  que menús.
- `model_id:id` del CSV = `model_estate_property` (puntos → guiones bajos, con prefijo `model_`).
- Filtro por usuario actual en search: `domain="[('create_uid', '=', uid)]"`.
- Agrupar: `context="{'group_by': 'create_date:month'}"`.
- Botón: `type="object"` → método; `type="action"` → otra acción.
- Odoo 18: `<list>` (no `<tree>`), `invisible="..."` directo (no `attrs`).

---

## Tema 17 — Simulacro: 25 preguntas tipo examen con respuestas

> Para entrenar el formato. Leé la pregunta, pensá la respuesta y recién después mirá la ✔.

**1. El campo `base.group_user` representa a:**
a) Portal  b) Usuario interno  c) Público  d) SuperUsuario
**✔ b)** Usuario interno (backend/empleado).

**2. Un usuario que no pertenece a ningún grupo con permisos sobre `estate.property` al
intentar leer registros obtiene:**
a) Lista vacía sin error  b) AccessError  c) Lectura limitada a 10 filas  d) Se lo hace
SuperUsuario automáticamente
**✔ b)** Sin ACL no hay acceso → AccessError.

**3. En `ir.model.access.csv`, una fila con `group_id:id` vacío significa que los permisos...**
a) no se aplican a nadie  b) aplican solo al admin  c) aplican a **todos** los usuarios
d) aplican solo a SuperUsuario
**✔ c)** Vacío = sin grupo = everyone (¡peligro!).

**4. Para que un usuario pueda además de leer crear, modificar y borrar, en la fila del CSV
debe haber `1` en:**
a) solo `perm_read`  b) `perm_write, perm_create, perm_unlink`
c) `perm_create` y `perm_unlink`  d) ninguna de las anteriores, eso va en XML
**✔ b)** Las cuatro columnas CRUD.

**5. Un campo computado sin `store=True`:**
a) genera una columna en la tabla  b) **no** genera columna y se calcula al mostrarlo
c) se almacena recién al cerrar sesión  d) solo funciona en vistas lista
**✔ b)** Se calcula en memoria en cada render; por eso no aparece en pgweb.

**6. Con `store=True` pero sin `@api.depends`, al modificar un campo de origen:**
a) Odoo lanza error  b) el campo **no se recalcula**  c) se recalcula igual  d) el campo deja
de existir
**✔ b)** Sin dependencias registradas no hay recomputo programado.

**7. ¿Cuál es el rol de `@api.depends`?**
a) Indicar el tipo del campo  b) Declarar qué campos, al modificarse, **re-disparan** el
cómputo  c) Hacer el campo editable  d) Guardarlo en BD
**✔ b)** Vigila dependencias; `store` decide si se guarda.

**8. `best_offer` (máximo de las ofertas) conviene almacenarlo:**
a) siempre  b) solo si hay menos de 100 registros  c) **no**, no hace falta almacenarlo
d) solo si es related
**✔ c)** Se muestra en formulario y depende de otro modelo → no store.

**9. Un campo `related` por defecto:**
a) se almacena y es editable  b) **no se almacena y es solo lectura**  c) se almacena y es
solo lectura  d) no se almacena y es editable
**✔ b)** Solo cambia si le agregás `store=True` (y sigue readonly).

**10. Un related con `store=True` permite además:**
a) escribir sobre él  b) **buscar y agrupar** por ese campo  c) que se comporte como onchange
d) nada extra
**✔ b)** Al tener columna, entra en búsquedas y group by (ofertas por tipo).

**11. `inverse=` en un campo computado sirve para:**
a) guardarlo en BD  b) hacerlo recalculable  c) **que deje de ser solo lectura** y recalcular
lo contrario  d) definir la relación con otro modelo
**✔ c)** Ej.: escribir `date_deadline` recalcula `validity`.

**12. En `fields.One2many(comodel_name=..., inverse_name=...)`, el `inverse_name` es:**
a) la primary key de la tabla  b) el nombre del campo **Many2one del modelo hijo** que apunta
al padre  c) el nombre de la tabla intermedia  d) un campo calculado
**✔ b)** Odoo resuelve la relación inversa por ese m2o.

**13. La relación One2many es "virtual" porque:**
a) no tiene valor hasta guardar  b) **no crea columna ni tabla propia**: es la vista inversa
de un Many2one existente en el hijo  c) existe solo en las vistas  d) usa XML
**✔ b)** La FK vive en el modelo hijo.

**14. Una propiedad con muchas etiquetas y una etiqueta en muchas propiedades se modela con:**
a) Many2one  b) One2many  c) **Many2many**  d) related
**✔ c)** Relación N:N con tabla intermedia.

**15. `Command.clear()` aplicado a `tag_ids`:**
a) borra todas las etiquetas de la BD  b) **desvincula todos los vínculos** (siguen existiendo
las etiquetas)  c) borra el campo  d) hace lo mismo que `delete`
**✔ b)** `Command.delete(id)` sí borraría el registro.

**16. `tag_ids = [Command.unlink(id)]` sobre una etiqueta:**
a) borra la etiqueta de la tabla  b) **solo desvincula**; la etiqueta sigue existiendo
c) la vincula otra vez  d) lanza UserError
**✔ b)** unlink = romper vínculo; delete = borrar registro.

**17. `tag_ids = [Command.create({'name': 'A estrenar'})]`:**
a) solo vincula si existe  b) **crea** el registro **y** lo vincula  c) solo crea sin vincular
d) borra y crea
**✔ b)** Equivale a `(0, 0, {...})`.

**18. El comando relacional `2` corresponde a:**
a) create  b) update  c) **delete (borrar el registro)**  d) unlink (desvincular)
**✔ c)** 2 = delete, 3 = unlink.

**19. Un `@api.onchange`:**
a) bloquea el guardado si falla  b) **corre solo en el cliente al editar y no bloquea**  c)
corre en cada `write()` del ORM  d) es lo mismo que un sql_constraint
**✔ b)** Es UX; las reglas de negocio van con UserError/constrains.

**20. ¿Cuál garantiza que la regla se cumple incluso si alguien escribe SQL directo?**
a) onchange  b) UserError en botón  c) **`_sql_constraints`**  d) widget statusbar
**✔ c)** Es restricción de PostgreSQL.

**21. Un `UNIQUE(partner_id, property_id)` en ofertas significa:**
a) que cada partner es único  b) que cada propiedad es única  c) **que la combinación
partner+propiedad no se repite** (no puede ofertar 2 veces la misma propiedad)  d) que no hay
nulos
**✔ c)** Unicidad compuesta.

**22. Un modelo con `_inherit = "res.users"` (sin `_name`) y un campo nuevo:**
a) crea una tabla nueva y necesita ACL nueva  b) **extiende el mismo modelo/tabla y NO
necesita ACL nueva**  c) borra `res.users`  d) requiere `depends` de dos módulos
**✔ b)** Herencia prototipo: sigue siendo `res.users`, que ya tiene permisos.

**23. En un módulo que extiende un método de otro, para no perder el comportamiento original
hay que:**
a) copiar y pegar el código  b) **llamar a `super()`**  c) borrar el método base  d) usar
`copy=False`
**✔ b)** Herencia de métodos con `super()`.

**24. En el manifest, `real_estate_menuitem.xml` debe incluirse:**
a) antes que las vistas/acciones  b) **después** (el menú referencia la acción por XML ID)
c) en `demo`  d) da igual el orden
**✔ b)** El orden de `data` es el orden de carga.

**25. `@api.ondelete(at_uninstall=False)` es preferible a redefinir `unlink()` porque:**
a) es más rápido  b) solo valida/bloquea el borrado sin reimplementar la lógica ni romper la
desinstalación  c) permite borrar más registros  d) evita usar UserError
**✔ b)** Forma recomendada por Odoo para proteger registros.

---

## Tema 18 — Simulacro de código: snippets y qué pasa

> Misma mecánica: mirá el snippet, pensá la respuesta y recién después la ✔.

**1. Definís un campo y lo verificás en pgweb:**

```python
total_area = fields.Float(string="Superficie total", compute="_compute_total_area")
```

¿Aparece `total_area` como columna en la tabla `estate_property`? ¿Y en el formulario?
**✔ No hay columna** (no tiene `store=True`); **sí se ve en el formulario**, porque Odoo lo
calcula en memoria al renderizar la vista.

**2.** (Mismo campo, ahora con `store=True` pero **sin** `@api.depends`.) El usuario modifica
`living_area` y guarda. ¿Qué valor tiene `total_area`?
**✔ El valor viejo (desactualizado)**: hay columna, pero Odoo no conoce las dependencias →
no dispara recomputo. Con `@api.depends("living_area", "garden_area")` sí se recalcula.

**3. En la consola / un método:**

```python
record.tag_ids = [Command.clear()]
# vs
record.tag_ids = [Command.delete(tag.id)]
```

¿Cuál deja a la propiedad sin etiquetas **y además borra** la etiqueta de la BD?
**✔ `delete`** (rompe vínculo **y** borra el registro). `clear()` solo vacía los vínculos
(las etiquetas siguen existiendo). Y `unlink(id)` desvincula **una sola** sin borrarla.

**4. Manifest:**

```python
"data": [
    "views/real_estate_menuitem.xml",      # action="action_estate_property"
    "views/estate_property_views.xml",
],
```

¿Qué pasa al actualizar el módulo?
**✔ Falla**: el menú referencia por `ref` la acción (`External ID not found`) que **todavía
no se creó**. El orden de `data` es el orden de carga → **acciones/vistas primero**.

**5. `ir.model.access.csv`:**

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_ep_all,estate.property.all,model_estate_property,,1,1,1,1
```

¿Quién tiene estos permisos?
**✔ Todos los usuarios** (grupo vacío = sin restricción), incluidos portal y público. Para
restringirlo hay que poner el XML ID del grupo (p. ej. `real_estate.group_estate_manager`).

**6.**

```python
offer_ids = fields.One2many("estate.property.offer", string="Ofertas")
```

¿Funciona? ¿Por qué?
**✔ No**: falta el **`inverse_name`** (`"property_id"`). Sin ese Many2one del hijo Odoo no
sabe cómo resolver la relación inversa (y la O2M es virtual: no tiene columna propia).

**7.**

```python
self.env["estate.property"].search([("total_area", ">", 50)])
```

`total_area` es computado **sin store**. ¿Qué ocurre?
**✔ No se puede buscar** por ese campo (no hay columna): Odoo rechaza el filtro ("campo no
almacenado/no buscable"). Para buscar: `store=True` o implementar un método `_search`.

**8. Onchange:**

```python
@api.onchange("garden")
def _onchange_garden(self):
    self.garden_area = 10 if self.garden else 0
```

a) El usuario tilda Jardín y aprieta **Cancelar**: ¿queda `garden_area = 10`?
b) Otro módulo hace `prop.write({"garden": True})`: ¿corre el onchange?
**✔ a) No** (el onchange vive en el formulario y no persiste; cancelar descarta).
**✔ b) No**: los onchange corren **solo en el cliente al editar**; `write()` desde código no
los dispara.

**9.**

```python
self.env["estate.property"].browse(ids).write({"state": "canceled"})
```

con 5 ids. ¿Qué pasa?
**✔ Los 5 registros** quedan `canceled`: `write()` aplica el **mismo diccionario** a todo el
recordset. Por eso los métodos propios iteran `for record in self`.

**10. Dominio:**

```python
[("|", ("state", "=", "new"), ("state", "=", "canceled"))]
```

¿Qué selecciona?
**✔ Propiedades Nuevas O Canceladas**: `|` combina los **dos operandos siguientes**; sin
prefijos, las tuplas se combinan con **Y**.

**11. Duplicar (Acción → Duplicar) un registro con:**

```python
selling_price = fields.Float(string="Precio de venta", copy=False)
state = fields.Selection(..., default="new", copy=False)
salesman_id = fields.Many2one(..., copy=False, default=lambda self: self.env.user)
```

¿Qué valores tiene el duplicado en esos tres campos?
**✔** `selling_price` → **0.0** (no se copia), `state` → su **default** ("new"),
`salesman_id` → **el usuario que duplica** (default corriente, no el original). Los campos
`copy=False` no heredan el valor del original.

**12.**

```python
@api.constrains("price")
def _check_price(self):
    if self.price <= 0:
        raise ValidationError("Precio inválido.")
```

a) Se dispara al guardar desde el formulario? b) Al `create()` de otro módulo vía ORM?
c) Con un `UPDATE` hecho a mano en pgweb?
**✔ a) Sí** (guardar usa `create`/`write` del ORM). **✔ b) Sí.**
**✔ c) No**: `@api.constrains` es Python en el ORM; para SQL directo hace falta un
`_sql_constraints`.

**13. En `estate.property.tag`:**

```python
_sql_constraints = [("unique_tag_name", "UNIQUE(name)", "El nombre debe ser único")]
```

Se inserta una etiqueta `name='Luminosa'` existente. ¿Qué ocurre?
**✔ Rechaza PostgreSQL** y Odoo muestra el mensaje "El nombre debe ser único". Por eso
hay que **limpiar duplicados antes** de agregar el constraint o la actualización del módulo
falla.

**14.**

```python
@api.ondelete(at_uninstall=False)
def _unlink_if_new_or_cancelled(self):
    for record in self:
        if record.state not in ("new", "canceled"):
            raise UserError("Solo se pueden borrar Nuevas o Canceladas.")
```

Se intenta `prop.unlink()` con `state == 'sold'`. ¿Y si el módulo se desinstala?
**✔ Primero**: lanza **UserError** y **no borra**. **Al desinstalar** (`at_uninstall=False`)
Odoo **se salta** este chequeo para poder limpiar sus registros; con `unlink()` redefinido y
bloqueo fijo, la desinstalación se rompería.

**15.**

```python
class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "salesman_id")
```

¿Se crea una tabla nueva? ¿Hay que agregar líneas en `ir.model.access.csv`?
**✔ No a ambas**: `_inherit` **sin `_name`** fusiona en el modelo/tabla existente
`res_users`, que **ya tiene sus permisos**. (Haría falta ACL si hubiera `_name` nuevo.)

**16. Redefinición "trucha" de `create`:**

```python
@api.model_create_multi
def create(self, vals_list):
    for vals in vals_list:
        if vals.get("price", 0) <= 0:
            raise UserError("Precio inválido")
    # ¿falta algo?
```

¿Qué pasa si no se agrega nada más?
**✔ No se crea ningún registro**: falta **`records = super().create(vals_list)`** y
`return records`. Toda redefinición de métodos core debe **llamar a `super()`**.

**17. Acción con `view_mode = "form"` únicamente.**
**✔** Al usarla (menú/botón) Odoo abre **directamente el formulario** — sin listado previo.
Con `"list"` solo, en cambio, **no hay forma de entrar al detalle** de un registro.

**18.**

```python
property_type_id = fields.Many2one(related="property_id.property_type_id")        # sin store
```

En la vista de todas las ofertas: ¿se puede "Agrupar por tipo de propiedad"?
**✔ No** (no hay columna → no se puede agrupar ni buscar). Con **`store=True`** sí, que es
justo lo que pide la guía para poder agrupar las ofertas por tipo.

**19.** La propiedad tiene etiquetas `[A, B, C]` y se ejecuta:

```python
record.tag_ids = [Command.set([tag_b.id])]
```

**✔** Queda **solo B**: `set` **reemplaza** toda la relación por la lista dada (desvincula A
y C; no las borra). `clear()` la dejaría **vacía**; `link(tag_b.id)` dejaría `[A, B, C]`.

**20. En la vista:**

```xml
<button name="action_sold" string="Vender" type="object"/>
```

¿A qué llama y qué pasa si el método no existe?
**✔** Al método **`action_sold(self)`** del modelo, con el registro actual (es `type="object"`;
`type="action"` en cambio dispararía otra acción de Odoo). Si el método no existe → **error**
al hacer clic (y si no valida con `UserError`, el estado podría quedar en un valor inválido).

**21.**

```python
date_availability = fields.Date(
    copy=False,
    default=lambda self: fields.Date.add(fields.Date.today(), months=3),
)
```

¿Qué valor tiene el default en un registro creado **el 1 de julio**?
**✔ 1 de octubre** (hoy + 3 meses). Es una **función**, evaluada **al crear cada registro**
(con el `self`/env actual), no al importar el módulo. `copy=False`: al duplicar, no se copia
la fecha original.

**22.** Un campo con `compute` **y** `inverse` (`date_deadline` / `validity`):
¿qué pasa si el usuario escribe la fecha a mano?
**✔** Odoo deja de tratarlo como solo lectura y llama al **inverso**, que recalcula
`validity = date_deadline - create_date`. Sin `inverse`, el campo no sería editable.

---

## Tema 19 — Checklist final

Antes del examen, asegurate de poder explicar/enunciar de memoria:

- [ ] Definición de ERP y qué lo hace "integrado" + qué es Odoo (open source, Python, PyMEs,
      Community vs Enterprise).
- [ ] Estructura de carpetas de un módulo y para qué sirve cada una; rol de `__init__.py` y
      `__manifest__.py` (claves `depends`, `data`, `demo`, `application`, `license`) y **por
      qué el orden de `data` importa**.
- [ ] Qué es Doodba, para qué sirve **pgweb** (ver columnas/campos automáticos) y **wdb**
      (`set_trace()`), para qué el modo debug y SuperUsuario.
- [ ] Todos los tipos de campo y los atributos `required/default/copy/string`; campos
      automáticos (`id`, `create_*`, `write_*`); naming `_id`/`_ids`.
- [ ] Tipos de usuario; grupos; por qué crearlos desde el módulo; categorías; **leer y
      escribir `ir.model.access.csv`**; qué pasa sin grupo.
- [ ] Many2one vs One2many vs Many2many: dónde vive la FK, `comodel_name`, `inverse_name`,
      por qué tag = M2M, por qué la O2M es virtual.
- [ ] Vista list/form/search: `view_mode`, widgets (`statusbar`, `many2many_tags`, ribbon),
      `editable`, acciones vs menús, herencia de vistas con xpath.
- [ ] Campo computado: método `_compute_*`, store vs no store (pgweb), `@api.depends`,
      criterios store/no-store, related (+store), inverse, related vs compute para
      `offer_partner_ids`.
- [ ] onchange (no bloqueante, warning) vs UserError vs `@api.constrains` vs
      `_sql_constraints`.
- [ ] Comandos relacionales **0 a 6** y helpers `Command` (unlink vs delete, clear vs set).
- [ ] Herencia: `_inherit` (con/sin `_name`), `_inherits`, `super()` en métodos, herencia de
      vistas, `depends` entre módulos (`estate_account`).
- [ ] `@api.ondelete` vs `unlink()`; redefinir `create()` con `@api.model_create_multi`.
- [ ] Los 25 ítems del Tema 15 (los "¿por qué?" de la guía) — son los más probables.

> Consejo de estudio: los ejercicios ya los tenés hechos; repasá **tu propio código**
> (`real_estate`, `estate_account`) preguntándote *"¿por qué está escrito así?"* — con este
> resumen como respaldo.

---

## Anexo — Hoja de ruta (repaso de 1 página)

> Para el repaso de las 2 horas previas. Si entendés estas 20 líneas, entendés la materia.

### Las 10 reglas de oro

1. **`store` decide si vive en la BD; `@api.depends` decide cuándo se recalcula.** Sin store →
   no hay columna (no se busca ni agrupa); con store y sin depends → no se recalcula.
2. **`related` es un compute abreviado**: por defecto no se guarda y es readonly; con
   `store=True` pasa a poder buscarse/agruparse. **`inverse`** hace editable un compute.
3. **La One2many es virtual** (FK en el hijo → `inverse_name`); **Many2many crea tabla
   intermedia**; **Many2one pone la FK acá**.
4. **Todo lo que rompe la integridad se valida en backend**: `UserError` en botones/métodos,
   `@api.constrains` en create/write, `_sql_constraints` en SQL. El `onchange` **solo avisa**.
5. **Seguridad por capas**: `ir.model.access.csv` = permisos por **modelo** (CRUD en 4
   columnas); sin grupo en la fila → aplica **a todos**; sin fila → **AccessError**.
6. **Orden de `data` = orden de carga**: grupos → ACL CSV → vistas/acciones → menús.
7. **Herencia**: `_inherit` sin `_name` = mismo modelo/tabla (sin ACL nueva); con `_name` =
   modelo nuevo; **siempre `super()`** en métodos; vistas con `inherit_id` + `xpath`.
8. **Comandos relacionales 0-6**: create y vincula / update / **delete = borra** /
   **unlink = desvincula** / link / clear = todos afuera / set = reemplaza exacto.
9. **`@api.ondelete` para proteger borrados** (valida y lanza; no reimplementa `unlink`;
   `at_uninstall=False` no rompe la desinstalación).
10. **`copy=False` = no se copia al duplicar**; `default` con lambda se evalúa por registro;
    `required` = UI + NOT NULL.

### Palabra clave en la pregunta → concepto

| Si la pregunta dice... | Pensá en... |
|---|---|
| "no aparece en pgweb pero sí en la vista" | campo computado **sin store** |
| "ya no se recalcula / quedó desactualizado" | `store=True` **sin `@api.depends`** |
| "agrupar por X" / "buscar por X" | ¿X **tiene columna**? (store o related store) |
| "el usuario ingresa la fecha a mano" | **`inverse=`** |
| "adviene pero no bloquea / posible tipeo" | **`onchange` con `warning`** |
| "no puede ofertar dos veces" | `UNIQUE(partner_id, property_id)` |
| "desvincular vs borrar" | Command **unlink(3)** vs **delete(2)** |
| "no se ven los menús" | **permisos/ACL** (o actualización/caché) → SuperUsuario |
| "extender `res.users` / módulo nativo" | **`_inherit` sin `_name`** + `super()` + herencia de vista |
| "crear factura al vender" | `estate_account`: `move_type="out_invoice"` + `Command.create` en `line_ids` |
| "cuándo sí y cuándo no almacenar" | ¿se busca? ¿se agrupa? ¿se muestra en lista? ¿depende de otro modelo? |

### Fichas exprés

- **Comandos:** `(0,0,v)` create+link · `(1,id,v)` update · `(2,id)` delete · `(3,id)` unlink ·
  `(4,id)` link · `(5)` clear · `(6,0,ids)` set → helpers `Command.*` desde `odoo import Command`.
- **Usuarios:** interno `base.group_user` · portal · público · SuperUsuario = id=1, ignora ACL.
- **CSV:** `model_estate_property` (puntos → `_`) + `perm_read/write/create/unlink` (1/0).
- **Tipos de campo:** `Char/Text/Integer/Float/Boolean/Date/Datetime/Selection` +
  `m2o(_id) / o2m(_ids) / m2m(_ids)`.
- **Form:** `header` (botones + `statusbar`) → `sheet` (ribbon, `h1`, `group`×2 = 2 columnas,
  `notebook/page`) → botón `type="object"` llama al método.
- **Search:** `<field>` = buscar · `filter domain` = filtro · `filter context group_by` = agrupar
  (`create_date:month` para por mes) · "mío" = `[('create_uid', '=', uid)]`.
- **Errores:** `UserError` (lógica de negocio) · `ValidationError` (constrains) ·
  `AccessError` (sin permisos) · error SQL (constraint único).
- **Puertos guía (Odoo 18):** Odoo 18069 · pgweb 18081 · wdb 18984 · MailHog 18025
  (tu entorno Odoo 19: 19069 / 19081 / 19984 / 19025).

