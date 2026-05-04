# Integración de Langfuse — Observabilidad y Evaluación

## 📊 ¿Qué es Langfuse?

Langfuse es una plataforma de **observabilidad para aplicaciones LLM** que permite:

- **Rastrear** cada llamada de agente (input/output, latencia, tokens)
- **Evaluar** la calidad de las respuestas con scores y métricas
- **Debuguear** pipelines complejos viendo la ejecución paso a paso
- **Optimizar** costos y rendimiento identificando cuellos de botella

## 🔧 Configuración

### 1. Instalar Langfuse

```bash
pip install langfuse>=2.0.0
```

O si ya instaló requirements.txt:
```bash
pip install -r requirements.txt
```

### 2. Obtener Credenciales

**Opción A: Cloud (recomendado para demostración)**

1. Ir a https://cloud.langfuse.com
2. Crear una cuenta gratuita
3. En "Settings" → "API Keys", copiar:
   - `Public Key`
   - `Secret Key`

**Opción B: Self-Hosted (para producción)**

```bash
docker run -d \
  -e DATABASE_URL="postgresql://user:password@db:5432/langfuse" \
  -p 3000:3000 \
  langfuse/langfuse:latest
```

### 3. Configurar `.env`

Crear archivo `.env` en la raíz del proyecto:

```env
# ──── Langfuse ────────────────────────────────────────────────────
LANGFUSE_ENABLED=true
LANGFUSE_PUBLIC_KEY=your_public_key_here
LANGFUSE_SECRET_KEY=your_secret_key_here
# Para self-hosted, descomenta:
# LANGFUSE_BASE_URL=http://localhost:3000
```

### 4. Validar conexión

```bash
python -c "
from src.langfuse_integration import LangfuseTracer
tracer = LangfuseTracer()
print('✅ Langfuse conectado' if tracer.enabled else '⚠️ Langfuse desactivado')
"
```

## 📈 Cómo Funciona la Integración

### Arquitectura de Traces

```
Pipeline (Pregunta del usuario)
├── Agente 1 (Intérprete) ────→ JSON Intent
├── Agente 2 (Consultor) ─────→ Cypher Query
├── Neo4j ────────────────────→ Filas resultantes
└── Agente 3 (Redactor) ──────→ Informe final
```

Cada agente genera un **span** con:
- **Entrada**: pregunta/intención/filas
- **Salida**: resultado del agente
- **Métrica**: score de calidad (0-1)
- **Latencia**: tiempo de ejecución automático

### Ejemplo: Tracing en Acción

```python
from src.langfuse_integration import LangfuseTracer

tracer = LangfuseTracer()

# Trace de agente individual
with tracer.trace_agent("Agente 1 — Intérprete") as span:
    resultado = agente1(pregunta)
    span.update(
        input=pregunta,
        output=resultado,
    )
    span.score(0.95, name="json_valid", reason="JSON bien formado")

# Trace completo del pipeline
with tracer.trace_pipeline("Chat Query", question=pregunta) as pipeline_span:
    # ... ejecutar pipeline ...
    pipeline_span.update(output=respuesta_final)
    pipeline_span.score(name="overall_quality", score=0.92)

tracer.flush()  # Sincronizar con Langfuse
```

## 🎯 Métricas Capturadas

### Por Agente

| Métrica | Descripción |
|---------|-------------|
| `input` | Texto/JSON de entrada al agente |
| `output` | Resultado generado por el agente |
| `latency` | Tiempo total (automático) |
| `quality_score` | Score 0-1 de calidad |
| `reason` | Explicación del score |

### Para Neo4j

| Métrica | Descripción |
|---------|-------------|
| `query` | Cypher ejecutado |
| `params` | Parámetros de consulta |
| `row_count` | Filas retornadas |
| `execution_time_ms` | Tiempo en BD |

### Para Pipeline Completo

