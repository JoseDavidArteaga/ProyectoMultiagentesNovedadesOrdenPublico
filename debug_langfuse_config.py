#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Debug: Verifica qué credenciales se están cargando."""

import os
from dotenv import load_dotenv

print("=" * 60)
print("🔍 DEBUG: Verificando variables de entorno de Langfuse")
print("=" * 60)

# Cargar .env si existe
load_dotenv()

# Variables de entorno directas
LANGFUSE_ENABLED = os.environ.get("LANGFUSE_ENABLED", "").strip()
LANGFUSE_PUBLIC_KEY = os.environ.get("LANGFUSE_PUBLIC_KEY", "").strip()
LANGFUSE_SECRET_KEY = os.environ.get("LANGFUSE_SECRET_KEY", "").strip()
LANGFUSE_HOST = os.environ.get("LANGFUSE_HOST", "").strip()

print(f"\n✅ LANGFUSE_ENABLED: {LANGFUSE_ENABLED if LANGFUSE_ENABLED else '❌ VACÍO'}")
print(f"✅ LANGFUSE_HOST: {LANGFUSE_HOST if LANGFUSE_HOST else '(usando default)'}")

# Mostrar prefijo y sufijo de credenciales (sin revelar la clave completa)
if LANGFUSE_PUBLIC_KEY:
    prefix = LANGFUSE_PUBLIC_KEY[:10]
    suffix = LANGFUSE_PUBLIC_KEY[-6:]
    print(f"✅ LANGFUSE_PUBLIC_KEY: {prefix}...{suffix} ({len(LANGFUSE_PUBLIC_KEY)} chars)")
else:
    print(f"❌ LANGFUSE_PUBLIC_KEY: VACÍO")

if LANGFUSE_SECRET_KEY:
    prefix = LANGFUSE_SECRET_KEY[:10]
    suffix = LANGFUSE_SECRET_KEY[-6:]
    print(f"✅ LANGFUSE_SECRET_KEY: {prefix}...{suffix} ({len(LANGFUSE_SECRET_KEY)} chars)")
else:
    print(f"❌ LANGFUSE_SECRET_KEY: VACÍO")

print("\n" + "=" * 60)
print("📋 Desde config.py:")
print("=" * 60)

from config import LANGFUSE_ENABLED as cfg_enabled, LANGFUSE_PUBLIC_KEY as cfg_pk, LANGFUSE_SECRET_KEY as cfg_sk, LANGFUSE_HOST as cfg_host

print(f"LANGFUSE_ENABLED: {cfg_enabled}")
print(f"LANGFUSE_HOST: {cfg_host}")
print(f"LANGFUSE_PUBLIC_KEY: {len(cfg_pk)} chars - {('❌ VACÍO' if not cfg_pk else ('✅ Configurado'))}")
print(f"LANGFUSE_SECRET_KEY: {len(cfg_sk)} chars - {('❌ VACÍO' if not cfg_sk else ('✅ Configurado'))}")

print("\n" + "=" * 60)
if not cfg_pk or not cfg_sk:
    print("❌ PROBLEMA DETECTADO: Las credenciales están vacías.")
    print("\n📝 Solución:")
    print("   En PowerShell, ejecuta:")
    print("   $env:LANGFUSE_ENABLED=\"true\"")
    print("   $env:LANGFUSE_PUBLIC_KEY=\"pk-lf-<tu-clave>\"")
    print("   $env:LANGFUSE_SECRET_KEY=\"sk-lf-<tu-secreto>\"")
    print("   $env:LANGFUSE_HOST=\"https://us.cloud.langfuse.com\"")
    print("\n   Luego verifica nuevamente con:")
    print("   python debug_langfuse_config.py")
else:
    print("✅ Credenciales detectadas. Intenta ejecutar:")
    print("   python migrate_prompts_to_langfuse.py")
print("=" * 60)
