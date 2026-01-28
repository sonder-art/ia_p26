:::homework{id="A.3.1" title="Leer seccion A.3 OS Setup & Instalación de Unix " due="2026-01-19" points="0"}
Leer seccion A.3 completa.  s
Instala WSL2 en tu computadora Windows siguiendo esta guía. Verifica que funciona ejecutando  `python3 --version` o `python --version` en la terminal de Ubuntu. Si tienes mac o linux o wsl2 ya instaldo no hay problema.

:::

# Guía de Sistema Operativo: WSL2 y Linux

> **⚠️ Nota Importante:** Esta guía proporciona instrucciones generales. Cada computadora es diferente (marca, modelo, versión de BIOS/UEFI, componentes).
>
> **No sigas instrucciones a ciegas.** Utiliza esta guía como mapa y apóyate en los LLMs (como ChatGPT o Gemini) para los detalles específicos de tu máquina.
> **Back-up** Aunque realices esta parte o estes listo no olvides de realizar tambien la guia 'clase/a_stack/02_b_sistema_operativo_browser.md' para siempre tener un back-up de donde seguir la calse o realizar tus tareas.
 
## Opción A: WSL2 (Windows Subsystem for Linux) - Recomendada

WSL2 te permite correr Linux *dentro* de Windows. Es la opción más segura y fácil si nunca has usado Linux.

### ¿Qué es realmente WSL2?
Imagina que tu computadora es una casa (Windows). WSL2 es como construir una habitación anexa que funciona con reglas totalmente diferentes (Linux).
*   **Separación:** Lo que instalas en WSL2 (programas, librerías de Python) "vive" en esa habitación. Windows puede ver los archivos, pero no "entiende" los programas de Linux directamente.
*   **Sistema de Archivos:** WSL2 tiene su propio disco duro virtual.
    *   Ruta Windows: `C:\Users\TuNombre\Documentos`
    *   Ruta WSL2 (Linux): `/home/tunombre/`
    *   *Tip:* Desde WSL2 puedes acceder a tus archivos de Windows en `/mnt/c/`.

### Paso 1: Preparación con IA
Antes de instalar, abre tu LLM favorito y usa este prompt para verificar que tu PC esté lista.

> **Prompt para LLM:**
> "Tengo una computadora con Windows [10 u 11]. Quiero instalar WSL2.
> 1. ¿Cómo verifico si mi versión de Windows es compatible?
> 2. ¿Cómo entro a la BIOS/UEFI de mi modelo [Tu Modelo de Laptop, ej. Dell XPS 15] para activar la virtualización? (Esto es indispensable para WSL2).
> 3. Dame los pasos para activar la característica 'Plataforma de máquina virtual' en Windows."

### Paso 2: Instalación
Generalmente es tan simple como abrir **PowerShell como Administrador** y ejecutar:
```powershell
wsl --install
```
Esto instalará Ubuntu por defecto. Reinicia tu computadora.

### Paso 3: Configuración Inicial
Al reiniciar, se abrirá una ventana negra (terminal). Te pedirá:
1.  **Username:** Crea un nombre de usuario (sin espacios, minúsculas). No tiene que ser igual al de Windows.
2.  **Password:** Escribe una contraseña. **OJO:** En Linux, cuando escribes contraseñas **no aparecen asteriscos ni puntos**. Parece que no escribes nada, pero sí lo estás haciendo. Presiona Enter.

### Paso 4: Verificación y Actualización
Una vez dentro de la terminal de Ubuntu:

> **Prompt para LLM:**
> "Ya instalé Ubuntu en WSL2.
> 1. Explícame qué significan los comandos `sudo apt update` y `sudo apt upgrade` y por qué debo correrlos ahora.
> 2. ¿Cómo puedo abrir la carpeta actual de Linux en mi explorador de archivos de Windows?" (Spoiler: el comando es `explorer.exe .`)

---

## Opción B: Dual Boot (Linux Nativo) - Avanzada

Esto significa instalar Linux *junto* a Windows. Al prender la compu, eliges cuál usar. Es más rápido y "real", pero tiene riesgo de borrar tus archivos si te equivocas. **Haz respaldo de todo antes de intentar esto.**

### Paso 1: Investigación de Hardware con IA
Linux funciona diferente en cada hardware.

> **Prompt para LLM:**
> "Tengo una [Marca y Modelo exacto, ej. Lenovo ThinkPad T480]. Quiero instalar Linux en Dual Boot con Windows.
> 1. ¿Hay problemas conocidos de compatibilidad (wifi, tarjeta gráfica, audio) con Ubuntu o Linux Mint en este modelo?
> 2. ¿Cómo entro a la BIOS y desactivo 'Secure Boot' y 'Fast Boot' en mi modelo específico?
> 3. ¿Qué distribución me recomiendas para principiantes?" (Generalmente Ubuntu o Linux Mint).

### Paso 2: Crear la USB de Instalación
Necesitas una memoria USB (se borrará todo lo que tenga) y un programa como **Rufus** o **BalenaEtcher**.

> **Prompt para LLM:**
> "Guíame paso a paso para crear un 'Live USB' de Ubuntu usando Rufus en Windows. Explícame qué es el esquema de partición MBR vs GPT y cuál debo elegir para mi computadora moderna (UEFI)."

### Paso 3: Particionamiento (El paso peligroso)
Necesitas hacer espacio en tu disco duro para Linux.

> **Prompt para LLM:**
> "Quiero reducir mi partición de Windows para dejar espacio libre para Linux.
> 1. ¿Cómo uso la herramienta 'Crear y formatear particiones del disco duro' en Windows?
> 2. ¿Cuánto espacio recomiendas dejar para Linux si voy a usarlo para programación de IA básica? (Sugerencia: al menos 50GB)."

### Paso 4: Instalación
Arranca desde la USB y sigue las instrucciones. Busca la opción "Instalar junto a Windows Boot Manager". **Si no ves esa opción, DETENTE y pregunta a la IA.**

---

## Post-Instalación (Para ambas opciones)

Ya sea WSL2 o Linux nativo, ahora tienes una terminal.

### ¿Cómo sé que todo está bien?
Prueba instalando un programa simple y verificando Python.

1.  Actualiza el sistema: `sudo apt update && sudo apt upgrade -y`
2.  Verifica Python: `python3 --version`
3.  Instala una herramienta divertida (ej. `neofetch`) para ver info de tu sistema:
    ```bash
    sudo apt install neofetch
    neofetch
    ```

> **Prompt Final para LLM:**
> "Ya tengo mi terminal de Linux lista.
> 1. Enséñame los 5 comandos básicos para moverme entre carpetas (`cd`, `ls`, `pwd`, `mkdir`, `rm`).
> 2. ¿Cómo configuro Git y mi cuenta de GitHub por primera vez en esta terminal?"

