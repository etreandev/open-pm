# Proyecto: OpenPM (Tech Lead & Project Management Suite)

## Contexto para el Agente (Tú)
Tu objetivo es ayudarme a construir una suite de herramientas de CLI/Python local para gestionar proyectos de software. No eres un agente generador de código final; en este proyecto, actuarás como el ingeniero de herramientas internas construyendo mi suite de "Tech Lead".

Esta suite está inspirada en "OpenExec" (gobernanza y flujos de trabajo estrictos) y "Ponytail" (Lazy Programming, máxima reutilización de código).

## Arquitectura del Sistema
Debes construir un orquestador (puede ser un script de Python usando LangChain, AutoGen, o simplemente llamadas directas a la API de OpenAI/Anthropic) que ejecute secuencialmente los siguientes roles:

1. **Ingesta de Requerimientos:** Toma un `.txt` con lo que pide el cliente.
2. **Filtro de "Pereza" (Ponytail):** Evalúa el requerimiento contra el mapa del repositorio (`CONTEXT.md`) para ver si se puede resolver con configuraciones, código existente o si requiere código nuevo.
3. **Especificación (Gatekeeper):** Genera un documento Markdown estricto definiendo qué se va a hacer y qué NO se va a hacer.
4. **Desglose Atómico (Task Planner):** Divide la especificación en tickets que un desarrollador (o agente programador) pueda resolver en menos de 2 horas.

## Tareas inmediatas
1. Lee los archivos adjuntos en esta carpeta (`laziness_protocol.md`, `spec_template.md`, `roles.md`).
2. Propón la estructura de carpetas en Python para construir este orquestador.
3. Espera mi aprobación antes de empezar a programar la lógica de la CLI.