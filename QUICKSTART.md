# 🎯 Guía de Inicio Rápido (5 minutos)

¿Acabas de clonar el proyecto? Sigue estos 5 pasos para tener todo funcionando.

---

## Paso 1: Preparar Variables de Entorno (2 min)

### 1a. Obtener API key de Gemini
- Ve a https://aistudio.google.com/apikey
- Crea o copia una API key
- Guárdala en un archivo

### 1b. Obtener MongoDB URI
- Ve a MongoDB Atlas (https://www.mongodb.com/cloud/atlas)
- Obtén tu connection string
- Debe verse como: `mongodb+srv://usuario:pass@cluster.mongodb.net/...`

### 1c. Crear archivo `.env`
En la carpeta `backend/`, crea un archivo llamado `.env`:

```env
GEMINI_API_KEY=tu_api_key_aqui
MONGODB_URI=tu_mongodb_uri_aqui
MONGODB_DBNAME=trabajo_titulo
```

**⚠️ IMPORTANTE:** Este archivo NO se sube a GitHub (está protegido en .gitignore)

---

## Paso 2: Instalar Backend (1 min)

Abre una terminal PowerShell en `backend/`:

```bash
cd backend

python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## Paso 3: Descargar Contenido de Activa (1 min)

Aún en la terminal de `backend/`:

```bash
python scraper_activa.py
```

Espera a que veas ✅ Descarga completado!

---

## Paso 4: Iniciar Backend (1 min)

En la misma terminal:

```bash
python app.py
```

Verás algo como:
```
✅ Conectado a MongoDB Atlas correctamente.
 * Running on http://127.0.0.1:5000
```

**Deja esta terminal abierta.**

---

## Paso 5: Iniciar Frontend (0 min)

Abre OTRA terminal en `frontend/`:

```bash
cd frontend
npm install    # Solo la primera vez
npm start
```

Tu navegador se abrirá automáticamente en `http://localhost:3000` ✅

---

## ✨ ¡Listo! Prueba el Bot

En el chat, escribe:
- "¿Qué es Active Research?"
- "¿Qué es Pulso Ciudadano?"
- "¿Cómo cotizo un estudio?"

El bot debería responder con información real de Activa Research. 🤖

---

## 🚨 Si algo no funciona

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError` | Asegúrate de ejecutar `pip install -r requirements.txt` |
| `Connection refused` en MongoDB | Verifica que MONGODB_URI es correcto en `.env` |
| `API key was reported as leaked` | Genera una nueva API key en Google AI Studio |
| El bot no responde | Verifica que ejecutaste `python scraper_activa.py` |
| Error de CORS | Asegúrate que backend está en puerto 5000 y frontend en 3000 |

👉 Ver **SETUP.md** sección "Troubleshooting" para más ayuda

---

## 📚 Próximos Pasos

- Lee **README.md** para entender mejor el proyecto
- Explora **PROGRESS.md** para ver qué se ha hecho
- Mira **SUMMARY.md** para ver arquitectura visual

---

## 🔗 URLs Importantes

```
Frontend:     http://localhost:3000
Backend:      http://localhost:5000
API Chat:     POST http://localhost:5000/api/chat
```

---

**¡Ahora sí estás listo para desarrollar! 🚀**
