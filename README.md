# 🗂️ Gestor de Tareas con Prioridades y Dependencias

Este proyecto en Python permite gestionar tareas pendientes con control de prioridades, fechas de vencimiento y dependencias entre tareas. Las tareas se guardan en un archivo JSON para mantener la persistencia entre ejecuciones.

---

## 📋 Características

- 📌 Añadir tareas con:
  - Nombre
  - Prioridad (entero, menor número = mayor prioridad)
  - Fecha de vencimiento (`YYYY-MM-DD`)
  - Dependencias (otras tareas que deben completarse primero)

- 📄 Mostrar todas las tareas pendientes ordenadas por prioridad

- ✅ Marcar tareas como completadas (solo si sus dependencias están resueltas)

- ⏩ Obtener la siguiente tarea ejecutable (por prioridad y dependencias)

- 💾 Persistencia automática en el archivo `tareas.json`

- 🛑 Validación de entrada:
  - Nombre no vacío
  - Prioridad debe ser entero
  - Fecha válida en formato `YYYY-MM-DD`
  - Verificación de días y meses válidos

---

## 🖥️ Requisitos

- Python 3.7 o superior

---

## 🚀 Cómo usar

1. Clona o descarga este repositorio.

2. Ejecuta el script:

python gestor_tareas.py
====== MENÚ DE GESTIÓN DE TAREAS ======
1. Añadir nueva tarea
2. Mostrar tareas pendientes
3. Marcar tarea como completada
4. Ver siguiente tarea ejecutable
5. Salir
