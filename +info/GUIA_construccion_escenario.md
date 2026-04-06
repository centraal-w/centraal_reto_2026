# Guía breve para construir el escenario

## Propósito

Esta guía resume los pasos que conviene considerar para construir la solución sin detallar cada implementación. La intención es orientar el trabajo técnico sin resolverlo por completo.

---

## 1. Entender el flujo completo

Antes de escribir código, conviene tener claro el recorrido de los datos:

1. Un cliente envía una lectura de sensor.
2. La API recibe y valida el evento.
3. El evento se guarda en storage.
4. Otra API consulta el histórico reciente.
5. Se calcula una probabilidad de fallo.
6. Se devuelve el resultado en JSON.

**Hint:** si el flujo está claro desde el inicio, el código suele ordenarse mejor en capas simples: API, validación, storage y lógica de predicción.

---

## 2. Definir el contrato de entrada

El evento mínimo debería responder estas preguntas:

- ¿De qué máquina viene?
- ¿Qué variable reporta?
- ¿Qué valor trae?
- ¿En qué momento fue medida?

Ejemplo esperado:

```json
{
  "machine_id": "PUMP-1001",
  "timestamp": "2026-04-06T10:15:00Z",
  "variable": "temperature_c",
  "value": 78.4
}
```

**Hint:** es mejor mantener el contrato pequeño y estable. Si el contrato es claro, el resto del sistema se simplifica.

---

## 3. Diseñar cómo se guardan los datos

La persistencia puede resolverse como eventos append-only en archivos NDJSON.

Estructura sugerida:

```text
raw/
  machine_id=PUMP-1001/
    year=2026/
      month=04/
        day=06/
          events.ndjson
```

Cada línea del archivo representa un evento.

**Hints:**
- Piensa en eventos históricos, no en “estado actual”.
- Una estructura por máquina y fecha facilita luego la lectura.
- No hace falta una base de datos para resolver este escenario.

---

## 4. Separar la lógica de ingesta de la lógica de predicción

Aunque ambas sean Functions HTTP, conviene tratarlas como responsabilidades distintas:

- **Ingesta:** recibe, valida y guarda.
- **Predicción:** lee, agrega, calcula y responde.

**Hint:** si una función hace demasiadas cosas, después cuesta probarla y mantenerla.

---

## 5. Decidir qué variables afectan el riesgo

Se espera trabajar con variables plausibles para mantenimiento predictivo, por ejemplo:

- `vibration_mm_s`
- `temperature_c`
- `current_a`
- `pressure_bar`
- `load_pct`

También conviene definir umbrales nominales o rangos esperados por máquina.

**Hint:** no necesitas un modelo entrenado; necesitas una lógica que tenga sentido técnico.

---

## 6. Construir un scoring simple y explicable

Una estrategia válida es:

1. leer las últimas 24 horas,
2. calcular algunos features simples,
3. comparar contra umbrales,
4. construir un score ponderado,
5. aplicar una sigmoide.

Idea general:

```text
failure_probability_24h = sigmoid(weighted_score)
```

**Hints:**
- “Último valor”, “promedio” y “máximo” suelen ser suficientes.
- Es útil devolver también factores de riesgo, no solo el número final.
- Si la probabilidad cambia de forma razonable al cambiar los datos, vas bien.

---

## 7. Resolver primero un caso pequeño

Antes de pensar en “todas las máquinas”, conviene resolver:

- una sola máquina,
- un solo día,
- pocos eventos,
- una predicción coherente.

Luego se generaliza.

**Hint:** primero haz que funcione un camino feliz pequeño; luego amplía.

---

## 8. Verificar localmente con emuladores

La solución local se apoya en Azure Functions Core Tools y Azurite. Microsoft indica que el desarrollo local de Functions depende de Core Tools, y Azurite ofrece un entorno local para probar aplicaciones de Azure Storage. citeturn402828search0turn402828search1

**Hints prácticos:**
- Si la Function arranca pero no escribe, revisa la conexión a storage.
- Si el storage existe pero no ves archivos, revisa el path que estás construyendo.
- Si quieres inspeccionar blobs con facilidad, Storage Explorer puede conectarse al emulador Azurite. citeturn402828search4turn402828search7

---

## 9. Probar con datos intencionales

No uses solo datos “bonitos”. Conviene probar:

- valores normales,
- valores altos,
- datos faltantes,
- timestamps fuera de orden,
- máquinas inexistentes.

**Hint:** muchas decisiones de diseño aparecen recién cuando pruebas datos imperfectos.

---

## 10. Mantener el código simple

Una estructura mínima razonable sería:

```text
src/
  ingestion.py
  prediction.py
  storage.py
  validation.py
  models.py
```

**Hint:** si un archivo empieza a mezclar HTTP, parseo, acceso a blob y scoring, probablemente convenga separar.

---

## Documentación relevante

- Desarrollo local de Azure Functions: https://learn.microsoft.com/en-us/azure/azure-functions/functions-develop-local citeturn402828search0
- Azure Functions Core Tools / ejecución local: https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local citeturn402828search8
- Referencia de Azure Functions para Python: https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python citeturn402828search2
- Uso de Azurite: https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azurite citeturn402828search1
- Instalación de Azurite: https://learn.microsoft.com/en-us/azure/storage/common/storage-install-azurite citeturn402828search9
- Conexión a Azurite con SDKs y herramientas: https://learn.microsoft.com/en-us/azure/storage/common/storage-connect-azurite citeturn402828search7
- Connection strings de Azure Storage: https://learn.microsoft.com/en-us/azure/storage/common/storage-configure-connection-string citeturn402828search14
- Storage Explorer con emuladores: https://learn.microsoft.com/en-us/azure/storage/common/storage-explorer-emulators citeturn402828search4

---

## Cierre

El objetivo no es construir una plataforma enorme, sino una solución pequeña pero bien pensada:

- contrato claro,
- almacenamiento coherente,
- separación de responsabilidades,
- predicción explicable,
- pruebas suficientes para demostrar que el flujo funciona.

**Hint final:** si dudas entre una solución “más compleja” y una “más clara”, casi siempre conviene la más clara.
