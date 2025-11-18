# Enjambre de agentes Codex

Enjambre de agentes Codex es un framework ligero que conecta el plugin OpenAI Codex con cualquier IDE donde esté instalado. Trata la sesión del IDE como un espacio de trabajo multiagente cooperativo, lo que te permite orquestar agentes especializados que colaboran en tareas que abarcan desde el desarrollo de software hasta la documentación, la planificación o la investigación.

## Cómo funciona

1. **Contrato centrado en el Orquestador.** `AGENTS.md` define únicamente las reglas globales, el estado compartido y el agente ORCHESTRATOR. El orquestador interpreta la meta de la persona usuaria, redacta un plan, solicita aprobación y delega el trabajo al resto de agentes.
2. **Registro externo de agentes.** Cada agente que no es el orquestador vive en `.AGENTS/<ID>.json`. Cuando el IDE carga este repositorio, importa dinámicamente cada documento JSON y registra el ID del agente, su rol, permisos y flujo de trabajo.
3. **Estado compartido de tareas.** Los planes legibles para humanos viven en `PLAN.md`, mientras que el progreso legible por máquinas se mantiene en `.AGENTS/TASKS.json`. Esta separación permite que los agentes compartan el estado de forma confiable sin importar el IDE en el que se ejecuten.
4. **Operación agnóstica al plugin.** Como las instrucciones son Markdown y JSON, cualquier IDE que admita el plugin Codex puede ejecutar los mismos flujos sin configuración adicional.

## Estructura del repositorio

```
.
├── AGENTS.md
├── LICENSE
├── PLAN.md
├── README.md
└── .AGENTS/
    ├── PLANNER.json
    ├── CODER.json
    ├── REVIEWER.json
    ├── DOCS.json
    ├── CREATOR.json
    └── TASKS.json
```

| Ruta | Propósito |
| --- | --- |
| `AGENTS.md` | Reglas globales, flujo de trabajo de commits y la especificación de ORCHESTRATOR (más la plantilla JSON para nuevos agentes). |
| `.AGENTS/PLANNER.json` | Define cómo se añaden o actualizan las tareas en `PLAN.md` y `.AGENTS/TASKS.json`. |
| `.AGENTS/CODER.json` | Especialista en implementación responsable de los cambios de código o configuración asociados a IDs de tareas. |
| `.AGENTS/REVIEWER.json` | Realiza revisiones, verifica el trabajo y cambia el estado de las tareas según corresponda. |
| `.AGENTS/DOCS.json` | Mantiene README y otros documentos sincronizados con el trabajo recién completado. |
| `.AGENTS/CREATOR.json` | Fábrica de agentes bajo demanda que escribe nuevos JSON además de actualizar el registro. |
| `.AGENTS/TASKS.json` | Espejo legible por máquinas del backlog; se considera la fuente canónica cuando hay discrepancias. |
| `PLAN.md` | Backlog legible para humanos que se comparte dentro de la conversación (secciones Backlog / Done). |
| `README.md` | Resumen de alto nivel y material de incorporación para el repositorio. |
| `LICENSE` | Licencia MIT del proyecto. |

## Ciclo de vida del agente

1. **Planificación.** El ORCHESTRATOR lee `AGENTS.md`, carga `.AGENTS/*.json` y crea un plan que asigna cada paso a un agente registrado (p.ej. PLANNER, CODER, REVIEWER, DOCS).
2. **Aprobación.** La persona usuaria puede aprobar, editar o cancelar el plan antes de que comience el trabajo.
3. **Ejecución.** El orquestador cambia `agent_mode` según el plan, permitiendo que cada agente siga dentro del IDE el flujo descrito en su JSON.
4. **Seguimiento del progreso.** Los agentes actualizan `PLAN.md` y `.AGENTS/TASKS.json` dentro de sus permisos para que tanto personas como herramientas vean el estado actual.

Esta estructura permite encadenar flujos arbitrarios, como implementación de código, actualizaciones de documentación, resúmenes de investigación o triage de tareas, todo en la misma sesión del IDE.

## Flujo de trabajo de commits

- El espacio de trabajo siempre es un repositorio git, así que cada cambio significativo debe llegar al control de versiones.
- Cada tarea atómica listada en `PLAN.md` se mapea a un único commit con un mensaje conciso y legible (idealmente mencionando el ID de la tarea).
- El agente que realiza el trabajo prepara y hace commit antes de devolver el control al orquestador, y el orquestador pausa el plan hasta que ese commit exista.
- Los resúmenes de cada paso mencionan el nuevo hash del commit y confirman que el árbol de trabajo está limpio para que las auditorías sean directas.
- Si un paso del plan no produce cambios en archivos, hay que indicarlo explícitamente; de lo contrario, el enjambre no puede continuar sin un commit.

## Detalles del estado compartido

- **`PLAN.md`**: checklist en Markdown pensada para humanos. Enumera las tareas con IDs, secciones (Backlog, In Progress, Done) y casillas de estado. Los agentes la leen completa antes de modificarla, y cada entrada completada recibe inmediatamente una línea con `Review:` que resuma en una o dos frases qué cambió y por qué.
- **`.AGENTS/TASKS.json`**: espejo para máquinas con un esquema JSON estricto que permite a los agentes analizar, filtrar y actualizar el estado de forma determinista. Cuando hay discrepancias, `.AGENTS/TASKS.json` es canónico y `PLAN.md` debe reconciliarse.

## Cómo agregar un nuevo agente

1. Duplicar la plantilla definida en `AGENTS.md` en la sección “JSON Template for New Agents”.
2. Guardar el archivo como `.AGENTS/<AGENT_ID>.json`, usando el ID en mayúsculas (por ejemplo, `RESEARCHER.json`).
3. Rellenar `role`, `description`, `inputs`, `outputs`, `permissions` y la lista ordenada `workflow`, que describe exactamente cómo debe comportarse el agente.
4. Hacer commit del archivo; en la siguiente ejecución el orquestador lo cargará de forma automática y lo registrará.

Como cada agente es puro JSON, puedes ampliar el enjambre con especialistas en QA, marketing, redacción técnica, procesamiento de datos o cualquier otro proceso que quieras automatizar dentro del IDE.

## Más allá del desarrollo

Aunque el Enjambre de agentes Codex se siente cómodo implementando código, nada limita a los agentes a tareas de desarrollo. Definiendo flujos en JSON puedes crear:

- Agentes de investigación que resuman documentación antes de iniciar el código.
- Revisores de cumplimiento que inspeccionen los commits en busca de violaciones de políticas.
- Runbooks operativos que coordinen despliegues o respuestas a incidentes.
- Bots de documentación que mantengan changelogs y READMEs sincronizados.

Si el plugin OpenAI Codex puede acceder al repositorio desde tu IDE, también puede orquestar a estos agentes con el mismo framework.
