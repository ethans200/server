## Sistema de Gestión de Restaurante - "Restauración 4.0"

Este es un proyecto integral desarrollado para la asignatura de **Lenguaje de Programación 2** en la **Universidad Agraria del Ecuador**. El sistema está diseñado para optimizar la gestión operativa de un restaurante, abarcando desde la toma de pedidos por los meseros hasta el monitoreo en tiempo real en la cocina.

## Características Principales

- **Gestión Multi-rol:** Acceso diferenciado para Administradores, Meseros y Cocineros.
- **Terminal Punto de Venta (POS):** Catálogo visual con selección de productos por categorías.
- **Monitor de Cocina Inteligente:** Gestión de flujo de órdenes mediante una estructura de cola dinámica.
- **Control de Mesas:** Visualización del estado de las mesas (Disponible/Ocupada) en tiempo real.
- **Administración de Inventario:** CRUD de productos con actualización de precios dinámica.

## Tecnologías Utilizadas

- **Lenguaje:** Python 3.13
- **Interfaz Gráfica (GUI):** Tkinter (Librería estándar de Python)
- **Base de Datos:** SQLite3 (Persistencia local)
- **Arquitectura:** Modelo-Vista-Controlador (MVC)

## Implementaciones de Algoritmos y Estructuras de Datos

El núcleo del sistema ha sido desarrollado sin depender exclusivamente de funciones nativas de alto nivel, con el fin de demostrar lógica de programación pura:

1. **Estructura de Datos Manual:** Implementación de una **Cola (Queue)** basada en **Nodos** dinámicos para la gestión de pedidos en cocina (Lógica FIFO).
2. **Algoritmo de Ordenamiento:** Uso de **Bubble Sort (Burbuja)** en la capa del controlador para organizar el catálogo de productos por ID de forma ascendente.
3. **Manejo de Memoria:** Uso de diccionarios (Hash Maps) para el carrito de compras volátil antes de la persistencia en base de datos.

## Estructura del Proyecto

```text
SistemaRestaurante/
├── base_datos/      # Gestión de conexión y creación de tablas SQLite.
├── controlador/     # Lógica de negocio y algoritmos (Bubble Sort, Controladores).
├── estructuras/     # Implementación manual de Nodos y Colas.
├── modelo/          # Definición de clases (Usuario, Producto, Pedido, Mesa).
├── vistas/          # Todas las interfaces gráficas y layouts (Tkinter).
├── main.py          # Punto de entrada de la aplicación.
└── README.md        # Documentación del proyecto.
