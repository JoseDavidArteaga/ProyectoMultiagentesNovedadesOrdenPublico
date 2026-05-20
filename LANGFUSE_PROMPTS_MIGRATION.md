# Migración de Prompts a Langfuse

## Resumen

Los prompts del sistema Vigía Cauca se han refactorizado para ser gestionados centralmente en **Langfuse Prompt Management**. Esto permite:

- ✅ **Versionado**: Historial de cambios en prompts
- ✅ **Control de producción**: Etiquetar versiones como "production"  
- ✅ **Testing**: Probar nuevas versiones antes de desplegar
- ✅ **Auditoría**: Ver quién cambió qué y cuándo
- ✅ **Fallback local**: Si Langfuse no está disponible, usa versiones locales

## Arquitectura

```
src/prompts_manager.py
├── get_interpreter_prompt()      → Intérprete (Agente 1)
├── get_consultant_prompt()       → Consultor Cypher (Agente 2)
├── get_redactor_prompt()         → Redactor (Agente 3)
└── Fallbacks locales (_LOCAL_*_PROMPT)

src/local_chat.py
├── Importa: get_interpreter_prompt, get_consultant_prompt, get_redactor_prompt
└── Usa los prompts en: _agente1_interpretar(), _agente2_cypher(), _agente3_redactar()

migrate_prompts_to_langfuse.py
└── Script para crear/actualizar los prompts en Langfuse
```

## Modo 1: Usar prompts locales (por defecto)

Cuando `LANGFUSE_ENABLED=false` o no está configurado, el sistema usa las versiones locales en `src/prompts_manager.py`:

```bash
# Los prompts se recuperarán desde las definiciones locales (_LOCAL_*_PROMPT)
python app.py
# o
streamlit run app.py
```

**Ventajas**: Sin dependencias en Langfuse, funciona offline.  
**Desventajas**: Los cambios de prompts requieren redeploy de código.

## Modo 2: Usar prompts desde Langfuse

### Paso 1: Configurar Langfuse

