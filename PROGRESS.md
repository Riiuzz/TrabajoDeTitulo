# 📋 Registro de Avances – Active Research Bot

## Avance #1 – Configuración Inicial y Prototipo Base
**Fecha:** Anterior a Diciembre 2025  
**Estado:** ✅ Completado

### Descripción General
Desarrollo del prototipo inicial del bot con arquitectura básica frontend-backend integrada con Google Gemini API.

### Cambios Principales

#### ✨ Nuevas Características
- **Chat conversacional básico** con interfaz flotante en React
- **Clasificación de intenciones** de usuario en 5 categorías:
  1. Preguntas sobre Active Research
  2. Preguntas sobre metodología de investigación
  3. Cotización de proyectos
  4. Pulso Ciudadano y encuestas
  5. Preguntas fuera del scope
- **Respuesta inteligente** mediante Google Gemini API
- **Sistema de fallback** con respuestas predeterminadas cuando Gemini no está disponible
- **Persistencia de datos** en MongoDB con registro de todas las interacciones

#### 🔧 Componentes Creados
```
backend/
  ├── app.py                    # Servidor Flask con endpoints de chat
  
frontend/
  ├── src/
  │   ├── App.js               # Componente principal
  │   ├── App.css              # Estilos
  │   └── components/          # Componentes React del chat
  
  └── public/
      └── index.html           # HTML base
```

#### 🛠️ Tecnologías Añadidas
- **Flask** – Backend REST API
- **Flask-CORS** – Manejo de CORS
- **React** – Frontend SPA
- **MongoDB** – Base de datos NoSQL
- **Google Generative AI** – Modelo Gemini para clasificación y respuestas
- **python-dotenv** – Gestión de variables de entorno

#### 🔐 Configuración
- Variables de entorno: `GEMINI_API_KEY`, `MONGODB_URI`, `MONGODB_DBNAME`
- Puerto backend: `5000`
- Puerto frontend: `3000`
- CORS configurado para conexión local

#### ⚠️ Problemas Conocidos (Resueltos después)
- API Key comprometida (resuelta con nueva clave)
- Modelo de Gemini no disponible inicialmente
- Método `datetime.utcnow()` deprecado

---

## Avance #2 – Integración de Web Scraping e Índice Local
**Fecha:** 1 de Diciembre 2025  
**Estado:** ✅ Completado

### Descripción General
Implementación de un sistema robusto de web scraping que descarga contenido en vivo del sitio de Activa Research y lo almacena en MongoDB como un "índice local". El bot ahora consulta esta información real para generar respuestas más precisas y actualizadas.

### Cambios Principales

#### ✨ Nuevas Características
- **Web Scraping Automático** – Script que extrae contenido de 3 secciones clave de Activa Research:
  - Pulso Ciudadano
  - Estudios de Opinión
  - Quiénes Somos
  
- **Índice Local en MongoDB** – Almacenamiento de contenido scraped en colección `activa_content`

- **Búsqueda Contextual** – El bot busca información relevante en MongoDB y la pasa a Gemini como contexto

- **Respuestas Más Precisas** – Las categorías 1 (Activa) y 4 (Pulso Ciudadano) ahora incluyen datos reales del sitio

#### 🔧 Componentes Creados/Modificados

**Nuevos archivos:**
```
backend/
  ├── scraper_activa.py        # Script de web scraping
  └── .gitignore              # Protección de archivos sensibles
```

**Modificados:**
```
backend/
  └── app.py                  # Integración de búsqueda en MongoDB
                              # Corrección de datetime.utcnow()
                              # Nueva colección activa_content_col
```

#### 🛠️ Tecnologías Añadidas
- **BeautifulSoup4** – Parsing de HTML y extracción de datos
- **requests** – Descargas HTTP de páginas web
- **PyMongo** – Operaciones adicionales en MongoDB
- **python-dotenv** – Ya existente, mejorado para nuevo script

#### 📝 Nuevas Funciones en `app.py`

```python
def buscar_contenido_activa(secciones: list, limite: int = 5) -> str
```
Busca contenido en MongoDB y lo formatea para pasar a Gemini como contexto.

#### 🔍 Estructura de Datos en MongoDB

**Colección:** `activa_content`

```json
{
  "_id": ObjectId(...),
  "seccion": "pulso_ciudadano|estudios|quienes_somos",
  "contenido": {
    "type": "string",
    "titulo": "string",
    "descripcion": "string",
    "especialidades": ["array"],
    "enlace": "string",
    "fecha": "string"
  },
  "fecha_actualizacion": ISODate(...)
}
```

#### 🔄 URLs Scrapeadas
| Sección | URL |
|---------|-----|
| Pulso Ciudadano | https://chile.activasite.com/pulso-ciudadano/ |
| Estudios de Opinión | https://chile.activasite.com/estudios-de-opinion/ |
| Quiénes Somos | https://chile.activasite.com/quienes-somos/ |

#### 🚀 Cómo Usar el Scraper

```bash
cd backend
python scraper_activa.py
```

**Salida esperada:**
```
🔄 Iniciando descarga de contenido de Activa Research...
📥 Procesando: pulso_ciudadano
   URL: https://chile.activasite.com/pulso-ciudadano/
✅ 1 documentos guardados para pulso_ciudadano
...
✅ Descarga completada!
```

#### 🔧 Integraciones Realizadas

