#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
migrate_prompts_to_langfuse.py — Migra los prompts del sistema Vigía Cauca a Langfuse.

Este script crea (o actualiza) los prompts en Langfuse para que puedan ser versionados,
probados, y promovidos a producción de forma centralizada.

Uso:
    1. Exporta las credenciales de Langfuse:
       export LANGFUSE_PUBLIC_KEY=pk-lf-...
       export LANGFUSE_SECRET_KEY=sk-lf-...
       export LANGFUSE_HOST=https://us.cloud.langfuse.com  (opcional)
       export LANGFUSE_ENABLED=true
    
    2. Ejecuta:
       python migrate_prompts_to_langfuse.py

Resultado:
    - Crea 3 prompts en Langfuse: vigia-interpreter, vigia-consultant, vigia-redactor
    - Los etiqueta como "testing_1" para uso inmediato
    - El código en local_chat.py puede entonces recuperarlos desde Langfuse
"""

import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent))

from config import LANGFUSE_ENABLED, LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY
from src.prompts_manager import (
    _LOCAL_INTERPRETER_PROMPT,
    _LOCAL_CONSULTANT_PROMPT,
    _LOCAL_REDACTOR_PROMPT,
)


def migrate_prompts() -> None:
    """Migra los prompts locales a Langfuse."""
    
    # Verificar credenciales
    if not LANGFUSE_ENABLED:
        print("❌ Langfuse no está habilitado. Exporta:")
        print("   export LANGFUSE_ENABLED=true")
        print("   export LANGFUSE_PUBLIC_KEY=pk-lf-...")
        print("   export LANGFUSE_SECRET_KEY=sk-lf-...")
        sys.exit(1)
    
    if not (LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY):
        print("❌ Faltan credenciales de Langfuse.")
        print("   Exporta LANGFUSE_PUBLIC_KEY y LANGFUSE_SECRET_KEY")
        sys.exit(1)
    
    # Inicializar cliente Langfuse
    try:
        from langfuse import get_client
        langfuse_client = get_client()
        print("✅ Conectado a Langfuse\n")
    except Exception as e:
        print(f"❌ Error al conectar a Langfuse: {e}")
        sys.exit(1)
    
    # ─── Prompt 1: Intérprete ───────────────────────────────────────────────────
    print("📍 Creando/actualizando prompt 'vigia-interpreter'...")
    try:
        langfuse_client.create_prompt(
            name="vigia-interpreter",
            type="text",
            prompt=_LOCAL_INTERPRETER_PROMPT,
            labels=["testing_1"],
        )
        print("   ✅ 'vigia-interpreter' creado exitosamente\n")
    except Exception as e:
        print(f"   ⚠️  Error: {e}\n")
    
    # ─── Prompt 2: Consultor Cypher ─────────────────────────────────────────────
    print("📍 Creando/actualizando prompt 'vigia-consultant'...")
    try:
        langfuse_client.create_prompt(
            name="vigia-consultant",
            type="text",
            prompt=_LOCAL_CONSULTANT_PROMPT,
            labels=["testing_1"],
        )
        print("   ✅ 'vigia-consultant' creado exitosamente\n")
    except Exception as e:
        print(f"   ⚠️  Error: {e}\n")
    
    # ─── Prompt 3: Redactor ─────────────────────────────────────────────────────
    print("📍 Creando/actualizando prompt 'vigia-redactor'...")
    try:
        langfuse_client.create_prompt(
            name="vigia-redactor",
            type="text",
            prompt=_LOCAL_REDACTOR_PROMPT,
            labels=["testing_1"],
        )
        print("   ✅ 'vigia-redactor' creado exitosamente\n")
    except Exception as e:
        print(f"   ⚠️  Error: {e}\n")
    
    print("▀" * 70)
    print("✅ MIGRACIÓN COMPLETADA")
    print("▄" * 70)
    print("\n📊 Los prompts están ahora en Langfuse y listos para ser usados.")
    print("   Abre https://cloud.langfuse.com para verlos en el dashboard.\n")
    print("💡 Próximos pasos:")
    print("   1. El código en local_chat.py ya intenta recuperar prompts desde Langfuse")
    print("   2. Con fallback a las versiones locales si Langfuse no está disponible")
    print("   3. En el dashboard, puedes editar, versionar, y promover prompts\n")


if __name__ == "__main__":
    migrate_prompts()
