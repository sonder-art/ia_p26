# Funcionalidades de IA en Cursor

Cursor no es solo un editor con un chat pegado al lado. La IA está integrada en el núcleo de la edición. Aquí están las 3 funciones principales que debes dominar.

## 1. Chat (`Cmd + L` / `Ctrl + L`)

Es como tener a ChatGPT dentro de tu editor, pero con esteroides.
*   **Contexto:** Puedes decirle "Explícame qué hace este archivo" y Cursor leerá tu archivo.
*   **Referencia Símbolos:** Usa `@` para mencionar archivos, funciones o carpetas específicas.
    *   Ejemplo: *"¿Cómo se relaciona @main.py con @utils.py?"*
*   **Codebase:** Usa `@Codebase` para que busque en todo tu proyecto.

## 2. Composer o Plan Mode (`Cmd + I` / `Ctrl + I`)

Esta es la funcionalidad "estrella". A diferencia del Chat (que solo te da código para copiar y pegar), **Composer puede editar múltiples archivos a la vez**.

*   **¿Qué es?** Es un agente que puede planificar y ejecutar cambios complejos.
*   **Uso:** Presiona `Ctrl + I` (o `Cmd + I` en Mac). Se abrirá una ventana flotante pequeña.
*   **Ejemplo de Prompt:** *"Crea un nuevo componente de React llamado 'Boton.tsx' y agrégalo a la página principal 'App.tsx' con estilos modernos."*
    *   Composer creará el archivo `Boton.tsx`.
    *   Editará `App.tsx` para importar el botón.
    *   Todo esto **automáticamente**. Tú solo tienes que revisar y darle a "Accept".

> **Nota:** En versiones recientes de Cursor, esto se conoce como "Composer". A veces la comunidad lo llama "Plan Mode" porque puede razonar sobre pasos complejos antes de escribir.

## 3. Tab Autocomplete (`Tab`)

Mientras escribes, Cursor intentará adivinar qué vas a escribir a continuación.
*   Es mucho más potente que el autocompletado normal. Puede predecir bloques enteros de código basándose en lo que hiciste en otros archivos recientes.
*   Si te gusta la sugerencia, presiona `Tab`. Si no, sigue escribiendo.

