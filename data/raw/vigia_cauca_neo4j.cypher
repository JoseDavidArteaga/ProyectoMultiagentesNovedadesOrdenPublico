// =============================================================
// VIGÍA CAUCA — Script Neo4j (Cypher)
// Bitnova · Dominios v2
// =============================================================


// -------------------------------------------------------------
// 1. CONSTRAINTS E ÍNDICES
// -------------------------------------------------------------

CREATE CONSTRAINT novedad_id       IF NOT EXISTS FOR (n:NOVEDAD)            REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT victima_id       IF NOT EXISTS FOR (v:VICTIMA)            REQUIRE v.id IS UNIQUE;
CREATE CONSTRAINT afectacion_id    IF NOT EXISTS FOR (a:AFECTACION_HUMANA)  REQUIRE a.id IS UNIQUE;
CREATE CONSTRAINT actor_id         IF NOT EXISTS FOR (a:ACTOR)              REQUIRE a.id IS UNIQUE;
CREATE CONSTRAINT usuario_id       IF NOT EXISTS FOR (u:USUARIO)            REQUIRE u.id IS UNIQUE;

// Ubicación — un constraint por nivel
CREATE CONSTRAINT municipio_id     IF NOT EXISTS FOR (m:MUNICIPIO)          REQUIRE m.id IS UNIQUE;
CREATE CONSTRAINT comuna_id        IF NOT EXISTS FOR (c:COMUNA)             REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT barrio_id        IF NOT EXISTS FOR (b:BARRIO)             REQUIRE b.id IS UNIQUE;
CREATE CONSTRAINT corregimiento_id IF NOT EXISTS FOR (c:CORREGIMIENTO)      REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT vereda_id        IF NOT EXISTS FOR (v:VEREDA)             REQUIRE v.id IS UNIQUE;
CREATE CONSTRAINT sector_id        IF NOT EXISTS FOR (s:SECTOR)             REQUIRE s.id IS UNIQUE;
CREATE CONSTRAINT territorio_id    IF NOT EXISTS FOR (t:TERRITORIO_INDIGENA) REQUIRE t.id IS UNIQUE;

// Índices de búsqueda frecuente
CREATE INDEX novedad_categoria     IF NOT EXISTS FOR (n:NOVEDAD)            ON (n.categoria);
CREATE INDEX novedad_fecha         IF NOT EXISTS FOR (n:NOVEDAD)            ON (n.fecha);
CREATE INDEX novedad_confianza     IF NOT EXISTS FOR (n:NOVEDAD)            ON (n.nivel_confianza);
CREATE INDEX novedad_visibilidad   IF NOT EXISTS FOR (n:NOVEDAD)            ON (n.visibilidad);
CREATE INDEX municipio_nombre      IF NOT EXISTS FOR (m:MUNICIPIO)          ON (m.nombre);
CREATE INDEX actor_nombre          IF NOT EXISTS FOR (a:ACTOR)              ON (a.nombre);
CREATE INDEX victima_grupo         IF NOT EXISTS FOR (v:VICTIMA)            ON (v.grupo_poblacional);
CREATE INDEX usuario_rol           IF NOT EXISTS FOR (u:USUARIO)            ON (u.rol);


// -------------------------------------------------------------
// 2. JERARQUÍA GEOGRÁFICA
//
// Estructura:
//   MUNICIPIO
//   ├── (urbano) COMUNA -[:CONTIENE]-> BARRIO
//   └── (rural)  CORREGIMIENTO -[:CONTIENE]-> VEREDA -[:CONTIENE]-> SECTOR
//
//   MUNICIPIO -[:CONTIENE]-> TERRITORIO_INDIGENA
//     (puede solaparse con veredas/corregimientos)
//
// NOVEDAD -[:OCURRE_EN]-> cualquier nivel de la jerarquía
// -------------------------------------------------------------

// — Municipios —
MERGE (:MUNICIPIO {id: "mun-1", nombre: "Popayán",     departamento: "Cauca", area: "Mixta"});
MERGE (:MUNICIPIO {id: "mun-2", nombre: "Corinto",     departamento: "Cauca", area: "Mixta"});
MERGE (:MUNICIPIO {id: "mun-3", nombre: "Toribío",     departamento: "Cauca", area: "Mixta"});
MERGE (:MUNICIPIO {id: "mun-4", nombre: "Buenos Aires",departamento: "Cauca", area: "Mixta"});
MERGE (:MUNICIPIO {id: "mun-5", nombre: "Jambaló",     departamento: "Cauca", area: "Mixta"});

