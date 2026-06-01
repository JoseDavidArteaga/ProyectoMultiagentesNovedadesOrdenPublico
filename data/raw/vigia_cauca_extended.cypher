// =============================================================
// VIGÍA CAUCA — Datos extendidos (15 novedades adicionales)
// Compatible con vigia_cauca_neo4j.cypher
// Novedades: nov-005 … nov-019
// =============================================================

// -------------------------------------------------------------
// 1. UBICACIONES ADICIONALES
// -------------------------------------------------------------

// — Municipios —
MERGE (:MUNICIPIO {id: "mun-6",  nombre: "Santander de Quilichao", departamento: "Cauca", area: "Mixta"});
MERGE (:MUNICIPIO {id: "mun-7",  nombre: "Silvia",                 departamento: "Cauca", area: "Mixta"});
MERGE (:MUNICIPIO {id: "mun-8",  nombre: "Inzá",                   departamento: "Cauca", area: "Rural"});
MERGE (:MUNICIPIO {id: "mun-9",  nombre: "Caloto",                 departamento: "Cauca", area: "Mixta"});
MERGE (:MUNICIPIO {id: "mun-10", nombre: "Timbío",                 departamento: "Cauca", area: "Rural"});

// — Veredas, barrios, territorios indígenas —

// Santander de Quilichao
MATCH (m:MUNICIPIO {id: "mun-6"})
MERGE (cr:CORREGIMIENTO {id: "crr-4", nombre: "Corregimiento Calle Larga", corregidor: "No asignado"})
MERGE (m)-[:CONTIENE {tipo: "rural"}]->(cr);
MATCH (cr:CORREGIMIENTO {id: "crr-4"})
MERGE (v:VEREDA {id: "ver-5", nombre: "Vereda Calle Larga"})
MERGE (cr)-[:CONTIENE]->(v);
MATCH (m:MUNICIPIO {id: "mun-6"})
MERGE (c:COMUNA {id: "com-3", nombre: "Comuna 3", numero: 3})
MERGE (m)-[:CONTIENE {tipo: "urbano"}]->(c);
MATCH (c:COMUNA {id: "com-3"})
MERGE (b:BARRIO {id: "bar-4", nombre: "Barrio El Carmen"})
MERGE (c)-[:CONTIENE]->(b);

// Silvia
MATCH (m:MUNICIPIO {id: "mun-7"})
MERGE (cr:CORREGIMIENTO {id: "crr-5", nombre: "Corregimiento Cacique", corregidor: "No asignado"})
MERGE (m)-[:CONTIENE {tipo: "rural"}]->(cr);
MATCH (cr:CORREGIMIENTO {id: "crr-5"})
MERGE (v:VEREDA {id: "ver-6", nombre: "Vereda La Meseta"})
MERGE (cr)-[:CONTIENE]->(v);
MATCH (v:VEREDA {id: "ver-6"})
MERGE (s:SECTOR {id: "sec-4", nombre: "Sector Belén"})
MERGE (v)-[:CONTIENE]->(s);
MATCH (m:MUNICIPIO {id: "mun-7"})
MERGE (ti:TERRITORIO_INDIGENA {id: "ti-3", nombre: "Resguardo Indígena de Silvia", pueblo: "Misak", cabildo: "Cabildo de Silvia"})
MERGE (m)-[:CONTIENE]->(ti);
MATCH (ti:TERRITORIO_INDIGENA {id: "ti-3"})
MATCH (v:VEREDA {id: "ver-6"})
MERGE (ti)-[:COMPRENDE]->(v);

// Inzá
MATCH (m:MUNICIPIO {id: "mun-8"})
MERGE (cr:CORREGIMIENTO {id: "crr-6", nombre: "Corregimiento El Crucero", corregidor: "No asignado"})
MERGE (m)-[:CONTIENE {tipo: "rural"}]->(cr);
MATCH (cr:CORREGIMIENTO {id: "crr-6"})
MERGE (v:VEREDA {id: "ver-7", nombre: "Vereda El Crucero"})
MERGE (cr)-[:CONTIENE]->(v);
MATCH (m:MUNICIPIO {id: "mun-8"})
MERGE (ti:TERRITORIO_INDIGENA {id: "ti-4", nombre: "Resguardo Indígena de Inzá", pueblo: "Nasa", cabildo: "Cabildo de Inzá"})
MERGE (m)-[:CONTIENE]->(ti);

