# PRE-ENTREGA 1

Cliente unificado, asíncrono y robusto para interactuar con diferentes proveedores de Large Language Models (LLMs) utilizando una interfaz común.

El proyecto implementa una arquitectura que permite utilizar **OpenAI** y **Anthropic** de forma intercambiable, utilizando `async/await`, streaming de respuestas, validación con Pydantic y manejo controlado de errores.

---

## Características

* ✅ Interfaz común para diferentes proveedores de LLM.
* ✅ Soporte para OpenAI.
* ✅ Soporte para Anthropic.
* ✅ Operaciones completamente asíncronas.
* ✅ Streaming de respuestas mediante `AsyncIterator`.
* ✅ Validación de mensajes y configuración mediante Pydantic.
* ✅ Configuración mediante variables de entorno.
* ✅ Manejo controlado de errores de autenticación.
* ✅ Manejo controlado de errores de conexión.
* ✅ Manejo de errores de rate limit y quota.
* ✅ Selección de proveedor mediante un manager.
* ✅ Tests automatizados con `pytest` y `pytest-asyncio`.
* ✅ Compatible con Python 3.12+.

---

## Arquitectura

El proyecto utiliza una abstracción común para desacoplar la aplicación de los proveedores concretos.

```text
                    ┌─────────────────────┐
                    │   AsyncLLMManager   │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   BaseLLMClient     │
                    │     (Interface)      │
                    └───────┬───────┬──────┘
                            │       │
                 ┌──────────▼──┐ ┌──▼─────────────┐
                 │ OpenAIClient │ │ AnthropicClient│
                 └─────────────┘ └────────────────┘
```

La aplicación trabaja contra `BaseLLMClient`, por lo que la lógica de alto nivel no necesita conocer los detalles específicos de cada proveedor.

---

## Estructura del proyecto

```text
unified-async-llm-client/

│
├── app/
│   ├── __init__.py
│   ├── schemas.py
│   ├── exceptions.py
│   ├── base.py
│   ├── openai_client.py
│   ├── anthropic_client.py
│   └── manager.py
│
├── tests/
│   ├── test_schemas.py
│   ├── test_manager.py
│   └── test_async_clients.py
│
├── main.py
├── test_stream.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### Responsabilidad de cada módulo

| Archivo               | Responsabilidad                                            |
| --------------------- | ---------------------------------------------------------- |
| `schemas.py`          | Modelos Pydantic para mensajes, configuración y respuestas |
| `exceptions.py`       | Excepciones propias del cliente                            |
| `base.py`             | Interfaz abstracta común para los proveedores              |
| `openai_client.py`    | Implementación asíncrona para OpenAI                       |
| `anthropic_client.py` | Implementación asíncrona para Anthropic                    |
| `manager.py`          | Selección y utilización del proveedor                      |
| `main.py`             | Ejemplo de utilización del cliente                         |
| `test_stream.py`      | Ejemplo de streaming local sin utilizar una API real       |
| `tests/`              | Tests automatizados                                        |

---

## Requisitos

* Python 3.12+
* Una API key de OpenAI y/o Anthropic.

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>

cd unified-async-llm-client
```

### 2. Crear el entorno virtual

Windows PowerShell:

```powershell
python -m venv .venv
```

Activar el entorno:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

---

## Configuración

Crear un archivo `.env` en la raíz del proyecto.

Se puede utilizar `.env.example` como referencia:

```env
LLM_PROVIDER=openai

OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key

OPENAI_MODEL=gpt-4o-mini
ANTHROPIC_MODEL=claude-3-5-sonnet-latest

LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=100
```

### Variables de entorno

| Variable            | Descripción                                  |
| ------------------- | -------------------------------------------- |
| `LLM_PROVIDER`      | Proveedor utilizado (`openai` o `anthropic`) |
| `OPENAI_API_KEY`    | API key de OpenAI                            |
| `ANTHROPIC_API_KEY` | API key de Anthropic                         |
| `OPENAI_MODEL`      | Modelo utilizado por OpenAI                  |
| `ANTHROPIC_MODEL`   | Modelo utilizado por Anthropic               |
| `LLM_TEMPERATURE`   | Temperatura utilizada para la generación     |
| `LLM_MAX_TOKENS`    | Cantidad máxima de tokens de la respuesta    |

La configuración se carga desde `.env` y posteriormente se valida mediante los modelos de Pydantic.

> **Importante:** el archivo `.env` no debe subirse al repositorio. Se encuentra incluido en `.gitignore`.

---

## Uso

El proyecto proporciona un `AsyncLLMManager` que permite seleccionar el proveedor:

