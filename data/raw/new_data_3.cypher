MERGE (a:AÑO {numero: 2026})

CREATE (h:HECHO {
  id: 'EVT_20260119_PATIA_01',
  fecha: date('2026-01-19'),
  descripcion: 'Ataque con drones cargados con explosivos contra unidades militares en El Estanquillo'
})

MATCH (cp:CentroPoblado {nombre: 'EL BORDO', nombre_municipio: 'PATÍA'})
MATCH (m:MES {numero: 1})
MATCH (a:AÑO {numero: 2026})
MATCH (c:Categoria {nombre: 'Ataque con Dron'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);


CREATE (h:HECHO {
  id: 'EVT_20260129_ARGELIA_01',
  fecha: date('2026-01-29'),
  descripcion: 'Ataque con explosivos lanzados desde drones cerca al parque principal de El Plateado'
})

MATCH (cp:CentroPoblado {nombre: 'EL PLATEADO', nombre_municipio: 'ARGELIA'})
MATCH (m:MES {numero: 1})
MATCH (a:AÑO {numero: 2026})
MATCH (c:Categoria {nombre: 'Ataque con Dron'})
MATCH (af1:Afectacion {nombre: 'Fallecido'})
MATCH (af2:Afectacion {nombre: 'Herido'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 1}]->(af1)
MERGE (h)-[:GENERA {cantidad: 14}]->(af2);


CREATE (h:HECHO {
  id: 'EVT_20260211_CAJIBIO_01',
  fecha: date('2026-02-11'),
  descripcion: 'Detonaciones sobre la estación de Policía en Cajibío mediante uso de tecnología armada'
})

MATCH (cp:CentroPoblado {nombre: 'CAJIBÍO', nombre_municipio: 'CAJIBÍO'})
MATCH (m:MES {numero: 2})
MATCH (a:AÑO {numero: 2026})
MATCH (c:Categoria {nombre: 'Ataque con Dron'})
MATCH (af:Afectacion {nombre: 'Material'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 1}]->(af);


CREATE (h:HECHO {
  id: 'EVT_20260114_SUAREZ_01',
  fecha: date('2026-01-14'),
  descripcion: 'Ataques y hostigamientos contra base militar del Amparo, estación de Policía y asonada en Asnazu'
})

MATCH (cp:CentroPoblado {nombre: 'SUÁREZ', nombre_municipio: 'SUÁREZ'})
MATCH (m:MES {numero: 1})
MATCH (a:AÑO {numero: 2026})
MATCH (c1:Categoria {nombre: 'Hostigamiento'})
MATCH (c2:Categoria {nombre: 'Otro'})
MATCH (ac:Actor {nombre: 'Grupo Armado Organizado'})
MATCH (af:Afectacion {nombre: 'Material'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c1)
MERGE (h)-[:ES_DE]->(c2)
MERGE (h)-[:RESPONSABLE]->(ac)
MERGE (h)-[:GENERA {cantidad: 1}]->(af);


CREATE (h:HECHO {
  id: 'EVT_20260216_BALBOA_01',
  fecha: date('2026-02-16'),
  descripcion: 'Fuertes enfrentamientos entre grupos armados ilegales en el sector Nariz del Diablo'
})

MATCH (cp:CentroPoblado {nombre: 'BALBOA', nombre_municipio: 'BALBOA'})
MATCH (m:MES {numero: 2})
MATCH (a:AÑO {numero: 2026})
MATCH (c:Categoria {nombre: 'Enfrentamiento'})
MATCH (ac:Actor {nombre: 'Grupo Armado Organizado'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:PARTICIPA]->(ac);


CREATE (h:HECHO {
  id: 'EVT_20260216_SUAREZ_01',
  fecha: date('2026-02-16'),
  descripcion: 'Hostigamientos contra base Los Pinos en Suárez'
})

MATCH (cp:CentroPoblado {nombre: 'SUÁREZ', nombre_municipio: 'SUÁREZ'})
MATCH (m:MES {numero: 2})
MATCH (a:AÑO {numero: 2026})
MATCH (c:Categoria {nombre: 'Hostigamiento'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);



CREATE (h:HECHO {
  id: 'EVT_20260217_CORINTO_01',
  fecha: date('2026-02-17'),
  descripcion: 'Hallazgo y detonación controlada de presunto artefacto explosivo en zona de buses'
})

MATCH (cp:CentroPoblado {nombre: 'CORINTO', nombre_municipio: 'CORINTO'})
MATCH (m:MES {numero: 2})
MATCH (a:AÑO {numero: 2026})
MATCH (c:Categoria {nombre: 'Hallazgo de Material'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);


CREATE (h:HECHO {
  id: 'EVT_20260217_SUAREZ_01',
  fecha: date('2026-02-17'),
  descripcion: 'Retención de 13 trabajadores de brigadas de mantenimiento preventivo en corredor Suárez Altamira'
})

MATCH (cp:CentroPoblado {nombre: 'ALTAMIRA', nombre_municipio: 'SUÁREZ'})
MATCH (m:MES {numero: 2})
MATCH (a:AÑO {numero: 2026})
MATCH (c:Categoria {nombre: 'Secuestro'})
MATCH (ac:Actor {nombre: 'Grupo Armado Organizado'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:RESPONSABLE]->(ac);


CREATE (h:HECHO {
  id: 'EVT_20260218_LOPEZ_01',
  fecha: date('2026-02-18'),
  descripcion: 'Hallazgo de depósito ilegal con armas, munición y equipos tecnológicos atribuidos a estructura Jaime Martínez'
})

MATCH (cp:CentroPoblado {nombre: 'LÓPEZ', nombre_municipio: 'LÓPEZ DE MICAY'})
MATCH (m:MES {numero: 2})
MATCH (a:AÑO {numero: 2026})
MATCH (c:Categoria {nombre: 'Hallazgo de Material'})
MATCH (ac:Actor {nombre: 'Grupo Armado Organizado'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:RESPONSABLE]->(ac);


CREATE (h:HECHO {
  id: 'EVT_20260218_CORINTO_01',
  fecha: date('2026-02-18'),
  descripcion: 'Hostigamiento y abandono de cilindro explosivo en vía Miranda Corinto'
})

MATCH (cp:CentroPoblado {nombre: 'CORINTO', nombre_municipio: 'CORINTO'})
MATCH (m:MES {numero: 2})
MATCH (a:AÑO {numero: 2026})
MATCH (c1:Categoria {nombre: 'Hostigamiento'})
MATCH (c2:Categoria {nombre: 'Hallazgo de Material'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c1)
MERGE (h)-[:ES_DE]->(c2);


CREATE (h:HECHO {
  id: 'EVT_20260218_MIRANDA_01',
  fecha: date('2026-02-18'),
  descripcion: 'Camioneta abandonada con múltiples impactos de proyectil en medio de hostigamiento'
})

MATCH (cp:CentroPoblado {nombre: 'MIRANDA', nombre_municipio: 'MIRANDA'})
MATCH (m:MES {numero: 2})
MATCH (a:AÑO {numero: 2026})
MATCH (c:Categoria {nombre: 'Hostigamiento'})
MATCH (af:Afectacion {nombre: 'Material'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 1}]->(af);


CREATE (h:HECHO {
  id: 'EVT_20260219_TORIBIO_01',
  fecha: date('2026-02-19'),
  descripcion: 'Desactivación controlada de dos cilindros bomba en la vereda La Natala por el equipo EXDE'
})

MATCH (cp:CentroPoblado {nombre: 'TORIBÍO', nombre_municipio: 'TORIBÍO'})
MATCH (m:MES {numero: 2})
MATCH (a:AÑO {numero: 2026})
MATCH (c:Categoria {nombre: 'Hallazgo de Material'})
MATCH (ac:Actor {nombre: 'Grupo Armado Organizado'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:RESPONSABLE]->(ac);


CREATE (h:HECHO {
  id: 'EVT_20260224_CAJIBIO_01',
  fecha: date('2026-02-24'),
  descripcion: 'Ataque con explosivos afectó infraestructura eléctrica entre Popayán y Santander de Quilichao'
})

MATCH (cp:CentroPoblado {nombre: 'CAJIBÍO', nombre_municipio: 'CAJIBÍO'})
MATCH (m:MES {numero: 2})
MATCH (a:AÑO {numero: 2026})
MATCH (c:Categoria {nombre: 'Atentado Terrorista'})
MATCH (af:Afectacion {nombre: 'Material'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 4}]->(af);



CREATE (h:HECHO {
  id: 'EVT_20260224_SANSEBASTIAN_01',
  fecha: date('2026-02-24'),
  descripcion: 'Amenaza con artefacto explosivo contra gerente del Banco Agrario'
})

MATCH (cp:CentroPoblado {nombre: 'SAN SEBASTIÁN', nombre_municipio: 'SAN SEBASTIÁN'})
MATCH (m:MES {numero: 2})
MATCH (a:AÑO {numero: 2026})
MATCH (c:Categoria {nombre: 'Atentado Terrorista'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);



CREATE (h:HECHO {
  id: 'EVT_20260224_PATIA_01',
  fecha: date('2026-02-24'),
  descripcion: 'Ataque a carro de valores en Piedra Sentada sobre la vía Panamericana'
})

MATCH (cp:CentroPoblado {nombre: 'PIEDRASENTADA', nombre_municipio: 'PATÍA'})
MATCH (m:MES {numero: 2})
MATCH (a:AÑO {numero: 2026})
MATCH (c1:Categoria {nombre: 'Homicidio'})
MATCH (c2:Categoria {nombre: 'Otro'})
MATCH (af1:Afectacion {nombre: 'Fallecido'})
MATCH (af2:Afectacion {nombre: 'Material'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c1)
MERGE (h)-[:ES_DE]->(c2)
MERGE (h)-[:GENERA {cantidad: 1}]->(af1)
MERGE (h)-[:GENERA {cantidad: 1}]->(af2);

CREATE (h:HECHO {
  id: 'EVT_20260225_SANTANDER_01',
  fecha: date('2026-02-25'),
  descripcion: 'Destrucción controlada de artefacto explosivo improvisado tipo cilindro en Lomitas Arriba'
})

MATCH (cp:CentroPoblado {nombre: 'LOMITAS ARRIBA', nombre_municipio: 'SANTANDER DE QUILICHAO'})
MATCH (m:MES {numero: 2})
MATCH (a:AÑO {numero: 2026})
MATCH (c:Categoria {nombre: 'Hallazgo de Material'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);


CREATE (h:HECHO {
  id: 'EVT_20260225_CALOTO_01',
  fecha: date('2026-02-25'),
  descripcion: 'Combates entre Ejército y presuntos integrantes del frente Dagoberto Ramos en López Adentro y Huasano'
})

MATCH (cp:CentroPoblado {nombre: 'LÓPEZ ADENTRO', nombre_municipio: 'CALOTO'})
MATCH (m:MES {numero: 2})
MATCH (a:AÑO {numero: 2026})
MATCH (c:Categoria {nombre: 'Enfrentamiento'})
MATCH (ac1:Actor {nombre: 'Fuerza Pública'})
MATCH (ac2:Actor {nombre: 'Grupo Armado Organizado'})
MATCH (af1:Afectacion {nombre: 'Material'})
MATCH (af2:Afectacion {nombre: 'Desplazamiento'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:PARTICIPA]->(ac1)
MERGE (h)-[:PARTICIPA]->(ac2)
MERGE (h)-[:GENERA {cantidad: 1}]->(af1)
MERGE (h)-[:GENERA {cantidad: 1}]->(af2);



CREATE (h:HECHO {
  id: 'EVT_20260225_TAMBO_01',
  fecha: date('2026-02-25'),
  descripcion: 'Desaparición de Ana Guetio tras reunión política en Pandiguando'
})

MATCH (cp:CentroPoblado {nombre: 'PANDIGUANDO', nombre_municipio: 'EL TAMBO'})
MATCH (m:MES {numero: 2})
MATCH (a:AÑO {numero: 2026})
MATCH (c:Categoria {nombre: 'Secuestro'})
MATCH (af:Afectacion {nombre: 'Otro'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 1}]->(af);


CREATE (h:HECHO {
  id: 'EVT_20260227_CORINTO_01',
  fecha: date('2026-02-27'),
  descripcion: 'Captura de tres presuntos cabecillas del frente Dagoberto Ramos en Corinto'
})

MATCH (cp:CentroPoblado {nombre: 'CORINTO', nombre_municipio: 'CORINTO'})
MATCH (m:MES {numero: 2})
MATCH (a:AÑO {numero: 2026})
MATCH (c:Categoria {nombre: 'Otro'})
MATCH (ac:Actor {nombre: 'Grupo Armado Organizado'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:RESPONSABLE]->(ac);


CREATE (h:HECHO {
  id: 'EVT_20260303_TIMBIO_01',
  fecha: date('2026-03-03'),
  descripcion: 'Artefacto explosivo abandonado sobre la vía hacia San Joaquín en vereda El Hato'
})

MATCH (cp:CentroPoblado {nombre: 'TIMBÍO', nombre_municipio: 'TIMBÍO'})
MATCH (m:MES {numero: 3})
MATCH (a:AÑO {numero: 2026})
MATCH (c:Categoria {nombre: 'Hallazgo de Material'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);

CREATE (h:HECHO {
  id: 'EVT_20260119_PADILLA_01',
  fecha: date('2026-01-19'),
  descripcion: 'Homicidio colectivo de cuatro personas en la vereda El Chamizo perpetrado por hombres armados'
})

MATCH (cp:CentroPoblado {nombre: 'EL CHAMIZO', nombre_municipio: 'PADILLA'})
MATCH (m:MES {numero: 1})
MATCH (a:AÑO {numero: 2026})
MATCH (c:Categoria {nombre: 'Homicidio'})
MATCH (ac:Actor {nombre: 'No identificado'})
MATCH (af:Afectacion {nombre: 'Fallecido'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:RESPONSABLE]->(ac)
MERGE (h)-[:GENERA {cantidad: 4}]->(af);


CREATE (h:HECHO {
  id: 'EVT_20260403_MIRANDA_01',
  fecha: date('2026-04-03'),
  descripcion: 'Homicidio de Andrés Giovanni Rodríguez Burgos, líder social y político del municipio de Miranda'
})

MATCH (cp:CentroPoblado {nombre: 'MIRANDA', nombre_municipio: 'MIRANDA'})
MATCH (m:MES {numero: 4})
MATCH (a:AÑO {numero: 2026})
MATCH (c:Categoria {nombre: 'Homicidio'})
MATCH (ac:Actor {nombre: 'No identificado'})
MATCH (af:Afectacion {nombre: 'Fallecido'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:RESPONSABLE]->(ac)
MERGE (h)-[:GENERA {cantidad: 1}]->(af);
