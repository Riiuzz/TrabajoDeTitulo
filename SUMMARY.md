# 📊 Resumen Visual del Proyecto

## Estado Actual del Desarrollo

```
┌─────────────────────────────────────────────────────────┐
│  ACTIVE RESEARCH BOT - TRABAJO DE TÍTULO                │
│  Estado: EN DESARROLLO ✅                               │
│  Última Actualización: 1 de Diciembre, 2025             │
└─────────────────────────────────────────────────────────┘
```

---

## Avances Completados

### ✅ Avance #1 – Prototipo Base (Anterior)
- Chat conversacional con interfaz React
- Clasificación de intenciones con Gemini (5 categorías)
- Backend Flask con endpoint `/api/chat`
- MongoDB para almacenar interacciones
- Sistema de fallback

**Archivos:** `app.py`, `App.js`, `App.css`  
**Tecnologías:** Flask, React, Google Gemini, MongoDB

---

### ✅ Avance #2 – Web Scraping e Índice Local (1 Dic 2025)
- Web scraper automático (`scraper_activa.py`)
- Descarga contenido de 3 secciones de Activa Research
- Almacena en colección `activa_content` en MongoDB
- Bot busca información local y la pasa a Gemini
- Respuestas más precisas y basadas en datos reales

**Archivos Nuevos:** `scraper_activa.py`, `backend/.gitignore`  
**Archivos Modificados:** `app.py`  
**Tecnologías Añadidas:** BeautifulSoup4, requests

---

## Arquitectura Actual

```
┌─────────────────────┐
│   USUARIO (Web)     │
│  localhost:3000     │
└──────────┬──────────┘
           │
      [FRONTEND]
           │
       React.js
           │
    Fetch API / CORS
           │
┌──────────▼──────────┐
│  BACKEND (Flask)    │
│  localhost:5000     │
│  /api/chat endpoint │
└──────┬──────────┬───┘
       │          │
    [GEMINI]  [MONGODB]
       │          │
    Classify   ┌─ interacciones
    Generate   └─ activa_content
    Response      (scraper)
```

---

## Flujo de una Pregunta

```
1️⃣  Usuario escribe en chat
     ↓
2️⃣  Frontend envía: POST /api/chat {message: "¿Qué es Activa?"}
     ↓
3️⃣  Backend recibe mensaje
     ↓
4️⃣  Gemini clasifica intención → Categoría 1
     ↓
5️⃣  Si categoría 1 o 4:
     └─→ Busca en MongoDB colección activa_content
     └─→ Obtiene información real (estudios, descripción)
     ↓
6️⃣  Envía a Gemini con contexto:
     "Eres un asistente de Activa Research.
      Información actual: [datos de MongoDB]
      Responde: ¿Qué es Activa?"
     ↓
7️⃣  Gemini genera respuesta en lenguaje natural
     ↓
8️⃣  Backend retorna respuesta al frontend
     ↓
9️⃣  Frontend muestra respuesta en chat
     ↓
🔟 Backend guarda en MongoDB:
     {usuario, categoría, respuesta, modo, timestamp}
```

---

## Base de Datos – Estructura

### Colección: `interacciones`
```json
{
  "_id": ObjectId(...),
  "mensaje_usuario": "¿Qué es Active Research?",
  "categoria": 1,
  "respuesta_bot": "Active Research es una empresa chilena...",
  "modo": "gemini",
  "timestamp": ISODate("2025-12-01T20:07:23.456Z")
}
```

### Colección: `activa_content` (nueva)
```json
{
  "_id": ObjectId(...),
  "seccion": "pulso_ciudadano",
  "contenido": {
    "type": "pulso_ciudadano",
    "titulo": "Pulso Ciudadano",
    "descripcion": "Tracking quincenal de opinión pública...",
    ...
  },
  "fecha_actualizacion": ISODate("2025-12-01T20:07:23.456Z")
}
```

---

## Dependencias del Proyecto

### Backend (Python)
```
✅ Flask 3.0.0                  – Web framework
✅ Flask-CORS 4.0.0            – CORS handling
✅ python-dotenv 1.2.1         – Environment variables
✅ pymongo 4.15.4              – MongoDB client
✅ google-generativeai 0.3.0   – Gemini API
✅ requests 2.32.5             – HTTP library (NEW)
✅ beautifulsoup4 4.14.3       – Web scraping (NEW)
```

### Frontend (JavaScript)
```
✅ React 18.x                  – UI framework
✅ React DOM 18.x              – React rendering
✅ Fetch API                   – Built-in, sin instalación
```

---

## URLs Principales

| Recurso | URL | Descripción |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Chat widget |
| **Backend API** | http://localhost:5000 | REST API |
| **Chat Endpoint** | POST http://localhost:5000/api/chat | Procesa mensajes |
| **Activa Web (Scraping)** | https://chile.activasite.com | Fuente de datos |

---

## Estadísticas del Código

| Métrica | Valor |
|---------|-------|
| Archivos Python | 2 (app.py, scraper_activa.py) |
| Líneas de código backend | ~625 |
| Archivos JavaScript/React | ~5+ |
| Líneas de código frontend | ~200+ |
| Colecciones MongoDB | 2 |
| Endpoints REST | 1 (/api/chat) |
| Categorías de clasificación | 5 |
| URLs scrapeadas | 3 |

---

## Categorías de Clasificación del Bot

```
1️⃣  Preguntas sobre ACTIVE RESEARCH
    • Qué es, a qué se dedica, servicios, clientes
    → Busca en: activa_content[quienes_somos]

2️⃣  Preguntas sobre INVESTIGACIÓN
    • Técnicas, encuestas, metodologías (CATI, CAWI)
    → Respuesta: Contexto predefinido + Gemini

3️⃣  Cotización de PROYECTOS
    • "Quiero cotizar un estudio"
    → Respuesta: Explicación general + contacto

4️⃣  PULSO CIUDADANO
    • Encuestas de opinión, resultados electorales
    → Busca en: activa_content[pulso_ciudadano, estudios]

5️⃣  NO APLICA
    • Preguntas fuera del contexto
    → Respuesta: "No puedo ayudarte con eso"
```

---

## Próximos Pasos Sugeridos

### Corto Plazo (1-2 semanas)
- [ ] Ejecutar scraper regularmente (semanal)
- [ ] Mejorar parsing de HTML del scraper
- [ ] Agregar más secciones (servicios, clientes, etc.)
- [ ] Testing manual del bot

### Mediano Plazo (1-2 meses)
- [ ] Automatizar scraper con APScheduler
- [ ] Implementar búsqueda full-text en MongoDB
- [ ] Cachear respuestas de Gemini
- [ ] Crear panel de administración

### Largo Plazo (3+ meses)
- [ ] Desplegar en producción (cloud)
- [ ] Integrar con CRM de Active Research
- [ ] Análisis de interacciones
- [ ] Mejoras de UX basadas en feedback

---

## Documentación de Referencia

- **PROGRESS.md** – Historial detallado de avances
- **README.md** – Descripción general del proyecto
- **SETUP.md** – Guía de instalación y ejecución
- **app.py** – Código fuente principal del backend
- **scraper_activa.py** – Código del web scraper

---

## Contacto y Soporte

Para preguntas sobre el desarrollo, contactar al autor del trabajo de título.

---

**Estado:** ✅ Funcional y en desarrollo activo  
**Última actualización:** 1 de Diciembre, 2025
