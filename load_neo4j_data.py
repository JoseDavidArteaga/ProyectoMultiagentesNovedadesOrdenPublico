"""
Script para cargar los archivos .cypher en Neo4j
Carga el esquema base y luego los datos de eventos
"""

from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE
import sys
from pathlib import Path

# Rutas de los archivos cypher
SCHEMA_FILE = Path("data/raw/vigia_cauca_neo4j.cypher")
DATA_FILE = Path("data/raw/load_data.cypher")


def cargar_archivo_cypher(driver, archivo_path: Path, nombre_archivo: str):
    """
    Lee y ejecuta un archivo .cypher en Neo4j
    
    Args:
        driver: Driver de Neo4j
        archivo_path: Ruta al archivo .cypher
        nombre_archivo: Nombre descriptivo para logs
    """
    if not archivo_path.exists():
        print(f"❌ ERROR: Archivo no encontrado: {archivo_path}")
        return False
    
    try:
        # Leer archivo
        with open(archivo_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        print(f"\n📂 Cargando {nombre_archivo}...")
        print(f"   Tamaño: {len(contenido)} caracteres")
        
        # Dividir por separadores de sentencias (///), ignorando comentarios
        import re
        
        # Reemplazar comentarios en líneas completas (no comentarios inline)
        lineas = contenido.split('\n')
        lineas_limpias = [l for l in lineas if not l.strip().startswith('//')]
        contenido_limpio = '\n'.join(lineas_limpias)
        
        # Dividir por ///, luego por punto y coma
        bloques = [s.strip() for s in contenido_limpio.split('///') if s.strip()]
        
        sentencias = []
        for bloque in bloques:
            # Dividir cada bloque por punto y coma
            sents = [s.strip() for s in bloque.split(';') if s.strip()]
            sentencias.extend(sents)
        
        print(f"   Sentencias encontradas: {len(sentencias)}")
        
        # Ejecutar cada sentencia
        exitosas = 0
        fallidas = 0
        
        with driver.session(database=NEO4J_DATABASE) as session:
            for i, sentencia in enumerate(sentencias, 1):
                if not sentencia:
                    continue
                
                try:
                    # Ejecutar transacción
                    session.run(sentencia)
                    exitosas += 1
                    
                    if i % 20 == 0:
                        print(f"   ✓ {i}/{len(sentencias)} sentencias procesadas...")
                
                except Exception as e:
                    fallidas += 1
                    if fallidas <= 3:  # Mostrar primeros 3 errores
                        error_msg = str(e)[:150]
                        print(f"   ⚠️  Sentencia {i} falló: {error_msg}")
        
        print(f"\n✅ {nombre_archivo} cargado exitosamente")
        print(f"   Sentencias exitosas: {exitosas}")
        if fallidas > 0:
            print(f"   Sentencias con error: {fallidas}")
        
        return True
    
    except Exception as e:
        print(f"❌ ERROR cargando {nombre_archivo}: {str(e)}")
        return False


def main():
    """Función principal"""
    
    print("=" * 70)
    print("🔌 CARGADOR DE DATOS NEO4J - VIGÍA CAUCA")
    print("=" * 70)
    print(f"🌐 Conectando a Neo4j: {NEO4J_URI}")
    
    try:
        # Conectar a Neo4j
        driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
        )
        
        # Verificar conexión
        with driver.session(database=NEO4J_DATABASE) as session:
            info = session.run("RETURN 1 as result").single()
        
        print(f"✅ Conexión establecida correctamente\n")
        
        # Cargar esquema primero
        schema_ok = cargar_archivo_cypher(
            driver,
            SCHEMA_FILE,
            "Esquema base (vigia_cauca_neo4j.cypher)"
        )
        
        if not schema_ok:
            print("\n⚠️  ADVERTENCIA: El esquema tiene errores, pero continuando con datos...")
        
        # Cargar datos
        data_ok = cargar_archivo_cypher(
            driver,
            DATA_FILE,
            "Datos de eventos (load_data.cypher)"
        )
        
        # Resumen
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE CARGA")
        print("=" * 70)
        
        with driver.session(database=NEO4J_DATABASE) as session:
            # Contar nodos
            nodes = session.run(
                "MATCH (n) RETURN count(n) as total"
            ).single()["total"]
            
            # Contar relaciones
            rels = session.run(
                "MATCH ()-[r]->() RETURN count(r) as total"
            ).single()["total"]
            
            # Contar por tipo
            result = session.run("""
                MATCH (n)
                RETURN labels(n)[0] as label, count(*) as cantidad
                ORDER BY cantidad DESC
            """)
            tipos = list(result)
            
            print(f"\nNodos totales: {nodes:,}")
            print(f"Relaciones totales: {rels:,}\n")
            print("Desglose por tipo de nodo:")
            for record in tipos:
                print(f"  • {record['label']}: {record['cantidad']:,}")
        
        print("\n✅ CARGA COMPLETADA")
        
        driver.close()
        return 0
    
    except Exception as e:
        print(f"\n❌ ERROR FATAL: {str(e)}")
        print(f"\nVerifica que:")
        print(f"  • Neo4j está corriendo en {NEO4J_URI}")
        print(f"  • Las credenciales son correctas")
        print(f"  • Los archivos .cypher existen en data/raw/")
        return 1


if __name__ == "__main__":
    sys.exit(main())