// — Comunas (área urbana) —
MATCH (m:MUNICIPIO {id: "mun-1"})
MERGE (c:COMUNA {id: "com-1", nombre: "Comuna 1", numero: 1})
MERGE (m)-[:CONTIENE {tipo: "urbano"}]->(c);

MATCH (m:MUNICIPIO {id: "mun-1"})
MERGE (c:COMUNA {id: "com-2", nombre: "Comuna 2", numero: 2})
MERGE (m)-[:CONTIENE {tipo: "urbano"}]->(c);

// — Barrios (pertenecen a una comuna) —
MATCH (c:COMUNA {id: "com-1"})
MERGE (b:BARRIO {id: "bar-1", nombre: "Alfonso López"})
MERGE (c)-[:CONTIENE]->(b);

MATCH (c:COMUNA {id: "com-1"})
MERGE (b:BARRIO {id: "bar-2", nombre: "El Uvo"})
MERGE (c)-[:CONTIENE]->(b);

MATCH (c:COMUNA {id: "com-2"})
MERGE (b:BARRIO {id: "bar-3", nombre: "Bella Vista"})
MERGE (c)-[:CONTIENE]->(b);

// — Corregimientos (área rural) —
MATCH (m:MUNICIPIO {id: "mun-2"})
MERGE (cr:CORREGIMIENTO {id: "crr-1", nombre: "Corregimiento La Paz", corregidor: "Pedro Sánchez"})
MERGE (m)-[:CONTIENE {tipo: "rural"}]->(cr);

MATCH (m:MUNICIPIO {id: "mun-3"})
MERGE (cr:CORREGIMIENTO {id: "crr-2", nombre: "Corregimiento El Palo", corregidor: "No asignado"})
MERGE (m)-[:CONTIENE {tipo: "rural"}]->(cr);

MATCH (m:MUNICIPIO {id: "mun-4"})
MERGE (cr:CORREGIMIENTO {id: "crr-3", nombre: "Corregimiento La Balsa", corregidor: "Rosa Carabalí"})
MERGE (m)-[:CONTIENE {tipo: "rural"}]->(cr);

// — Veredas (pertenecen a un corregimiento) —
MATCH (cr:CORREGIMIENTO {id: "crr-1"})
MERGE (v:VEREDA {id: "ver-1", nombre: "Vereda Mandivá"})
MERGE (cr)-[:CONTIENE]->(v);

MATCH (cr:CORREGIMIENTO {id: "crr-2"})
MERGE (v:VEREDA {id: "ver-2", nombre: "Vereda Los Monos"})
MERGE (cr)-[:CONTIENE]->(v);

MATCH (cr:CORREGIMIENTO {id: "crr-3"})
MERGE (v:VEREDA {id: "ver-3", nombre: "Vereda La Balsa"})
MERGE (cr)-[:CONTIENE]->(v);

MATCH (cr:CORREGIMIENTO {id: "crr-3"})
MERGE (v:VEREDA {id: "ver-4", nombre: "Vereda El Ceral"})
MERGE (cr)-[:CONTIENE]->(v);

// — Sectores (parte específica de una vereda) —
MATCH (v:VEREDA {id: "ver-1"})
MERGE (s:SECTOR {id: "sec-1", nombre: "Sector La Montaña"})
MERGE (v)-[:CONTIENE]->(s);

MATCH (v:VEREDA {id: "ver-3"})
MERGE (s:SECTOR {id: "sec-2", nombre: "Sector Bolivia"})
MERGE (v)-[:CONTIENE]->(s);

MATCH (v:VEREDA {id: "ver-3"})
MERGE (s:SECTOR {id: "sec-3", nombre: "Sector Betania"})
MERGE (v)-[:CONTIENE]->(s);

// — Territorios indígenas —
// Nota: un territorio indígena puede solaparse geográficamente
// con veredas y corregimientos. Se modela como nodo independiente
// que también puede relacionarse con éstos mediante [:COMPRENDE].
MATCH (m:MUNICIPIO {id: "mun-3"})
MERGE (ti:TERRITORIO_INDIGENA {
  id:      "ti-1",
  nombre:  "Resguardo Indígena de Toribío",
  pueblo:  "Nasa",
  cabildo: "Cabildo de Toribío"
})
MERGE (m)-[:CONTIENE]->(ti);

