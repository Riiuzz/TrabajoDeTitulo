import os
from datetime import datetime, UTC

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
import google.generativeai as genai

# =========================
# Configuración inicial
# =========================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DBNAME = os.getenv("MONGODB_DBNAME", "trabajo_titulo")

GEMINI_MODEL_CLASSIFIER = "gemini-2.5-flash"
GEMINI_MODEL_CHAT = "gemini-2.5-flash-lite"


if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("⚠️  GEMINI_API_KEY no está definido. Se usará solo la lógica de respaldo.")

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# =========================
# Conexión a MongoDB
# =========================

mongo_client = None
interacciones_col = None
activa_content_col = None

if MONGODB_URI:
    try:
        mongo_client = MongoClient(MONGODB_URI)
        mongo_db = mongo_client[MONGODB_DBNAME]
        interacciones_col = mongo_db["interacciones"]
        activa_content_col = mongo_db["activa_content"]
        print("✅ Conectado a MongoDB Atlas correctamente.")
    except Exception as e:
        print("⚠️  Error conectando a MongoDB Atlas:", repr(e))
else:
    print("⚠️  MONGODB_URI no está definido. No se guardarán interacciones en BD.")


# =========================
# Funciones auxiliares
# =========================

def llamar_gemini(prompt: str, model_name: str) -> str | None:
    """
    Llama a Gemini con el prompt dado.
    Devuelve el texto de respuesta o None si hay error.
    """
    if not GEMINI_API_KEY:
        return None

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        texto = (response.text or "").strip()
        if not texto:
            return None
        return texto
    except Exception as e:
        print("⚠️  Error al llamar a Gemini:", repr(e))
        return None


def buscar_contenido_activa(secciones: list, limite: int = 5) -> str:
    """
    Busca contenido sobre Activa Research en MongoDB.
    
    Args:
        secciones: lista de secciones a buscar (ej: ["pulso_ciudadano", "estudios"])
        limite: máximo número de documentos a recuperar por sección
    
    Returns:
        Texto formateado con el contenido encontrado, o string vacío si no hay nada.
    """
    if activa_content_col is None:
        return ""
    
    try:
        contenido = []
        
        for seccion in secciones:
            docs = list(activa_content_col.find(
                {"seccion": seccion},
                {"contenido": 1, "fecha_actualizacion": 1}
            ).limit(limite))
            
            for doc in docs:
                item = doc.get("contenido", {})
                
                # Formatear según el tipo de contenido
                if isinstance(item, dict):
                    titulo = item.get("titulo", "")
                    descripcion = item.get("descripcion", "")
                    especialidades = item.get("especialidades", [])
                    nombre = item.get("nombre", "")
                    texto = item.get("texto", "")
                    
                    if titulo:
                        contenido.append(f"📌 {titulo}")
                    if descripcion:
                        contenido.append(f"   {descripcion}")
                    if especialidades:
                        contenido.append(f"   Áreas: {', '.join(especialidades)}")
                    if nombre:
                        contenido.append(f"   - {nombre}")
                    if texto:
                        contenido.append(f"   {texto[:200]}...")  # Limitar a 200 caracteres
        
        return "\n".join(contenido)
    
    except Exception as e:
        print(f"⚠️  Error buscando contenido: {repr(e)}")
        return ""


# =========================
# Clasificación de intención
# =========================

