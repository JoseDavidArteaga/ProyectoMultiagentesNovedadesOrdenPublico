MERGE (a:AÑO {numero: 2024})
///

CREATE (h:HECHO {
  id: 'EVT_20240117_TORIBIO_01',
  fecha: date('2024-01-17'),
  descripcion: 'Artefacto explosivo tipo cilindro bomba cerca de vivienda y sede educativa'
})

MATCH (cp:CentroPoblado {nombre: 'TORIBÍO', nombre_municipio: 'TORIBÍO'})
MATCH (m:MES {numero: 1})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Hallazgo de Material'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);

///
CREATE (h:HECHO {
  id: 'EVT_20240131_PIENDAMO_01',
  fecha: date('2024-01-31'),
  descripcion: 'Bloqueo vía Panamericana por comunidades MISAK y asesinato de transportador'
})

MATCH (cp:CentroPoblado {nombre: 'PIENDAMÓ', nombre_municipio: 'PIENDAMÓ - TUNÍA'})
MATCH (m:MES {numero: 1})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Acción de Protesta'})
MATCH (af:Afectacion {nombre: 'Fallecido'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 1}]->(af);
////
CREATE (h:HECHO {
  id: 'EVT_20240207_CAJIBIO_01',
  fecha: date('2024-02-07'),
  descripcion: 'Invasión de predio SMURFIT KAPPA por grupo armado con artefactos explosivos'
})

MATCH (cp:CentroPoblado {nombre: 'LA CAPILLA', nombre_municipio: 'CAJIBÍO'})
MATCH (m:MES {numero: 2})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Hostigamiento'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);
///
CREATE (h:HECHO {
  id: 'EVT_20240217_BUENOSAIRES_01',
  fecha: date('2024-02-17'),
  descripcion: 'Combate entre Ejército Nacional y grupo armado ilegal'
})

MATCH (cp:CentroPoblado {nombre: 'BUENOS AIRES', nombre_municipio: 'BUENOS AIRES'})
MATCH (m:MES {numero: 2})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Enfrentamiento'})
MATCH (af:Afectacion {nombre: 'Herido'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 2}]->(af);
///
CREATE (h:HECHO {
  id: 'EVT_20240217_TORIBIO_02',
  fecha: date('2024-02-17'),
  descripcion: 'Homicidio de lider indígena Carmelina Yule Paví'
})

MATCH (cp:CentroPoblado {nombre: 'LA CRUZ', nombre_municipio: 'TORIBÍO'})
MATCH (m:MES {numero: 2})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Homicidio'})
MATCH (af:Afectacion {nombre: 'Fallecido'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 1}]->(af);
///
CREATE (h:HECHO {
  id: 'EVT_20240322_ARGELIA_01',
  fecha: date('2024-03-22'),
  descripcion: 'Combates entre Ejército y Frente Carlos Patiño'
})

MATCH (cp:CentroPoblado {nombre: 'ARGELIA', nombre_municipio: 'ARGELIA'})
MATCH (m:MES {numero: 3})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Enfrentamiento'})
MATCH (af1:Afectacion {nombre: 'Confinamiento'})
MATCH (af2:Afectacion {nombre: 'Desplazamiento'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 100}]->(af1)
MERGE (h)-[:GENERA {cantidad: 20}]->(af2);
///
CREATE (h:HECHO {
  id: 'EVT_20240325_CORINTO_02',
  fecha: date('2024-03-25'),
  descripcion: 'Combate entre Ejército y Frente Dagoberto Ramos'
})

MATCH (cp:CentroPoblado {nombre: 'SAN LUIS', nombre_municipio: 'CORINTO'})
MATCH (m:MES {numero: 3})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Enfrentamiento'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);
///
CREATE (h:HECHO {
  id: 'EVT_20240325_TORIBIO_01',
  fecha: date('2024-03-25'),
  descripcion: 'Combate entre Ejército Nacional y Frente Dagoberto Ramos'
})

