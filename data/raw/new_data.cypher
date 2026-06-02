CREATE (h:HECHO {
  id: 'EVT_20240517_MIRANDA_01',
  fecha: date('2024-05-17'),
  descripcion: 'Atentado con carrobomba en la vía que conduce de Miranda a Corinto'
})

MATCH (cp:CentroPoblado {nombre: 'MIRANDA', nombre_municipio: 'MIRANDA'})
MATCH (m:MES {numero: 5})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Atentado Terrorista'})
MATCH (af1:Afectacion {nombre: 'Fallecido'})
MATCH (af2:Afectacion {nombre: 'Herido'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 2}]->(af1)
MERGE (h)-[:GENERA {cantidad: 1}]->(af2);


CREATE (h:HECHO {
  id: 'EVT_20240518_CALOTO_01',
  fecha: date('2024-05-18'),
  descripcion: 'Bloqueo de las vías hacia Santander de Quilichao y Villa Rica por altas tarifas de energía'
})

MATCH (cp:CentroPoblado {nombre: 'CALOTO', nombre_municipio: 'CALOTO'})
MATCH (m:MES {numero: 5})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Acción de Protesta'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);


CREATE (h:HECHO {
  id: 'EVT_20240520_SANTANDER_01',
  fecha: date('2024-05-20'),
  descripcion: 'Homicidio con arma de fuego de dos menores de edad en el corregimiento de Mondomo'
})

MATCH (cp:CentroPoblado {nombre: 'MONDOMO', nombre_municipio: 'SANTANDER DE QUILICHAO'})
MATCH (m:MES {numero: 5})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Homicidio'})
MATCH (af:Afectacion {nombre: 'Fallecido'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 2}]->(af);


CREATE (h:HECHO {
  id: 'EVT_20240520_MORALES_01',
  fecha: date('2024-05-20'),
  descripcion: 'Ataque contra la estación de Policía del municipio de Morales'
})

MATCH (cp:CentroPoblado {nombre: 'MORALES', nombre_municipio: 'CALOTO'})
MATCH (m:MES {numero: 5})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Hostigamiento'})
MATCH (af1:Afectacion {nombre: 'Herido'})
MATCH (af2:Afectacion {nombre: 'Fallecido'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 3}]->(af1)
MERGE (h)-[:GENERA {cantidad: 3}]->(af2);


CREATE (h:HECHO {
  id: 'EVT_20240520_TIMBIQUI_01',
  fecha: date('2024-05-20'),
  descripcion: 'Hostigamiento a la base militar de la Armada Nacional'
})

MATCH (cp:CentroPoblado {nombre: 'TIMBIQUÍ', nombre_municipio: 'TIMBIQUÍ'})
MATCH (m:MES {numero: 5})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Hostigamiento'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);


CREATE (h:HECHO {
  id: 'EVT_20240520_CAJIBIO_01',
  fecha: date('2024-05-20'),
  descripcion: 'Ataque contra una patrulla del Ejército Nacional en la vereda El Dinde'
})

MATCH (cp:CentroPoblado {nombre: 'LA LAGUNA DINDE', nombre_municipio: 'CAJIBÍO'})
MATCH (m:MES {numero: 5})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Hostigamiento'})
MATCH (af:Afectacion {nombre: 'Herido'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 2}]->(af);


CREATE (h:HECHO {
  id: 'EVT_20240521_SANTANDER_01',
  fecha: date('2024-05-21'),
  descripcion: 'Hostigamientos contra el Ejército Nacional al parecer por disidencias de las FARC'
})