MATCH (m:MUNICIPIO {id: "mun-5"})
MERGE (ti:TERRITORIO_INDIGENA {
  id:      "ti-2",
  nombre:  "Resguardo Indígena de Jambaló",
  pueblo:  "Nasa",
  cabildo: "Cabildo de Jambaló"
})
MERGE (m)-[:CONTIENE]->(ti);

// Relación territorio ↔ vereda (solapamiento geográfico)
MATCH (ti:TERRITORIO_INDIGENA {id: "ti-1"})
MATCH (v:VEREDA {id: "ver-2"})
MERGE (ti)-[:COMPRENDE]->(v);


// -------------------------------------------------------------
// 3. ACTORES
// -------------------------------------------------------------

MERGE (:ACTOR {id: "actor-1", nombre: "Fuerza Pública",          tipo: "Institucional"});
MERGE (:ACTOR {id: "actor-2", nombre: "Grupo Armado Organizado", tipo: "GAO"});
MERGE (:ACTOR {id: "actor-3", nombre: "ELN",                     tipo: "GAO"});
MERGE (:ACTOR {id: "actor-4", nombre: "Segunda Marquetalia",     tipo: "GAO"});
MERGE (:ACTOR {id: "actor-5", nombre: "Civil / Comunidad",       tipo: "Civil"});
MERGE (:ACTOR {id: "actor-6", nombre: "No Identificado",         tipo: "Desconocido"});
MERGE (:ACTOR {id: "actor-7", nombre: "Otro",                    tipo: "Otro"});


// -------------------------------------------------------------
// 4. USUARIOS
// rol:    Administrador | Operador | Visitante
// activo: true | false
// -------------------------------------------------------------

MERGE (:USUARIO {
  id:        "user-1",
  nombre:    "Ana Torres",
  email:     "ana.torres@vigiacauca.gov.co",
  rol:       "Administrador",
  activo:    true,
  creado_en: datetime("2024-01-15T08:00:00")
});

MERGE (:USUARIO {
  id:        "user-2",
  nombre:    "Carlos Muñoz",
  email:     "carlos.munoz@vigiacauca.gov.co",
  rol:       "Operador",
  activo:    true,
  creado_en: datetime("2024-02-10T09:30:00")
});

MERGE (:USUARIO {
  id:        "user-3",
  nombre:    "Visitante Demo",
  email:     "demo@vigiacauca.gov.co",
  rol:       "Visitante",
  activo:    false,
  creado_en: datetime("2024-03-01T00:00:00")
});


// -------------------------------------------------------------
// 5. NOVEDADES + RELACIONES
//
// OCURRE_EN apunta al nodo más específico conocido:
//   sector > vereda > corregimiento > municipio
//   barrio  > comuna > municipio
//   territorio_indigena
//
// categoria:       Enfrentamiento | Hostigamiento | Atentado Terrorista |
//                  Ataque con Dron | Homicidio | Secuestro | Retén Ilegal |
//                  Reclutamiento Ilícito | Acción de Protesta |
//                  Hallazgo de Material | Otro
// nivel_confianza: Confirmado | Preliminar | En verificación | No confirmado
// visibilidad:     Público | Privado
// -------------------------------------------------------------

// — Novedad 1: ocurre en un sector rural específico —
MATCH (actor:ACTOR  {id: "actor-3"})
MATCH (usr:USUARIO  {id: "user-2"})
MATCH (loc:SECTOR   {id: "sec-1"})
CREATE (n:NOVEDAD {
  id:              "nov-001",
  categoria:       "Hostigamiento",
  descripcion:     "Hostigamiento a unidad militar en el sector La Montaña, vereda Mandivá.",
  fecha:           date("2024-04-10"),
  hora:            time("14:30:00"),
  nivel_confianza: "Confirmado",
  visibilidad:     "Público",
  fuente:          "Informe de unidad",
  creado_en:       datetime()
})
CREATE (actor)-[:PARTICIPA_EN {rol: "Agresor"}]->(n)
CREATE (n)-[:OCURRE_EN]->(loc)
CREATE (usr)-[:REPORTA {fecha_reporte: datetime()}]->(n);

