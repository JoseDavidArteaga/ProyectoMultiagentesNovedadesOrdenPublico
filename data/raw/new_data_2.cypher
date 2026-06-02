CREATE (h:HECHO {
  id: 'EVT_20240701_ARGELIA_01',
  fecha: date('2024-07-01'),
  descripcion: 'Ataque mediante drones presuntamente realizado por integrantes del frente Carlos Patiño'
})

MATCH (cp:CentroPoblado {nombre: 'ARGELIA', nombre_municipio: 'ARGELIA'})
MATCH (m:MES {numero: 7})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Ataque con Dron'})
MATCH (ac:Actor {nombre: 'Grupo Armado Organizado'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:RESPONSABLE]->(ac);

CREATE (h:HECHO {
  id: 'EVT_20240701_PIENDAMO_01',
  fecha: date('2024-07-01'),
  descripcion: 'Homicidio de dos personas y retención de una tercera persona'
})

MATCH (cp:CentroPoblado {nombre: 'PIENDAMÓ', nombre_municipio: 'PIENDAMÓ - TUNÍA'})
MATCH (m:MES {numero: 7})
MATCH (a:AÑO {numero: 2024})
MATCH (c1:Categoria {nombre: 'Homicidio'})
MATCH (c2:Categoria {nombre: 'Secuestro'})
MATCH (af:Afectacion {nombre: 'Fallecido'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c1)
MERGE (h)-[:ES_DE]->(c2)
MERGE (h)-[:GENERA {cantidad: 2}]->(af);


CREATE (h:HECHO {
  id: 'EVT_20240702_TORIBIO_01',
  fecha: date('2024-07-02'),
  descripcion: 'Homicidio de comunero Cristian Fabian Dizú tras secuestro atribuido al frente Dagoberto Ramos'
})

MATCH (cp:CentroPoblado {nombre: 'TORIBÍO', nombre_municipio: 'TORIBÍO'})
MATCH (m:MES {numero: 7})
MATCH (a:AÑO {numero: 2024})
MATCH (c1:Categoria {nombre: 'Homicidio'})
MATCH (c2:Categoria {nombre: 'Secuestro'})
MATCH (af:Afectacion {nombre: 'Fallecido'})
MATCH (ac:Actor {nombre: 'Grupo Armado Organizado'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c1)
MERGE (h)-[:ES_DE]->(c2)
MERGE (h)-[:RESPONSABLE]->(ac)
MERGE (h)-[:GENERA {cantidad: 1}]->(af);


CREATE (h:HECHO {
  id: 'EVT_20240703_SANTANDER_01',
  fecha: date('2024-07-03'),
  descripcion: 'Hostigamiento a unidad del Ejército cerca de Mondomo en vereda Cachimbal'
})

MATCH (cp:CentroPoblado {nombre: 'CACHIRINVAL', nombre_municipio: 'SANTANDER DE QUILICHAO'})
MATCH (m:MES {numero: 7})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Hostigamiento'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);



CREATE (h:HECHO {
  id: 'EVT_20240704_POPAYAN_01',
  fecha: date('2024-07-04'),
  descripcion: 'Acciones propagandistas del ELN mediante instalación de banderas y panfletos en Popayán'
})

MATCH (cp:CentroPoblado {nombre: 'POPAYÁN', nombre_municipio: 'POPAYÁN'})
MATCH (m:MES {numero: 7})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Otro'})
MATCH (ac:Actor {nombre: 'ELN'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:RESPONSABLE]->(ac);



CREATE (h:HECHO {
  id: 'EVT_20240704_PIENDAMO_01',
  fecha: date('2024-07-04'),
  descripcion: 'Presencia de guerrilleros del ELN en la vía Panamericana sector El Mango'
})

MATCH (cp:CentroPoblado {nombre: 'PIENDAMÓ', nombre_municipio: 'PIENDAMÓ - TUNÍA'})
MATCH (m:MES {numero: 7})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Retén Ilegal'})
MATCH (ac:Actor {nombre: 'ELN'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:RESPONSABLE]->(ac);



CREATE (h:HECHO {
  id: 'EVT_20240704_PESCADOR_01',
  fecha: date('2024-07-04'),
  descripcion: 'Instalación de banderas alusivas al ELN en el sector de Pescador'
})

MATCH (cp:CentroPoblado {nombre: 'PESCADOR', nombre_municipio: 'CALDONO'})
MATCH (m:MES {numero: 7})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Otro'})
MATCH (ac:Actor {nombre: 'ELN'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:RESPONSABLE]->(ac);


CREATE (h:HECHO {
  id: 'EVT_20240704_SUAREZ_01',
  fecha: date('2024-07-04'),
  descripcion: 'Presencia de cilindro con posibles explosivos y hostigamiento a base militar'
})

MATCH (cp:CentroPoblado {nombre: 'SUÁREZ', nombre_municipio: 'SUÁREZ'})
MATCH (m:MES {numero: 7})
MATCH (a:AÑO {numero: 2024})
MATCH (c1:Categoria {nombre: 'Hallazgo de Material'})
MATCH (c2:Categoria {nombre: 'Hostigamiento'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c1)
MERGE (h)-[:ES_DE]->(c2);


CREATE (h:HECHO {
  id: 'EVT_20240704_SILVIA_01',
  fecha: date('2024-07-04'),
  descripcion: 'Retención ilegal de comunero Uberney Flórez Flórez por integrantes del Frente Jaime Martínez'
})

MATCH (cp:CentroPoblado {nombre: 'SILVIA', nombre_municipio: 'SILVIA'})
MATCH (m:MES {numero: 7})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Retén Ilegal'})
MATCH (ac:Actor {nombre: 'Grupo Armado Organizado'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:RESPONSABLE]->(ac);



CREATE (h:HECHO {
  id: 'EVT_20240707_PAEZ_01',
  fecha: date('2024-07-07'),
  descripcion: 'Confrontaciones entre disidencias del frente Dagoberto Ramos y guerrilleros del ELN'
})

MATCH (cp:CentroPoblado {nombre: 'BELALCÁZAR', nombre_municipio: 'PÁEZ'})
MATCH (m:MES {numero: 7})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Enfrentamiento'})
MATCH (ac1:Actor {nombre: 'ELN'})
MATCH (ac2:Actor {nombre: 'Grupo Armado Organizado'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:PARTICIPA]->(ac1)
MERGE (h)-[:PARTICIPA]->(ac2);



CREATE (h:HECHO {
  id: 'EVT_20240708_ARGELIA_01',
  fecha: date('2024-07-08'),
  descripcion: 'Ataque con explosivos lanzados desde drones contra unidad militar'
})

MATCH (cp:CentroPoblado {nombre: 'ARGELIA', nombre_municipio: 'ARGELIA'})
MATCH (m:MES {numero: 7})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Ataque con Dron'})
MATCH (ac:Actor {nombre: 'Grupo Armado Organizado'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:RESPONSABLE]->(ac);



CREATE (h:HECHO {
  id: 'EVT_20240708_CALDONO_01',
  fecha: date('2024-07-08'),
  descripcion: 'Hostigamiento a estación de Policía en el corregimiento de Siberia'
})

MATCH (cp:CentroPoblado {nombre: 'SIBERIA', nombre_municipio: 'CALDONO'})
MATCH (m:MES {numero: 7})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Hostigamiento'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);


CREATE (h:HECHO {
  id: 'EVT_20240708_POPAYAN_01',
  fecha: date('2024-07-08'),
  descripcion: 'Paro de taxistas y bloqueo en sector Pomona por exigencias sobre regulación de transporte'
})

MATCH (cp:CentroPoblado {nombre: 'POPAYÁN', nombre_municipio: 'POPAYÁN'})
MATCH (m:MES {numero: 7})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Acción de Protesta'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);



CREATE (h:HECHO {
  id: 'EVT_20240708_POPAYAN_02',
  fecha: date('2024-07-08'),
  descripcion: 'Bloqueo de vía en sector Río Blanco por movilización campesina nacional'
})

MATCH (cp:CentroPoblado {nombre: 'POPAYÁN', nombre_municipio: 'POPAYÁN'})
MATCH (m:MES {numero: 7})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Acción de Protesta'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);


CREATE (h:HECHO {
  id: 'EVT_20240708_SANTANDER_01',
  fecha: date('2024-07-08'),
  descripcion: 'Ubicación de pancartas alusivas a disidencias Dagoberto Ramos en vía San Pedro'
})

MATCH (cp:CentroPoblado {nombre: 'SANTANDER DE QUILICHAO', nombre_municipio: 'SANTANDER DE QUILICHAO'})
MATCH (m:MES {numero: 7})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Otro'})
MATCH (ac:Actor {nombre: 'Grupo Armado Organizado'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:RESPONSABLE]->(ac);



CREATE (h:HECHO {
  id: 'EVT_20240708_POPAYAN_03',
  fecha: date('2024-07-08'),
  descripcion: 'Concentración campesina, paso intermitente y toma de instalaciones de INVIAS'
})

MATCH (cp:CentroPoblado {nombre: 'POPAYÁN', nombre_municipio: 'POPAYÁN'})
MATCH (m:MES {numero: 7})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Acción de Protesta'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);


CREATE (h:HECHO {
  id: 'EVT_20240709_MONDOMO_01',
  fecha: date('2024-07-09'),
  descripcion: 'Hostigamiento a la subestación de Policía en Mondomo'
})

MATCH (cp:CentroPoblado {nombre: 'MONDOMO', nombre_municipio: 'SANTANDER DE QUILICHAO'})
MATCH (m:MES {numero: 7})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Hostigamiento'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);



