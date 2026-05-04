#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_langfuse.py — Demo de Langfuse con la orquestación

Simula una consulta completa para verificar que el tracing funciona.

Uso:
    python test_langfuse.py
"""

import os
import sys
import json
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config import LANGFUSE_ENABLED
from langfuse_integration import LangfuseTracer


def simulate_agent1(question: str) -> dict:
    """Simula Agente 1: Intérprete."""
    # Simulación: convertir pregunta a intención JSON
    intencion = {
        "tipo_consulta": "evento",
        "municipios": ["Santander de Quilichao"],
        "fecha_desde": "2024-01-01",
        "fecha_hasta": "2024-12-31",
    }
    return intencion


def simulate_agent2(intencion: dict) -> str:
    """Simula Agente 2: Consultor (generador de Cypher)."""
    cypher = """
    MATCH (n:Novedad {municipio: 'Santander de Quilichao'})
    WHERE n.fecha >= '2024-01-01' AND n.fecha <= '2024-12-31'
    RETURN n LIMIT 10
    """
    return cypher


def simulate_neo4j(cypher: str) -> dict:
    """Simula ejecución Neo4j."""
    # Simulación: resultados
    records = [
        {"id": 1, "titulo": "Evento 1", "municipio": "Santander de Quilichao"},
        {"id": 2, "titulo": "Evento 2", "municipio": "Santander de Quilichao"},
    ]
    return {
        "records": records,
        "row_count": len(records),
        "execution_time_ms": 145.3,
    }


def simulate_agent3(question: str, records: list) -> str:
    """Simula Agente 3: Redactor."""
    answer = f"""
INFORME DE NOVEDADES - ORDEN PÚBLICO
═════════════════════════════════════

Pregunta: {question}

Resultados encontrados: {len(records)} eventos

Resumen:
Se han identificado {len(records)} novedad(es) en Santander de Quilichao
durante el período consultado. Los eventos se relacionan con temas de
orden público y seguridad ciudadana.