// — Novedad 2: ocurre en un territorio indígena —
MATCH (actor:ACTOR              {id: "actor-4"})
MATCH (usr:USUARIO              {id: "user-2"})
MATCH (loc:TERRITORIO_INDIGENA  {id: "ti-1"})
CREATE (n:NOVEDAD {
  id:              "nov-002",
  categoria:       "Ataque con Dron",
  descripcion:     "Artefacto explosivo lanzado desde dron sobre posición en resguardo de Toribío.",
  fecha:           date("2024-05-02"),
  hora:            time("03:15:00"),
  nivel_confianza: "Preliminar",
  visibilidad:     "Privado",
  fuente:          "Reporte policial",
  creado_en:       datetime()
})
CREATE (actor)-[:PARTICIPA_EN {rol: "Agresor"}]->(n)
CREATE (n)-[:OCURRE_EN]->(loc)
CREATE (usr)-[:REPORTA {fecha_reporte: datetime()}]->(n);

// — Novedad 3: ocurre en una vereda (sin sector identificado) —
MATCH (actor:ACTOR  {id: "actor-6"})
MATCH (usr:USUARIO  {id: "user-1"})
MATCH (loc:VEREDA   {id: "ver-3"})
CREATE (n:NOVEDAD {
  id:              "nov-003",
  categoria:       "Homicidio",
  descripcion:     "Cuerpo hallado en vereda La Balsa. Actor no identificado.",
  fecha:           date("2024-05-18"),
  hora:            time("07:00:00"),
  nivel_confianza: "En verificación",
  visibilidad:     "Privado",
  fuente:          "CTI - Fiscalía",
  creado_en:       datetime()
})
CREATE (actor)-[:PARTICIPA_EN {rol: "Presunto autor"}]->(n)
CREATE (n)-[:OCURRE_EN]->(loc)
CREATE (usr)-[:REPORTA {fecha_reporte: datetime()}]->(n);

// — Novedad 4: ocurre en un barrio urbano —
MATCH (actor:ACTOR  {id: "actor-5"})
MATCH (usr:USUARIO  {id: "user-2"})
MATCH (loc:BARRIO   {id: "bar-1"})
CREATE (n:NOVEDAD {
  id:              "nov-004",
  categoria:       "Acción de Protesta",
  descripcion:     "Bloqueo vial en barrio Alfonso López, Popayán.",
  fecha:           date("2024-06-03"),
  hora:            time("09:00:00"),
  nivel_confianza: "Confirmado",
  visibilidad:     "Público",
  fuente:          "Policía Metropolitana",
  creado_en:       datetime()
})
CREATE (actor)-[:PARTICIPA_EN {rol: "Participante"}]->(n)
CREATE (n)-[:OCURRE_EN]->(loc)
CREATE (usr)-[:REPORTA {fecha_reporte: datetime()}]->(n);


// -------------------------------------------------------------
// 6. VÍCTIMAS
// genero:            Masculino | Femenino | LGBTI+ | No especificado
// grupo_poblacional: Campesino/a | Indígena | Afrocolombiano/a |
//                    Nino | Adolecente | Adulto | Adulto_Mayor |
//                    Discapacidad | Ninguno / No especificado
// -------------------------------------------------------------

MATCH (n:NOVEDAD {id: "nov-001"})
CREATE (v:VICTIMA {
  id:                "vic-001",
  nombre:            "No identificado",
  edad:              35,
  genero:            "Masculino",
  grupo_poblacional: "Campesino/a",
  condicion:         "Herido"
})
CREATE (n)-[:TIENE_VICTIMA]->(v);

MATCH (n:NOVEDAD {id: "nov-003"})
CREATE (v:VICTIMA {
  id:                "vic-002",
  nombre:            "Reservado",
  edad:              42,
  genero:            "Masculino",
  grupo_poblacional: "Indígena",
  condicion:         "Fallecido"
})
CREATE (n)-[:TIENE_VICTIMA]->(v);

MATCH (n:NOVEDAD {id: "nov-003"})
CREATE (v:VICTIMA {
  id:                "vic-003",
  nombre:            "Reservado",
  edad:              16,
  genero:            "Femenino",
  grupo_poblacional: "Adolecente",
  condicion:         "Desaparecida"
})
CREATE (n)-[:TIENE_VICTIMA]->(v);


// -------------------------------------------------------------
// 7. AFECTACIÓN HUMANA
// reclutamiento_menores_flag: Sí | No | No aplica | En investigación
// -------------------------------------------------------------

