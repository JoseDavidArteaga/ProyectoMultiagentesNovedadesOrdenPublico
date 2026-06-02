# Documentación del esquema Neo4j — Vigía Cauca

Este documento describe el modelo de datos, restricciones, índices, prácticas de ingestión, consultas útiles y verificación para la base de datos Neo4j usada en el proyecto "ProyectoMultiagentesNovedadesOrdenPublico".

## 1. Objetivo

Proveer una referencia completa para desarrolladores y operadores sobre cómo está modelada la información de eventos (`HECHO`), actores, afectaciones y la geografía (centros poblados y municipios) en Neo4j.

## 2. Entidades (Nodos) y propiedades

- `HECHO`
  - `id` (STRING, único) — identificador primario
  - `fecha` (DATE)
  - `descripcion` (STRING)
  - `fuente` (STRING, opcional)
  - `creado_en` (DATETIME, opcional)

- `Categoria`
  - `nombre` (STRING, único)

- `Actor`
  - `nombre` (STRING, único)
  - `tipo` (STRING, opcional)

- `Afectacion`
  - `nombre` (STRING, único)

- `CentroPoblado`
  - `nombre` (STRING)
  - `nombre_municipio` (STRING)
  - `lat`, `lon` (FLOAT, opcional)

- `Municipio`
  - `nombre` (STRING, único)
  - `departamento` (STRING, opcional)

- `MES`, `AÑO`
  - `MES.numero` (INT 1..12)
  - `AÑO.numero` (INT)

## 3. Relaciones y propiedades

- `(HECHO)-[:OCURRE_EN]->(CentroPoblado)`
- `(HECHO)-[:EN_MES]->(MES)`
- `(HECHO)-[:EN_AÑO]->(AÑO)`
- `(HECHO)-[:ES_DE]->(Categoria)`
- `(HECHO)-[:GENERA {cantidad: INT}]->(Afectacion)`
- `(CentroPoblado)-[:PERTENECE_A]->(Municipio)`
- `(HECHO)-[:RESPONSABLE]->(Actor)` y `(HECHO)-[:PARTICIPA]->(Actor)`

Observaciones: permitir múltiples relaciones `ES_DE` por `HECHO` si el evento cubre más de una categoría.

## 4. Constraints e índices recomendados

Ejemplo de comandos Cypher a ejecutar en la consola de administración (ajustar según versión de Neo4j):

```
CREATE CONSTRAINT ON (h:HECHO) ASSERT h.id IS UNIQUE;
CREATE CONSTRAINT ON (c:Categoria) ASSERT c.nombre IS UNIQUE;
CREATE CONSTRAINT ON (a:Actor) ASSERT a.nombre IS UNIQUE;
CREATE CONSTRAINT ON (af:Afectacion) ASSERT af.nombre IS UNIQUE;
CREATE CONSTRAINT ON (m:Municipio) ASSERT m.nombre IS UNIQUE;
CREATE CONSTRAINT ON (cp:CentroPoblado) ASSERT (cp.nombre, cp.nombre_municipio) IS NODE KEY;
CREATE INDEX FOR (n:HECHO) ON (n.fecha);
```

Nota: en Neo4j 5+ la sintaxis de constraints/indices puede diferir; revisar documentación oficial.

## 5. Flujo de ingestión recomendado

1. Preparar vocabularios controlados: `Categoria`, `Actor`, `Afectacion`, `Municipio`, `CentroPoblado`.
2. Cargar/crear nodos de referencia con `MERGE`.
3. Cargar eventos (`HECHO`) garantizando `id` único.
4. Relacionar cada `HECHO` con nodos de referencia usando `MATCH`/`MERGE`.
5. Registrar `fuente` e `ingest_job_id` para trazabilidad.

Pequeño patrón de carga (CSV -> Cypher):

```
USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM 'file:///hechos.csv' AS row
MERGE (c:Categoria {nombre: row.categoria})
MERGE (cp:CentroPoblado {nombre: row.centro_poblado, nombre_municipio: row.municipio})
MERGE (h:HECHO {id: row.id})
SET h.fecha = date(row.fecha), h.descripcion = row.descripcion, h.fuente = row.fuente
MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:ES_DE]->(c);
```

## 6. Consultas útiles

- Eventos por municipio y periodo:

```
MATCH (cp:CentroPoblado {nombre_municipio: $municipio})<-[:OCURRE_EN]-(h:HECHO)
WHERE h.fecha >= date($desde) AND h.fecha <= date($hasta)
RETURN h ORDER BY h.fecha DESC
```

- Conteo por categoría:

```
MATCH (h:HECHO)-[:ES_DE]->(cat:Categoria)
WHERE h.fecha >= date($desde) AND h.fecha <= date($hasta)
RETURN cat.nombre AS categoria, COUNT(h) AS total ORDER BY total DESC
```

- Afectaciones agregadas:

```
MATCH (h:HECHO)-[r:GENERA]->(af:Afectacion)
WHERE h.fecha >= date($desde) AND h.fecha <= date($hasta)
RETURN af.nombre, SUM(r.cantidad) AS total
```

## 7. Verificación y pruebas

- Ejecutar `src/verify_neo4j.py` (configurar las credenciales en `config.py`) para comprobar conectividad y algunos checks básicos.
- Validaciones mínimas:
  - No existen duplicados en `HECHO.id`.
  - Todos los `HECHO` tienen relación con `AÑO` y `MES` cuando `fecha` está presente.

## 8. Proveniencia y versionado

- Mantener en cada `HECHO` los campos `fuente` e `ingest_job_id`.
- Documentar cualquier cambio de vocabulario o nueva categoría en este fichero y en el historial de commits.

## 9. Operación y despliegue

- Instrucciones rápidas:

  1. Levantar Neo4j (Docker o servicio gestionado).
  2. Aplicar constraints/indices.
  3. Cargar nodos de referencia.
  4. Ejecutar scripts de ingestión (`data/raw/load_data.cypher` o pipelines CSV).

Ejemplo Docker (rápido):

```powershell
docker run --name vigia-neo4j -p7474:7474 -p7687:7687 -d -e NEO4J_AUTH=neo4j/test neo4j:5
```

## 10. Contacto y mantenimiento

Registrar en el README del proyecto quién es responsable del modelo de datos y cómo solicitar cambios.

---

Este documento debe mantenerse sincronizado con `src/vigia_schema.py` (constante `GRAPH_SCHEMA_FOR_LLM`) y con cualquier archivo `.cypher` en `data/raw/`.
