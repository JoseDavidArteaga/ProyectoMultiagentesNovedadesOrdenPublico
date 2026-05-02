"""
Modelo canónico Vigía Cauca v2 (Neo4j) — resumen para prompts de los agentes.
Fuente de verdad: CONTEXTO.md y data/raw/vigia_cauca_neo4j.cypher
"""

GRAPH_SCHEMA_FOR_LLM = """
## Nodos y propiedades (Vigía Cauca v2)

### NOVEDAD
- id (STRING), descripcion (STRING), fecha (DATE date("YYYY-MM-DD")), hora (TIME time("HH:MM:SS")),
  fuente (STRING), creado_en (DATETIME)
- categoria (ENUM): Enfrentamiento | Hostigamiento | Atentado Terrorista | Ataque con Dron |
  Homicidio | Secuestro | Retén Ilegal | Reclutamiento Ilícito | Acción de Protesta |
  Hallazgo de Material | Otro
- nivel_confianza (ENUM): Confirmado | Preliminar | En verificación | No confirmado
- visibilidad (ENUM): Público | Privado   ← el campo se llama "visibilidad", NO "nivel_visibilidad"

### VICTIMA
- id, nombre, edad, genero (Masculino|Femenino|LGBTI+|No especificado),
  grupo_poblacional (Campesino/a|Indígena|Afrocolombiano/a|Niño|Adolescente|Adulto|Adulto Mayor|Discapacidad|Ninguno / No especificado),
  condicion (STRING)

### AFECTACION_HUMANA
- id, heridos_civiles, heridos_fuerza_publica, fallecidos_civiles, fallecidos_fuerza_publica,
  desplazados, reclutamiento_menores_flag (Sí|No|No aplica|En investigación), observaciones

### ACTOR
- id, nombre (ENUM): Fuerza Pública | Grupo Armado Organizado | ELN | Segunda Marquetalia |
  Civil / Comunidad | No Identificado | Otro
- tipo (STRING): Institucional | GAO | Civil | Desconocido | Otro

### USUARIO
- id, nombre, email, rol (Administrador|Operador|Visitante), activo, creado_en

### Ubicación
- MUNICIPIO (id, nombre, departamento, area)
- COMUNA, BARRIO, CORREGIMIENTO, VEREDA, SECTOR, TERRITORIO_INDIGENA (ver CONTEXTO para propiedades)

## Relaciones (dirección fija — no invertir)
- (ACTOR)-[:PARTICIPA_EN {rol: Agresor|Presunto autor|Participante}]->(NOVEDAD)
- (NOVEDAD)-[:OCURRE_EN]->(lugar)   — lugar = cualquier nivel geográfico
- (USUARIO)-[:REPORTA {fecha_reporte}]->(NOVEDAD)
- (NOVEDAD)-[:TIENE_VICTIMA]->(VICTIMA)
- (NOVEDAD)-[:GENERA]->(AFECTACION_HUMANA)
- (VICTIMA)-[:REGISTRA]->(AFECTACION_HUMANA)
- (padre)-[:CONTIENE {tipo: urbano|rural solo desde MUNICIPIO hacia COMUNA/CORREGIMIENTO}]->(hijo)
- (TERRITORIO_INDIGENA)-[:COMPRENDE]->(VEREDA)

## Jerarquía geográfica
Para filtrar por municipio, subir/bajar con:
MATCH (m:MUNICIPIO {nombre: $nombre})-[:CONTIENE*1..4]->(lugar)<-[:OCURRE_EN]-(n:NOVEDAD)
SIEMPRE usar CONTIENE*1..4 entre MUNICIPIO y el lugar del hecho.
""".strip()
