# Protocolo de "Lazy Programming" y Eficiencia

**MANDATO PRINCIPAL PARA TODOS LOS AGENTES:**
El mejor código es el que no se escribe. Antes de proponer nuevas funciones, tablas o módulos, debes justificar por qué las soluciones existentes no son suficientes.

## La Escalera de la Pereza (The Ladder of Laziness)
Evalúa cada requerimiento técnico pasando por estos peldaños. Solo puedes avanzar al siguiente si el anterior es imposible:

1. **Rechazo / Re-negociación (YAGNI):** ¿Podemos convencer al cliente de no hacer esto porque el sistema actual ya resuelve su problema de fondo, aunque la interfaz sea diferente?
2. **Configuración existente:** ¿Podemos resolver esto cambiando una variable de entorno, un feature flag, o una entrada en la base de datos?
3. **Reutilización de Dominio:** ¿Existe ya una clase, función auxiliar o modelo de datos en `CONTEXT.md` que haga el 80% del trabajo y solo necesite una pequeña modificación?
4. **Biblioteca Estándar o Framework:** ¿El framework que usamos (ej. Django, React, FastAPI) tiene una función nativa para esto? Úsala, no escribas un wrapper.
5. **Nuevo Código Aislado:** Si no hay más remedio, diseña la solución más pequeña y aislada posible.

## Criterios de Rechazo de PRs
Cualquier ticket o PR será rechazado automáticamente si:
- Introduce una nueva dependencia de npm/pip/etc. sin justificación explícita.
- Duplica lógica que ya existe en utilerías.
- Crea tablas de BD para datos que podrían vivir en columnas JSON existentes (si aplica).