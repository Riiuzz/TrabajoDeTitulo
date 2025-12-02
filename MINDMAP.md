# 🧠 Mapa Mental del Proyecto

## Niveles de Profundidad en la Documentación

```
                    ┌─────────────────────────┐
                    │ QUICKSTART.md (5 min)   │
                    │ "Haz que funcione YA"   │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  README.md (15 min)     │
                    │ "¿Qué es este proyecto?"│
                    └────────────┬────────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          │                      │                      │
    ┌─────▼────┐         ┌──────▼──────┐       ┌──────▼──────┐
    │SETUP.md  │         │SUMMARY.md   │       │PROGRESS.md  │
    │ Instalar │         │Visualizar   │       │ Historial   │
    │y ejecutar│         │arquitectura │       │  de avances │
    └──────────┘         └─────────────┘       └─────────────┘
          │
          │
    ┌─────▼──────────────────────┐
    │ Profundizar en código      │
    │ (app.py, scraper_activa.py)│
    └────────────────────────────┘
```

---

## Árbol de Temas

```
├── 📍 ¿DÓNDE EMPEZAR?
│   ├── 👶 Completamente nuevo → QUICKSTART.md
│   ├── 📚 Conocer el proyecto → README.md
│   ├── 🛠️ Instalar y ejecutar → SETUP.md
│   └── 🗺️ Ver todo de un vistazo → SUMMARY.md
│
├── 📖 DOCUMENTACIÓN
│   ├── 🚀 QUICKSTART.md - Inicio en 5 minutos
│   ├── 📖 README.md - Descripción general
│   ├── 🛠️ SETUP.md - Instalación detallada
│   ├── 📊 SUMMARY.md - Visión visual
│   ├── 🗂️ TREE.md - Estructura de carpetas
│   ├── 📋 PROGRESS.md - Historial de avances
│   ├── 📑 INDEX.md - Índice de documentación
│   ├── 🧠 MINDMAP.md - Este archivo
│   └── 💡 QUICKSTART.md - Ideas rápidas
│
├── 💻 CÓDIGO
│   ├── 🐍 Backend (Python)
│   │   ├── app.py - Lógica principal
│   │   └── scraper_activa.py - Web scraping
│   │
│   ├── 🔵 Frontend (JavaScript/React)
│   │   ├── App.js - Componente principal
│   │   └── App.css - Estilos
│   │
│   └── ⚙️ Configuración
│       ├── requirements.txt - Dependencias Python
│       ├── package.json - Dependencias Node
│       ├── .env - Credenciales (NO git)
│       └── .gitignore - Exclusiones
│
├── 📊 BASE DE DATOS
│   ├── Interacciones
│   │   └── Almacena chats del usuario
│   │
│   └── Activa Content
│       └── Almacena contenido scrapeado
│
├── 🔧 TECNOLOGÍAS
│   ├── Backend
│   │   ├── Flask - Web framework
│   │   ├── Gemini - IA/Clasificación
│   │   ├── MongoDB - Base de datos
│   │   ├── BeautifulSoup - Web scraping
│   │   └── Python-dotenv - Config
│   │
│   ├── Frontend
│   │   ├── React - UI framework
│   │   ├── JavaScript ES6 - Lógica
│   │   └── CSS3 - Estilos
│   │
│   └── Externo
│       ├── Google Gemini API
│       ├── MongoDB Atlas
│       └── Activa Research (sitio)
│
├── 📈 AVANCES
│   ├── Avance #1 - Prototipo Base
│   │   ├── Chat conversacional
│   │   ├── Clasificación 5 categorías
│   │   ├── Respuestas con Gemini
│   │   └── MongoDB para persistencia
│   │
│   └── Avance #2 - Web Scraping (1 Dic)
│       ├── Descarga contenido Activa
│       ├── Almacena en MongoDB
│       ├── Bot busca información local
│       ├── Respuestas más precisas
│       └── Fixes: datetime, API keys
│
└── 🚀 PRÓXIMOS PASOS
    ├── Automatizar scraper (APScheduler)
    ├── Búsqueda full-text en MongoDB
    ├── Cachear respuestas de Gemini
    ├── Panel de administración
    ├── Tests unitarios
    └── Desplegar en producción
```

---

## Decisiones de Diseño

```
PROBLEMA: Bot con información genérica
           │
           ├─ Opción 1: Scraping en tiempo real (lento)
           ├─ Opción 2: Gemini con búsqueda web (dependencias)
           │
           └─ ✅ Opción 3: Web Scraping + Índice Local
              │
              ├─ Ventajas:
              │  ├─ Rápido (búsqueda local)
              │  ├─ Confiable (datos reales)
              │  └─ Flexible (fácil actualizar)
              │
              └─ Implementación:
                 ├─ scraper_activa.py descarga HTML
                 ├─ BeautifulSoup extrae contenido
                 ├─ MongoDB almacena en activa_content
                 └─ Bot busca y passa a Gemini
```

---

## Flujo de Datos

