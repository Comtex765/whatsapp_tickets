# 🎟️ WHATSAPP_TICKETS

**WHATSAPP_TICKETS** es un sistema de atención automatizado por WhatsApp, diseñado para gestionar el flujo completo de reserva y pago de tickets. Está construido con **FastAPI**, utilizando una arquitectura modular y lógica conversacional basada en **fases** y **estados**, integrando la **WhatsApp Cloud API**.

---

## 🚀 ¿Qué hace este sistema?

- Registra usuarios nuevos desde WhatsApp de manera automatizada.
- Gestiona reservas de tickets en un flujo conversacional.
- Permite realizar pagos desde la misma conversación.
- Controla sesiones activas por número de WhatsApp.
- Reinicia automáticamente la sesión si el usuario está inactivo durante un tiempo definido.

---

## 🧠 ¿Cómo funciona?

El sistema está diseñado con una **arquitectura por fases y estados**, simulando un chatbot estructurado:

- **Fases**: Representan el flujo actual del usuario, como `registro`, `reserva`, `pago`, etc.
- **Estados**: Son los pasos específicos dentro de una fase, como `esperando_cédula`, `confirmando_pago`, etc.

Cada mensaje del usuario se procesa según la fase y estado actual, lo que permite guiarlo paso a paso.

---

## 🗂️ Estructura del Proyecto

```
WHATSAPP_TICKETS/
├── app/
│   ├── core/                         # Lógica principal del negocio
│   │   ├── factory/                  # Fábrica para instanciar el handler correcto según la fase
│   │   │   └── handler_factory.py
│   │   ├── handlers/                # Lógica para manejar cada fase (inicio, registro, reserva, pago)
│   │   │   ├── inicio_handler.py
│   │   │   ├── pago_handler.py
│   │   │   ├── registro_handler.py
│   │   │   └── reserva_handler.py
│   │   └── states/                 # Subestados para cada fase, ayuda a guiar las interacciones
│   │       ├── inicio.py
│   │       ├── pago.py
│   │       ├── registro.py
│   │       ├── reserva.py
│   │       └── inactividad.py     # Lógica para manejar sesiones inactivas
│   │
│   ├── routes/                     # Endpoints de la API (rutas FastAPI)
│   │   ├── __init__.py
│   │   ├── transferencia.py       # Endpoint para pruebas de transferencias
│   │   └── webhook.py             # Webhook que recibe mensajes desde WhatsApp
│   │
│   ├── utils/                      # Utilidades y funciones de apoyo
│   │   ├── constantes/            # Constantes como estados, IDs y mensajes
│   │   │   ├── estados.py
│   │   │   ├── id_interactivos.py
│   │   │   └── mensajes.py
│   │   └── whatsapp/              # Lógica de envío y recepción de mensajes WhatsApp
│   │       ├── responses.py
│   │       ├── sender.py
│   │       ├── requests.py
│   │       ├── session.py         # Gestión de sesiones de usuario
│   │       └── validaciones.py    # Validaciones de datos ingresados
│   │
│   ├── config.py                   # Configuraciones generales del sistema
│   ├── database.py                 # Conexión a base de datos (si aplica)
│   ├── main.py                     # Punto de entrada de la aplicación
│   └── models.py                   # Modelos de datos (si se usa ORM o esquemas)
│
├── images/                         # Recursos gráficos o diagramas (opcional)
└── venv/                           # Entorno virtual de Python
```


## 👨‍💻 Autor

**Desarrollado por:**  Fernando Novillo

Estudiante de Ingeniería en Software – Escuela Superior Politécnica de Chimborazo.  

---

## 📬 Contacto

- 📧 Email: ferchon123443@gmail.com  
- 💻 GitHub: [Comtex765](https://github.com/Comtex765)
