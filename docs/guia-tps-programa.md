# Guía de estudio y trabajos prácticos — ERP con Odoo

UNLa · Licenciatura en Sistemas · Departamento de Desarrollo Productivo y Tecnológico.
Materia: Programación de Sistemas ERP con Odoo. Docentes: Gustavo Siciliano, Javier Vescio.
Transcripción de la guía v20250927b (el PDF original está en `guia-tps-programa-v20250927b.pdf`).

> Nota de entorno: la guía pide Odoo 18 con puertos `18xxx`. Acá se usa Odoo 19,
> así que los puertos son `19xxx` (Odoo `19069`, pgweb `19081`, MailHog `19025`, wdb `19984`).

---

## Unidad 1 — Módulo propio, vistas, seguridad y relaciones

Creación de módulo propio (modelos y vistas). Uso de pgweb. Seguridad con grupos.
Relaciones Many2one, One2many y Many2many.

1. Generá un entorno con Odoo 18 usando Doodba Copier Template.
2. Creá un módulo custom llamado `real_estate` con los archivos `__init__.py` y
   `__manifest__.py` e instalalo.
3. Sobre el módulo anterior, creá un modelo `estate.property` con estos atributos
   y actualizá el módulo (los modelos van en la carpeta `models`, incluidos en el
   init de `models` y en el init del módulo):

   | Nombre | Tipo | Atributos del campo |
   |---|---|---|
   | name | Char | string="Título", required=True |
   | description | Text | string="Descripción" |
   | postcode | Char | string="Código Postal" |
   | date_availability | Date | string="Fecha disponibilidad" |
   | expected_price | Float | string="Precio esperado" |
   | selling_price | Float | string="Precio de venta" |
   | bedrooms | Integer | string="Habitaciones", default=2 |
   | living_area | Integer | string="Superficie cubierta" |
   | facades | Integer | string="Fachadas" |
   | garage | Boolean | string="Garage" |
   | garden | Boolean | string="Jardín" |
   | garden_orientation | Selection | selection=[('north','Norte'),('south','Sur'),('east','Este'),('west','Oeste')], default="north", string="Orientación del jardín" |
   | garden_area | Integer | string="Superficie jardín" |

4. Ingresá a pgweb y buscá el modelo creado. Aparte de tus campos, ¿qué otros
   campos adicionales se crearon?
5. Creá un `estate_property_views.xml` en `views` y definí una acción
   (`ir.actions.act_window`) para el modelo, name "Propiedades" y
   view_mode "list, form". Incluí el archivo en el manifest.
6. Creá un `real_estate_menuitem.xml` con tres niveles de menú (raíz, primer
   nivel y acción): "Inmobiliaria" → "Anuncios" → "Propiedades" (conectado a la
   acción del punto anterior). Incluilo en el manifest debajo de
   `estate_property_views.xml` y actualizá. Aún no vas a ver los menús.
   ¿Qué pasa si incluís `real_estate_menuitem.xml` después de
   `estate_property_views.xml`? Probá.
7. Todavía no ves los menús (¿por qué?). Entrá en modo debug y convertite en
   SuperUsuario (para salir, cerrá sesión y volvé a identificarte).
8. ¿Qué pasa si el view_mode de la acción tiene solo "list"? ¿Y solo "form"?
   Probá ambos y dejá "list, form" como estaba.
9. ¿Qué tipos de usuario existen en Odoo?
10. Creá `ir.model.access.csv` en `security` para que el grupo `base.group_user`
    solo pueda leer `estate.property` (incluí el csv en el manifest). ¿A qué tipo
    de usuario representa ese grupo? ¿Cómo le darías también crear, modificar y
    eliminar?
11. Desde Odoo, creá un grupo "Manager de Propiedades", asigná a tu usuario y
    dale lectura, creación, modificación y eliminación sobre `estate.property`.
    Probá crear, modificar y eliminar.