```
┌──────────────────────┐
│  Usuario en Chat     │
│ (http://localhost:3  │
│      000)            │
└────────────┬─────────┘
             │
      ┌──────▼──────┐
      │   POST      │
      │ /api/chat   │
      │ {message}   │
      └──────┬──────┘
             │
      ┌──────▼──────────────────┐
      │ Backend Flask (5000)    │
      │ 1. Clasificar mensaje   │
      │ 2. Buscar en MongoDB    │
      │ 3. Enviar a Gemini      │
      │ 4. Guardar en BD        │
      └──────┬──────────────────┘
             │
    ┌────────┼────────┐
    │        │        │
┌───▼──┐  ┌─▼────┐  ┌▼─────────┐
│Gemini│  │Mongo │  │Activa Web│
│API   │  │Atlas │  │(Scraper) │
└──────┘  └──────┘  └──────────┘
    │        │
    └────────┼────────┐
             │        │
      ┌──────▼────────▼────┐
      │ Respuesta del Bot  │
      │ + Categoría        │
      │ + Modo (Gemini)    │
      └──────┬─────────────┘
             │
      ┌──────▼──────────┐
      │ Frontend React  │
      │ (3000)          │
      │ Muestra respuesta
      └─────────────────┘
```

---

## Matriz de Responsabilidades

```
┌──────────────────┬─────────────────────────────────────┐
│ COMPONENTE       │ RESPONSABILIDAD                     │
├──────────────────┼─────────────────────────────────────┤
│ App.py           │ Lógica del bot, clasificación       │
│ Scraper          │ Descargar y procesar web            │
│ Gemini API       │ Clasificar y generar respuestas     │
│ MongoDB          │ Persistencia de datos               │
│ React            │ Interfaz visual                     │
│ .env             │ Credenciales y configuración        │
└──────────────────┴─────────────────────────────────────┘
```

---

## Ciclo de Vida de un Mensaje

```
Paso 1: Usuario escribe "¿Qué es Activa?"
         │
         ▼
Paso 2: Frontend envía POST /api/chat
         │
         ▼
Paso 3: Backend recibe JSON {message: "¿Qué es Activa?"}
         │
         ▼
Paso 4: Llama clasificar_mensaje(mensaje)
         │
         ├─ Usa Gemini para clasificar
         └─ Resultado: categoría = 1 (Sobre Activa)
         │
         ▼
Paso 5: Si categoría == 1:
         │
         └─ Busca en MongoDB colección "activa_content"
            └─ Extrae información sobre "Quiénes Somos"
         │
         ▼
Paso 6: Crea prompt para Gemini:
         "Eres asistente de Activa.
          Información: [datos de MongoDB]
          Pregunta: ¿Qué es Activa?"
         │
         ▼
Paso 7: Gemini genera respuesta
         │
         ▼
Paso 8: Backend guarda en MongoDB:
         {
           usuario_msg: "¿Qué es Activa?",
           categoría: 1,
           respuesta: "[respuesta de Gemini]",
           modo: "gemini",
           timestamp: ahora
         }
         │
         ▼
Paso 9: Retorna JSON al frontend
         │
         ▼
Paso 10: React muestra respuesta en el chat
         │
         ▼
✅ Usuario ve respuesta en tiempo real
```

---

## Dependencias y sus Funciones

```
Backend
├─ Flask (3.0.0) - Crear servidor web
├─ Flask-CORS (4.0.0) - Permitir peticiones desde frontend
├─ python-dotenv (1.2.1) - Leer .env
├─ pymongo (4.15.4) - Conectar a MongoDB
├─ google-generativeai (0.3.0) - Usar API Gemini
├─ requests (2.32.5) - Descargar HTML [NUEVO]
└─ beautifulsoup4 (4.14.3) - Parsear HTML [NUEVO]

Frontend
├─ React (18.x) - Framework UI
├─ React-DOM (18.x) - Renderizar DOM
└─ Fetch API - HTTP client (nativo)

Externo
├─ Google Gemini API - IA
├─ MongoDB Atlas - Base de datos
└─ Activa Research Web - Fuente datos
```

---

## Checklist del Proyecto

### Instalación
- [ ] Python 3.8+ instalado
- [ ] Node.js 14+ instalado
- [ ] Entorno virtual creado (venv)
- [ ] Dependencias Python instaladas
- [ ] Dependencias Node instaladas
- [ ] Archivo .env creado en backend/

### Configuración
- [ ] GEMINI_API_KEY en .env
- [ ] MONGODB_URI en .env
- [ ] MONGODB_DBNAME en .env

### Ejecución
- [ ] Scraper ejecutado (`python scraper_activa.py`)
- [ ] Backend corriendo (puerto 5000)
- [ ] Frontend corriendo (puerto 3000)
- [ ] Bot responde en navegador

### Verificación
- [ ] Mensaje "¿Qué es Activa?" → respuesta real
- [ ] MongoDB contiene datos en ambas colecciones
- [ ] Logs muestran clasificación correcta
- [ ] No hay errores en consola

---

## Preguntas Frecuentes Referencia Rápida

```
P: ¿Por dónde empiezo?
R: QUICKSTART.md (5 minutos)

P: ¿Cómo instalo todo?
R: SETUP.md (paso a paso)

P: ¿Qué se ha hecho?
R: PROGRESS.md (historial completo)

P: ¿Cómo funciona el bot?
R: SUMMARY.md (diagrama visual)

P: ¿Dónde está cada archivo?
R: TREE.md (estructura del proyecto)

P: ¿Cómo sigue de aquí?
R: Ver "Próximos Pasos" en PROGRESS.md
```

---

**Última actualización:** 1 de Diciembre, 2025  
**Versión:** 2.0 con Web Scraping