```python
manager = AsyncLLMManager(
    openai_api_key=openai_api_key,
    anthropic_api_key=anthropic_api_key,
)
```

Luego se puede generar una respuesta indicando el proveedor:

```python
response = await manager.generate(
    provider="openai",
    messages=messages,
    config=config,
)
```

También se puede utilizar Anthropic:

```python
response = await manager.generate(
    provider="anthropic",
    messages=messages,
    config=config,
)
```

La implementación del manager se encarga de seleccionar el cliente correspondiente.

El proveedor utilizado por el ejemplo principal se configura mediante `LLM_PROVIDER`.

---

## Streaming

El cliente permite recibir la respuesta progresivamente mediante un `async generator`.

Ejemplo:

```python
async for chunk in manager.stream(
    provider="openai",
    messages=messages,
    config=config,
):
    print(chunk, end="", flush=True)
```

Esto permite procesar la respuesta a medida que el proveedor genera contenido, en lugar de esperar a que la respuesta completa esté disponible.

El mismo mecanismo está disponible para Anthropic:

```python
async for chunk in manager.stream(
    provider="anthropic",
    messages=messages,
    config=config,
):
    print(chunk, end="", flush=True)
```

---

## Validación con Pydantic

Los mensajes y la configuración del modelo son validados antes de enviarse al proveedor.

Ejemplo:

```python
message = ChatMessage(
    role="user",
    content="¿Qué es la entropía?",
)
```

Los roles permitidos son:

```text
system
user
assistant
```

La configuración del modelo también posee validaciones:

```python
config = ModelConfig(
    model="gpt-4o-mini",
    temperature=0.7,
    max_tokens=500,
)
```

La temperatura está limitada al rango:

```text
0 <= temperature <= 2
```

y `max_tokens` debe ser mayor que cero.

---

## Manejo de errores

Los errores específicos de cada proveedor se transforman en excepciones propias de la aplicación.

La jerarquía utilizada es:

```text
LLMClientError
├── LLMRateLimitError
├── LLMConnectionError
└── LLMAuthenticationError
```

Por ejemplo:

```python
try:
    response = await manager.generate(
        provider="openai",
        messages=messages,
        config=config,
    )

except LLMRateLimitError as error:
    print(f"Rate limit / quota error: {error}")

except LLMAuthenticationError as error:
    print(f"Authentication error: {error}")

except LLMConnectionError as error:
    print(f"Connection error: {error}")
```

Esto evita que la aplicación dependa directamente de las excepciones internas de cada SDK y permite trabajar con una interfaz de errores común.

---

## Ejecución

Para ejecutar el ejemplo principal:

```powershell
python main.py
```

El programa realiza una llamada normal y una llamada mediante streaming utilizando el proveedor configurado en `LLM_PROVIDER`.

También existe un ejemplo de streaming completamente local que no requiere API keys:

```powershell
python test_stream.py
```

Este ejemplo utiliza un cliente ficticio para demostrar el comportamiento asíncrono del streaming.

---

## Tests

El proyecto utiliza `pytest` y `pytest-asyncio`.

Para ejecutar todos los tests:

```powershell
pytest
```

La suite actual cuenta con **17 tests automatizados**, cubriendo:

* Validación de mensajes.
* Validación de configuración.
* Selección de proveedores.
* Selección case-insensitive del proveedor.
* Rechazo de proveedores no soportados.
* Generación asíncrona con OpenAI.
* Streaming con OpenAI.
* Generación asíncrona con Anthropic.
* Streaming con Anthropic.
* Manejo de rate limits.
* Manejo de errores de conexión.
* Manejo de errores de autenticación.

Los tests utilizan mocks/fakes, por lo que no requieren realizar llamadas reales a las APIs.

---

## Tecnologías utilizadas

* **Python 3.12**
* **Pydantic**
* **OpenAI SDK**
* **Anthropic SDK**
* **python-dotenv**
* **pytest**
* **pytest-asyncio**

---

## Objetivo del proyecto

El objetivo es construir un cliente LLM desacoplado del proveedor, permitiendo que la aplicación pueda trabajar con diferentes servicios de inteligencia artificial utilizando una interfaz común.

La arquitectura facilita incorporar nuevos proveedores en el futuro sin modificar la lógica principal de la aplicación.

---

## Estado del proyecto

**Pre-entrega 1 — Cliente de LLM robusto y asíncrono**

Implementación funcional de:

* Intercambiabilidad entre proveedores.
* Operaciones asíncronas.
* Streaming.
* Validación de datos.
* Configuración mediante variables de entorno.
* Manejo controlado de errores.
* Tests automatizados.

**Tests: 17/17 pasando.**