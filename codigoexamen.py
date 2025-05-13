import heapq
import json
import os
from datetime import datetime

TAREAS_FILE = "tareas.json"

class Tarea:
    def __init__(self, nombre, prioridad, fecha_vencimiento, dependencias=None, completada=False):
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        if not isinstance(prioridad, int):
            raise ValueError("La prioridad debe ser un número entero.")
        self.nombre = nombre
        self.prioridad = prioridad
        self.fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%Y-%m-%d")
        self.dependencias = dependencias or []
        self.completada = completada

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "prioridad": self.prioridad,
            "fecha_vencimiento": self.fecha_vencimiento.strftime("%Y-%m-%d"),
            "dependencias": self.dependencias,
            "completada": self.completada
        }

    @staticmethod
    def from_dict(data):
        return Tarea(
            nombre=data["nombre"],
            prioridad=data["prioridad"],
            fecha_vencimiento=data["fecha_vencimiento"],
            dependencias=data["dependencias"],
            completada=data["completada"]
        )


class GestorTareas:
    def __init__(self):
        self.tareas = []
        self.cargar_tareas()

    def guardar_tareas(self):
        with open(TAREAS_FILE, "w") as f:
            json.dump([t.to_dict() for t in self.tareas], f, indent=4)

    def cargar_tareas(self):
        if os.path.exists(TAREAS_FILE):
            with open(TAREAS_FILE, "r") as f:
                data = json.load(f)
                self.tareas = [Tarea.from_dict(t) for t in data]

    def añadir_tarea(self):
        try:
            nombre = input("Nombre de la tarea: ").strip()
            prioridad = int(input("Prioridad (entero, menor número = más importante): "))
            fecha_str = input("Fecha de vencimiento (YYYY-MM-DD): ").strip()
            dependencias = input("Dependencias (nombres separados por comas, o dejar vacío): ").strip()
            deps = [d.strip() for d in dependencias.split(",")] if dependencias else []
            try:
                fecha_vencimiento = datetime.strptime(fecha_str, "%Y-%m-%d")
            except ValueError as e:
                if "month must be in 1..12" in str(e):
                    print("❌ Error: El mes debe estar entre 1 y 12.")
                elif "day is out of range for month" in str(e):
                    print("❌ Error: El día no es válido para el mes especificado.")
                elif "year" in str(e):
                    print("❌ Error: El año debe ser un número válido.")
                else:
                    print("❌ Error: Fecha inválida. Asegúrate de usar el formato YYYY-MM-DD.")
                return
            nueva_tarea = Tarea(nombre, prioridad, fecha_str, deps)
            self.tareas.append(nueva_tarea)
            self.guardar_tareas()
            print("✅ Tarea añadida correctamente.")
        except ValueError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

    def mostrar_pendientes(self):
        if not self.tareas:
            print("No hay tareas registradas.")
            return

        tareas_pendientes = [t for t in self.tareas if not t.completada]
        tareas_pendientes.sort(key=lambda t: t.prioridad)

        if not tareas_pendientes:
            print("No hay tareas pendientes.")
            return

        print("\n--- Tareas Pendientes ---")
        for t in tareas_pendientes:
            print(f"- {t.nombre} | Prioridad: {t.prioridad} | Vence: {t.fecha_vencimiento.date()} | Depende de: {t.dependencias}")
        print("-------------------------")

    def marcar_completada(self):
        nombre = input("Nombre de la tarea a marcar como completada: ").strip().lower()
        for t in self.tareas:
            if t.nombre.lower() == nombre:
                # Permitir completar la tarea si no tiene dependencias o si es ejecutable
                if t.dependencias and not self.es_ejecutable(t):
                    print(f"❌ No se puede completar la tarea '{t.nombre}' porque no se han completado todas sus dependencias: {t.dependencias}")
                    return
                t.completada = True
                self.guardar_tareas()
                print(f"✅ Tarea '{t.nombre}' marcada como completada.")
                return
        print("❌ Tarea no encontrada.")

    def obtener_siguiente(self):
        heap = [
            (t.prioridad, t.fecha_vencimiento, t)
            for t in self.tareas
            if not t.completada and self.es_ejecutable(t)
        ]
        heapq.heapify(heap)
        if heap:
            _, _, tarea = heapq.heappop(heap)
            print(f"👉 Siguiente tarea ejecutable: {tarea.nombre} (Prioridad: {tarea.prioridad}, Vence: {tarea.fecha_vencimiento.date()})")
        else:
            print("⚠️ No hay tareas ejecutables disponibles.")

    def es_ejecutable(self, tarea):
        # Si la tarea no tiene dependencias, es ejecutable
        if not tarea.dependencias:
            return True
        # Verificar que todas las dependencias estén completadas
        return all(
            any(t.nombre == dep and t.completada for t in self.tareas)
            for dep in tarea.dependencias
        )


def mostrar_menu():
    print("""
====== MENÚ DE GESTIÓN DE TAREAS ======
1. Añadir nueva tarea
2. Mostrar tareas pendientes
3. Marcar tarea como completada
4. Ver siguiente tarea ejecutable
5. Salir
======================================
""")


def main():
    gestor = GestorTareas()
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción (1-5): ").strip()
        if opcion == "1":
            gestor.añadir_tarea()
        elif opcion == "2":
            gestor.mostrar_pendientes()
        elif opcion == "3":
            gestor.marcar_completada()
        elif opcion == "4":
            gestor.obtener_siguiente()
        elif opcion == "5":
            print("👋 Saliendo del programa.")
            break
        else:
            print("❌ Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    main()