1. Crea una cuenta en [https://cloud.langfuse.com](https://cloud.langfuse.com) (o usa tu instancia self-hosted)
2. Crea un proyecto
3. Ve a **Settings > API Keys** y copia:
   - `LANGFUSE_PUBLIC_KEY` (pk-lf-...)
   - `LANGFUSE_SECRET_KEY` (sk-lf-...)
   - (opcional) `LANGFUSE_HOST` (ej: https://us.cloud.langfuse.com)

### Paso 2: Migrar prompts a Langfuse

Exporta las credenciales en tu terminal:

```bash
export LANGFUSE_ENABLED=true
export LANGFUSE_PUBLIC_KEY=pk-lf-<your-key>
export LANGFUSE_SECRET_KEY=sk-lf-<your-key>
# Opcional (por defecto es https://us.cloud.langfuse.com):
# export LANGFUSE_HOST=https://cloud.langfuse.com
```

Ejecuta el script de migración:

```bash
python migrate_prompts_to_langfuse.py
```

Esperado:
```
✅ Conectado a Langfuse

📍 Creando/actualizando prompt 'vigia-interpreter'...
   ✅ 'vigia-interpreter' creado exitosamente

📍 Creando/actualizando prompt 'vigia-consultant'...
   ✅ 'vigia-consultant' creado exitosamente

📍 Creando/actualizando prompt 'vigia-redactor'...
   ✅ 'vigia-redactor' creado exitosamente

▀▄▀▄▀▄ MIGRACIÓN COMPLETADA ▀▄▀▄▀▄
✅ Los prompts están ahora en Langfuse y listos para ser usados.
   Abre https://cloud.langfuse.com para verlos en el dashboard.
```

### Paso 3: Usar prompts desde Langfuse

Una vez migrados, el sistema automáticamente:

1. **Intenta recuperar** los prompts desde Langfuse
2. **Usa la versión etiquetada** como "production" (creada en el paso anterior)
3. **Compila** las variables (ej: schema, fechas)
4. **Retrocede** a las versiones locales si Langfuse no está disponible

Ejecuta la app:

```bash
# Configurar variables (importante: LANGFUSE_ENABLED=true)
export LANGFUSE_ENABLED=true
export LANGFUSE_PUBLIC_KEY=pk-lf-<your-key>
export LANGFUSE_SECRET_KEY=sk-lf-<your-key>

# Ejecutar la app
streamlit run app.py
```

## Ejemplo: Editar un prompt en Langfuse

### Editar en el dashboard:

1. Abre https://cloud.langfuse.com
2. Ve a **Prompts** → busca "vigia-interpreter"
3. Haz clic en el prompt
4. Haz clic en **Edit** para cambiar el contenido
5. Guarda como nueva **versión**
6. Prueba la versión (opcional)
7. Etiquétala como **production** cuando esté lista

### Cambios se aplican automáticamente:

- La próxima vez que llames a `get_interpreter_prompt()`, recuperará la nueva versión con etiqueta "production"
- No requiere redeploy de código
- Los traces en Langfuse mostrarán qué versión de prompt se usó

## Estructura de los prompts en Langfuse

### vigia-interpreter

- **Nombre**: `vigia-interpreter`
- **Tipo**: `text`
- **Contenido**: System prompt para el Agente 1 (Intérprete)
- **Entrada**: pregunta del usuario + schema de Neo4j
- **Salida**: JSON con intención, categoría, ubicación, período, etc.

### vigia-consultant

- **Nombre**: `vigia-consultant`
- **Tipo**: `text`
- **Contenido**: System prompt para el Agente 2 (Consultor Cypher)
- **Entrada**: pregunta original + JSON de intención + schema
- **Salida**: JSON con query Cypher segura y parámetros

### vigia-redactor

- **Nombre**: `vigia-redactor`
- **Tipo**: `text`
- **Contenido**: System prompt para el Agente 3 (Redactor)
- **Entrada**: pregunta + intención + resultados Neo4j
- **Salida**: Informe redactado en lenguaje natural

## Troubleshooting

### Error: "Failed to fetch prompt from Langfuse"

```
⚠️  Failed to fetch prompt 'vigia-interpreter' from Langfuse: ...
```

**Causas comunes**:
- `LANGFUSE_ENABLED` no está en `true`
- Credenciales no están exportadas o son inválidas
- El host de Langfuse es incorrecto
- El prompt no existe en Langfuse (aún no fue migrado)

**Solución**:
```bash
# 1. Verifica las variables
echo $LANGFUSE_ENABLED        # Debe ser: true
echo $LANGFUSE_PUBLIC_KEY     # Debe ser: pk-lf-...
echo $LANGFUSE_SECRET_KEY     # Debe ser: sk-lf-...

# 2. Re-ejecuta la migración
python migrate_prompts_to_langfuse.py

# 3. Verifica en el dashboard
# https://cloud.langfuse.com/prompts → busca "vigia-"
```

### Los cambios en Langfuse no se aplican

Cuando editas un prompt en Langfuse:
1. Asegúrate de etiquetarlo como **production**
2. Espera 5-10 segundos (caching del SDK)
3. Reinicia la app o llama a `get_prompt()` nuevamente

### Usar una versión específica (no production)

Si quieres probar una versión sin promover a production:

```python
# En src/prompts_manager.py, modifica get_interpreter_prompt():
prompt_obj = client.get_prompt("vigia-interpreter", version="2.0.0")
# en lugar de:
prompt_obj = client.get_prompt("vigia-interpreter")  # usa "production"
```

## Próximos pasos

1. **Enlazar prompts a traces**: Ve a Langfuse > Prompts > vigia-interpreter → Link to traces
   - Esto mostrará cómo el prompt afecta la calidad de los outputs

2. **Agregar evaluaciones**: Usa Langfuse Evals para puntuar automáticamente los outputs
   - Ej: ¿La respuesta es coherente? ¿Está basada en datos?

3. **Monitoreo**: Crea dashboards en Langfuse para monitorear qué prompts se usan y su rendimiento

## Referencias

- [Langfuse Prompt Management Docs](https://langfuse.com/docs/prompts/get-started)
- [Langfuse Python SDK](https://langfuse.com/docs/observability/sdk/overview)
- [Langfuse Skills (AI agent integration)](https://github.com/langfuse/skills)