def clasificar_mensaje_gemini(mensaje: str) -> int | None:
    """
    Usa Gemini para clasificar el mensaje en categorías 1–5.
    Devuelve un int o None si falla.
    """
    prompt = f"""
Eres un clasificador de intención para un bot de la empresa Active Research,
una empresa chilena de estudios de mercado y opinión pública.

Supón SIEMPRE que el usuario está en el sitio web de Active Research.
Por lo tanto, cuando el usuario diga cosas como "esta empresa",
"ustedes", "la encuesta", "sus estudios", etc., se refiere a Active Research
y a su trabajo.

Tu tarea es leer el mensaje del usuario y RESPONDER ÚNICAMENTE con un número
del 1 al 5, sin explicación extra, según estas categorías:

1. Preguntas sobre Active Research:
   - qué es la empresa, a qué se dedica, en qué país está,
     qué servicios ofrece, qué tipo de estudios realiza,
     unidades de negocio, clientes, historia, etc.
   - También considera cuando escriben mal el nombre:
     "Activa", "Active Reserch", "Activeresearch", "Activa Research", etc.
   - También preguntas generales como:
     "¿A qué se dedica esta empresa?",
     "¿Qué hace esta empresa?",
     "¿Qué hacen ustedes?".

2. Preguntas de investigación:
   - metodologías, técnicas, estadísticas, encuestas, cuestionarios,
     márgenes de error, muestras, muestreo, CATI, CAWI, encuestas online, etc.
   - Ejemplos: "¿Qué es la técnica CATI?", "¿Qué es una encuesta de opinión?",
     "¿Cómo se calcula el margen de error?".

3. Cotizar proyectos:
   - cotizar, cotización, presupuesto, precio, cuánto cuesta un estudio,
     cuánto sale un estudio, quiero cotizar un estudio, etc.
   - Ejemplos: "Quiero cotizar un estudio de opinión en Santiago",
     "¿Cuánto cuesta un estudio de mercado?".

4. Pulso Ciudadano y encuestas de opinión de Activa:
   - "Pulso Ciudadano", "encuesta de Activa", "encuesta de Active Research",
     "última encuesta de Activa", "resultados de la encuesta de Activa",
     pronósticos electorales, aprobación de gobierno, resultados de encuestas
     de opinión pública de la empresa.
   - También preguntas como:
     "¿Qué tipo de encuestas puedo ver aquí?",
     "¿Dónde puedo ver los resultados de las encuestas de Activa?".

5. Cualquier otra cosa que NO tenga relación con lo anterior:
   - preguntas genéricas (frutas, chistes, definiciones sin relación
     con investigación de mercado),
   - matemáticas o programación que no se conectan con estudios de mercado,
   - temas personales, religión, deportes, etc.

Regla importante:
- Si el mensaje tiene ALGO que pueda relacionarse con la empresa,
  sus estudios de mercado, encuestas, investigación o cotizaciones,
  elige SIEMPRE una categoría entre 1 y 4.
- Usa la categoría 5 SOLO cuando el mensaje claramente no tiene
  ninguna relación con el trabajo de Active Research.

Ejemplos:

Mensaje: "Qué es Active Research?"
Respuesta: 1

Mensaje: "A qué se dedica esta empresa?"
Respuesta: 1

Mensaje: "Qué tipo de encuestas puedo ver?"
Respuesta: 4

Mensaje: "Qué es la técnica CATI?"
Respuesta: 2

Mensaje: "Quiero cotizar un estudio de opinión en Santiago"
Respuesta: 3

Mensaje: "Dame los resultados de la última encuesta de Activa"
Respuesta: 4

Mensaje: "Qué es una naranja?"
Respuesta: 5

Recuerda: responde SOLO con el número 1, 2, 3, 4 o 5.

Mensaje del usuario:
"{mensaje}"
"""

    texto = llamar_gemini(prompt, GEMINI_MODEL_CLASSIFIER)
    if texto is None:
        return None

    texto = texto.strip()
    # Nos quedamos solo con los dígitos
    solo_numero = "".join(ch for ch in texto if ch.isdigit())

    if solo_numero in {"1", "2", "3", "4", "5"}:
        return int(solo_numero)

    # Si no se pudo interpretar, devolvemos None para usar la lógica de respaldo
    print("⚠️  Respuesta del clasificador no válida:", repr(texto))
    return None