// Caloto
MATCH (m:MUNICIPIO {id: "mun-9"})
MERGE (cr:CORREGIMIENTO {id: "crr-7", nombre: "Corregimiento Piedra Sentada", corregidor: "No asignado"})
MERGE (m)-[:CONTIENE {tipo: "rural"}]->(cr);
MATCH (cr:CORREGIMIENTO {id: "crr-7"})
MERGE (v:VEREDA {id: "ver-8", nombre: "Vereda Piedra Sentada"})
MERGE (cr)-[:CONTIENE]->(v);

// Timbío
MATCH (m:MUNICIPIO {id: "mun-10"})
MERGE (v:VEREDA {id: "ver-9", nombre: "Vereda La Cascada"})
MERGE (m)-[:CONTIENE {tipo: "rural"}]->(v);


// -------------------------------------------------------------
// 2. NOVEDADES ADICIONALES (15 registros)
// -------------------------------------------------------------

// nov-005 — Santander de Quilichao, 2022
MATCH (actor:ACTOR {id: "actor-2"})
MATCH (usr:USUARIO {id: "user-1"})
MATCH (loc:VEREDA {id: "ver-5"})
CREATE (n:NOVEDAD {
  id: "nov-005", categoria: "Enfrentamiento",
  descripcion: "Enfrentamiento armado entre grupos en vereda Calle Larga.",
  fecha: date("2022-08-15"), hora: time("22:00:00"),
  nivel_confianza: "Confirmado", visibilidad: "Público",
  fuente: "Informe militar", creado_en: datetime()
})
CREATE (actor)-[:PARTICIPA_EN {rol: "Agresor"}]->(n)
CREATE (n)-[:OCURRE_EN]->(loc)
CREATE (usr)-[:REPORTA {fecha_reporte: datetime()}]->(n);

// nov-006 — Silvia, 2022
MATCH (actor:ACTOR {id: "actor-3"})
MATCH (usr:USUARIO {id: "user-2"})
MATCH (loc:SECTOR {id: "sec-4"})
CREATE (n:NOVEDAD {
  id: "nov-006", categoria: "Hostigamiento",
  descripcion: "Hostigamiento a patrulla de policía en Sector Belén.",
  fecha: date("2022-11-03"), hora: time("03:45:00"),
  nivel_confianza: "Confirmado", visibilidad: "Público",
  fuente: "Policía Nacional", creado_en: datetime()
})
CREATE (actor)-[:PARTICIPA_EN {rol: "Agresor"}]->(n)
CREATE (n)-[:OCURRE_EN]->(loc)
CREATE (usr)-[:REPORTA {fecha_reporte: datetime()}]->(n);

// nov-007 — Toribío (territorio indígena), 2023
MATCH (actor:ACTOR {id: "actor-4"})
MATCH (usr:USUARIO {id: "user-1"})
MATCH (loc:TERRITORIO_INDIGENA {id: "ti-1"})
CREATE (n:NOVEDAD {
  id: "nov-007", categoria: "Secuestro",
  descripcion: "Secuestro de líder comunitario en resguardo de Toribío.",
  fecha: date("2023-01-20"), hora: time("19:30:00"),
  nivel_confianza: "Preliminar", visibilidad: "Privado",
  fuente: "CTI - Fiscalía", creado_en: datetime()
})
CREATE (actor)-[:PARTICIPA_EN {rol: "Presunto autor"}]->(n)
CREATE (n)-[:OCURRE_EN]->(loc)
CREATE (usr)-[:REPORTA {fecha_reporte: datetime()}]->(n);