12. Formalizá lo anterior desde el módulo: creá `real_estate_res_groups.xml` en
    `security` y definí ahí el grupo "Manager de Propiedades". ¿Ventajas y
    desventajas de cambiar desde Odoo vs desde el módulo?
13. En el mismo archivo, creá el grupo "Vendedor de Propiedades".
14. En `ir.model.access.csv`, dale todos los permisos sobre `estate.property`
    al Manager, y cambiá la línea original de `base.group_user` al grupo
    Vendedor.
15. ¿Qué pasa si un usuario no pertenece al grupo Vendedor ni al Manager?
16. Creá una categoría "Inmobiliaria" y vinculá ambos grupos, para encontrarlos
    fácilmente en la vista de grupos.
17. En `estate_property_views.xml`, definí una vista search para `estate.property`:
    a. buscar por name, postcode, expected_price, bedrooms, living_area y facades;
    b. filtrar lo creado por el usuario actual;
    c. agrupar por usuario creador;
    d. agrupar por mes;
    e. agrupar por código postal.
    (Referencia: `view_account_invoice_report_search` del módulo Account.)
18. Creá un registro, y desde la lista usá Acción → Duplicar. Observá.
19. En `date_availability` y `selling_price` poné `copy=False`, repetí y compará.
20. `date_availability` por defecto = fecha actual + 3 meses (ver `today()`).
21. Agregá el campo `state` (Selection, requerido, default "Nuevo", copy=False):
    Nuevo, Oferta recibida, Oferta aceptada, Vendido, Cancelado.
22. Creá una vista de lista custom de `estate.property` con name, postcode,
    bedrooms, living_area, expected_price, selling_price y date_availability
    (sin vista propia, Odoo muestra solo el nombre).
23. Creá una vista de formulario custom: título (name) en H1 con placeholder
    "Nombre propiedad"; dos columnas (código postal + fecha disponibilidad /
    precio esperado + precio de venta); notebook con description, bedrooms,
    living_area, facades, garage en un grupo y garden, garden_area,
    garden_orientation en otro; `state` en el header con widget `statusbar`.
24. En la search: a. filtrar disponibles (Nuevo u Oferta recibida);
    b. agrupar por estado.
25. Creá el modelo `estate.property.type` con `name` Char requerido.
26. Manager: totales sobre tipos; Vendedor: solo lectura.
27. Creá `estate_property_type_views.xml` con acción "Tipos de propiedad",
    view_mode "list, form".
28. En `real_estate_menuitem.xml`: a. menú de primer nivel "Ajustes" bajo
    "Inmobiliaria"; b. menú de acción bajo el anterior conectado a la acción
    del punto 27. (Si no ves los menús: actualizá desde Odoo o borrá caché.)
29. En `estate.property`, campos many2one:
    a. `property_type_id` ("Tipo Propiedad") a `estate.property.type`;
    b. `buyer_id` ("Comprador") a `res.partner`;
    c. `salesman_id` ("Vendedor") a `res.users`, copy=False, default = usuario
    logueado.
30. En el formulario: `property_type_id` en el primer grupo sobre el código
    postal, y nueva notebook "Más info." con Comprador y Vendedor.
31. Creá `estate.property.tag` con `name` Char requerido, `_description`
    "Etiqueta de propiedad" (y agregá `_description` a los otros dos modelos:
    "Propiedad" y "Tipo de propiedad").
32. Manager: totales sobre etiquetas; Vendedor: solo lectura.
33. Creá `estate_property_tag_views.xml`:
    a. acción "Etiquetas de propiedad" solo con view_mode "list";
    b. lista custom con name y `editable="top"`;
    c. replicá en `estate_property_type_views.xml` para crear tipos desde la lista.
34. Menú de acción en "Ajustes" conectado a la acción de etiquetas.
35. En `estate.property`, `tag_ids` many2many a `estate.property.tag`
    ("Etiquetas"). ¿Por qué many2many y no many2one/one2many?
