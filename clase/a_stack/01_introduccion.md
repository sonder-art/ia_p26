# Introduccion al Stack tecnologico
**Codigo render**: para renderizar la pagina de markdown en vscode o simialres usen `ctrl+shift+v`. Si no funciona busca en google o preguntale a un llm como renderizarlo para tu caso especifico (sistema operativo e IDE que estas usando)  

## Tarea: Configuración de Cuentas

### 1. Cuentas de LLMs
Es necesario crear cuentas en las principales plataformas de IA para tener acceso a diferentes modelos:

*   **Google Gemini:** [https://gemini.google/](https://gemini.google/)
    *   *Nota:* Para estudiantes, hay un plan gratuito por un año: [Gemini para estudiantes](https://gemini.google/mx/students/?hl=es-419).
    *   *Verificación:* Asegúrate también de que [Google Colab](https://colab.google/) funcione correctamente creando un nuevo notebook.
*   **OpenAI (ChatGPT):** [https://chatgpt.com/](https://chatgpt.com/)
*   **Anthropic (Claude):** [https://claude.ai/](https://claude.ai/)
*   **Mistral AI:** [https://mistral.ai/](https://mistral.ai/)
*   **Perplexity:** [https://www.perplexity.ai/](https://www.perplexity.ai/)
*   **DeepSeek:** [https://deepseek.com/](https://deepseek.com/)

### 2. Cuenta de DataCamp (Acceso Institucional)
Utilizaremos DataCamp para cursos prácticos. **Es obligatorio usar tu correo institucional (`@itam.mx`).**

1.  **Inicio de Sesión:**
    *   Ve a [DataCamp](https://app.datacamp.com/) y asegúrate de iniciar sesión con tu correo `@itam.mx`.
    *   *Importante:* Si tienes otra sesión abierta, ciérrala antes de continuar.
2.  **Unirse a la Organización:**
    *   Una vez logueado, usa este enlace para unirte al grupo de la clase:
    *   [Link de Invitación DataCamp ITAM](https://www.datacamp.com/groups/shared_links/af811a55e5f91a7c05c65caeafacc2bd784d36a969bc062cc73c7397fb47ce6f)
3.  **Verificación:**
    *   Intenta iniciar cualquier curso para confirmar que tienes acceso completo.
    *   Te sugiero probar con el curso de una futura tarea, solo verifica que puedas acceder al curso (no es tarea inmediata): [AI Assisted Coding for Developers](https://app.datacamp.com/learn/courses/ai-assisted-coding-for-developers).

## Stack
Para la clase necesitamos aprender a utilizar 5 herramientas principales:

1. **LLMs**: Large Language Models
2. **Sistema Operativo**: Ubuntu o Linux o Mac o WSL2
3. **Github**: Servicio y sistema (git) de control de versiones
4. **VSCode/Cursor**: Editor de codigo con IA o LLM itegrada
5. **Python**: Lenguaje de programacion

Estas herramientas nos permitiran crear un pipeline de trabajo en el que podamos aprender sobre inteligencia artificial. Per-se no estudiaremos a detalle cada una de estas herramientas, ni entraremos mucho en su teoria particular, sin embargo aprender a utilizarlas es escencial.


### 1. LLMs (Large Language Models)
Son modelos de inteligencia artificial entrenados con cantidades masivas de texto. Tienen la capacidad de entender y generar lenguaje humano, lo que nos permite interactuar con ellos para obtener respuestas, generar código, resumir textos y mucho más. Ejemplos populares incluyen Gemini, GPT, Claude y Llama.

### 2. Sistema Operativo
Recomiendo encarecidamente trabajar en un entorno basado en Unix (Linux o macOS) para el desarrollo de IA y programación en general. Hay una guia mas general y detallada en las siguientes secciones.

*   **Usuarios de Windows:** La mejor opción es instalar **WSL2 (Windows Subsystem for Linux 2)**. Esto te permite ejecutar un entorno Linux completo integrado directamente en Windows.
    *   *Nota:* WSL2 funciona como un sistema independiente; los archivos y programas instalados en WSL2 están separados de tu sistema Windows principal, aunque puedes acceder a ellos.
    *   *Alternativa:* Configurar un **Dual Boot** (Linux junto a Windows) o usar Linux como sistema principal si te sientes cómodo.
*   **Usuarios de macOS / Linux:** No necesitan configuración adicional, ya están listos para trabajar.

> **Advertencia:** Eviten trabajar directamente sobre Windows (sin WSL2). El desarrollo de IA y los comandos de terminal suelen ser mucho más lentos y problemáticos en Windows nativo. Además, los LLMs generan mejor código para sistemas Unix. 

👉 **Guía Detallada:** Consulta el archivo [`clase/a_stack/a_sistema_operativo.md`](./a_sistema_operativo.md) para instrucciones paso a paso sobre cómo instalar WSL2 o configurar Linux.

### B. Alternativa: Programación en la Nube (Sin computadora personal)
Si no tienes una computadora personal adecuada o no puedes realizar instalaciones, no te preocupes. Puedes programar directamente desde el navegador usando servicios en la nube.

*   **GitHub Codespaces:** Entorno de desarrollo completo en la nube, gratuito para estudiantes.
*   **Gitpod:** Similar a Codespaces, ofrece horas gratuitas al mes.
*   **Google Colab:** Ideal para notebooks de Python y ciencia de datos.

👉 **Guía Detallada:** Consulta [`clase/a_stack/b_sistema_operativo_browser.md`](./b_sistema_operativo_browser.md) para aprender a configurar estos entornos remotos.


### 3. Github
Es una plataforma en la nube que utiliza Git, un sistema de control de versiones. Nos permite guardar nuestro código, llevar un historial de cambios y colaborar con otros desarrolladores. Es fundamental para compartir proyectos y trabajar en equipo de manera organizada.  

### 4. VSCode / Cursor
**VSCode** es un editor de código ligero y potente creado por Microsoft, muy popular por su extensibilidad. **Cursor** es un editor basado en VSCode que integra inteligencia artificial de forma nativa, permitiéndonos escribir, refactorizar y entender código mucho más rápido con la ayuda de LLMs.

### 5. Python
Es un lenguaje de programación de alto nivel, conocido por su sintaxis clara y legible. Es el lenguaje estándar en la industria de la Inteligencia Artificial y Ciencia de Datos debido a su enorme ecosistema de librerías especializadas (como PyTorch, TensorFlow y Pandas) y su facilidad de uso.