MATCH (cp:CentroPoblado {nombre: 'TACUEYO', nombre_municipio: 'TORIBÍO'})
MATCH (m:MES {numero: 3})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Enfrentamiento'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);
///
CREATE (h:HECHO {
  id: 'EVT_20240327_SUAREZ_01',
  fecha: date('2024-03-27'),
  descripcion: 'Combate entre Ejército Nacional y Frente Jaime Martínez'
})

MATCH (cp:CentroPoblado {nombre: 'LA BETULIA', nombre_municipio: 'SUÁREZ'})
MATCH (m:MES {numero: 3})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Enfrentamiento'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);
///
CREATE (h:HECHO {
  id: 'EVT_20240328_ARGELIA_01',
  fecha: date('2024-03-28'),
  descripcion: 'Combates entre Ejército Nacional y disidencias'
})

MATCH (cp:CentroPoblado {nombre: 'LA CABAÑA', nombre_municipio: 'ARGELIA'})
MATCH (m:MES {numero: 3})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Enfrentamiento'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);

///
CREATE (h:HECHO {
  id: 'EVT_20240331_PAEZ_01',
  fecha: date('2024-03-31'),
  descripcion: 'Retén ilegal y hurto de tres vehículos por Frente Dagoberto Ramos'
})

MATCH (cp:CentroPoblado {nombre: 'PÁEZ', nombre_municipio: 'PÁEZ'})
MATCH (m:MES {numero: 3})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Retén Ilegal'})
MATCH (af:Afectacion {nombre: 'Material'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 3}]->(af);
///
CREATE (h:HECHO {
  id: 'EVT_20240402_SUAREZ_01',
  fecha: date('2024-04-02'),
  descripcion: 'Hostigamiento contra base militar BATOT 13'
})

MATCH (cp:CentroPoblado {nombre: 'SUÁREZ', nombre_municipio: 'SUÁREZ'})
MATCH (m:MES {numero: 4})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Hostigamiento'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);
///
CREATE (h:HECHO {
  id: 'EVT_20240405_PIENDAMO_01',
  fecha: date('2024-04-05'),
  descripcion: 'Ataque a patrulla de tránsito: 1 muerto, 8 heridos y daños a infraestructura hospitalaria'
})

MATCH (cp:CentroPoblado {nombre: 'PIENDAMÓ', nombre_municipio: 'PIENDAMÓ - TUNÍA'})
MATCH (m:MES {numero: 4})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Atentado Terrorista'})
MATCH (af1:Afectacion {nombre: 'Fallecido'})
MATCH (af2:Afectacion {nombre: 'Herido'})
MATCH (af3:Afectacion {nombre: 'Material'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 1}]->(af1)
MERGE (h)-[:GENERA {cantidad: 8}]->(af2)
MERGE (h)-[:GENERA {cantidad: 1}]->(af3);
///
CREATE (h:HECHO {
  id: 'EVT_20240407_TORIBIO_01',
  fecha: date('2024-04-07'),
  descripcion: 'Combates en Tacueyó con retenes ilegales y desplazamientos'
})