36. Agregá `tag_ids` debajo del name en el formulario y en la lista, con
    `widget="many2many_tags"` (probá con y sin widget).
37. Creá `estate.property.offer` (`_description` "Oferta sobre propiedad"):

   | Nombre | Tipo | Atributos |
   |---|---|---|
   | price | Float | string="Precio", required=True |
   | status | Selection | selection=[("accepted","Aceptada"),("refused","Rechazada")] |
   | partner_id | Many2one | comodel="res.partner", string="Ofertante", required=True |
   | property_id | Many2one | comodel="estate.property", string="Propiedad", required=True |

38. Manager: totales sobre ofertas; Vendedor: solo lectura.
39. En `estate.property`: `offer_ids = fields.One2many("estate.property.offer", "property_id", string="Ofertas")`.
    ¿Por qué el `inverse_name`? ¿Qué implica que la One2many sea virtual?
40. Creá `estate_property_offer_views.xml` con lista custom `editable="top"`
    (price, partner_id, status), sin acción. ¿Por qué no hace falta acción?
41. En `estate_property_views.xml`, página "Ofertas" con el campo `offer_ids`.

## Unidad 2 — Computados, ORM, constraints, herencia

Campos computados, `@api.depends`, `@api.onchange`, related, ORM/CRUD,
constraints, comandos relacionales, herencia, wdb.

1. En `estate.property`, campo computado `total_area` ("Superficie total") =
    living_area + garden_area, sin `store=True` (método `_compute_total_area`).
2. Mostralo en el formulario (página "Descripción") y probá modificar ambos campos.
3. En pgweb: ¿por qué no está en la tabla pero sí en la vista?
4. Agregá `store=True`, actualizá y probá: ya no se recomputa. ¿Por qué?
5. Agregá `@api.depends('living_area', 'garden_area')`, actualizá y probá:
    vuelve a computarse. ¿Por qué?
6. Cargá al menos dos ofertas con distintos precios en alguna propiedad.
7. Campo Float computado `best_offer` ("Mejor oferta") = máximo de
    `offer_ids.mapped('price')`, bajo el precio de venta. ¿Lo almacenarías?
8. Sacá el `editable="top"` de la lista de ofertas (se crean desde formulario).
9. En `estate.property.offer`: a. `validity` Integer default 7 ("Validez (días)");
    b. `date_deadline` Date ("Fecha límite"). Agregalos a la lista.
10. `date_deadline` se computa de `create_date + validity`, pero si el usuario
    ingresa la fecha, se recalcula la validez (función inversa).
11. En la oferta, campo related almacenado con el tipo de propiedad.
12. Vista formulario + menú de todas las ofertas. ¿Se pueden agrupar por tipo?
13. Onchange: al tildar `garden`, `garden_area` = 10; al destildar, = 0.
14. Onchange no bloqueante si `expected_price` < 10000 (posible error de tipeo).
    Se puede depurar con `wdb.set_trace()` y verlo en el wdb de Doodba.
15. Botones "Cancelar" y "Marcar como vendida" en el header; UserError si se
    intenta vender una cancelada o viceversa (idealmente validación backend +
    visibilidad frontend por estado). Al vender, ribbon "Vendida".
16. Botón en la lista de ofertas para aceptar una oferta: carga comprador y
    precio en la propiedad, estado "oferta aceptada" y rechaza las demás.
17. `sql_constraints` de nombre único en etiquetas y tipos de propiedad
    (verificar que no haya duplicados antes).
18. `sql_constraint` en ofertas: `UNIQUE(partner_id, property_id)` (limpiar
    duplicados antes desde la UI).
19. Campo `offer_partner_ids` con todos los partners ofertantes (computado;
    ¿serviría un related?).
20. Botón "Generar oferta automática": precio = esperado ±30% aleatorio, ofertante
    al azar entre contactos activos que aún no ofertaron (`random.choice()`).
