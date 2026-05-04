"""
Modelo canónico Vigía Cauca v2 (Neo4j) — resumen para prompts de los agentes.
Fuente de verdad: CONTEXTO.md y data/raw/vigia_cauca_neo4j.cypher
"""

GRAPH_SCHEMA_FOR_LLM = """
## Nodos y propiedades (Vigía Cauca — esquema real según .cypher)

### HECHO
- id (STRING): Identificador único del evento (p.ej. 'EVT_20240117_TORIBIO_01')
- fecha (DATE): Formato date('YYYY-MM-DD')
- descripcion (STRING): Descripción del hecho

### Categoría
- nombre (ENUM): 
  'Enfrentamiento', 'Hostigamiento', 'Atentado Terrorista', 'Ataque con Dron',
  'Homicidio', 'Secuestro', 'Retén Ilegal', 'Reclutamiento Ilícito',
  'Acción de Protesta', 'Hallazgo de Material', 'Otro'

### Actor
- nombre (ENUM): 
  'Fuerza Pública', 'Grupo Armado Organizado', 'ELN', 'Segunda Marquetalia',
  'Civil / Comunidad', 'No identificado', 'Otro'

### Afectacion
- nombre (ENUM): 'Fallecido', 'Herido', 'Material', 'Desplazamiento', 'Confinamiento', 'Otro'

### CentroPoblado
- nombre (STRING): Nombre del centro poblado
- nombre_municipio (STRING): Nombre del municipio al que pertenece
- Constraint: (nombre, nombre_municipio) UNIQUE

### Municipio
- nombre (STRING): Nombre del municipio

### MES
- numero (INTEGER): 1-12

### AÑO
- numero (INTEGER): Año (p.ej. 2024)

## Relaciones (dirección fija)
- (HECHO)-[:OCURRE_EN]->(CentroPoblado): Dónde ocurrió el hecho
- (HECHO)-[:EN_MES]->(MES): Mes del evento
- (HECHO)-[:EN_AÑO]->(AÑO): Año del evento
- (HECHO)-[:ES_DE]->(Categoria): Categoría del hecho
- (HECHO)-[:GENERA {cantidad: N}]->(Afectacion): Afectaciones generadas (cantidad numérica)
- (CentroPoblado)-[:PERTENECE_A]->(Municipio): Relación geográfica

## Patrones de consulta

### Filtrar por municipio y período:
MATCH (cp:CentroPoblado {nombre_municipio: $municipio})<-[:OCURRE_EN]-(h:HECHO)
WHERE h.fecha >= date($desde) AND h.fecha <= date($hasta)
RETURN h

### Contar eventos por categoría en un período:
MATCH (h:HECHO)-[:ES_DE]->(cat:Categoria)
WHERE h.fecha >= date($desde) AND h.fecha <= date($hasta)
  AND cat.nombre = $categoria
RETURN COUNT(h) AS total

### Obtener eventos y sus afectaciones:
MATCH (h:HECHO)-[:GENERA]->(af:Afectacion)
WHERE h.fecha >= date($desde) AND h.fecha <= date($hasta)
RETURN h.descripcion, af.nombre, COUNT(*) AS cantidad
""".strip()
