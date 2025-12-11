# Guía para Estudiantes: Usar GitHub Codespaces y Ona (antes Gitpod) Solo con el Navegador

Esta guía explica, paso a paso y en español, cómo tus estudiantes pueden crear cuentas y usar **GitHub Codespaces** y **Ona (antes Gitpod)** sin instalar nada en las laptops de la escuela.  
Pueden hacerlo todo desde el navegador.

***

## 1. Requisitos Generales

Para seguir esta guía, cada estudiante necesita:

- Una conexión a Internet.
- Un navegador moderno (Chrome, Edge, Firefox, Brave, etc.).
- Una dirección de correo electrónico personal.
- Idealmente: un correo institucional (por ejemplo: `@tu-escuela.edu`), pero no siempre es obligatorio.

***

## 2. Parte 1 – GitHub Codespaces

GitHub Codespaces permite usar **Visual Studio Code en la nube**, directamente desde el navegador, con una máquina Linux detrás. No se instala nada en la computadora de la escuela.

### 2.1. Crear una cuenta en GitHub

1. Ir a: [https://github.com](https://github.com)
2. Hacer clic en el botón **Sign up** (Registrarse).
3. Ingresar:
   - Correo electrónico.
   - Nombre de usuario.
   - Contraseña.
4. Confirmar el correo (GitHub envía un email de verificación).
5. Iniciar sesión en [https://github.com](https://github.com) con la nueva cuenta.

> Recomendación: usar un nombre de usuario sencillo y profesional, por ejemplo `nombre-apellido`.

***

### 2.2. Solicitar el GitHub Student Developer Pack (Muy recomendado)

Esto da acceso a **GitHub Pro** y mejores límites para **Codespaces**, gratis para estudiantes.

#### 2.2.1. Requisitos

- Ser estudiante de secundaria, preparatoria, universidad o equivalente.
- Tener algún **comprobante de estudios**, por ejemplo:
  - Credencial escolar con fecha vigente.
  - Historial académico (kardex).
  - Comprobante de inscripción.
  - Carta de la escuela indicando que eres estudiante.
- Tener una cuenta de GitHub personal lista.

#### 2.2.2. Pasos para solicitar el Pack

1. Iniciar sesión en GitHub.
2. Ir a: [https://education.github.com/pack](https://education.github.com/pack)
3. Hacer clic en **Get your Pack** o **Sign up for Student Developer Pack**.
4. Elegir **I’m a student** cuando pregunte tu rol.
5. Completar el formulario:
   - Nombre completo.
   - Nombre de la institución.
   - Nivel de estudios.
   - Explicar brevemente para qué usarás GitHub (por ejemplo: “para aprender programación y trabajar en proyectos escolares”).
6. Elegir el método de verificación:
   - Usar correo institucional (por ejemplo `@universidad.mx`) **o**
   - Subir un documento (credencial, comprobante, etc.) donde se vea tu nombre y tu escuela.
7. Enviar la solicitud.

GitHub revisará la solicitud. El tiempo típico de respuesta es de **1 a 7 días**.  
Cuando te aprueben, recibirás un correo confirmando que ya tienes el **Student Developer Pack**.

> Si rechazan la solicitud, normalmente explican el motivo. Se puede corregir y volver a aplicar.

***

### 2.3. Crear tu primer Codespace

Un **Codespace** es una máquina de desarrollo en la nube con VS Code en el navegador.

#### Opción A: Desde un repositorio en GitHub

1. Inicia sesión en [https://github.com](https://github.com).
2. Entra a cualquier repositorio:
   - Puede ser un repo propio (por ejemplo un proyecto de la clase).
   - O un repo de ejemplo que el profesor comparta.
3. Haz clic en el botón verde **Code**.
4. Ve a la pestaña **Codespaces**.
5. Haz clic en **Create codespace on main** (o en la rama que quieras).
6. Espera 1–2 minutos mientras GitHub crea el entorno.

Se abrirá una pestaña con una interfaz muy parecida a **Visual Studio Code**, pero corriendo en el navegador.

#### Opción B: Desde el panel de Codespaces

1. Ir a: [https://github.com/codespaces](https://github.com/codespaces)
2. Hacer clic en **New codespace**.
3. Elegir un repositorio de tu cuenta.
4. Elegir la rama (por defecto `main`).
5. Hacer clic en **Create codespace**.

***

### 2.4. Usar el entorno de GitHub Codespaces

Dentro del Codespace verás:

- **Explorador de archivos** (panel izquierdo).
- **Editor de código** (panel central).
- **Terminal integrada** (parte inferior).
- **Panel de extensiones** (icono de bloques en la barra lateral izquierda).

Acciones básicas:

1. **Abrir terminal**:
   - Menú: `Terminal → New Terminal`  
   - O usar el que aparece en la parte inferior.
2. **Ejecutar comandos** como si fuera Linux:
   - `ls`, `cd`, `python main.py`, `npm install`, etc.
3. **Instalar extensiones**:
   - Click en el ícono de Extensiones (panel izquierdo).
   - Buscar, por ejemplo: `Python`, `Jupyter`, `ESLint`, etc.
   - Hacer clic en **Install**.
4. **Ejecutar tu programa**:
   - Usar la terminal para lanzar tu script o servidor web.
   - Si tu app usa un puerto (por ejemplo 3000 o 8000), Codespaces detecta el puerto y permite abrir la app en otra pestaña del navegador.
5. **Guardar y hacer commit**:
   - Git ya viene configurado con tu cuenta de GitHub.
   - Puedes usar el panel de Source Control (icono de rama) para hacer commits y push.

***

### 2.5. Administrar tus Codespaces

1. Ir a: [https://github.com/codespaces](https://github.com/codespaces)
2. Verás la lista de tus Codespaces:
   - Estado (Running/Stopped).
   - Última vez que se usaron.
3. Acciones:
   - **Open in browser**: abrir el Codespace.
   - **Stop**: detenerlo (deja de consumir horas).
   - **Delete**: borrarlo para liberar recursos.

> GitHub detiene automáticamente los Codespaces después de un tiempo de inactividad (normalmente 30 minutos).  
> Los estudiantes con el Student Pack tienen una cuota mensual de horas muy razonable para uso académico.

***

## 3. Parte 2 – Ona (antes Gitpod)

**Ona** es el nuevo nombre de Gitpod. Ofrece entornos de desarrollo en la nube con un editor tipo VS Code directamente en el navegador.

***

### 3.1. Crear una cuenta en Ona (Gitpod)

1. Ir a: [https://ona.com](https://ona.com) (antes [https://gitpod.io](https://gitpod.io)).
2. Hacer clic en **Get started** o **Sign up**.
3. Elegir **Sign in with GitHub**.
4. Iniciar sesión con tu cuenta de GitHub.
5. Autorizar a Ona/Gitpod para acceder a tus repositorios de GitHub.
6. Serás redirigido al **panel de Ona/Gitpod**.

No se necesita tarjeta de crédito para empezar con el plan gratuito.

***

### 3.2. Crear tu primer workspace en Ona

Un **workspace** es tu entorno de desarrollo en la nube.

#### Opción A: Desde el panel de Ona

1. En el panel principal, buscar un botón como **New Workspace** o **Create Workspace**.
2. Elegir un repositorio de tu GitHub:
   - Puede ser un repo propio.
   - O un repo de ejemplo que usemos en clase.
3. Elegir la rama (por ejemplo `main`).
4. Hacer clic en **Create Workspace**.
5. Esperar mientras se construye el contenedor (1–5 minutos la primera vez).

#### Opción B: Método rápido desde cualquier enlace de GitHub

Esta es la forma más sencilla para estudiantes:

1. Buscar la URL del repositorio en GitHub, por ejemplo:  
   `https://github.com/sonder-art/ia_p26`
2. Agregar delante `https://gitpod.io/#` (siguen funcionando los enlaces legacy de Gitpod en Ona), por ejemplo:  
   `https://gitpod.io/#https://github.com/sonder-art/ia_p26`
3. Pegar esa URL en el navegador y presionar Enter.
4. Esto abrirá Ona/Gitpod y creará automáticamente un workspace para ese repo.

> Tip: El profesor puede compartir directamente el enlace largo con `gitpod.io/#` para que los estudiantes solo hagan clic.

***

### 3.3. Usar el entorno de Ona/Gitpod

Dentro del workspace verás algo muy parecido a VS Code:

- Explorador de archivos.
- Editor de texto.
- Terminal integrada.
- Panel de extensiones.

Acciones básicas:

1. **Terminal**:
   - Menú `Terminal → New Terminal` o usar la terminal ya abierta.
   - Ejecutar comandos: `python main.py`, `npm run dev`, etc.
2. **Instalar dependencias**:
   - `pip install -r requirements.txt`
   - `npm install`
   - etc.
3. **Previsualizar aplicaciones web**:
   - Si ejecutas un servidor (por ejemplo en el puerto 3000), Ona/Gitpod detecta el puerto.
   - Aparecerá un aviso para abrir la previsualización en el navegador.
4. **Guardar cambios y usar Git**:
   - Puedes hacer commits desde la terminal.
   - También puedes usar el panel de Control de Código Fuente.

***
### 3.4. Personalizar el entorno con `.gitpod.yml` (opcional, para clases más avanzadas)

En el repositorio se puede crear un archivo llamado `.gitpod.yml` para automatizar tareas cuando se abre el workspace.

Ejemplo simple:

```yaml
tasks:
  - init: pip install -r requirements.txt
    command: python main.py

ports:
  - port: 8000
    onOpen: open-preview
```

Esto hace que, cada vez que se inicia el workspace:

- Se instalen las dependencias de Python.
- Se ejecute `python main.py`.
- Se abra automáticamente la previsualización del puerto 8000.

El profesor puede preparar este archivo una vez, y los estudiantes solo dan clic en el enlace de Gitpod/Ona.

***

### 3.5. Administrar workspaces en Ona/Gitpod

1. Ir a: [https://gitpod.io/workspaces](https://gitpod.io/workspaces) o al panel de Ona y buscar **Workspaces**.
2. Verás la lista de workspaces:
   - Nombre.
   - Estado (Running/Stopped).
   - Última vez que se usaron.
3. Acciones típicas:
   - **Start**: arrancar un workspace detenido.
   - **Stop**: detenerlo para no gastar horas.
   - **Delete**: eliminarlo definitivamente.
   - **Pin** (fijar):
     - Sirve para que el workspace no se borre automáticamente después de cierto tiempo.
     - Útil para proyectos de largo plazo (por ejemplo todo el semestre).

> En el plan gratuito, los workspaces se pueden borrar si no se usan por un tiempo. Pueden “pinearse” para evitarlo en proyectos importantes.

***

## 4. Consejos para Profesores

- Crear un repositorio base (plantilla) con el código inicial de cada práctica.
- Incluir un archivo `README.md` con:
  - Objetivos de la práctica.
  - Instrucciones rápidas para abrir en Codespaces.
  - Instrucciones rápidas para abrir en Ona/Gitpod.
- Compartir con los estudiantes:
  - El enlace del repositorio.
  - El enlace directo de Gitpod/Ona usando el prefijo `https://gitpod.io/#...`.
- Pedir a los estudiantes que:
  - Soliciten el **GitHub Student Developer Pack** al inicio del curso.
  - Usen Codespaces como herramienta principal.
  - Usen Ona/Gitpod como herramienta secundaria cuando haya problemas de cuota o rendimiento.

***

## 5. Resumen para Estudiantes (versión ultra corta)

1. **Crear cuenta en GitHub**:  
   - Ir a [github.com](https://github.com), registrarse y confirmar el correo.

2. **Pedir el Student Developer Pack**:  
   - Ir a [education.github.com/pack](https://education.github.com/pack)  
   - Enviar comprobante de estudios.

3. **Usar GitHub Codespaces**:  
   - Abrir un repo en GitHub.  
   - Botón **Code → Codespaces → Create codespace**.  
   - Programar desde el navegador (VS Code online).

4. **Crear cuenta en Ona/Gitpod**:  
   - Ir a [ona.com](https://ona.com), entrar con GitHub.

5. **Usar Ona/Gitpod**:  
   - Entrar a `https://gitpod.io/#https://github.com/sonder-art/ia_p26`  
   - Esperar que se cree el workspace.  
   - Programar desde el navegador (VS Code-like online).

Con esto, los estudiantes pueden programar en Python, JavaScript, etc., desde las laptops de la escuela, **sin instalar absolutamente nada**.
