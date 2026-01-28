/**
 * Task Pages Data
 *
 * Defines the auto-generated task list pages (tareas, examenes, proyectos).
 * Uses Eleventy pagination to generate one page per task type.
 */

module.exports = [
  {
    slug: 'tareas',
    title: 'Lista de Tareas',
    taskType: 'homework',
    emptyTitle: 'No hay tareas registradas',
    emptyMessage: 'Las tareas aparecerán aquí automáticamente cuando se definan en el contenido del curso usando marcadores `:::homework{...}`.',
    description: 'Todas las tareas del curso ordenadas por fecha de entrega.'
  },
  {
    slug: 'examenes',
    title: 'Exámenes',
    taskType: 'exams',
    emptyTitle: 'No hay exámenes programados',
    emptyMessage: 'Los exámenes aparecerán aquí automáticamente cuando se definan en el contenido del curso usando marcadores `:::exam{...}`.',
    description: 'Información sobre exámenes parciales y finales del curso.'
  },
  {
    slug: 'proyectos',
    title: 'Proyectos',
    taskType: 'projects',
    emptyTitle: 'No hay proyectos registrados',
    emptyMessage: 'Los proyectos aparecerán aquí automáticamente cuando se definan en el contenido del curso usando marcadores `:::project{...}`.',
    description: 'Proyectos del curso con fechas de entrega y especificaciones.'
  }
];