MATCH (cp:CentroPoblado {nombre: 'SANTANDER DE QUILICHAO', nombre_municipio: 'SANTANDER DE QUILICHAO'})
MATCH (m:MES {numero: 5})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Hostigamiento'})
MATCH (ac:Actor {nombre: 'Segunda Marquetalia'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:RESPONSABLE]->(ac);


CREATE (h:HECHO {
  id: 'EVT_20240521_BORDO_01',
  fecha: date('2024-05-21'),
  descripcion: 'Combates entre disidencias de las FARC y el Ejército Nacional'
})

MATCH (cp:CentroPoblado {nombre: 'EL BORDO', nombre_municipio: 'PATÍA'})
MATCH (m:MES {numero: 5})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Enfrentamiento'})
MATCH (af1:Afectacion {nombre: 'Fallecido'})
MATCH (af2:Afectacion {nombre: 'Herido'})
MATCH (ac1:Actor {nombre: 'Segunda Marquetalia'})
MATCH (ac2:Actor {nombre: 'Fuerza Pública'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:PARTICIPA]->(ac1)
MERGE (h)-[:PARTICIPA]->(ac2)
MERGE (h)-[:GENERA {cantidad: 1}]->(af1)
MERGE (h)-[:GENERA {cantidad: 2}]->(af2);


CREATE (h:HECHO {
  id: 'EVT_20240521_MIRANDA_01',
  fecha: date('2024-05-21'),
  descripcion: 'Homicidio del líder juvenil y defensor de Derechos Humanos Luis Oswaldo Yule Palco'
})

MATCH (cp:CentroPoblado {nombre: 'MIRANDA', nombre_municipio: 'MIRANDA'})
MATCH (m:MES {numero: 5})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Homicidio'})
MATCH (af:Afectacion {nombre: 'Fallecido'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 1}]->(af);


CREATE (h:HECHO {
  id: 'EVT_20240524_TORIBIO_01',
  fecha: date('2024-05-24'),
  descripcion: 'Confrontación entre el grupo Dagoberto Ramos y otro grupo por establecer en vereda La Despensa'
})

MATCH (cp:CentroPoblado {nombre: 'LA DESPENSA', nombre_municipio: 'TORIBÍO'})
MATCH (m:MES {numero: 5})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Enfrentamiento'})
MATCH (af:Afectacion {nombre: 'Fallecido'})
MATCH (ac:Actor {nombre: 'Grupo Armado Organizado'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:PARTICIPA]->(ac)
MERGE (h)-[:GENERA {cantidad: 3}]->(af);


CREATE (h:HECHO {
  id: 'EVT_20240524_CALDONO_01',
  fecha: date('2024-05-24'),
  descripcion: 'Hostigamiento contra la Policía Nacional en el corregimiento de Siberia'
})

MATCH (cp:CentroPoblado {nombre: 'SIBERIA', nombre_municipio: 'CALDONO'})
MATCH (m:MES {numero: 5})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Hostigamiento'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);


CREATE (h:HECHO {
  id: 'EVT_20240526_SANTANDER_01',
  fecha: date('2024-05-26'),
  descripcion: 'Detonación de explosivos en la vía Santander de Quilichao - Timba'
})

MATCH (cp:CentroPoblado {nombre: 'SANTANDER DE QUILICHAO', nombre_municipio: 'SANTANDER DE QUILICHAO'})
MATCH (m:MES {numero: 5})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Atentado Terrorista'})
MATCH (af:Afectacion {nombre: 'Material'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 1}]->(af);



CREATE (h:HECHO {
  id: 'EVT_20240528_SUAREZ_01',
  fecha: date('2024-05-28'),
  descripcion: 'Atentado contra la estación de Policía de Suárez mediante lanzamiento de explosivos desde una motocicleta'
})

MATCH (cp:CentroPoblado {nombre: 'SUÁREZ', nombre_municipio: 'SUÁREZ'})
MATCH (m:MES {numero: 5})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Atentado Terrorista'})
MATCH (af:Afectacion {nombre: 'Herido'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 1}]->(af);


CREATE (h:HECHO {
  id: 'EVT_20240528_SANTANDER_01',
  fecha: date('2024-05-28'),
  descripcion: 'Bloqueo en la vía Panamericana por protestas relacionadas con tarifas del servicio de energía'
})

MATCH (cp:CentroPoblado {nombre: 'SANTANDER DE QUILICHAO', nombre_municipio: 'SANTANDER DE QUILICHAO'})
MATCH (m:MES {numero: 5})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Acción de Protesta'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);


CREATE (h:HECHO {
  id: 'EVT_20240529_BALBOA_01',
  fecha: date('2024-05-29'),
  descripcion: 'Combate entre el Ejército Nacional y el frente Jaime Martínez durante acompañamiento a velorio en vereda Papayal'
})

MATCH (cp:CentroPoblado {nombre: 'BALBOA', nombre_municipio: 'BALBOA'})
MATCH (m:MES {numero: 5})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Enfrentamiento'})
MATCH (af1:Afectacion {nombre: 'Fallecido'})
MATCH (af2:Afectacion {nombre: 'Herido'})
MATCH (ac1:Actor {nombre: 'Fuerza Pública'})
MATCH (ac2:Actor {nombre: 'Grupo Armado Organizado'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:PARTICIPA]->(ac1)
MERGE (h)-[:PARTICIPA]->(ac2)
MERGE (h)-[:GENERA {cantidad: 5}]->(af1)
MERGE (h)-[:GENERA {cantidad: 3}]->(af2);


CREATE (h:HECHO {
  id: 'EVT_20240531_ARGELIA_01',
  fecha: date('2024-05-31'),
  descripcion: 'Hostigamiento mediante uso de drones'
})

MATCH (cp:CentroPoblado {nombre: 'ARGELIA', nombre_municipio: 'ARGELIA'})
MATCH (m:MES {numero: 5})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Ataque con Dron'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);


CREATE (h:HECHO {
  id: 'EVT_20240607_POPAYAN_01',
  fecha: date('2024-06-07'),
  descripcion: 'Atentado con drones al comando de Policía del departamento del Cauca'
})

MATCH (cp:CentroPoblado {nombre: 'POPAYÁN', nombre_municipio: 'POPAYÁN'})
MATCH (m:MES {numero: 6})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Ataque con Dron'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);


CREATE (h:HECHO {
  id: 'EVT_20240612_CAJIBIO_01',
  fecha: date('2024-06-12'),
  descripcion: 'Hostigamiento a la estación de Policía del municipio de Cajibío'
})

MATCH (cp:CentroPoblado {nombre: 'CAJIBÍO', nombre_municipio: 'CAJIBÍO'})
MATCH (m:MES {numero: 6})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Hostigamiento'})
MATCH (af:Afectacion {nombre: 'Material'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 1}]->(af);


CREATE (h:HECHO {
  id: 'EVT_20240612_SUAREZ_01',
  fecha: date('2024-06-12'),
  descripcion: 'Ataque contra la fuerza pública mediante uso de drones en La Salvajina'
})

MATCH (cp:CentroPoblado {nombre: 'SUÁREZ', nombre_municipio: 'SUÁREZ'})
MATCH (m:MES {numero: 6})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Ataque con Dron'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);


CREATE (h:HECHO {
  id: 'EVT_20240612_ARGELIA_01',
  fecha: date('2024-06-12'),
  descripcion: 'Ataque contra el Ejército Nacional mediante uso de drones'
})

MATCH (cp:CentroPoblado {nombre: 'ARGELIA', nombre_municipio: 'ARGELIA'})
MATCH (m:MES {numero: 6})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Ataque con Dron'})
MATCH (af:Afectacion {nombre: 'Herido'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 3}]->(af);


CREATE (h:HECHO {
  id: 'EVT_20240613_CAJIBIO_01',
  fecha: date('2024-06-13'),
  descripcion: 'Hostigamiento a la subestación de Policía del Carmelo en Cajibío'
})

MATCH (cp:CentroPoblado {nombre: 'EL CARMELO', nombre_municipio: 'CAJIBÍO'})
MATCH (m:MES {numero: 6})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Hostigamiento'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);


CREATE (h:HECHO {
  id: 'EVT_20240613_SUAREZ_01',
  fecha: date('2024-06-13'),
  descripcion: 'Hostigamiento a la estación de Policía del municipio de Suárez'
})

MATCH (cp:CentroPoblado {nombre: 'SUÁREZ', nombre_municipio: 'SUÁREZ'})
MATCH (m:MES {numero: 6})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Hostigamiento'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);


CREATE (h:HECHO {
  id: 'EVT_20240613_LOPEZ_01',
  fecha: date('2024-06-13'),
  descripcion: 'Combate con el GAOR Jaime Martínez en el sector de Noanamito'
})

MATCH (cp:CentroPoblado {nombre: 'NOANAMITO', nombre_municipio: 'LÓPEZ DE MICAY'})
MATCH (m:MES {numero: 6})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Enfrentamiento'})
MATCH (ac1:Actor {nombre: 'Grupo Armado Organizado'})
MATCH (ac2:Actor {nombre: 'Fuerza Pública'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:PARTICIPA]->(ac1)
MERGE (h)-[:PARTICIPA]->(ac2);


CREATE (h:HECHO {
  id: 'EVT_20240614_SANTANDER_01',
  fecha: date('2024-06-14'),
  descripcion: 'Atentado contra la sede de la Fiscalía General de la Nación mediante lanzamiento de granada'
})

MATCH (cp:CentroPoblado {nombre: 'SANTANDER DE QUILICHAO', nombre_municipio: 'SANTANDER DE QUILICHAO'})
MATCH (m:MES {numero: 6})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Atentado Terrorista'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);


CREATE (h:HECHO {
  id: 'EVT_20240614_SILVIA_01',
  fecha: date('2024-06-14'),
  descripcion: 'Homicidio del líder social y defensor de Derechos Humanos Willan Ramírez Muñoz'
})

MATCH (cp:CentroPoblado {nombre: 'SILVIA', nombre_municipio: 'SILVIA'})
MATCH (m:MES {numero: 6})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Homicidio'})
MATCH (af:Afectacion {nombre: 'Fallecido'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 1}]->(af);


CREATE (h:HECHO {
  id: 'EVT_20240615_SUAREZ_01',
  fecha: date('2024-06-15'),
  descripcion: 'Ubicación y destrucción controlada de artefacto explosivo improvisado por grupo EXDE'
})

MATCH (cp:CentroPoblado {nombre: 'SUÁREZ', nombre_municipio: 'SUÁREZ'})
MATCH (m:MES {numero: 6})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Hallazgo de Material'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);


CREATE (h:HECHO {
  id: 'EVT_20240615_LOPEZ_01',
  fecha: date('2024-06-15'),
  descripcion: 'Combate con el GAOR Jaime Martínez'
})

MATCH (cp:CentroPoblado {nombre: 'LÓPEZ DE MICAY', nombre_municipio: 'LÓPEZ DE MICAY'})
MATCH (m:MES {numero: 6})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Enfrentamiento'})
MATCH (ac1:Actor {nombre: 'Grupo Armado Organizado'})
MATCH (ac2:Actor {nombre: 'Fuerza Pública'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:PARTICIPA]->(ac1)
MERGE (h)-[:PARTICIPA]->(ac2);


CREATE (h:HECHO {
  id: 'EVT_20240617_ARGELIA_01',
  fecha: date('2024-06-17'),
  descripcion: 'Atentado contra local comercial en El Plateado mediante uso de dron con explosivos'
})

MATCH (cp:CentroPoblado {nombre: 'EL PLATEADO', nombre_municipio: 'ARGELIA'})
MATCH (m:MES {numero: 6})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Ataque con Dron'})
MATCH (af:Afectacion {nombre: 'Material'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 1}]->(af);


CREATE (h:HECHO {
  id: 'EVT_20240617_ARGELIA_01',
  fecha: date('2024-06-17'),
  descripcion: 'Atentado contra local comercial en El Plateado mediante uso de dron con explosivos'
})

MATCH (cp:CentroPoblado {nombre: 'EL PLATEADO', nombre_municipio: 'ARGELIA'})
MATCH (m:MES {numero: 6})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Ataque con Dron'})
MATCH (af:Afectacion {nombre: 'Material'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 1}]->(af);



CREATE (h:HECHO {
  id: 'EVT_20240617_ARGELIA_02',
  fecha: date('2024-06-17'),
  descripcion: 'Confrontaciones entre grupos armados ilegales y ataques con drones en vereda El Diamante'
})

MATCH (cp:CentroPoblado {nombre: 'ARGELIA', nombre_municipio: 'ARGELIA'})
MATCH (m:MES {numero: 6})
MATCH (a:AÑO {numero: 2024})
MATCH (c1:Categoria {nombre: 'Enfrentamiento'})
MATCH (c2:Categoria {nombre: 'Ataque con Dron'})
MATCH (ac:Actor {nombre: 'Grupo Armado Organizado'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c1)
MERGE (h)-[:ES_DE]->(c2)
MERGE (h)-[:PARTICIPA]->(ac);


CREATE (h:HECHO {
  id: 'EVT_20240617_SUAREZ_01',
  fecha: date('2024-06-17'),
  descripcion: 'Ataques con drones y artefactos explosivos improvisados contra base militar de La Salvajina'
})

MATCH (cp:CentroPoblado {nombre: 'SUÁREZ', nombre_municipio: 'SUÁREZ'})
MATCH (m:MES {numero: 6})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Ataque con Dron'})
MATCH (af:Afectacion {nombre: 'Material'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 1}]->(af);


CREATE (h:HECHO {
  id: 'EVT_20240618_MORALES_01',
  fecha: date('2024-06-18'),
  descripcion: 'Hostigamiento contra la estación de Policía del municipio de Morales'
})

MATCH (cp:CentroPoblado {nombre: 'MORALES', nombre_municipio: 'MORALES'})
MATCH (m:MES {numero: 6})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Hostigamiento'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);


CREATE (h:HECHO {
  id: 'EVT_20240624_CAJIBIO_01',
  fecha: date('2024-06-24'),
  descripcion: 'Enfrentamiento y uso de drones con explosivos en el corregimiento de Ortega'
})

MATCH (cp:CentroPoblado {nombre: 'ORTEGA', nombre_municipio: 'CAJIBÍO'})
MATCH (m:MES {numero: 6})
MATCH (a:AÑO {numero: 2024})
MATCH (c1:Categoria {nombre: 'Enfrentamiento'})
MATCH (c2:Categoria {nombre: 'Ataque con Dron'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c1)
MERGE (h)-[:ES_DE]->(c2);


CREATE (h:HECHO {
  id: 'EVT_20240627_CALOTO_01',
  fecha: date('2024-06-27'),
  descripcion: 'Homicidio de comunero indígena del resguardo San Francisco tras secuestro atribuido al frente Dagoberto Ramos'
})

MATCH (cp:CentroPoblado {nombre: 'CALOTO', nombre_municipio: 'CALOTO'})
MATCH (m:MES {numero: 6})
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
  id: 'EVT_20240629_INZA_01',
  fecha: date('2024-06-29'),
  descripcion: 'Enfrentamiento entre integrantes del frente Dagoberto Ramos y el ELN en sector San Francisco'
})

MATCH (cp:CentroPoblado {nombre: 'INZÁ', nombre_municipio: 'INZÁ'})
MATCH (m:MES {numero: 6})
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
  id: 'EVT_20240629_TAMBO_01',
  fecha: date('2024-06-29'),
  descripcion: 'Explosión de artefacto explosivo y hostigamiento contra subestación de Policía en El Crucero de Pandiguando'
})

MATCH (cp:CentroPoblado {nombre: 'EL CRUCERO DE PANDIGUANDO', nombre_municipio: 'EL TAMBO'})
MATCH (m:MES {numero: 6})
MATCH (a:AÑO {numero: 2024})
MATCH (c1:Categoria {nombre: 'Atentado Terrorista'})
MATCH (c2:Categoria {nombre: 'Hostigamiento'})
MATCH (af:Afectacion {nombre: 'Material'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c1)
MERGE (h)-[:ES_DE]->(c2)
MERGE (h)-[:GENERA {cantidad: 1}]->(af);