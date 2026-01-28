:::homework{id="A.4.1" title="Instalar Cursor" due="2026-01-19" points="0"}
Leer seccion A.4 completa  
Instala Cursor en tu sistema operativo y verifica que el comando `cursor .` funciona desde la terminal.

:::

# Instalación de Cursor

Cursor es un fork de VSCode que integra modelos de lenguaje avanzados directamente en el editor.

## Guía de Instalación con Ayuda de IA

Cada sistema operativo tiene sus trucos. En lugar de darte una lista estática de pasos, usa los siguientes prompts con tu LLM favorito (ChatGPT, Claude, etc.) para obtener una guía personalizada y actualizada.

### Prompt para Windows (WSL2) - **CRÍTICO**

La instalación en WSL2 es la más delicada. Necesitas que Cursor (instalado en Windows) se comunique con tu sistema de archivos de Linux (WSL).

> **Copia y pega esto a tu LLM:**
> "Estoy usando Windows 11 con WSL2 (Ubuntu). Quiero instalar el IDE Cursor.
> 1. Explícame cómo instalar Cursor en Windows.
> 2. Una vez instalado, ¿cómo abro una carpeta que está dentro de WSL desde Cursor?
> 3. ¿Cómo instalo el comando `cursor .` en mi terminal de WSL para poder abrir proyectos escribiendo ese comando directamente en la terminal de Ubuntu? (Explícame la diferencia entre usar el Remote Server de VSCode vs Cursor).
> 4. Si tengo problemas de conexión con el servidor remoto, ¿qué comandos de diagnóstico debo correr?"

**Puntos Clave para WSL2:**
*   Instalas el `.exe` en Windows.
*   Al abrirlo, instalas la extensión "WSL" (normalmente viene preinstalada o sugerida).
*   En la terminal de Ubuntu, el comando mágico suele ser `cursor .` (similar a `code .`). Si no funciona, el LLM te dirá cómo agregarlo al PATH.

### Prompt para macOS

> **Copia y pega esto a tu LLM:**
> "Tengo una Mac (Apple Silicon / Intel). Quiero instalar Cursor.
> 1. Dame los pasos para descargarlo e instalarlo.
> 2. ¿Cómo configuro el comando de terminal `cursor` para poder abrir carpetas desde mi terminal (zsh/bash)?"

### Prompt para Linux Nativo

> **Copia y pega esto a tu LLM:**
> "Uso Linux (Ubuntu/Fedora/Arch). Quiero instalar Cursor usando el AppImage o instalador recomendado.
> 1. ¿Cuál es la forma recomendada de instalarlo para que se actualice o sea fácil de manejar?
> 2. ¿Cómo agrego el AppImage a mi PATH o creo un alias para poder ejecutar `cursor .` desde cualquier carpeta?"

---

## Verificación de Instalación

Para confirmar que todo está listo:

1.  Abre tu terminal (WSL, Mac o Linux).
2.  Crea una carpeta de prueba: `mkdir prueba_cursor`
3.  Entra: `cd prueba_cursor`
4.  Ejecuta: `cursor .`

Si se abre la ventana de Cursor mostrando esa carpeta, **¡Felicidades!** Ya tienes tu entorno listo.

