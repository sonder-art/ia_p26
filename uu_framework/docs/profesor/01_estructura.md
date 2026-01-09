# Estructura de Directorios

Convención de nombres para archivos y carpetas.

## Prefijos Numéricos

Los archivos y carpetas se ordenan por su prefijo:

| Prefijo | Significado | Ejemplo |
|---------|-------------|---------|
| `00_` | Índice del directorio | `00_index.md` |
| `01_`, `02_` | Capítulos/secciones ordenadas | `01_introduccion/` |
| `a_`, `b_` | Apéndices (van al final) | `a_stack/` |
| `??_` | Trabajo en progreso (oculto) | `??_borrador/` |

## Estructura Recomendada

```
clase/
├── 00_index.md              # Página principal
├── 01_tema/                 # Capítulo 1
│   ├── 00_index.md          # Índice del capítulo
│   ├── 01_subtema.md        # Sección 1.1
│   └── 02_subtema.md        # Sección 1.2
├── 02_tema/                 # Capítulo 2
│   └── ...
├── a_stack/                 # Apéndice A
│   ├── 00_index.md
│   └── 01_setup.md
└── b_libros/                # Apéndice B (no renderizado)
```

## Reglas Importantes

### 1. Siempre incluir `00_index.md`

Cada directorio debe tener un archivo `00_index.md` para aparecer en la navegación.

### 2. Usar números de dos dígitos

```
01_tema/     ✓ Correcto
1_tema/      ✗ Incorrecto
tema/        ✗ Sin orden
```

### 3. Nombres en minúsculas con guiones bajos

```
01_mi_tema.md     ✓ Correcto
01_MiTema.md      ✗ Mayúsculas
01-mi-tema.md     ✗ Guiones
```

### 4. Sin espacios ni caracteres especiales

```
01_introduccion.md           ✓ Correcto
01_introducción.md           ✗ Acentos
01_mi archivo.md             ✗ Espacios
```

## Numeración Jerárquica

La navegación muestra números automáticos:

```
clase/
├── 01_intro/           → 1 Introducción
│   ├── 01_conceptos.md → 1.1 Conceptos
│   └── 02_practica.md  → 1.2 Práctica
├── 02_avanzado/        → 2 Avanzado
└── a_stack/            → A Stack
    └── 01_setup.md     → A.1 Setup
```

## Carpetas Especiales

### `b_libros/`

PDFs y referencias. **No se renderizan** como páginas web.

### `??_borrador/`

Contenido en desarrollo. **Oculto** de la navegación.

### `code/`

Archivos Python dentro de un módulo. Mostrados en sidebar con sintaxis.

## Ejemplos

### Nuevo Módulo

```bash
mkdir clase/03_nuevo_modulo
touch clase/03_nuevo_modulo/00_index.md
touch clase/03_nuevo_modulo/01_primera_leccion.md
```

### Nueva Sección

```bash
touch clase/01_intro/03_nueva_seccion.md
```

### Nuevo Apéndice

```bash
mkdir clase/c_referencias
touch clase/c_referencias/00_index.md
```