MATCH (n:NOVEDAD  {id: "nov-001"})
MATCH (v:VICTIMA  {id: "vic-001"})
CREATE (af:AFECTACION_HUMANA {
  id:                         "af-001",
  heridos_civiles:            1,
  heridos_fuerza_publica:     2,
  fallecidos_civiles:         0,
  fallecidos_fuerza_publica:  0,
  desplazados:                0,
  reclutamiento_menores_flag: "No aplica",
  observaciones:              "Dos uniformados con heridas leves."
})
CREATE (n)-[:GENERA]->(af)
CREATE (v)-[:REGISTRA]->(af);

MATCH (n:NOVEDAD {id: "nov-003"})
MATCH (v2:VICTIMA {id: "vic-002"})
MATCH (v3:VICTIMA {id: "vic-003"})
CREATE (af:AFECTACION_HUMANA {
  id:                         "af-002",
  heridos_civiles:            0,
  heridos_fuerza_publica:     0,
  fallecidos_civiles:         1,
  fallecidos_fuerza_publica:  0,
  desplazados:                12,
  reclutamiento_menores_flag: "En investigación",
  observaciones:              "Menor desaparecida. Posible reclutamiento bajo investigación."
})
CREATE (n)-[:GENERA]->(af)
CREATE (v2)-[:REGISTRA]->(af)
CREATE (v3)-[:REGISTRA]->(af);


// =============================================================
// 8. CONSULTAS DE EJEMPLO
// =============================================================

// -- 8.1 Subir la jerarquía desde un sector hasta el municipio
//        (útil para reportes agregados)
MATCH (s:SECTOR {nombre: "Sector La Montaña"})
      <-[:CONTIENE]-(v:VEREDA)
      <-[:CONTIENE]-(cr:CORREGIMIENTO)
      <-[:CONTIENE]-(m:MUNICIPIO)
RETURN s.nombre AS sector, v.nombre AS vereda,
       cr.nombre AS corregimiento, m.nombre AS municipio;

// -- 8.2 Todas las novedades de un municipio, sin importar
//        en qué nivel de la jerarquía ocurrieron
MATCH (m:MUNICIPIO {nombre: "Buenos Aires"})
      -[:CONTIENE*1..4]->(lugar)
      <-[:OCURRE_EN]-(n:NOVEDAD)
RETURN n.id, n.categoria, n.fecha, labels(lugar)[0] AS nivel, lugar.nombre AS lugar
ORDER BY n.fecha DESC;

// -- 8.3 Novedades en territorios indígenas con menores en riesgo
MATCH (n:NOVEDAD)-[:OCURRE_EN]->(ti:TERRITORIO_INDIGENA),
      (n)-[:GENERA]->(af:AFECTACION_HUMANA)
WHERE af.reclutamiento_menores_flag IN ["Sí", "En investigación"]
RETURN n.id, n.categoria, ti.nombre AS territorio,
       ti.pueblo AS pueblo, af.reclutamiento_menores_flag
ORDER BY n.fecha DESC;

// -- 8.4 Municipios con más novedades (agrupando toda la jerarquía)
MATCH (m:MUNICIPIO)-[:CONTIENE*1..4]->(lugar)<-[:OCURRE_EN]-(n:NOVEDAD)
RETURN m.nombre AS municipio, count(DISTINCT n) AS total_novedades
ORDER BY total_novedades DESC;

// -- 8.5 Actores más activos por tipo de área (urbano / rural)
MATCH (a:ACTOR)-[:PARTICIPA_EN]->(n:NOVEDAD)-[:OCURRE_EN]->(lugar)
WITH a, n, lugar,
     CASE
       WHEN lugar:BARRIO OR lugar:COMUNA THEN "Urbano"
       WHEN lugar:TERRITORIO_INDIGENA    THEN "Territorio indígena"
       ELSE "Rural"
     END AS area
RETURN a.nombre AS actor, area, count(n) AS total
ORDER BY total DESC;

// -- 8.6 Ruta completa: usuario → novedad → lugar → municipio
MATCH (usr:USUARIO)-[:REPORTA]->(n:NOVEDAD)-[:OCURRE_EN]->(lugar)
OPTIONAL MATCH (lugar)<-[:CONTIENE*1..3]-(m:MUNICIPIO)
RETURN usr.nombre AS operador, n.categoria,
       labels(lugar)[0] AS nivel_ubicacion,
       lugar.nombre     AS lugar,
       coalesce(m.nombre, lugar.nombre) AS municipio;
