# Cheatsheet: Comandos Básicos de Git, GitHub y Terminal

> **📚 Guía para principiantes** - Una referencia rápida de los comandos más importantes

## 🖥️ Comandos Básicos de Terminal

### Navegación y Ubicación
```bash
# Mostrar la ruta actual donde estás
pwd

# Listar archivos y carpetas en el directorio actual
ls

# Listar archivos con detalles (permisos, tamaño, fecha)
ls -la

# Cambiar de directorio
cd [nombre_carpeta]

# Ir al directorio padre (subir un nivel)
cd ..

# Ir al directorio home del usuario
cd ~

# Ir al directorio raíz
cd /
```

### Manipulación de Archivos y Carpetas
```bash
# Crear una carpeta nueva
mkdir [nombre_carpeta]

# Crear un archivo vacío
touch [nombre_archivo]

# Copiar archivo
cp [archivo_origen] [archivo_destino]

# Mover o renombrar archivo
mv [archivo_origen] [archivo_destino]

# Eliminar archivo
rm [nombre_archivo]

# Eliminar carpeta y su contenido
rm -rf [nombre_carpeta]

# Ver contenido de un archivo
cat [nombre_archivo]
```

### Comandos Útiles
```bash
# Limpiar la terminal
clear

# Ver historial de comandos
history

# Buscar en el historial (Ctrl+R)
# Cancelar comando actual (Ctrl+C)
# Salir de un programa (Ctrl+Z o q)
```

---

## 🔧 Configuración Inicial de Git

### Configurar tu Identidad (Solo una vez)
```bash
# Configurar tu nombre
git config --global user.name "Tu Nombre"

# Configurar tu email
git config --global user.email "tu.email@ejemplo.com"

# Ver tu configuración actual
git config --list
```

---

## 📁 Comandos Básicos de Git

### Inicializar y Clonar Repositorios

```bash
# Inicializar un nuevo repositorio Git en la carpeta actual
git init

# Clonar un repositorio existente desde GitHub
git clone [URL_del_repositorio]

# Ejemplo:
git clone https://github.com/usuario/mi-proyecto.git
```

### Verificar Estado y Cambios

```bash
# Ver el estado actual del repositorio
git status

# Ver qué archivos han cambiado
git diff

# Ver el historial de commits
git log

# Ver historial de commits en una línea
git log --oneline

# Ver las ramas disponibles
git branch
```

### Trabajar con Archivos

```bash
# Añadir un archivo específico al staging area
git add [nombre_archivo]

# Añadir todos los archivos modificados
git add .

# Añadir todos los archivos con extensión específica
git add *.txt

# Quitar archivo del staging area (antes del commit)
git reset [nombre_archivo]

# Ver qué archivos están en staging
git status
```

### Hacer Commits

```bash
# Hacer commit con mensaje
git commit -m "Descripción de los cambios"

# Hacer commit añadiendo todos los archivos modificados
git commit -am "Mensaje del commit"

# Modificar el último commit (antes de hacer push)
git commit --amend -m "Nuevo mensaje"
```

---

## 🌿 Trabajar con Ramas (Branches)

### Crear y Cambiar Ramas

```bash
# Ver todas las ramas
git branch

# Crear una nueva rama
git branch [nombre_rama]

# Cambiar a una rama existente
git checkout [nombre_rama]

# Crear y cambiar a una nueva rama en un solo comando
git checkout -b [nombre_rama]

# Cambiar a la rama main/master
git checkout main
```

### Fusionar Ramas

```bash
# Fusionar una rama con la rama actual
git merge [nombre_rama]

# Eliminar una rama (después de fusionar)
git branch -d [nombre_rama]

# Forzar eliminación de rama
git branch -D [nombre_rama]
```

---

## ☁️ Comandos para GitHub (Repositorios Remotos)

### Conectar con Repositorios Remotos

```bash
# Ver repositorios remotos configurados
git remote -v

# Añadir un repositorio remoto
git remote add origin [URL_del_repositorio]

# Añadir repositorio upstream (para forks)
git remote add upstream [URL_del_repositorio_original]

# Cambiar URL del repositorio remoto
git remote set-url origin [nueva_URL]
```

### Subir y Descargar Cambios

```bash
# Subir cambios al repositorio remoto
git push origin [nombre_rama]

# Subir por primera vez una rama nueva
git push -u origin [nombre_rama]

# Descargar cambios del repositorio remoto
git pull origin [nombre_rama]

# Traer cambios sin fusionar automáticamente
git fetch origin

# Traer cambios del repositorio upstream
git fetch upstream
git pull upstream main
```