def clasificar_mensaje_fallback(mensaje: str) -> int:
    """
    Clasificador de respaldo con reglas simples por palabras clave.
    No usa IA, pero permite que el sistema siempre tenga una categoría.
    Aquí tratamos de detectar CUALQUIER relación con el dominio
    para devolver 1–4 y dejar 5 solo para cosas totalmente fuera de contexto.
    """
    text = mensaje.lower()

    # 4 - Pulso Ciudadano / encuestas de Activa (más específico)
    if any(
        palabra in text
        for palabra in [
            "pulso ciudadano",
            "encuesta de activa",
            "encuesta de actíva",
            "encuesta activa",
            "encuesta de active research",
            "última encuesta",
            "ultima encuesta",
            "encuesta pública de activa",
            "encuesta publica de activa",
        ]
    ):
        return 4

    # 3 - Cotizar proyectos
    if any(
        palabra in text
        for palabra in [
            "cotizar",
            "cotización",
            "cotizacion",
            "presupuesto",
            "cuánto cuesta",
            "cuanto cuesta",
            "precio",
            "cuánto sale",
            "cuanto sale",
            "quiero un presupuesto",
        ]
    ):
        return 3

    # 2 - Investigación / técnicas / encuestas en general
    if any(
        palabra in text
        for palabra in [
            "cati",
            "cawi",
            "encuesta",
            "encuestas",
            "margen de error",
            "margen de muestreo",
            "muestra",
            "muestreo",
            "cuestionario",
            "metodología",
            "metodologia",
            "estudio de mercado",
            "estudios de mercado",
            "investigación de mercado",
            "investigacion de mercado",
            "opinión pública",
            "opinion publica",
        ]
    ):
        return 2

    # 1 - Preguntas generales sobre la empresa / quiénes somos
    if any(
        palabra in text
        for palabra in [
            "active research",
            "activa research",
            "activa",
            "activeresearch",
            "active reserch",
            "empresa",
            "ustedes",
            "a que se dedica",
            "a qué se dedica",
            "que hacen",
            "qué hacen",
            "que hace esta empresa",
            "qué hace esta empresa",
            "que tipo de estudios realizan",
            "qué tipo de estudios realizan",
        ]
    ):
        return 1

    # 5 - No aplica (no encontramos relación con el dominio)
    return 5


def clasificar_mensaje(mensaje: str) -> int:
    """
    Intenta clasificar con Gemini y, si falla, usa la lógica de respaldo.
    Si Gemini devuelve 5 (no aplica) pero el clasificador de respaldo
    detecta relación con el dominio (1–4), se usa la categoría del respaldo.
    Así evitamos rechazar preguntas que sí tienen que ver con la empresa.
    """
    categoria_gemini = clasificar_mensaje_gemini(mensaje)
    categoria_fallback = clasificar_mensaje_fallback(mensaje)

    if categoria_gemini is None:
        # Si Gemini falla, usamos el fallback directamente
        return categoria_fallback

    if categoria_gemini == 5 and categoria_fallback != 5:
        # Gemini dice "no aplica", pero vemos palabras del dominio:
        # preferimos la categoría 1–4 del fallback.
        return categoria_fallback

    # En cualquier otro caso confiamos en Gemini
    return categoria_gemini


# =========================
# Generación de respuesta
# =========================

