# 🗂️ Estructura Completa del Proyecto

```
TrabajoDeTitulo/
│
├── 📄 README.md                  (Descripción general del proyecto)
├── 📋 PROGRESS.md               (Historial detallado de avances #1 y #2)
├── 🚀 SETUP.md                  (Guía de instalación paso a paso)
├── 📊 SUMMARY.md                (Resumen visual y estadísticas)
├── 📑 INDEX.md                  (Índice y guía de navegación)
├── 📚 TREE.md                   (Este archivo - estructura del proyecto)
└── .gitignore                   (Exclusiones de git)

│
├── backend/                     (Servidor Flask + Gemini)
│   │
│   ├── 🐍 app.py               (Servidor Flask principal ~625 líneas)
│   │   ├── Clasificación de intención con Gemini
│   │   ├── Generación de respuestas
│   │   ├── Búsqueda en MongoDB (NUEVO - Avance #2)
│   │   ├── Endpoint POST /api/chat
│   │   └── Registro de interacciones
│   │
│   ├── 🕷️ scraper_activa.py    (Web scraper ~240 líneas) [NUEVO - Avance #2]
│   │   ├── Descarga HTML de 3 URLs
│   │   ├── Extrae contenido con BeautifulSoup
│   │   ├── Guarda en MongoDB colección "activa_content"
│   │   └── Función main() para ejecutar
│   │
│   ├── 📦 requirements.txt       (Dependencias Python)
│   │   ├── Flask==3.0.0
│   │   ├── Flask-CORS==4.0.0
│   │   ├── pymongo==4.15.4
│   │   ├── google-generativeai==0.3.0
│   │   ├── python-dotenv==1.2.1
│   │   ├── requests==2.32.5 [NUEVO]
│   │   └── beautifulsoup4==4.14.3 [NUEVO]
│   │
│   ├── .env                     (Variables de entorno - NO SUBIR A GIT)
│   │   ├── GEMINI_API_KEY=...
│   │   ├── MONGODB_URI=...
│   │   └── MONGODB_DBNAME=trabajo_titulo
│   │
│   ├── .gitignore              (Protección de archivos sensibles) [MEJORADO]
│   │   ├── .env y variantes
│   │   ├── venv/ y __pycache__/
│   │   ├── .vscode/ e .idea/
│   │   └── *.log
│   │
│   ├── venv/                    (Entorno virtual Python - NO SUBIR)
│   │   └── Scripts/, Lib/, etc.
│   │
│   └── __pycache__/             (Caché Python - NO SUBIR)
│
│
├── frontend/                    (Interfaz React)
│   │
│   ├── 📁 src/                  (Código fuente)
│   │   │
│   │   ├── 🔵 App.js            (Componente principal React)
│   │   │   ├── Estado del chat
│   │   │   ├── Envío de mensajes a /api/chat
│   │   │   ├── Renderizado de mensajes
│   │   │   └── Widget flotante
│   │   │
│   │   ├── 🎨 App.css           (Estilos principales)
│   │   │   ├── Layout del chat
│   │   │   ├── Animaciones
│   │   │   └── Responsive design
│   │   │
│   │   ├── 📱 index.js          (Punto de entrada)
│   │   │   ├── ReactDOM.render
│   │   │   └── App.js
│   │   │
│   │   ├── 📄 index.css         (Estilos globales)
│   │   │
│   │   ├── components/          (Componentes reutilizables)
│   │   │   └── [Según implementación]
│   │   │
│   │   └── assets/              (Imágenes, iconos, etc.)
│   │       └── [Archivos estáticos]
│   │
│   ├── 📁 public/               (Archivos públicos)
│   │   ├── 📄 index.html        (HTML base)
│   │   ├── favicon.ico
│   │   ├── manifest.json
│   │   └── robots.txt
│   │
│   ├── 📦 package.json          (Dependencias Node)
│   │   ├── react
│   │   ├── react-dom
│   │   └── scripts de desarrollo
│   │
│   ├── 📝 README.md             (README específico del frontend)
│   │
│   ├── node_modules/            (Paquetes npm - NO SUBIR)
│   │   └── [Cientos de dependencias]
│   │
│   └── .gitignore               (Exclusiones del frontend)
│       ├── node_modules/
│       ├── build/
│       └── .env
│
│
└── 📊 MongoDB Atlas (Nube)
    │
    └── trabajo_titulo/          (Base de datos)
        │
        ├── interacciones        (Colección - Avance #1)
        │   └── Documentos: {usuario, categoría, respuesta, modo, timestamp}
        │
        └── activa_content       (Colección - NUEVA en Avance #2)
            └── Documentos: {seccion, contenido, fecha_actualizacion}
```