---

## 🔄 Flujo de Trabajo Típico

### Flujo Básico Diario
```bash
# 1. Verificar en qué rama estás
git status

# 2. Actualizar tu rama con los últimos cambios
git pull origin main

# 3. Crear una nueva rama para tu trabajo
git checkout -b mi-nueva-funcionalidad

# 4. Hacer cambios en tus archivos...

# 5. Ver qué archivos cambiaron
git status

# 6. Añadir archivos al staging
git add .

# 7. Hacer commit
git commit -m "Añadir nueva funcionalidad"

# 8. Subir tu rama a GitHub
git push origin mi-nueva-funcionalidad
```

### Sincronizar con Repositorio Original (Fork)
```bash
# 1. Traer cambios del repositorio original
git fetch upstream

# 2. Cambiar a tu rama main
git checkout main

# 3. Fusionar cambios del upstream
git merge upstream/main

# 4. Subir los cambios a tu fork
git push origin main
```

---

## 🚨 Comandos de Emergencia

### Deshacer Cambios

```bash
# Deshacer cambios en un archivo (antes de add)
git checkout -- [nombre_archivo]

# Deshacer todos los cambios no guardados
git checkout -- .

# Deshacer el último commit (mantener cambios)
git reset --soft HEAD~1

# Deshacer el último commit (eliminar cambios)
git reset --hard HEAD~1

# Volver a un commit específico
git reset --hard [hash_del_commit]
```

### Resolver Problemas Comunes

```bash
# Si olvidaste hacer pull antes de push
git pull origin main
# Resuelve conflictos si los hay, luego:
git push origin main

# Si necesitas forzar un push (¡cuidado!)
git push --force-with-lease origin [rama]

# Ver diferencias entre ramas
git diff main..mi-rama

# Guardar cambios temporalmente
git stash

# Recuperar cambios guardados
git stash pop
```

---

## 📋 Comandos Útiles para Archivos Especiales

### Trabajar con .gitignore

```bash
# Crear archivo .gitignore
touch .gitignore

# Ejemplo de contenido para .gitignore:
# *.log
# node_modules/
# .DS_Store
# .env

# Aplicar .gitignore a archivos ya trackeados
git rm --cached [nombre_archivo]
git commit -m "Remover archivo del tracking"
```

### Crear archivo .gitkeep para carpetas vacías

```bash
# Git no trackea carpetas vacías, usa .gitkeep
mkdir mi-carpeta-vacia
touch mi-carpeta-vacia/.gitkeep
git add mi-carpeta-vacia/.gitkeep
```

---

## 🎯 Tips y Buenas Prácticas

### Mensajes de Commit
```bash
# ✅ Buenos mensajes
git commit -m "Añadir función de login"
git commit -m "Corregir bug en el formulario de contacto"
git commit -m "Actualizar documentación del API"

# ❌ Malos mensajes
git commit -m "cambios"
git commit -m "fix"
git commit -m "asdf"
```

### Nombres de Ramas
```bash
# ✅ Buenos nombres
git checkout -b feature/login-usuario
git checkout -b bugfix/corregir-formulario
git checkout -b hotfix/error-critico

# ❌ Malos nombres
git checkout -b rama1
git checkout -b test
git checkout -b asdf
```

---

## 🆘 Comandos de Ayuda

```bash
# Ayuda general de Git
git help

# Ayuda específica de un comando
git help [comando]
# Ejemplo: git help commit

# Versión de Git instalada
git --version

# Ver configuración actual
git config --list
```

---

## 🔗 Atajos de Teclado Útiles en Terminal

| Atajo | Función |
|-------|---------|
| `Ctrl + C` | Cancelar comando actual |
| `Ctrl + Z` | Suspender proceso |
| `Ctrl + R` | Buscar en historial |
| `Ctrl + L` | Limpiar pantalla |
| `Tab` | Autocompletar |
| `↑ ↓` | Navegar historial |

---

## 📚 Recursos Adicionales

- **GitHub Desktop**: Interfaz gráfica para Git
- **GitKraken**: Cliente Git visual
- **VS Code**: Editor con integración Git
- **GitHub CLI**: `gh` para comandos de GitHub desde terminal

> **💡 Consejo**: Practica estos comandos en un repositorio de prueba antes de usarlos en proyectos importantes. ¡La práctica hace al maestro!