---
Informe generado por Agente 3 (Redactor)
    """
    return answer.strip()


def demo_individual_spans():
    """Demo: Rastrear agentes individuales."""
    print("\n" + "="*70)
    print("DEMO 1: Rastrear Agentes Individuales")
    print("="*70)
    
    tracer = LangfuseTracer()
    
    if not tracer.enabled:
        print("⚠️  Langfuse desactivado. Configure LANGFUSE_ENABLED=true en .env")
        return
    
    print("✅ Conectado a Langfuse\n")
    
    question = "¿Qué eventos de orden público ocurrieron en Santander de Quilichao?"
    
    # ─── Agente 1
    print("📍 Ejecutando Agente 1 (Intérprete)...")
    with tracer.trace_agent("Agente 1 — Intérprete") as span:
        intencion = simulate_agent1(question)
        span.update(
            input={"question": question},
            output=intencion,
        )
        span.score(name="json_valid", score=0.98, reason="JSON bien formado")
    print(f"   Intención: {json.dumps(intencion, ensure_ascii=False, indent=2)}\n")
    
    # ─── Agente 2
    print("📍 Ejecutando Agente 2 (Consultor)...")
    with tracer.trace_agent("Agente 2 — Consultor") as span:
        cypher = simulate_agent2(intencion)
        span.update(
            input={"intencion": intencion},
            output={"cypher": cypher},
        )
        span.score(name="cypher_valid", score=0.95, reason="Cypher sin errores de sintaxis")
    print(f"   Cypher: {cypher[:100]}...\n")
    
    # ─── Neo4j
    print("📍 Ejecutando Neo4j...")
    with tracer.trace_neo4j(cypher) as span:
        result = simulate_neo4j(cypher)
        span.update(
            row_count=result["row_count"],
            execution_time_ms=result["execution_time_ms"],
        )
        span.score(name="query_success", score=0.92, reason=f"{result['row_count']} filas retornadas")
    print(f"   Filas retornadas: {result['row_count']}")
    print(f"   Tiempo ejecución: {result['execution_time_ms']}ms\n")
    
    # ─── Agente 3
    print("📍 Ejecutando Agente 3 (Redactor)...")
    with tracer.trace_agent("Agente 3 — Redactor") as span:
        answer = simulate_agent3(question, result["records"])
        span.update(
            input={"question": question, "rows": result["row_count"]},
            output=answer[:150],
        )
        span.score(name="coherence", score=0.90, reason="Respuesta coherente")
    print(f"   Respuesta: {answer[:100]}...\n")
    
    # Sincronizar
    print("🔄 Sincronizando traces con Langfuse...")
    tracer.flush()
    print("✅ Traces enviados correctamente\n")
    
    print(f"📊 Dashboard: https://cloud.langfuse.com")
    print("   Busca traces con nombre 'Agente 1', 'Agente 2', etc.\n")


def demo_pipeline_trace():
    """Demo: Rastrear pipeline completo."""
    print("\n" + "="*70)
    print("DEMO 2: Rastrear Pipeline Completo")
    print("="*70)
    
    tracer = LangfuseTracer()
    
    if not tracer.enabled:
        print("⚠️  Langfuse desactivado. Configure LANGFUSE_ENABLED=true en .env")
        return
    
    print("✅ Conectado a Langfuse\n")
    
    question = "¿Cuántas novedades ocurrieron en la región?"
    
    print("📍 Ejecutando pipeline completo...")
    with tracer.trace_pipeline("Chat Query Demo", question=question) as pipeline_span:
        # Simular ejecución
        intencion = simulate_agent1(question)
        cypher = simulate_agent2(intencion)
        result = simulate_neo4j(cypher)
        answer = simulate_agent3(question, result["records"])
        
        # Actualizar pipeline
        pipeline_span.update(
            output={
                "answer": answer[:100],
                "rows_returned": result["row_count"],
                "query_success": True,
            }
        )
        
        # Score final
        pipeline_span.score(
            name="overall_quality",
            score=0.91,
            reason="Todos los agentes completados, respuesta coherente",
        )
    
    print(f"   Pregunta: {question}")
    print(f"   Respuesta: {answer[:80]}...")
    print(f"   Filas procesadas: {result['row_count']}\n")
    
    print("🔄 Sincronizando...")
    tracer.flush()
    print("✅ Trace de pipeline enviado\n")
    
    print(f"📊 Dashboard: https://cloud.langfuse.com")
    print("   Busca trace 'Chat Query Demo'\n")


def main():
    """Punto de entrada."""
    print("\n" + "▀"*70)
    print("🔍 TEST LANGFUSE — Demostración de Tracing")
    print("▄"*70)
    
    # Verificar configuración
    print(f"\n📋 Configuración:")
    print(f"   LANGFUSE_ENABLED = {LANGFUSE_ENABLED}")
    
    if not LANGFUSE_ENABLED:
        print("\n⚠️  Langfuse está DESACTIVADO.")
        print("\nPara activarlo:")
        print("   1. Crear archivo .env:")
        print("      LANGFUSE_ENABLED=true")
        print("      LANGFUSE_PUBLIC_KEY=your_key")
        print("      LANGFUSE_SECRET_KEY=your_secret")
        print("\n   2. O ejecutar:")
        print("      export LANGFUSE_ENABLED=true")
        return
    
    # Ejecutar demos
    try:
        demo_individual_spans()
        demo_pipeline_trace()
        
        print("▀"*70)
        print("✅ DEMO COMPLETADA")
        print("▄"*70)
        print("\n💡 Próximos pasos:")
        print("   1. Abre https://cloud.langfuse.com")
        print("   2. Verifica los traces recién enviados")
        print("   3. Inspecciona inputs, outputs y scores")
        print("   4. Ejecuta: python app.py (para traces reales)")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
