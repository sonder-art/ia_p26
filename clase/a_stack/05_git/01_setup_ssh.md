# Git y GitHub: Tu Pasaporte al Mundo del Software

## Tarea: Configuración y Primer Pull Request

### 1. Curso de DataCamp
Para comprender los conceptos fundamentales, completa el siguiente curso:
*   [Introduction to GitHub Concepts](https://app.datacamp.com/learn/courses/introduction-to-github-concepts)

### 2. Configuración del Entorno
Una vez finalizado el curso de DataCamp, lee detenidamente **este documento** (secciones inferiores). Aquí entenderás la importancia de GitHub en el curso y aprenderás a configurar tu entorno: Git, tu cuenta de GitHub y, **muy importante**, tus llaves SSH.

> **Recomendación:** Utiliza LLMs (como Cursor o ChatGPT) para guiarte en la configuración. Sin embargo, lee primero toda la documentación para saber qué pedir y verificar que todo esté correcto.

### 3. Entender el Flujo de Trabajo (Examen)
El método de trabajo del curso está resumido en:
👉 **[03_workflow.md](./03_workflow.md)**

Es crucial que comprendas este flujo a detalle. **Habrá un examen sobre este tema.**
El examen se enfocará en:
*   Explicar el ciclo de vida de una tarea (Sync -> Branch -> Work -> Push -> PR).
*   Qué está permitido y qué está prohibido (Zona Prohibida vs Zona Segura).
*   Comandos básicos.

Si dominas el contenido de **[03_workflow.md](./03_workflow.md)**, no tendrás problemas. Aunque los agentes de IA pueden ejecutar los comandos por ti, tú eres el responsable de supervisar que sigan las reglas.

### 4. Tarea: Entregar Certificaciones
La tarea consiste en crear tu espacio personal y enviar un Pull Request con tus evidencias.

Toda la guía paso a paso está aquí:
👉 **[Instrucciones de la Tarea 01: Certificaciones](./05_task_certifications.md)**

Pasos generales:
1.  Crear tu carpeta personal en `estudiantes/`.
2.  Subir las evidencias de los cursos (DataCamp de LLMs y GitHub).
3.  Hacer el Pull Request final.

---

### Recursos de Aprendizaje (Lectura Obligatoria)
Antes de intentar la tarea, asegúrate de entender los conceptos leyendo estos documentos en orden:

1.  **[01_setup_ssh.md](./01_setup_ssh.md)** (Este documento): Instala Git y configura tus SSH Keys.
2.  **[02_repo_structure.md](./02_repo_structure.md)**: Configura el repositorio, haz el Fork, el Clone y crea tu carpeta personal.
3.  **[03_workflow.md](./03_workflow.md)**: Aprende el ciclo de trabajo diario (Branches, Commits, Push).

### 3. Entregable (Tu Primer PR)
Para completar esta tarea, debes lograr lo siguiente:
1.  Tener Git instalado y las SSH keys funcionando (incluso después de reiniciar).
2.  Tener tu carpeta `estudiantes/tu_usuario/` creada con un archivo `.gitkeep`.
3.  Hacer un **Pull Request** de tu rama `tarea-1-setup` (o similar) hacia el repositorio del profesor, conteniendo únicamente tu nueva carpeta.

> **Recurso Extra:** Usa el [Cheatsheet de Git](./04_cheatsheet.md) para referencia rápida de comandos.

## ¿Qué es esto y por qué lo necesitamos?

*   **Git:** Es un sistema de "control de versiones". Imagina que es una máquina del tiempo para tus archivos. Te permite guardar "fotos" (commits) de tu código en diferentes momentos, volver atrás si rompes algo y mezclar tu trabajo con el de otros sin borrar lo que ellos hicieron.
*   **GitHub:** Es una red social y plataforma en la nube para alojar repositorios de Git. Es donde vive el código de la clase y donde subirás tus tareas.

---

## Parte 1: Instalación de Git

Dependiendo de tu sistema operativo (que configuramos en el paso anterior), la instalación varía. Aquí es donde usarás a tu **LLM** (ChatGPT, Claude, Gemini) para que te guíe específicamente según tu máquina.

### Paso 1: Pregúntale a tu LLM

Copia y pega este prompt, pero adáptalo a tu caso (WSL2, Mac o Linux Nativo):

> **Prompt:**
> "Estoy configurando mi entorno de desarrollo. Tengo [Sistema Operativo: ej. Windows 11 con WSL2 Ubuntu / MacOS Sequoia].
> 1. ¿Cómo verifico si ya tengo 'git' instalado en mi terminal?
> 2. Si no está instalado, dame el comando exacto para instalarlo.
> 3. Una vez instalado, ¿cómo configuro mi nombre de usuario y correo global (`git config --global`)?"

**Lo que debes lograr:**
Al escribir `git --version` en tu terminal, debe salir algo como `git version 2.x.x`.

---

## Parte 2: Configuración de Llaves SSH (CRÍTICO)

GitHub necesita saber que eres tú quien está subiendo código y no un impostor. Para esto usamos **SSH Keys**. Es como una llave digital: una parte se queda en tu compu (privada) y la otra se la das a GitHub (pública).

**Esta es la parte donde más gente falla.** La configuración debe ser **persistente** (que no se olvide cuando apagues la compu).

### Paso 1: Generar y Configurar SSH con ayuda del LLM

Usa este prompt detallado para que la IA te guíe paso a paso.

> **Prompt:**
> "Necesito configurar una llave SSH para conectarme a GitHub desde mi terminal [WSL2 / Mac / Linux].
> Guíame paso a paso para:
> 1. Generar una nueva llave SSH ed25519 (que es más segura).
> 2. Iniciar el 'ssh-agent' en mi terminal.
> 3. Agregar mi llave al agente.
> 4. **IMPORTANTE:** ¿Cómo hago para que el 'ssh-agent' se inicie automáticamente y cargue mi llave cada vez que abro una nueva terminal o reinicio la computadora? (Dame el código para poner en mi archivo .bashrc o .zshrc).
> 5. Explícame dónde encuentro la llave pública para copiarla y pegarla en la configuración de GitHub."

### Paso 2: Poner la llave en GitHub

1.  Ve a [GitHub Settings > SSH and GPG keys](https://github.com/settings/keys).
2.  Click en **New SSH key**.
3.  Pega el contenido de tu llave pública (que empieza con `ssh-ed25519...`).

---

## Parte 3: La Prueba de Fuego (Reboot)

No confíes en que funciona solo porque funcionó una vez. Necesitamos asegurar la persistencia.

1.  Cierra todas tus terminales.
2.  **Reinicia tu computadora** (Apagar y prender).
3.  Abre tu terminal (WSL2 o Mac).
4.  Escribe el siguiente comando:

```bash
ssh -T git@github.com
```

**Resultado Esperado:**
Debes ver un mensaje como este:
> *Hi [TuUsuario]! You've successfully authenticated, but GitHub does not provide shell access.*

**Si te pide contraseña o dice "Permission denied":** Algo salió mal con el `ssh-agent`. Vuelve a preguntar a tu LLM con el error que te salió. **No avances hasta que esto funcione después de reiniciar.**

