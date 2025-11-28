# Active Research Bot – Prototipo de Asistente Conversacional

## Descripción general del proyecto

Active Research Bot es un prototipo de asistente conversacional desarrollado como trabajo de título para apoyar la atención de potenciales clientes y visitantes del sitio web de la empresa **Active Research**.  

El sistema se presenta como un chat integrado en una página web y está diseñado para:

- Filtrar y responder únicamente preguntas relacionadas con el ámbito de la empresa (estudios de mercado y opinión pública).
- Clasificar cada mensaje del usuario en categorías temáticas predefinidas.
- Registrar todas las interacciones en una base de datos NoSQL, con fines de trazabilidad y análisis posterior.

El prototipo funciona en entorno local (localhost) y está pensado como una base sobre la cual la empresa puede construir un bot empresarial más completo en el futuro.

---

## Lenguajes de programación

El proyecto está desarrollado utilizando los siguientes lenguajes:

- **JavaScript (ES6+)** – Desarrollo del frontend con React.
- **Python 3** – Desarrollo del backend y la integración con el modelo de IA.
- **HTML5 y CSS3** – Estructura y estilos de la interfaz web.

---

## Tecnologías y herramientas utilizadas

### Frontend

- **React** (Create React App)  
  Aplicación de una sola página (SPA) que muestra la información del servicio y el widget de chat flotante.
- **Fetch API**  
  Comunicación del cliente web con el backend mediante solicitudes HTTP a un endpoint REST.

### Backend

- **Python 3**
- **Flask**  
  Microframework utilizado para exponer la API REST que recibe los mensajes del usuario y retorna la respuesta del bot.
- **Flask-CORS**  
  Configuración de CORS para permitir la comunicación entre el frontend (puerto 3000) y el backend (puerto 5000).
- **python-dotenv**  
  Manejo de variables de entorno (claves de API, URI de la base de datos, etc.).

### Inteligencia Artificial

- **Google Gemini API**  
  Modelo generativo utilizado para:
  - Clasificar la intención del mensaje del usuario en una de las categorías definidas.
  - Generar respuestas en lenguaje natural coherentes con el contexto de Active Research, cuando la pregunta es válida.

Además, el backend incorpora una lógica de respaldo simple (reglas básicas) para entregar respuestas mínimas en caso de fallo de la API de IA.

### Base de datos

- **MongoDB Atlas (NoSQL)**  
  - Almacenamiento de las interacciones del chat.
  - Cada documento contiene: mensaje del usuario, categoría asignada, respuesta del bot, modo de respuesta (Gemini / fallback) y marca de tiempo (timestamp).

### Entorno de desarrollo y otras herramientas

- **Node.js y npm** – Gestión de dependencias del frontend.
- **Git y GitHub** – Control de versiones y resguardo del código fuente.
- **Visual Studio Code** – Entorno principal de desarrollo.

---

## Arquitectura de alto nivel

1. El usuario accede a la página web y visualiza un widget de chat flotante en la esquina inferior derecha.
2. Al abrir el chat, el bot muestra un mensaje de bienvenida explicando qué tipo de consultas puede atender.
3. Cada mensaje que el usuario envía se envía al backend mediante una solicitud HTTP `POST` al endpoint `/api/chat`.
4. El backend:
   - Llama al modelo de **Gemini** para clasificar la intención del mensaje en una de las cinco categorías definidas.
   - Si la pregunta es relevante para el contexto de Active Research, el modelo genera una respuesta en lenguaje natural.
   - Si la pregunta no es pertinente, el sistema responde que la consulta no aplica al contexto del sitio.
5. La interacción completa (mensaje, categoría, respuesta, modo, timestamp) se guarda en **MongoDB Atlas**.
6. El backend retorna al frontend un objeto JSON con la categoría y la respuesta, que se muestran en la interfaz del chat.

---

## Habilidades y funcionalidades finales del bot para Active Research

Al finalizar el trabajo de título, el prototipo de Active Research Bot ofrece a la empresa las siguientes capacidades:

1. **Filtrado de consultas según el contexto de la empresa**  
   El bot diferencia entre mensajes relacionados con Active Research y su ámbito de trabajo, y preguntas genéricas o fuera de tema. Cuando detecta que una pregunta no aplica al contexto, responde de forma explícita indicando que la consulta no corresponde al sitio.

2. **Clasificación temática de los mensajes**  
   Cada mensaje del usuario es clasificado en una de las siguientes categorías, alineadas con los requerimientos del profesor guía y de la empresa:
   1. Preguntas sobre **Active Research** (información general de la empresa).
   2. **Preguntas de investigación** (técnicas, estadísticas, encuestas, metodologías como CATI, CAWI, etc.).
   3. **Cotización de proyectos** de estudios de mercado u opinión pública.
   4. Preguntas sobre el **pulso ciudadano** y resultados de encuestas de opinión.
   5. **No aplica** (consultas fuera del alcance del bot).

3. **Generación de respuestas en lenguaje natural**  
   Para los mensajes clasificados en las categorías 1 a 4, el sistema utiliza el modelo de IA (Gemini) para elaborar respuestas coherentes, en español y adaptadas al contexto de la empresa. Esto permite entregar información más rica y útil a potenciales clientes y usuarios del sitio.

4. **Registro estructurado de las interacciones**  
   Todas las conversaciones se almacenan en **MongoDB Atlas**, incluyendo:
   - Mensaje original del usuario.
   - Categoría asignada.
   - Respuesta entregada por el bot.
   - Modo de generación (IA principal o lógica de respaldo).
   - Fecha y hora de la interacción.

   Este registro permite a Active Research:
   - Analizar las consultas más frecuentes.
   - Detectar necesidades de información de los clientes.
   - Evaluar el desempeño futuro del bot y planificar mejoras.

5. **Interfaz web integrada y amigable**  
   - Frontend desarrollado en React con diseño simple, moderno y responsivo.
   - Widget de chat flotante que no interfiere con el contenido principal del sitio.
   - Mensaje de bienvenida y flujo de conversación en formato similar a aplicaciones de mensajería modernas.

6. **Base tecnológica preparada para extensiones futuras**  
   La arquitectura elegida (React + Flask + Gemini + MongoDB Atlas) permite que la empresa, o futuros desarrollos, puedan:
   - Conectar el bot con encuestas reales de Active Research.
   - Incorporar análisis automáticos de resultados.
   - Desplegar el sistema en un entorno de producción (cloud) con mínimos cambios.

---

Este README resume la intención académica y práctica del trabajo de título, y documenta las decisiones de diseño y tecnologías empleadas para construir un asistente conversacional funcional y extensible para Active Research.