// nov-008 — Popayán, 2023
MATCH (actor:ACTOR {id: "actor-5"})
MATCH (usr:USUARIO {id: "user-2"})
MATCH (loc:BARRIO {id: "bar-2"})
CREATE (n:NOVEDAD {
  id: "nov-008", categoria: "Acción de Protesta",
  descripcion: "Manifestación y cierre de vías en barrio El Uvo, Popayán.",
  fecha: date("2023-03-12"), hora: time("08:00:00"),
  nivel_confianza: "Confirmado", visibilidad: "Público",
  fuente: "Prensa local", creado_en: datetime()
})
CREATE (actor)-[:PARTICIPA_EN {rol: "Participante"}]->(n)
CREATE (n)-[:OCURRE_EN]->(loc)
CREATE (usr)-[:REPORTA {fecha_reporte: datetime()}]->(n);

// nov-009 — Corinto, 2023
MATCH (actor:ACTOR {id: "actor-6"})
MATCH (usr:USUARIO {id: "user-3"})
MATCH (loc:SECTOR {id: "sec-1"})
CREATE (n:NOVEDAD {
  id: "nov-009", categoria: "Homicidio",
  descripcion: "Homicidio de civil en Sector La Montaña, Corinto.",
  fecha: date("2023-06-28"), hora: time("23:15:00"),
  nivel_confianza: "En verificación", visibilidad: "Privado",
  fuente: "Informe de unidad", creado_en: datetime()
})
CREATE (actor)-[:PARTICIPA_EN {rol: "Presunto autor"}]->(n)
CREATE (n)-[:OCURRE_EN]->(loc)
CREATE (usr)-[:REPORTA {fecha_reporte: datetime()}]->(n);

// nov-010 — Buenos Aires, 2023
MATCH (actor:ACTOR {id: "actor-1"})
MATCH (usr:USUARIO {id: "user-1"})
MATCH (loc:VEREDA {id: "ver-3"})
CREATE (n:NOVEDAD {
  id: "nov-010", categoria: "Enfrentamiento",
  descripcion: "Combates entre fuerza pública y grupo armado en vereda La Balsa.",
  fecha: date("2023-09-05"), hora: time("14:00:00"),
  nivel_confianza: "Confirmado", visibilidad: "Público",
  fuente: "Ejército Nacional", creado_en: datetime()
})
CREATE (actor)-[:PARTICIPA_EN {rol: "Participante"}]->(n)
CREATE (n)-[:OCURRE_EN]->(loc)
CREATE (usr)-[:REPORTA {fecha_reporte: datetime()}]->(n);

// nov-011 — Jambaló, 2023
MATCH (actor:ACTOR {id: "actor-3"})
MATCH (usr:USUARIO {id: "user-2"})
MATCH (loc:TERRITORIO_INDIGENA {id: "ti-2"})
CREATE (n:NOVEDAD {
  id: "nov-011", categoria: "Retén Ilegal",
  descripcion: "Retén ilegal en vía hacia resguardo de Jambaló.",
  fecha: date("2023-10-18"), hora: time("11:30:00"),
  nivel_confianza: "Confirmado", visibilidad: "Público",
  fuente: "Policía Metropolitana", creado_en: datetime()
})
CREATE (actor)-[:PARTICIPA_EN {rol: "Agresor"}]->(n)
CREATE (n)-[:OCURRE_EN]->(loc)
CREATE (usr)-[:REPORTA {fecha_reporte: datetime()}]->(n);

// nov-012 — Inzá, 2024
MATCH (actor:ACTOR {id: "actor-2"})
MATCH (usr:USUARIO {id: "user-1"})
MATCH (loc:VEREDA {id: "ver-7"})
CREATE (n:NOVEDAD {
  id: "nov-012", categoria: "Atentado Terrorista",
  descripcion: "Atentado con explosivos contra infraestructura en vereda El Crucero.",
  fecha: date("2024-02-14"), hora: time("04:20:00"),
  nivel_confianza: "Preliminar", visibilidad: "Privado",
  fuente: "CTI - Fiscalía", creado_en: datetime()
})
CREATE (actor)-[:PARTICIPA_EN {rol: "Agresor"}]->(n)
CREATE (n)-[:OCURRE_EN]->(loc)
CREATE (usr)-[:REPORTA {fecha_reporte: datetime()}]->(n);