def generar_respuesta_gemini(mensaje: str, categoria: int) -> str | None:
    """
    Genera una respuesta usando Gemini, con contexto distinto según la categoría.
    Busca información en MongoDB cuando es relevante.
    Devuelve None si hay algún problema.
    """

    base_instrucciones = """
Eres un asistente virtual de la empresa chilena Active Research,
especializada en estudios de mercado y opinión pública.

Responde SIEMPRE en español, de forma profesional pero cercana,
en un máximo de 3 a 4 frases. No inventes datos numéricos muy específicos
(por ejemplo, porcentajes exactos) si no los conoces con certeza; en ese caso
habla de forma general.
"""

    if categoria == 1:
        # Buscar información sobre "Quiénes Somos"
        contenido_adicional = buscar_contenido_activa(["quienes_somos"])
        contexto = """
Contexto (categoría 1 - Active Research):

Active Research (a veces llamada "Activa") es una empresa de estudios de mercado
y opinión pública en Chile. Realiza estudios cuantitativos y cualitativos para
apoyar la toma de decisiones de empresas e instituciones.

Algunas ideas para tus respuestas:
- Explica brevemente qué hace la empresa.
- Puedes mencionar que cuenta con unidades de negocio como Customer Experience
  y Marketing Intelligence.
- Evita inventar nombres de clientes concretos si no estás seguro.
"""
        if contenido_adicional:
            contexto += f"\n\nInformación actual sobre la empresa:\n{contenido_adicional}"
    
    elif categoria == 2:
        contexto = """
Contexto (categoría 2 - Investigación):

Responde como un especialista en investigación de mercados, explicando conceptos
como:
- encuestas,
- cuestionarios,
- técnicas de levantamiento de datos (CATI, CAWI, encuestas online, etc.),
- márgenes de error,
- diseño muestral y análisis de datos.

Usa un lenguaje claro, pensado para alguien que no es experto.
"""
    
    elif categoria == 3:
        contexto = """
Contexto (categoría 3 - Cotización de proyectos):

El usuario está interesado en cotizar un estudio o proyecto con Active Research.

Tu respuesta debe:
- Agradecer el interés.
- Explicar de forma general qué información se suele necesitar para cotizar
  (objetivo del estudio, público objetivo, cobertura geográfica, plazos, etc.).
- Sugerir que la persona entregue sus datos de contacto por los canales oficiales
  de la empresa (por ejemplo, página web o correo corporativo), SIN inventar
  direcciones específicas si no las conoces.
"""
    
    elif categoria == 4:
        # Buscar información sobre Pulso Ciudadano y Estudios
        contenido_pulso = buscar_contenido_activa(["pulso_ciudadano", "estudios"])
        contexto = """
Contexto (categoría 4 - Pulso Ciudadano y encuestas de opinión):

Pulso Ciudadano es un estudio de opinión pública asociado a Activa
(Active Research) que mide temas como aprobación de gobierno,
intención de voto y otros temas de actualidad.

Reglas para tus respuestas en esta categoría:

- Si la pregunta del usuario menciona "última encuesta", "último estudio",
  "último pronóstico", "última medición", "resultados más recientes"
  o frases similares, intenta responder de forma directa a esa petición:
  * Indica el período de levantamiento (fechas aproximadas) y el tema
    del estudio (por ejemplo, primera vuelta presidencial 2025).
  * Si recuerdas resultados o tendencias principales, puedes mencionarlos
    de forma resumida.
  * Si no estás seguro de los números exactos o no tienes la información,
    dilo explícitamente (por ejemplo: "no dispongo de los resultados
    exactos más recientes"), y da una explicación general sobre el estudio.

- Si la pregunta es más general, como "¿qué es Pulso Ciudadano?" o
  "¿de qué se tratan las encuestas de Activa?", entonces explica en forma
  general qué es este tipo de estudio y qué tipo de información entrega.

Siempre responde en un máximo de 3 a 4 frases, en un tono profesional
pero cercano, y sin inventar datos muy específicos cuando no estés seguro.
"""
        if contenido_pulso:
            contexto += f"\n\nEstudios recientes disponibles:\n{contenido_pulso}"
    
    else:
        contexto = ""

    prompt = f"""{base_instrucciones}

{contexto}

Pregunta del usuario:
\"\"\"{mensaje}\"\"\"

Redacta la mejor respuesta posible para el usuario:
"""

    return llamar_gemini(prompt, GEMINI_MODEL_CHAT)