---

## 📋 Archivos Clave por Función

### Configuración y Setup
- `backend/requirements.txt` – Instala dependencias Python
- `backend/.env` – Credenciales (crear manualmente)
- `frontend/package.json` – Instala dependencias Node
- `.gitignore` – Protege archivos sensibles

### Documentación
- `README.md` – Visión general del proyecto
- `PROGRESS.md` – Historial de avances #1 y #2
- `SETUP.md` – Cómo instalar y ejecutar
- `SUMMARY.md` – Resumen visual y estadísticas
- `INDEX.md` – Guía de navegación de documentación
- `TREE.md` – Este archivo (estructura del proyecto)

### Backend (Python/Flask)
- `backend/app.py` – Servidor principal con:
  - Clasificación de intenciones
  - Generación de respuestas
  - Búsqueda en MongoDB (nuevo)
  - Endpoint /api/chat
  
- `backend/scraper_activa.py` – Web scraper con:
  - Descarga de HTML
  - Parsing con BeautifulSoup
  - Guardado en MongoDB

### Frontend (React)
- `frontend/src/App.js` – Lógica del chat
- `frontend/src/App.css` – Estilos
- `frontend/public/index.html` – HTML base

### Base de Datos (MongoDB)
- Colección `interacciones` – Historial de chats
- Colección `activa_content` – Contenido scrapeado

---

## 🔄 Flujo de Dependencias

```
npm install (frontend/)
    ↓
├─ react
├─ react-dom
└─ scripts de dev

pip install -r requirements.txt (backend/)
    ↓
├─ Flask
├─ Flask-CORS
├─ pymongo
├─ google-generativeai
├─ python-dotenv
├─ requests (nuevo)
└─ beautifulsoup4 (nuevo)

npm start (frontend/)
    ↓
React en http://localhost:3000

python app.py (backend/)
    ↓
Flask en http://localhost:5000

python scraper_activa.py (backend/)
    ↓
Actualiza MongoDB
```

---

## 📊 Tamaños de Archivos

| Archivo | Tamaño | Líneas |
|---------|--------|--------|
| app.py | ~25 KB | ~625 |
| scraper_activa.py | ~8 KB | ~240 |
| App.js | ~? | ~200+ |
| PROGRESS.md | 10 KB | ~500 |
| SETUP.md | 5 KB | ~250 |
| SUMMARY.md | 7 KB | ~350 |
| INDEX.md | 5 KB | ~300 |
| requirements.txt | 200 B | 7 líneas |

---

## 🎯 Qué Modificar Según tu Necesidad

### Para cambiar las URLs a scrapear:
→ Edita `backend/scraper_activa.py` línea ~26:
```python
URLS_TO_SCRAPE = {
    "nombre": "https://nueva-url.com/"
}
```

### Para cambiar el prompt del bot:
→ Edita `backend/app.py` función `generar_respuesta_gemini()` 

### Para cambiar estilos:
→ Edita `frontend/src/App.css`

### Para cambiar lógica del chat:
→ Edita `frontend/src/App.js`

### Para cambiar categorías:
→ Edita `backend/app.py` función `clasificar_mensaje_gemini()`

---

## 🔐 Archivos NO SUBIR A GIT

Estos archivos están protegidos en `.gitignore`:

```
backend/.env
backend/venv/
backend/__pycache__/
backend/*.log
frontend/node_modules/
frontend/build/
.DS_Store
*.swp
.vscode/
.idea/
```

---

## ✅ Checklist de Carpetas

Verifica que tengas estas carpetas:

- [ ] `backend/` con app.py y scraper_activa.py
- [ ] `backend/venv/` creado (después de activar entorno virtual)
- [ ] `frontend/src/` con App.js, App.css
- [ ] `frontend/public/` con index.html
- [ ] Archivo `.env` en `backend/` (creado manualmente)

---

## 📝 Próximos Archivos a Crear

Según los "Próximos Pasos" en PROGRESS.md:

- `backend/scheduler.py` – Automatizar scraper (APScheduler)
- `backend/tests/` – Tests unitarios
- `admin/dashboard.html` – Panel de administración
- `docker-compose.yml` – Para despliegue
- `requirements-dev.txt` – Dependencias de desarrollo

---

**Última actualización:** 1 de Diciembre, 2025  
**Versión:** 2.0
