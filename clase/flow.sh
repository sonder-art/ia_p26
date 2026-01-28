#!/bin/bash

# ==============================================================================
# Script de Automatización de Flujo de Trabajo - IA P26
# ==============================================================================
# Este script ayuda a gestionar el ciclo de vida de las tareas de la clase.
# Diseñado para ser usado por estudiantes o agentes de IA.
#
# Uso: ./flow.sh [comando] [argumentos]
# ==============================================================================

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables de configuración - Auto-detect from repo.json
REPO_JSON="uu_framework/eleventy/_data/repo.json"

# Try to read from repo.json if it exists
if [ -f "$REPO_JSON" ]; then
    # Extract upstream_url from JSON using grep/sed (no jq dependency)
    UPSTREAM_URL=$(grep '"upstream_url"' "$REPO_JSON" | sed 's/.*"upstream_url": "\([^"]*\)".*/\1/')
fi

# Fallback to git remote if repo.json doesn't exist or is empty
if [ -z "$UPSTREAM_URL" ]; then
    UPSTREAM_URL=$(git config --get remote.origin.url)
fi

# Hard fail if still empty
if [ -z "$UPSTREAM_URL" ]; then
    echo -e "${RED}ERROR: Cannot determine upstream repository${NC}"
    echo "Run: python3 uu_framework/scripts/preprocess.py"
    exit 1
fi

# Función de ayuda
show_help() {
    echo -e "${BLUE}IA P26 - Asistente de Flujo de Git${NC}"
    echo "Uso: ./flow.sh [comando]"
    echo ""
    echo "Comandos disponibles:"
    echo -e "  ${GREEN}setup${NC}      Configura el repositorio inicial (upstream + user folder)"
    echo -e "  ${GREEN}sync${NC}       Sincroniza tu main con el profesor (upstream)"
    echo -e "  ${GREEN}start${NC}      Inicia una nueva tarea (crea rama)"
    echo -e "              Uso: ./flow.sh start tarea-1-intro"
    echo -e "  ${GREEN}save${NC}       Guarda cambios en tu carpeta (commit)"
    echo -e "              Uso: ./flow.sh save \"Mensaje del commit\""
    echo -e "  ${GREEN}upload${NC}     Sube tu rama actual a GitHub (push)"
    echo -e "  ${GREEN}finish${NC}     Limpia y regresa a main después de que te acepten el PR"
    echo ""
}

# 1. SETUP INICIAL
cmd_setup() {
    echo -e "${YELLOW}>>> Iniciando configuración inicial...${NC}"
    
    # Configurar upstream
    if git remote | grep -q "upstream"; then
        echo -e "${GREEN}✓ Upstream ya configurado.${NC}"
    else
        git remote add upstream $UPSTREAM_URL
        echo -e "${GREEN}✓ Upstream configurado exitosamente.${NC}"
    fi

    # Crear carpeta de usuario si no existe
    GITHUB_USER=$(git config user.name)
    # Intenta obtener el usuario del remoto si el local es genérico
    if [ -z "$GITHUB_USER" ]; then
        echo -e "${RED}Error: No tienes configurado git user.name${NC}"
        echo "Ejecuta: git config --global user.name \"tu_usuario_github\""
        exit 1
    fi

    echo -e "${BLUE}Identificado usuario: $GITHUB_USER${NC}"
    USER_FOLDER="estudiantes/$GITHUB_USER"

    if [ ! -d "$USER_FOLDER" ]; then
        echo -e "${YELLOW}Creando carpeta de estudiante: $USER_FOLDER${NC}"
        mkdir -p "$USER_FOLDER"
        touch "$USER_FOLDER/.gitkeep"
        echo -e "${GREEN}✓ Carpeta creada.${NC}"
    else
        echo -e "${GREEN}✓ Tu carpeta de estudiante ya existe.${NC}"
    fi
}

# 2. SINCRONIZACIÓN (SYNC)
cmd_sync() {
    echo -e "${YELLOW}>>> Sincronizando con el profesor (upstream)...${NC}"
    
    # Guardar rama actual
    CURRENT_BRANCH=$(git branch --show-current)
    
    if [ "$CURRENT_BRANCH" != "main" ]; then
        echo -e "${YELLOW}Cambiando a main...${NC}"
        git checkout main
    fi

    echo "Bajando cambios de upstream..."
    git pull upstream main
    
    echo "Subiendo cambios a origin (tu nube)..."
    git push origin main

    echo -e "${GREEN}✓ Sincronización completada. Tu repositorio está al día.${NC}"
}

# 3. INICIAR TAREA (START)
cmd_start() {
    if [ -z "$1" ]; then
        echo -e "${RED}Error: Debes dar un nombre a la tarea.${NC}"
        echo "Uso: ./flow.sh start tarea-1-intro"
        exit 1
    fi

    TASK_NAME=$1
    echo -e "${YELLOW}>>> Iniciando tarea: $TASK_NAME${NC}"

    # Asegurarnos de estar actualizados primero
    cmd_sync

    echo "Creando rama..."
    git checkout -b "$TASK_NAME"
    echo -e "${GREEN}✓ Estás listo para trabajar en la rama '$TASK_NAME'.${NC}"
}