// nov-013 — Caloto, 2024
MATCH (actor:ACTOR {id: "actor-4"})
MATCH (usr:USUARIO {id: "user-2"})
MATCH (loc:VEREDA {id: "ver-8"})
CREATE (n:NOVEDAD {
  id: "nov-013", categoria: "Reclutamiento Ilícito",
  descripcion: "Presunto reclutamiento de menores en vereda Piedra Sentada.",
  fecha: date("2024-07-22"), hora: time("16:45:00"),
  nivel_confianza: "En verificación", visibilidad: "Público",
  fuente: "Defensoría del Pueblo", creado_en: datetime()
})
CREATE (actor)-[:PARTICIPA_EN {rol: "Presunto autor"}]->(n)
CREATE (n)-[:OCURRE_EN]->(loc)
CREATE (usr)-[:REPORTA {fecha_reporte: datetime()}]->(n);

// nov-014 — Timbío, 2024
MATCH (actor:ACTOR {id: "actor-5"})
MATCH (usr:USUARIO {id: "user-3"})
MATCH (loc:VEREDA {id: "ver-9"})
CREATE (n:NOVEDAD {
  id: "nov-014", categoria: "Hallazgo de Material",
  descripcion: "Hallazgo de material de guerra abandonado en vereda La Cascada.",
  fecha: date("2024-09-10"), hora: time("09:00:00"),
  nivel_confianza: "Confirmado", visibilidad: "Público",
  fuente: "Ejército Nacional", creado_en: datetime()
})
CREATE (actor)-[:PARTICIPA_EN {rol: "Participante"}]->(n)
CREATE (n)-[:OCURRE_EN]->(loc)
CREATE (usr)-[:REPORTA {fecha_reporte: datetime()}]->(n);

// nov-015 — Popayán, 2024
MATCH (actor:ACTOR {id: "actor-6"})
MATCH (usr:USUARIO {id: "user-1"})
MATCH (loc:BARRIO {id: "bar-3"})
CREATE (n:NOVEDAD {
  id: "nov-015", categoria: "Hostigamiento",
  descripcion: "Hostigamiento a estación de policía en barrio Bella Vista, Popayán.",
  fecha: date("2024-10-30"), hora: time("02:10:00"),
  nivel_confianza: "Confirmado", visibilidad: "Público",
  fuente: "Policía Nacional", creado_en: datetime()
})
CREATE (actor)-[:PARTICIPA_EN {rol: "Agresor"}]->(n)
CREATE (n)-[:OCURRE_EN]->(loc)
CREATE (usr)-[:REPORTA {fecha_reporte: datetime()}]->(n);

// nov-016 — Santander de Quilichao, 2024
MATCH (actor:ACTOR {id: "actor-7"})
MATCH (usr:USUARIO {id: "user-2"})
MATCH (loc:BARRIO {id: "bar-4"})
CREATE (n:NOVEDAD {
  id: "nov-016", categoria: "Otro",
  descripcion: "Amenazas a comerciantes en barrio El Carmen.",
  fecha: date("2024-11-15"), hora: time("18:00:00"),
  nivel_confianza: "En verificación", visibilidad: "Privado",
  fuente: "Gaula Policía", creado_en: datetime()
})
CREATE (actor)-[:PARTICIPA_EN {rol: "Presunto autor"}]->(n)
CREATE (n)-[:OCURRE_EN]->(loc)
CREATE (usr)-[:REPORTA {fecha_reporte: datetime()}]->(n);

// nov-017 — Corinto, 2024
MATCH (actor:ACTOR {id: "actor-3"})
MATCH (usr:USUARIO {id: "user-1"})
MATCH (loc:CORREGIMIENTO {id: "crr-1"})
CREATE (n:NOVEDAD {
  id: "nov-017", categoria: "Ataque con Dron",
  descripcion: "Sobrevuelo de dron con carga explosiva sobre corregimiento La Paz.",
  fecha: date("2024-12-01"), hora: time("05:00:00"),
  nivel_confianza: "Preliminar", visibilidad: "Público",
  fuente: "Informe de unidad", creado_en: datetime()
})
CREATE (actor)-[:PARTICIPA_EN {rol: "Agresor"}]->(n)
CREATE (n)-[:OCURRE_EN]->(loc)
CREATE (usr)-[:REPORTA {fecha_reporte: datetime()}]->(n);