| Métrica | Descripción |
|---------|-------------|
| `question` | Pregunta original usuario |
| `answer` | Respuesta final |
| `rows_returned` | Total de filas procesadas |
| `query_success` | Booleano de éxito |
| `overall_quality` | Score final 0-1 |

## 🚀 Flujo en `app.py`

El tracer ya está integrado en `local_chat.py`. Cuando llamas desde `app.py`:

```python
from src.local_chat import LocalGraphChat

chat = LocalGraphChat()
resultado = chat.ask(pregunta, rol_usuario)  # ← Genera traces automáticos
```

**Internamente:**
1. `ask()` crea un `trace_pipeline()` 
2. Cada agente crea su `trace_agent()`
3. Neo4j crea un `trace_neo4j()`
4. Al final, llama a `tracer.flush()`

## 📱 Ver Traces en Dashboard

### En Cloud (Langfuse)

1. Abrir https://cloud.langfuse.com
2. Ir a "Dashboard"
3. Ver traces en tiempo real:
   - **Traces**: lista de ejecutiones completas
   - **Scores**: gráficos de métricas
   - **Latency**: histogramas de tiempos

### En Self-Hosted

1. Abrir http://localhost:3000
2. Misma interfaz que Cloud

### Inspeccionar un Trace

Click en cualquier trace:
- **Inputs**: ver pregunta original
- **Outputs**: respuesta final
- **Timeline**: gráfico de latencia por etapa
- **Scores**: todos los scores registrados
- **Metadata**: información adicional

## 🔌 Desactivar/Activar Langfuse

En `.env`:
```env
LANGFUSE_ENABLED=true   # Activado
# o
LANGFUSE_ENABLED=false  # Desactivado
```

Con `LANGFUSE_ENABLED=false`, la app funciona idénticamente pero sin enviar traces.

## 🐛 Debugging

### Verificar que se envían traces

```bash
LANGFUSE_ENABLED=true python app.py
# En consola verá: [✅ Langfuse] Conectado exitosamente
```

### Si dice "No se pudo conectar"

1. ¿Public Key/Secret Key correctas?
   ```bash
   python -c "import os; print(os.getenv('LANGFUSE_PUBLIC_KEY'))"
   ```

2. ¿Red accesible?
   ```bash
   curl https://api.langfuse.com/ping
   ```

3. ¿Firewall bloquea?
   ```bash
   nc -zv api.langfuse.com 443
   ```

### Ver logs detallados

```python
import logging
logging.basicConfig(level=logging.DEBUG)
# Luego tracer = LangfuseTracer()
```

## 📊 Evaluación Automática

Langfuse permite configurar evaluadores que califican respuestas:

```python
# En pipeline_span.score()
pipeline_span.score(
    name="factual_accuracy",
    score=0.92,  # 0-1 o True/False
    reason="Consulta validada contra Neo4j",
)
```

Luego en el dashboard verá:
- Distribución de scores
- Tendencias a lo largo del tiempo
- Alertas si score cae por debajo de umbral

## 💰 Costos y Límites

**Cloud (Langfuse)**
- Free: 1 millón de traces/mes
- Pago: $0.10 por millón de traces adicionales

**Self-Hosted**
- Sin costo directo (solo infraestructura)
- PostgreSQL + Docker

## 🔄 Integración Futura

Posibles extensiones:

1. **A/B Testing**: Comparar agentes con scores
2. **Fine-tuning**: Datos de evaluaciones → mejorar modelos
3. **Cost Tracking**: Token usage × precio modelo
4. **Alerting**: Webhook si quality < umbral

## 📚 Referencias

- Docs: https://docs.langfuse.com
- API: https://docs.langfuse.com/api
- GitHub: https://github.com/langfuse/langfuse

---

**Pregunta frecuente**: ¿Mi data es privada?
- **Cloud**: Encriptada en tránsito, almacenada en servidores Langfuse
- **Self-hosted**: Todo en tu infraestructura local/privada

**Próximo paso**: Ejecutar `python app.py` y abrir Langfuse dashboard para ver traces en vivo.