21. Botones: a. "Sacar etiquetas" (desvincular todas);
    b. "Cargar todas las etiquetas"; c. "A estrenar" (crear+vincular si no existe).
22. Método `_unlink_if_new_or_cancelled` con `@api.ondelete()`: solo borrar en
    "Nueva" o "Cancelada". ¿Por qué ondelete en vez de redefinir `unlink()`?
23. Redefinir `create()` en `estate.property.offer`: a. solo si supera la mejor
    oferta; b. solo si la propiedad está "Nuevo" u "Oferta recibida";
    c. la propiedad pasa a "Oferta recibida".
24. Modelo que herede `res.users` con `property_ids` One2many inverso de
    `salesman_id`. ¿Hacen falta reglas en `ir.model.access.csv`?
25. `res_users_views.xml`: herencia de vista con página "Propiedades" mostrando
    `property_ids` (readonly).
26. Módulo `estate_account` (`__init__.py` + `__manifest__.py`, depende de
    `real_estate` y `account`). Instalarlo.
27. En el módulo nuevo, modelo que herede `estate.property` y redefina "Marcar
    como vendida" generando un `account.move` (`out_invoice` al comprador) con
    dos líneas (propiedad: selling_price; "Gastos administrativos": 100),
    usando comandos relacionales.

## Unidad 3

Creación de asistentes. QWeb. Generación de reportes. Creación de acciones
planificadas. Uso de MailHog. Pytest. Traducciones.

## Material teórico

- **ERP**: sistema que gestiona todas las áreas de la empresa de forma integral,
  con información centralizada en una única base de datos.
- **Odoo**: ERP open source en Python, deploy cloud u on-premise, una versión
  mayor por año; foco en PyMEs (vs SAP en grandes corps). Modular y extensible.
- **Campo related**: valor desde un campo de un modelo relacionado; por defecto
  no se almacena y es readonly (`email = fields.Char(related='partner_id.email')`).
- **Campo computado**: se calcula con un método en cada vista que lo muestra,
  salvo `store=True` (se lee de base). Con store, usar `@api.depends` para
  re-disparar el cálculo. Criterio store/no-store según búsqueda en listas,
  volumen de registros y costo (ver guía).
- **Cómputo inverso**: con `inverse=` el computado deja de ser readonly.
- **Comandos relacionales** (`from odoo import Command`): `create`, `update`,
  `delete`, `unlink`, `link`, `clear`, `set` (tuplas `(0..6, id, valores)`).

## Programa

1. **Fundamentación**: Odoo open source con presencia regional; arquitectura
   modular; la materia enseña personalización y desarrollo de módulos.
2. **Objetivos**: decidir configuración vs desarrollo; modelar con el ORM;
   implementar vistas, lógica y reportes; levantar Odoo con Doodba en contenedores.
3. **Contenidos mínimos**: ERP, Community vs Enterprise, anatomía de módulo,
   Doodba, módulo propio, herencia, seguridad, computados, relaciones, ORM/CRUD,
   wizards.
4. **Contenidos**: U1 (ERP, módulo propio, seguridad, relaciones, pgweb),
   U2 (computados, api, related, ORM, constraints, relacionales, herencia, wdb),
   U3 (wizards, QWeb, cron, MailHog, pytest, traducciones).
5. **Metodología**: clases teórico-prácticas; entorno Odoo 18+; tareas grupales
   por clase + TP cuatrimestral grupal, todo en GitHub.
6. **Actividades**: tareas grupales al final de cada clase + TP cuatrimestral grupal.
7. **Evaluación**: 75% asistencia presencial; 75% de tareas de clases virtuales;
   aprobar el TP cuatrimestral (con recuperación).
8. **Bibliografía**: Doodba Copier Template, Server Framework 101,
   Technical Training de Odoo, documentación oficial y curso técnico en video
   (ver guía PDF).