// nov-018 — Toribío, 2025
MATCH (actor:ACTOR {id: "actor-2"})
MATCH (usr:USUARIO {id: "user-2"})
MATCH (loc:VEREDA {id: "ver-2"})
CREATE (n:NOVEDAD {
  id: "nov-018", categoria: "Enfrentamiento",
  descripcion: "Enfrentamiento entre grupos armados en vereda Los Monos, Toribío.",
  fecha: date("2025-01-15"), hora: time("20:30:00"),
  nivel_confianza: "Confirmado", visibilidad: "Público",
  fuente: "Ejército Nacional", creado_en: datetime()
})
CREATE (actor)-[:PARTICIPA_EN {rol: "Participante"}]->(n)
CREATE (n)-[:OCURRE_EN]->(loc)
CREATE (usr)-[:REPORTA {fecha_reporte: datetime()}]->(n);

// nov-019 — Buenos Aires, 2025
MATCH (actor:ACTOR {id: "actor-4"})
MATCH (usr:USUARIO {id: "user-1"})
MATCH (loc:SECTOR {id: "sec-3"})
CREATE (n:NOVEDAD {
  id: "nov-019", categoria: "Homicidio",
  descripcion: "Homicidio selectivo en Sector Betania, Buenos Aires.",
  fecha: date("2025-03-08"), hora: time("22:45:00"),
  nivel_confianza: "Confirmado", visibilidad: "Público",
  fuente: "CTI - Fiscalía", creado_en: datetime()
})
CREATE (actor)-[:PARTICIPA_EN {rol: "Presunto autor"}]->(n)
CREATE (n)-[:OCURRE_EN]->(loc)
CREATE (usr)-[:REPORTA {fecha_reporte: datetime()}]->(n);


// -------------------------------------------------------------
// 3. VÍCTIMAS Y AFECTACIONES (solo algunas novedades)
// -------------------------------------------------------------

// Víctima nov-005
MATCH (n:NOVEDAD {id: "nov-005"})
CREATE (v:VICTIMA {
  id: "vic-004", nombre: "No identificado", edad: 28,
  genero: "Masculino", grupo_poblacional: "Campesino/a", condicion: "Herido"
})
CREATE (n)-[:TIENE_VICTIMA]->(v);

// Víctimas nov-009
MATCH (n:NOVEDAD {id: "nov-009"})
CREATE (v:VICTIMA {
  id: "vic-005", nombre: "Reservado", edad: 45,
  genero: "Masculino", grupo_poblacional: "Indígena", condicion: "Fallecido"
})
CREATE (n)-[:TIENE_VICTIMA]->(v);

// Víctima nov-015
MATCH (n:NOVEDAD {id: "nov-015"})
CREATE (v:VICTIMA {
  id: "vic-006", nombre: "No identificado", edad: 32,
  genero: "Femenino", grupo_poblacional: "Afrocolombiano/a", condicion: "Herido"
})
CREATE (n)-[:TIENE_VICTIMA]->(v);

// Afectación nov-005
MATCH (n:NOVEDAD {id: "nov-005"})
MATCH (v:VICTIMA {id: "vic-004"})
CREATE (af:AFECTACION_HUMANA {
  id: "af-003", heridos_civiles: 1, heridos_fuerza_publica: 0,
  fallecidos_civiles: 0, fallecidos_fuerza_publica: 0, desplazados: 0,
  reclutamiento_menores_flag: "No aplica", observaciones: "Civil herido leve."
})
CREATE (n)-[:GENERA]->(af)
CREATE (v)-[:REGISTRA]->(af);

// Afectación nov-009
MATCH (n:NOVEDAD {id: "nov-009"})
MATCH (v:VICTIMA {id: "vic-005"})
CREATE (af:AFECTACION_HUMANA {
  id: "af-004", heridos_civiles: 0, heridos_fuerza_publica: 0,
  fallecidos_civiles: 1, fallecidos_fuerza_publica: 0, desplazados: 5,
  reclutamiento_menores_flag: "No aplica", observaciones: "Familia desplazada."
})
CREATE (n)-[:GENERA]->(af)
CREATE (v)-[:REGISTRA]->(af);


