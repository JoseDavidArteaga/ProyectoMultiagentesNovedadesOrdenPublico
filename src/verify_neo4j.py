"""
Verificador de integridad de datos en Neo4j - Vigía Cauca
"""

from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE

def verificar_datos():
    """Verificar integridad de los datos cargados"""
    
    print("=" * 70)
    print("🔍 VERIFICADOR DE INTEGRIDAD - VIGÍA CAUCA")
    print("=" * 70)
    
    try:
        driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
        )
        
        with driver.session(database=NEO4J_DATABASE) as session:
            
            # 1. Contar eventos
            eventos = session.run(
                "MATCH (h:HECHO) RETURN count(h) as total"
            ).single()["total"]
            print(f"\n📊 Eventos cargados: {eventos}")
            
            # 2. Eventos por mes
            print(f"\n📅 Distribución por mes:")
            result = session.run("""
                MATCH (h:HECHO)-[:EN_MES]->(m:MES)
                RETURN m.numero as mes, count(h) as cantidad
                ORDER BY m.numero
            """)
            for record in result:
                mes = int(record['mes'])
                cantidad = record['cantidad']
                meses_dict = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo'}
                print(f"  • {meses_dict.get(mes, 'Mes ' + str(mes))}: {cantidad} eventos")
            
            # 3. Eventos por categoría
            print(f"\n🏷️  Eventos por categoría:")
            result = session.run("""
                MATCH (h:HECHO)-[:ES_DE]->(c:Categoria)
                RETURN c.nombre as categoria, count(h) as cantidad
                ORDER BY cantidad DESC
            """)
            for record in result:
                print(f"  • {record['categoria']}: {record['cantidad']}")
            
            # 4. Municipios con más eventos
            print(f"\n🗺️  Top 10 municipios con más eventos:")
            result = session.run("""
                MATCH (h:HECHO)-[:OCURRE_EN]->(cp:CentroPoblado)-[:PERTENECE_A]->(m:Municipio)
                RETURN m.nombre as municipio, count(h) as cantidad
                ORDER BY cantidad DESC
                LIMIT 10
            """)
            for record in result:
                print(f"  • {record['municipio']}: {record['cantidad']}")
            
            # 5. Afectaciones
            print(f"\n💔 Estadísticas de afectaciones:")
            result = session.run("""
                MATCH (h:HECHO)-[r:GENERA]->(a:Afectacion)
                RETURN a.nombre as tipo, sum(r.cantidad) as total
                ORDER BY total DESC
            """)
            for record in result:
                tipo = record['tipo']
                total = record['total'] if record['total'] is not None else 0
                print(f"  • {tipo}: {total}")
            
            # 6. Verificar consistencia
            print(f"\n✅ Verificaciones:")
            
            # Eventos sin categoría
            sin_cat = session.run(
                "MATCH (h:HECHO) WHERE NOT (h)-[:ES_DE]->() RETURN count(h) as total"
            ).single()["total"]
            print(f"  • Eventos sin categoría: {sin_cat}")
            
            # Eventos sin ubicación
            sin_ubicación = session.run(
                "MATCH (h:HECHO) WHERE NOT (h)-[:OCURRE_EN]->() RETURN count(h) as total"
            ).single()["total"]
            print(f"  • Eventos sin ubicación: {sin_ubicación}")
            
            # Eventos sin mes
            sin_mes = session.run(
                "MATCH (h:HECHO) WHERE NOT (h)-[:EN_MES]->() RETURN count(h) as total"
            ).single()["total"]
            print(f"  • Eventos sin mes: {sin_mes}")
            
            # Eventos sin año
            sin_año = session.run(
                "MATCH (h:HECHO) WHERE NOT (h)-[:EN_AÑO]->() RETURN count(h) as total"
            ).single()["total"]
            print(f"  • Eventos sin año: {sin_año}")
            
            print("\n" + "=" * 70)
            print("✅ Verificación completada")
            print("=" * 70)
        
        driver.close()
    
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")


if __name__ == "__main__":
    verificar_datos()