# 4. GUARDAR CAMBIOS (SAVE)
cmd_save() {
    if [ -z "$1" ]; then
        echo -e "${RED}Error: Debes incluir un mensaje para el commit.${NC}"
        echo "Uso: ./flow.sh save \"Terminé el ejercicio 1\""
        exit 1
    fi

    MSG=$1
    echo -e "${YELLOW}>>> Guardando cambios...${NC}"

    # Verificación de seguridad: ¿Estamos en nuestra carpeta?
    # Esto es básico, se podría hacer más robusto
    GITHUB_USER=$(git config user.name)
    
    # Intentar agregar cambios de forma inteligente
    # Primero vemos si hay cambios
    if [ -z "$(git status --porcelain)" ]; then
        echo -e "${GREEN}No hay cambios pendientes.${NC}"
        exit 0
    fi

    git add .
    git commit -m "$MSG"
    
    echo -e "${GREEN}✓ Cambios guardados localmente.${NC}"
}

# 5. SUBIR CAMBIOS (UPLOAD)
cmd_upload() {
    CURRENT_BRANCH=$(git branch --show-current)
    
    if [ "$CURRENT_BRANCH" == "main" ]; then
        echo -e "${RED}Error: No deberías hacer push directo desde main para tareas.${NC}"
        echo "Usa 'start' para crear una rama primero."
        exit 1
    fi

    echo -e "${YELLOW}>>> Subiendo rama $CURRENT_BRANCH a GitHub...${NC}"
    git push origin "$CURRENT_BRANCH"
    
    echo -e "${GREEN}✓ Rama subida.${NC}"
    echo -e "${BLUE}Ahora ve a GitHub y crea el Pull Request:${NC}"

    # Try to read PR URL from repo.json
    if [ -f "$REPO_JSON" ]; then
        PR_URL=$(grep '"pr_compare_url"' "$REPO_JSON" | sed 's/.*"pr_compare_url": "\([^"]*\)".*/\1/')
    fi

    # Hard fail if empty
    if [ -z "$PR_URL" ]; then
        echo -e "${RED}ERROR: Cannot determine PR URL. Run preprocessing first.${NC}"
        exit 1
    fi

    echo "$PR_URL"
}

# 6. TERMINAR (FINISH)
cmd_finish() {
    echo -e "${YELLOW}>>> Limpiando entorno...${NC}"
    
    CURRENT_BRANCH=$(git branch --show-current)
    
    if [ "$CURRENT_BRANCH" == "main" ]; then
        echo "Ya estás en main."
    else
        git checkout main
    fi

    cmd_sync
    
    if [ "$CURRENT_BRANCH" != "main" ]; then
        read -p "¿Quieres borrar la rama local '$CURRENT_BRANCH'? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git branch -d "$CURRENT_BRANCH"
            echo -e "${GREEN}✓ Rama borrada.${NC}"
        fi
    fi
}

# 7. COPIAR ARCHIVOS (COPY)
cmd_copy() {
    if [ -z "$1" ] || [ -z "$2" ]; then
        echo -e "${RED}Error: Faltan argumentos.${NC}"
        echo "Uso: ./flow.sh copy [origen] [destino]"
        exit 1
    fi

    ORIGEN=$1
    DESTINO=$2

    echo -e "${YELLOW}>>> Copiando archivos...${NC}"
    
    if [ ! -e "$ORIGEN" ]; then
        echo -e "${RED}Error: El archivo de origen '$ORIGEN' no existe.${NC}"
        exit 1
    fi

    # Verificar si el destino ya existe
    if [ -e "$DESTINO" ]; then
        echo -e "${RED}¡ALERTA! El destino '$DESTINO' ya existe.${NC}"
        echo -e "${RED}Para proteger tu trabajo, NO se sobrescribirá automáticamente.${NC}"
        echo -e "${YELLOW}Si deseas actualizarlo, por favor hazlo manualmente o renombra tu archivo existente.${NC}"
        exit 1
    fi

    # Crear directorio padre si no existe
    mkdir -p "$(dirname "$DESTINO")"
    
    cp -r "$ORIGEN" "$DESTINO"
    echo -e "${GREEN}✓ Archivo copiado exitosamente a: $DESTINO${NC}"
}

# Router de comandos
case "$1" in
    setup)
        cmd_setup
        ;;
    sync)
        cmd_sync
        ;;
    start)
        cmd_start "$2"
        ;;
    save)
        cmd_save "$2"
        ;;
    upload)
        cmd_upload
        ;;
    finish)
        cmd_finish
        ;;
    copy)
        cmd_copy "$2" "$3"
        ;;
    *)
        show_help
        ;;
esac