// -------------------------------------------------------------
// 4. CILINDROS BOMBA (6 registros)
//    Categoría: Atentado Terrorista (explotaron)
//    Categoría: Hallazgo de Material (NO explotaron / ineficientes)
// -------------------------------------------------------------

// nov-020 — Toribío, 2022  (SÍ explotó → Atentado Terrorista)
MATCH (actor:ACTOR {id: "actor-3"})
MATCH (usr:USUARIO {id: "user-2"})
MATCH (loc:VEREDA {id: "ver-2"})
CREATE (n:NOVEDAD {
  id: "nov-020", categoria: "Atentado Terrorista",
  descripcion: "Lanzamiento de cilindro bomba que impactó vivienda en vereda Los Monos, Toribío. Artefacto detonó causando daños estructurales.",
  fecha: date("2022-03-17"), hora: time("01:45:00"),
  nivel_confianza: "Confirmado", visibilidad: "Público",
  fuente: "Ejército Nacional", creado_en: datetime()
})
CREATE (actor)-[:PARTICIPA_EN {rol: "Agresor"}]->(n)
CREATE (n)-[:OCURRE_EN]->(loc)
CREATE (usr)-[:REPORTA {fecha_reporte: datetime()}]->(n);

// nov-021 — Corinto, 2022  (NO explotó → Hallazgo de Material)
MATCH (actor:ACTOR {id: "actor-4"})
MATCH (usr:USUARIO {id: "user-1"})
MATCH (loc:CORREGIMIENTO {id: "crr-1"})
CREATE (n:NOVEDAD {
  id: "nov-021", categoria: "Hallazgo de Material",
  descripcion: "Hallazgo de cilindro bomba sin detonar en corregimiento La Paz, Corinto. Material fue neutralizado por brigada de desminado.",
  fecha: date("2022-07-08"), hora: time("10:20:00"),
  nivel_confianza: "Confirmado", visibilidad: "Público",
  fuente: "Policía Nacional", creado_en: datetime()
})
CREATE (actor)-[:PARTICIPA_EN {rol: "Presunto autor"}]->(n)
CREATE (n)-[:OCURRE_EN]->(loc)
CREATE (usr)-[:REPORTA {fecha_reporte: datetime()}]->(n);

// nov-022 — Inzá, 2023  (SÍ explotó → Atentado Terrorista)
MATCH (actor:ACTOR {id: "actor-2"})
MATCH (usr:USUARIO {id: "user-2"})
MATCH (loc:TERRITORIO_INDIGENA {id: "ti-4"})
CREATE (n:NOVEDAD {
  id: "nov-022", categoria: "Atentado Terrorista",
  descripcion: "Cilindro bomba lanzado desde montaña hacia resguardo indígena de Inzá. Detonación afectó viviendas cercanas.",
  fecha: date("2023-04-25"), hora: time("04:10:00"),
  nivel_confianza: "Confirmado", visibilidad: "Privado",
  fuente: "CTI - Fiscalía", creado_en: datetime()
})
CREATE (actor)-[:PARTICIPA_EN {rol: "Agresor"}]->(n)
CREATE (n)-[:OCURRE_EN]->(loc)
CREATE (usr)-[:REPORTA {fecha_reporte: datetime()}]->(n);

// nov-023 — Caloto, 2023  (NO explotó → Hallazgo de Material)
MATCH (actor:ACTOR {id: "actor-6"})
MATCH (usr:USUARIO {id: "user-3"})
MATCH (loc:VEREDA {id: "ver-8"})
CREATE (n:NOVEDAD {
  id: "nov-023", categoria: "Hallazgo de Material",
  descripcion: "Cilindro bomba de fabricación casera encontrado en vereda Piedra Sentada, Caloto. Artefacto resultó ineficiente y no detonó.",
  fecha: date("2023-08-14"), hora: time("15:30:00"),
  nivel_confianza: "Preliminar", visibilidad: "Público",
  fuente: "Informe de unidad", creado_en: datetime()
})
CREATE (actor)-[:PARTICIPA_EN {rol: "Presunto autor"}]->(n)
CREATE (n)-[:OCURRE_EN]->(loc)
CREATE (usr)-[:REPORTA {fecha_reporte: datetime()}]->(n);