def generar_respuesta_fallback(mensaje: str, categoria: int) -> str:
    """
    Respuestas simples de respaldo cuando Gemini no está disponible.
    """
    if categoria == 1:
        return (
            "Active Research es una empresa de estudios de mercado y opinión "
            "pública que se dedica a levantar y analizar información para apoyar "
            "la toma de decisiones de sus clientes."
        )
    if categoria == 2:
        return (
            "En investigación de mercado se utilizan encuestas, muestras y "
            "técnicas como CATI o encuestas online para obtener datos de las "
            "personas y poder analizarlos estadísticamente."
        )
    if categoria == 3:
        return (
            "Para cotizar un proyecto de estudio normalmente se necesita saber "
            "el objetivo del estudio, el público objetivo, la cobertura geográfica "
            "y los plazos. Un ejecutivo de Active Research podría ayudarte con una "
            "cotización más detallada."
        )
    if categoria == 4:
        return (
            "Pulso Ciudadano es un estudio de opinión pública asociado a Activa, "
            "donde se miden temas como aprobación de gobierno e intención de voto. "
            "Los resultados se actualizan periódicamente."
        )

    # Categoría 5 - no aplica
    return (
        "La consulta ingresada no se relaciona con el ámbito de este asistente. "
        "Por favor formule preguntas vinculadas a Active Research, sus estudios de "
        "mercado y opinión pública, metodologías de investigación, cotizaciones de "
        "proyectos o el estudio Pulso Ciudadano."
    )


def generar_respuesta(mensaje: str, categoria: int) -> tuple[str, str]:
    """
    Genera la respuesta final para el usuario.

    Devuelve una tupla (texto_respuesta, modo), donde 'modo' puede ser:
    - "no_aplica": para categoría 5 (no se llama a Gemini).
    - "gemini": respuesta generada por Gemini.
    - "fallback": respuesta generada por la lógica de respaldo.
    """

    # Categoría 5: no aplica → no se gasta token de Gemini
    if categoria == 5:
        texto = (
            "La consulta ingresada no se relaciona con el ámbito de este asistente. "
            "Por favor formule preguntas vinculadas a Active Research, sus estudios de "
            "mercado y opinión pública, metodologías de investigación, cotizaciones de "
            "proyectos o el estudio Pulso Ciudadano."
        )
        return texto, "no_aplica"

    # Intentamos con Gemini
    texto = generar_respuesta_gemini(mensaje, categoria)
    if texto:
        return texto, "gemini"

    # Si falla Gemini, usamos la lógica de respaldo
    texto = generar_respuesta_fallback(mensaje, categoria)
    return texto, "fallback"


# =========================
# Guardar interacciones
# =========================

def guardar_interaccion(
    mensaje_usuario: str,
    categoria: int,
    respuesta_bot: str,
    modo: str,
) -> None:
    """
    Guarda la interacción en MongoDB, si la colección está disponible.
    """
    if interacciones_col is None:
        # Si no hay BD, solo lo mostramos en consola
        print(
            f"(Sin BD) [{modo}] Usuario: {mensaje_usuario} | "
            f"Categoría: | Respuesta: {respuesta_bot[:60]}..."
        )
        return

    doc = {
        "mensaje_usuario": mensaje_usuario,
        "categoria": categoria,
        "respuesta_bot": respuesta_bot,
        "modo": modo,
        "timestamp": datetime.now(UTC),
    }

    try:
        interacciones_col.insert_one(doc)
    except Exception as e:
        print("⚠️  Error guardando en MongoDB:", repr(e))


# =========================
# Endpoint principal de chat
# =========================

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    mensaje_usuario = (data.get("message") or "").strip()

    if not mensaje_usuario:
        return jsonify({"error": "Mensaje vacío"}), 400

    # 1) Clasificar el mensaje
    categoria = clasificar_mensaje(mensaje_usuario)

    # 2) Generar la respuesta según la categoría
    respuesta_texto, modo = generar_respuesta(mensaje_usuario, categoria)

    # 3) Guardar en MongoDB
    guardar_interaccion(
        mensaje_usuario=mensaje_usuario,
        categoria=categoria,
        respuesta_bot=respuesta_texto,
        modo=modo,
    )

    # 4) Responder al frontend
    return jsonify(
        {
            "respuesta": respuesta_texto,
            "categoria": categoria,
            "modo": modo,
        }
    )


# =========================
# Main
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