MATCH (cp:CentroPoblado {nombre: 'TACUEYO', nombre_municipio: 'TORIBÍO'})
MATCH (m:MES {numero: 4})
MATCH (a:AÑO {numero: 2024})
MATCH (c1:Categoria {nombre: 'Enfrentamiento'})
MATCH (c2:Categoria {nombre: 'Retén Ilegal'})
MATCH (af:Afectacion {nombre: 'Desplazamiento'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c1)
MERGE (h)-[:ES_DE]->(c2)
MERGE (h)-[:GENERA {cantidad: 1}]->(af);
///
CREATE (h:HECHO {
  id: 'EVT_20240408_INZA_01',
  fecha: date('2024-04-08'),
  descripcion: 'Hostigamiento con artefactos explosivos contra Ejército'
})

MATCH (cp:CentroPoblado {nombre: 'QUIGUANAS', nombre_municipio: 'INZÁ'})
MATCH (m:MES {numero: 4})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Hostigamiento'})
MATCH (af:Afectacion {nombre: 'Material'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 1}]->(af);
///
CREATE (h:HECHO {
  id: 'EVT_20240408_PIENDAMO_01',
  fecha: date('2024-04-08'),
  descripcion: 'Se presenta sobrevuelo de Drones, activación plan defensa, observación por presuntos integrantes de Frente Jaime Martínez y/o Frente Dagoberto Ramos.'
})

MATCH (cp:CentroPoblado {nombre: 'TUNÍA', nombre_municipio: 'PIENDAMÓ - TUNÍA'})
MATCH (m:MES {numero: 4})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Hostigamiento'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);
///
CREATE (h:HECHO {
  id: 'EVT_20240408_PAEZ_01',
  fecha: date('2024-04-08'),
  descripcion: 'Se presenta hostigamiento, disparos contra unidades del Ejército Nacional por presuntos integrantes de Frente Dagoberto Ramos.'
})

MATCH (cp:CentroPoblado {nombre: 'GUADUALEJO', nombre_municipio: 'PÁEZ'})
MATCH (m:MES {numero: 4})
MATCH (a:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Hostigamiento'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(m)
MERGE (h)-[:EN_AÑO]->(a)
MERGE (h)-[:ES_DE]->(c);
///
CREATE (h:HECHO {
  id: 'EVT_20240409_JAMBALO_01',
  fecha: date('2024-04-09'),
  descripcion: 'Hostigamiento con disparos esporádicos contra estación de policía'
})

MATCH (cp:CentroPoblado {nombre: 'JAMBALÓ', nombre_municipio: 'JAMBALÓ'})
MATCH (mes:MES {numero: 4})
MATCH (anio:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Hostigamiento'})
MATCH (a1:Actor {nombre: 'Fuerza Pública'})
MATCH (a2:Actor {nombre: 'Grupo Armado Organizado'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(mes)
MERGE (h)-[:EN_AÑO]->(anio)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:RESPONSABLE]->(a2)
MERGE (h)-[:PARTICIPA]->(a1);
///
CREATE (h:HECHO {
  id: 'EVT_20240410_CORINTO_01',
  fecha: date('2024-04-10'),
  descripcion: 'Hostigamiento contra unidades policiales'
})

MATCH (cp:CentroPoblado {nombre: 'CORINTO', nombre_municipio: 'CORINTO'})
MATCH (mes:MES {numero: 4})
MATCH (anio:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Hostigamiento'})
MATCH (a1:Actor {nombre: 'Fuerza Pública'})
MATCH (a2:Actor {nombre: 'Grupo Armado Organizado'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(mes)
MERGE (h)-[:EN_AÑO]->(anio)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:RESPONSABLE]->(a2)
MERGE (h)-[:PARTICIPA]->(a1);
///
CREATE (h:HECHO {
  id: 'EVT_20240410_BUENOSAIRES_01',
  fecha: date('2024-04-10'),
  descripcion: 'Combate entre Ejército Nacional y Frente Jaime Martínez'
})

MATCH (cp:CentroPoblado {nombre: 'TIMBA', nombre_municipio: 'BUENOS AIRES'})
MATCH (mes:MES {numero: 4})
MATCH (anio:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Enfrentamiento'})
MATCH (a1:Actor {nombre: 'Fuerza Pública'})
MATCH (a2:Actor {nombre: 'Grupo Armado Organizado'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(mes)
MERGE (h)-[:EN_AÑO]->(anio)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:RESPONSABLE]->(a2)
MERGE (h)-[:PARTICIPA]->(a1);
///
CREATE (h:HECHO {
  id: 'EVT_20240410_TORIBIO_01',
  fecha: date('2024-04-10'),
  descripcion: 'Combate entre Ejército Nacional y Frente Dagoberto Ramos'
})

MATCH (cp:CentroPoblado {nombre: 'TORIBÍO', nombre_municipio: 'TORIBÍO'})
MATCH (mes:MES {numero: 4})
MATCH (anio:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Enfrentamiento'})
MATCH (a1:Actor {nombre: 'Fuerza Pública'})
MATCH (a2:Actor {nombre: 'Grupo Armado Organizado'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(mes)
MERGE (h)-[:EN_AÑO]->(anio)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:RESPONSABLE]->(a2)
MERGE (h)-[:PARTICIPA]->(a1);
///
CREATE (h:HECHO {
  id: 'EVT_20240411_CORINTO_01',
  fecha: date('2024-04-11'),
  descripcion: 'Hostigamiento simultáneo a Policía y Ejército'
})

MATCH (cp:CentroPoblado {nombre: 'CORINTO', nombre_municipio: 'CORINTO'})
MATCH (mes:MES {numero: 4})
MATCH (anio:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Hostigamiento'})
MATCH (a1:Actor {nombre: 'Fuerza Pública'})
MATCH (a2:Actor {nombre: 'Grupo Armado Organizado'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(mes)
MERGE (h)-[:EN_AÑO]->(anio)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:RESPONSABLE]->(a2)
MERGE (h)-[:PARTICIPA]->(a1);
///
CREATE (h:HECHO {
  id: 'EVT_20240411_MIRANDA_01',
  fecha: date('2024-04-11'),
  descripcion: 'Carro bomba con 4 heridos y daños a 14 viviendas'
})

MATCH (cp:CentroPoblado {nombre: 'MIRANDA', nombre_municipio: 'MIRANDA'})
MATCH (mes:MES {numero: 4})
MATCH (anio:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Atentado Terrorista'})
MATCH (a:Actor {nombre: 'Grupo Armado Organizado'})
MATCH (af1:Afectacion {nombre: 'Herido'})
MATCH (af2:Afectacion {nombre: 'Material'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(mes)
MERGE (h)-[:EN_AÑO]->(anio)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:RESPONSABLE]->(a)
MERGE (h)-[:GENERA {cantidad: 4}]->(af1)
MERGE (h)-[:GENERA {cantidad: 14}]->(af2);
///
CREATE (h:HECHO {
  id: 'EVT_20240412_CALOTO_01',
  fecha: date('2024-04-12'),
  descripcion: 'Combate con una persona lesionada'
})

MATCH (cp:CentroPoblado {nombre: 'EL PAJARITO', nombre_municipio: 'CALOTO'})
MATCH (mes:MES {numero: 4})
MATCH (anio:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Enfrentamiento'})
MATCH (a1:Actor {nombre: 'Fuerza Pública'})
MATCH (a2:Actor {nombre: 'Grupo Armado Organizado'})
MATCH (af:Afectacion {nombre: 'Herido'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(mes)
MERGE (h)-[:EN_AÑO]->(anio)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:RESPONSABLE]->(a2)
MERGE (h)-[:PARTICIPA]->(a1)
MERGE (h)-[:GENERA {cantidad: 1}]->(af);
///
CREATE (h:HECHO {
  id: 'EVT_20240412_CORINTO_02',
  fecha: date('2024-04-12'),
  descripcion: 'Perturbación al transporte con afectación a viviendas'
})

MATCH (cp:CentroPoblado {nombre: 'EL JAGUAL', nombre_municipio: 'CORINTO'})
MATCH (mes:MES {numero: 4})
MATCH (anio:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Otro'})
MATCH (a:Actor {nombre: 'Grupo Armado Organizado'})
MATCH (af:Afectacion {nombre: 'Material'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(mes)
MERGE (h)-[:EN_AÑO]->(anio)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:RESPONSABLE]->(a)
MERGE (h)-[:GENERA {cantidad: 1}]->(af);
///
CREATE (h:HECHO {
  id: 'EVT_20240412_CALOTO_02',
  fecha: date('2024-04-12'),
  descripcion: 'Combates y retén ilegal en múltiples veredas'
})

MATCH (cp:CentroPoblado {nombre: 'HUASANÓ', nombre_municipio: 'CALOTO'})
MATCH (mes:MES {numero: 4})
MATCH (anio:AÑO {numero: 2024})
MATCH (c1:Categoria {nombre: 'Enfrentamiento'})
MATCH (c2:Categoria {nombre: 'Retén Ilegal'})
MATCH (a:Actor {nombre: 'Grupo Armado Organizado'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(mes)
MERGE (h)-[:EN_AÑO]->(anio)
MERGE (h)-[:ES_DE]->(c1)
MERGE (h)-[:ES_DE]->(c2)
MERGE (h)-[:RESPONSABLE]->(a);
///
CREATE (h:HECHO {
  id: 'EVT_20240416_BALBOA_01',
  fecha: date('2024-04-16'),
  descripcion: 'Combates que interrumpen actividades escolares'
})

MATCH (cp:CentroPoblado {nombre: 'PURETO', nombre_municipio: 'BALBOA'})
MATCH (mes:MES {numero: 4})
MATCH (anio:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Enfrentamiento'})
MATCH (a1:Actor {nombre: 'Fuerza Pública'})
MATCH (a2:Actor {nombre: 'Grupo Armado Organizado'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(mes)
MERGE (h)-[:EN_AÑO]->(anio)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:RESPONSABLE]->(a2)
MERGE (h)-[:PARTICIPA]->(a1);
///
CREATE (h:HECHO {
  id: 'EVT_20240417_ARGELIA_01',
  fecha: date('2024-04-17'),
  descripcion: 'Combates con uso de tatucos, 1 soldado muerto y 3 heridos, desplazamientos en varias veredas'
})

MATCH (cp:CentroPoblado {nombre: 'EL PLATEADO', nombre_municipio: 'ARGELIA'})
MATCH (mes:MES {numero: 4})
MATCH (anio:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Enfrentamiento'})
MATCH (a1:Actor {nombre: 'Fuerza Pública'})
MATCH (a2:Actor {nombre: 'Grupo Armado Organizado'})
MATCH (af1:Afectacion {nombre: 'Fallecido'})
MATCH (af2:Afectacion {nombre: 'Herido'})
MATCH (af3:Afectacion {nombre: 'Desplazamiento'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(mes)
MERGE (h)-[:EN_AÑO]->(anio)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:RESPONSABLE]->(a2)
MERGE (h)-[:PARTICIPA]->(a1)
MERGE (h)-[:GENERA {cantidad: 1}]->(af1)
MERGE (h)-[:GENERA {cantidad: 3}]->(af2)
MERGE (h)-[:GENERA {cantidad: 210}]->(af3);
///
CREATE (h:HECHO {
  id: 'EVT_20240417_ARGELIA_02',
  fecha: date('2024-04-17'),
  descripcion: 'Combates con confinamiento, reclutamiento y afectación a institución educativa'
})

MATCH (cp:CentroPoblado {nombre: 'ARGELIA', nombre_municipio: 'ARGELIA'})
MATCH (mes:MES {numero: 4})
MATCH (anio:AÑO {numero: 2024})
MATCH (c1:Categoria {nombre: 'Enfrentamiento'})
MATCH (c2:Categoria {nombre: 'Reclutamiento Ilícito'})
MATCH (a1:Actor {nombre: 'Fuerza Pública'})
MATCH (a2:Actor {nombre: 'Grupo Armado Organizado'})
MATCH (af1:Afectacion {nombre: 'Confinamiento'})
MATCH (af2:Afectacion {nombre: 'Desplazamiento'})
MATCH (af3:Afectacion {nombre: 'Material'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(mes)
MERGE (h)-[:EN_AÑO]->(anio)
MERGE (h)-[:ES_DE]->(c1)
MERGE (h)-[:ES_DE]->(c2)
MERGE (h)-[:RESPONSABLE]->(a2)
MERGE (h)-[:PARTICIPA]->(a1)
MERGE (h)-[:GENERA]->(af1)
MERGE (h)-[:GENERA]->(af2)
MERGE (h)-[:GENERA]->(af3);
///
CREATE (h:HECHO {
  id: 'EVT_20240419_QUILICHAO_01',
  fecha: date('2024-04-19'),
  descripcion: 'Secuestro de 3 personas y hurto de vehículos y armamento'
})

MATCH (cp:CentroPoblado {nombre: 'SANTANDER DE QUILICHAO', nombre_municipio: 'SANTANDER DE QUILICHAO'})
MATCH (mes:MES {numero: 4})
MATCH (anio:AÑO {numero: 2024})
MATCH (c1:Categoria {nombre: 'Secuestro'})
MATCH (c2:Categoria {nombre: 'Retén Ilegal'})
MATCH (a:Actor {nombre: 'Grupo Armado Organizado'})
MATCH (af:Afectacion {nombre: 'Material'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(mes)
MERGE (h)-[:EN_AÑO]->(anio)
MERGE (h)-[:ES_DE]->(c1)
MERGE (h)-[:ES_DE]->(c2)
MERGE (h)-[:RESPONSABLE]->(a)
MERGE (h)-[:GENERA {cantidad: 1}]->(af);
///
CREATE (h:HECHO {
  id: 'EVT_20240421_CORINTO_01',
  fecha: date('2024-04-21'),
  descripcion: 'Homicidio de líder social y una persona herida'
})

MATCH (cp:CentroPoblado {nombre: 'CORINTO', nombre_municipio: 'CORINTO'})
MATCH (mes:MES {numero: 4})
MATCH (anio:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Homicidio'})
MATCH (af1:Afectacion {nombre: 'Fallecido'})
MATCH (af2:Afectacion {nombre: 'Herido'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(mes)
MERGE (h)-[:EN_AÑO]->(anio)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 1}]->(af1)
MERGE (h)-[:GENERA {cantidad: 1}]->(af2);
///
CREATE (h:HECHO {
  id: 'EVT_20240425_ARGELIA_01',
  fecha: date('2024-04-25'),
  descripcion: 'Combate con baja de 15 subversivos'
})

MATCH (cp:CentroPoblado {nombre: 'EL PLATEADO', nombre_municipio: 'ARGELIA'})
MATCH (mes:MES {numero: 4})
MATCH (anio:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Enfrentamiento'})
MATCH (af:Afectacion {nombre: 'Fallecido'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(mes)
MERGE (h)-[:EN_AÑO]->(anio)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 15}]->(af);
///
CREATE (h:HECHO {
  id: 'EVT_20240426_CORINTO_01',
  fecha: date('2024-04-26'),
  descripcion: 'Masacre de 4 personas y 1 herida'
})

MATCH (cp:CentroPoblado {nombre: 'CORINTO', nombre_municipio: 'CORINTO'})
MATCH (mes:MES {numero: 4})
MATCH (anio:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Homicidio'})
MATCH (af1:Afectacion {nombre: 'Fallecido'})
MATCH (af2:Afectacion {nombre: 'Herido'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(mes)
MERGE (h)-[:EN_AÑO]->(anio)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 4}]->(af1)
MERGE (h)-[:GENERA {cantidad: 1}]->(af2);
///
CREATE (h:HECHO {
  id: 'EVT_20240427_TORIBIO_01',
  fecha: date('2024-04-27'),
  descripcion: 'Secuestro de un soldado'
})

MATCH (cp:CentroPoblado {nombre: 'TORIBÍO', nombre_municipio: 'TORIBÍO'})
MATCH (mes:MES {numero: 4})
MATCH (anio:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Secuestro'})
MATCH (a1:Actor {nombre: 'Fuerza Pública'})
MATCH (a2:Actor {nombre: 'Grupo Armado Organizado'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(mes)
MERGE (h)-[:EN_AÑO]->(anio)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:RESPONSABLE]->(a2)
MERGE (h)-[:PARTICIPA]->(a1);
///
CREATE (h:HECHO {
  id: 'EVT_20240502_ARGELIA_01',
  fecha: date('2024-05-02'),
  descripcion: 'Combate con 4 soldados asesinados'
})

MATCH (cp:CentroPoblado {nombre: 'ARGELIA', nombre_municipio: 'ARGELIA'})
MATCH (mes:MES {numero: 5})
MATCH (anio:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Enfrentamiento'})
MATCH (af:Afectacion {nombre: 'Fallecido'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(mes)
MERGE (h)-[:EN_AÑO]->(anio)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 4}]->(af);
///
CREATE (h:HECHO {
  id: 'EVT_20240506_SILVIA_01',
  fecha: date('2024-05-06'),
  descripcion: 'Combate con explosivos, muertos, heridos y desplazamiento'
})

MATCH (cp:CentroPoblado {nombre: 'SILVIA', nombre_municipio: 'SILVIA'})
MATCH (mes:MES {numero: 5})
MATCH (anio:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Enfrentamiento'})
MATCH (af1:Afectacion {nombre: 'Fallecido'})
MATCH (af2:Afectacion {nombre: 'Herido'})
MATCH (af3:Afectacion {nombre: 'Desplazamiento'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(mes)
MERGE (h)-[:EN_AÑO]->(anio)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 2}]->(af1)
MERGE (h)-[:GENERA {cantidad: 2}]->(af2)
MERGE (h)-[:GENERA]->(af3);
///
CREATE (h:HECHO {
  id: 'EVT_20240506_SUAREZ_01',
  fecha: date('2024-05-06'),
  descripcion: 'Homicidio de lideresa con desplazamiento posterior'
})

MATCH (cp:CentroPoblado {nombre: 'SUÁREZ', nombre_municipio: 'SUÁREZ'})
MATCH (mes:MES {numero: 5})
MATCH (anio:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Homicidio'})
MATCH (af1:Afectacion {nombre: 'Fallecido'})
MATCH (af2:Afectacion {nombre: 'Desplazamiento'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(mes)
MERGE (h)-[:EN_AÑO]->(anio)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:GENERA {cantidad: 1}]->(af1)
MERGE (h)-[:GENERA]->(af2);
///
CREATE (h:HECHO {
  id: 'EVT_20240510_MIRANDA_01',
  fecha: date('2024-05-10'),
  descripcion: 'Ataque con carro bomba a base militar'
})

MATCH (cp:CentroPoblado {nombre: 'MIRANDA', nombre_municipio: 'MIRANDA'})
MATCH (mes:MES {numero: 5})
MATCH (anio:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Atentado Terrorista'})
MATCH (a:Actor {nombre: 'Grupo Armado Organizado'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(mes)
MERGE (h)-[:EN_AÑO]->(anio)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:RESPONSABLE]->(a);
///
CREATE (h:HECHO {
  id: 'EVT_20240514_PATIA_01',
  fecha: date('2024-05-14'),
  descripcion: 'Bloqueo de vía panamericana'
})

MATCH (cp:CentroPoblado {nombre: 'EL BORDO', nombre_municipio: 'PATÍA'})
MATCH (mes:MES {numero: 5})
MATCH (anio:AÑO {numero: 2024})
MATCH (c:Categoria {nombre: 'Acción de Protesta'})
MATCH (a:Actor {nombre: 'Civil / Comunidad'})

MERGE (h)-[:OCURRE_EN]->(cp)
MERGE (h)-[:EN_MES]->(mes)
MERGE (h)-[:EN_AÑO]->(anio)
MERGE (h)-[:ES_DE]->(c)
MERGE (h)-[:RESPONSABLE]->(a);