// nov-024 — Santander de Quilichao, 2024  (SÍ explotó → Atentado Terrorista)
MATCH (actor:ACTOR {id: "actor-3"})
MATCH (usr:USUARIO {id: "user-1"})
MATCH (loc:VEREDA {id: "ver-5"})
CREATE (n:NOVEDAD {
  id: "nov-024", categoria: "Atentado Terrorista",
  descripcion: "Cilindro bomba detonó cerca de escuela rural en vereda Calle Larga, Santander de Quilichao. Se reportan daños materiales.",
  fecha: date("2024-03-03"), hora: time("06:50:00"),
  nivel_confianza: "Confirmado", visibilidad: "Público",
  fuente: "Defensoría del Pueblo", creado_en: datetime()
})
CREATE (actor)-[:PARTICIPA_EN {rol: "Agresor"}]->(n)
CREATE (n)-[:OCURRE_EN]->(loc)
CREATE (usr)-[:REPORTA {fecha_reporte: datetime()}]->(n);

// nov-025 — Silvia, 2024  (NO explotó → Hallazgo de Material)
MATCH (actor:ACTOR {id: "actor-5"})
MATCH (usr:USUARIO {id: "user-2"})
MATCH (loc:SECTOR {id: "sec-4"})
CREATE (n:NOVEDAD {
  id: "nov-025", categoria: "Hallazgo de Material",
  descripcion: "Cilindro bomba localizado en Sector Belén, Silvia. Dispositivo no detonó y fue desactivado por unidades antiexplosivos.",
  fecha: date("2024-08-19"), hora: time("11:15:00"),
  nivel_confianza: "En verificación", visibilidad: "Privado",
  fuente: "Policía Nacional", creado_en: datetime()
})
CREATE (actor)-[:PARTICIPA_EN {rol: "Presunto autor"}]->(n)
CREATE (n)-[:OCURRE_EN]->(loc)
CREATE (usr)-[:REPORTA {fecha_reporte: datetime()}]->(n);

// Víctima nov-020
MATCH (n:NOVEDAD {id: "nov-020"})
CREATE (v:VICTIMA {
  id: "vic-007", nombre: "Reservado", edad: 62,
  genero: "Masculino", grupo_poblacional: "Indígena", condicion: "Herido"
})
CREATE (n)-[:TIENE_VICTIMA]->(v);

// Afectación nov-020
MATCH (n:NOVEDAD {id: "nov-020"})
MATCH (v:VICTIMA {id: "vic-007"})
CREATE (af:AFECTACION_HUMANA {
  id: "af-005", heridos_civiles: 1, heridos_fuerza_publica: 0,
  fallecidos_civiles: 0, fallecidos_fuerza_publica: 0, desplazados: 3,
  reclutamiento_menores_flag: "No aplica", observaciones: "Daños en vivienda, familia evacuada."
})
CREATE (n)-[:GENERA]->(af)
CREATE (v)-[:REGISTRA]->(af);

// Víctima nov-022
MATCH (n:NOVEDAD {id: "nov-022"})
CREATE (v:VICTIMA {
  id: "vic-008", nombre: "No identificado", edad: 34,
  genero: "Femenino", grupo_poblacional: "Indígena", condicion: "Herido"
})
CREATE (n)-[:TIENE_VICTIMA]->(v);

// Afectación nov-022
MATCH (n:NOVEDAD {id: "nov-022"})
MATCH (v:VICTIMA {id: "vic-008"})
CREATE (af:AFECTACION_HUMANA {
  id: "af-006", heridos_civiles: 2, heridos_fuerza_publica: 0,
  fallecidos_civiles: 0, fallecidos_fuerza_publica: 0, desplazados: 8,
  reclutamiento_menores_flag: "No aplica", observaciones: "Múltiples viviendas afectadas por onda expansiva."
})
CREATE (n)-[:GENERA]->(af)
CREATE (v)-[:REGISTRA]->(af);