1. **En `generar_respuesta_gemini()` – Categoría 1:**
   - Busca contenido de "Quiénes Somos"
   - Añade información real al contexto de Gemini

2. **En `generar_respuesta_gemini()` – Categoría 4:**
   - Busca contenido de "Pulso Ciudadano" y "Estudios"
   - Proporciona estudios recientes al contexto

3. **Importación de UTC:**
   - `from datetime import UTC`
   - Reemplazó `datetime.utcnow()` por `datetime.now(UTC)`

#### 🗑️ Eliminaciones/Cambios Importantes

| Antes | Después | Razón |
|-------|---------|-------|
| `datetime.utcnow()` | `datetime.now(UTC)` | Deprecación en Python 3.12+ |
| Sin búsqueda local | Con búsqueda en MongoDB | Mayor precisión en respuestas |
| Modelos `gemini-1.5-flash-latest` | `gemini-1.5-flash` | Compatibilidad con API |

#### ⚡ Instalación de Dependencias

```bash
pip install beautifulsoup4 requests pymongo python-dotenv
```

#### 📊 Estadísticas del Scraper

| Métrica | Valor |
|---------|-------|
| URLs scrapeadas | 3 |
| Secciones indexadas | 3 |
| Documentos extraídos (promedio) | ~10 por sección |
| Tiempo de ejecución | ~5-10 segundos |
| Frecuencia recomendada | Semanal |

#### 🔐 Seguridad

- `.env` protegido en `.gitignore` (ya existente)
- Creado nuevo `.gitignore` en `backend/` con:
  - `venv/`, `__pycache__/`
  - `.env` y variantes
  - Carpetas de IDE (`.vscode/`, `.idea/`)

#### 📌 Ventajas del Enfoque (Opción 3)

✅ Información **actualizada y real**  
✅ **Rápido** en tiempo de respuesta (sin latencia de scraping por solicitud)  
✅ **Robusto** – No depende de cambios en estructura HTML en tiempo real  
✅ **Escalable** – Fácil agregar más secciones  
✅ **Flexible** – Información local, procesable por Gemini  

#### 🔄 Flujo de Ejecución Actualizado

```
1. Script scraper_activa.py (ejecutar 1x o periódicamente)
   ↓
2. Descarga HTML de 3 URLs de Activa Research
   ↓
3. Extrae y procesa contenido
   ↓
4. Guarda en MongoDB colección "activa_content"
   ↓
5. Usuario pregunta en el bot
   ↓
6. Bot clasifica la intención
   ↓
7. Bot busca en MongoDB si es categoría 1 o 4
   ↓
8. Bot pasa información a Gemini como contexto
   ↓
9. Gemini genera respuesta basada en datos reales
   ↓
10. Respuesta entregada al usuario
```

#### 📝 Próximos Pasos Sugeridos

- [ ] Automatizar scraping con APScheduler (semanal)
- [ ] Mejorar parsing de HTML dinámico con Selenium
- [ ] Agregar más secciones (servicios, clientes, etc.)
- [ ] Implementar búsqueda full-text en MongoDB
- [ ] Cachear resultados de Gemini
- [ ] Panel de admin para visualizar índice local
- [ ] Tests unitarios para scraper y búsqueda

#### 🐛 Problemas Resueltos en Este Avance

| Problema | Solución |
|----------|----------|
| Modelos de Gemini no encontrados | Cambiar a `gemini-1.5-flash` válido |
| API Key comprometida | Generar nueva clave en Google AI Studio |
| `datetime.utcnow()` deprecado | Usar `datetime.now(UTC)` |
| Bot sin contexto real | Implementar scraping e índice local |
| Respuestas genéricas | Integrar búsqueda en MongoDB |

---

## Resumen de Cambios Acumulados

### Archivos Modificados
- `app.py` – Añadida búsqueda en MongoDB, correcciones de datetime
- `README.md` – Este archivo de progreso

### Archivos Creados
- `scraper_activa.py` – Web scraper con ParseJSoup
- `backend/.gitignore` – Protección mejorada
- `PROGRESS.md` – Este registro de avances

### Dependencias Añadidas (Avance #2)
- beautifulsoup4==4.14.3
- requests==2.32.5
- pymongo==4.15.4

### Base de Datos
- Nueva colección: `activa_content`
- Estructura: Documentos con secciones, contenido, y timestamps

---

## Estadísticas del Proyecto

| Aspecto | Avance #1 | Avance #2 | Total |
|---------|-----------|-----------|-------|
| Archivos Python | 1 | 2 | 3 |
| Endpoints REST | 1 | 1 | 1 |
| Categorías de clasificación | 5 | 5 | 5 |
| Colecciones MongoDB | 1 | 2 | 2 |
| Dependencias Python | 7 | 10 | 10 |
| Líneas de código backend | ~550 | ~625 | ~625 |

---

## Notas Importantes

1. **Scraper Actual:** Extrae títulos, descripciones y enlaces. Para información más granular, puede mejorarse el parsing.

2. **Frecuencia de Actualización:** Se recomienda ejecutar `scraper_activa.py` semanalmente o antes de cambios importantes en el sitio de Activa.

3. **Performance:** La búsqueda local en MongoDB es mucho más rápida que hacer scraping en cada solicitud.

4. **Contexto a Gemini:** El contenido buscado se pasa como contexto a Gemini, quien puede procesarlo y generar respuestas coherentes.

---

**Última actualización:** 1 de Diciembre, 2025
