# 🎮 Pong Leaderboard

[![Tests](https://img.shields.io/badge/tests-36%20passed-brightgreen)](https://github.com/kevinbetancourt/pong-leaderboard)
[![Coverage](https://img.shields.io/badge/coverage-27%25-yellow)](https://github.com/kevinbetancourt/pong-leaderboard)
[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)

Un juego Pong clásico desarrollado en Python con un backend FastAPI y almacenamiento en SQLite. Las puntuaciones de los partidos se guardan en una base de datos y pueden consultarse a través de una REST API.

---

## Demo

El proyecto consiste en dos partes que trabajan en conjunto:

1. **Juego (Frontend)**: Un juego Pong desarrollado con `turtle` donde dos jugadores compiten localmente
2. **API (Backend)**: Un servidor FastAPI que almacena las puntuaciones y expone endpoints para consultarlas

Cuando un jugador gana un partido, su puntuación se calcula según la diferencia de goles y se envía automáticamente a la API.

---

## Tecnologías

| Categoría | Tecnología |
|-----------|-------------|
| Lenguaje | Python 3.12 |
| Juego | Turtle (Python stdlib) |
| Backend | FastAPI |
| Base de datos | SQLite |
| ORM | SQLAlchemy |
| Servidor | Uvicorn |
| Config | pydantic-settings |
| Rate Limiting | slowapi |
| Testing | pytest + pytest-cov |

---

## Arquitectura

```
pong-leaderboard/
├── game/                  # Lógica del juego Pong
│   ├── main.py            # Punto de entrada del juego
│   ├── game_controller.py # Controlador principal
│   ├── player.py          # Modelo de jugador
│   ├── paddle.py          # Paletas
│   ├── ball.py            # Pelota
│   ├── collision.py       # Detección de colisiones
│   ├── scoreboard.py      # Marcador visual
│   ├── borders.py         # Bordes del campo
│   ├── player_setup.py    # Configuración de jugadores
│   └── config.py          # Configuración global
├── api/                   # Backend FastAPI
│   ├── main.py            # Endpoints de la API
│   ├── models.py          # Modelos SQLAlchemy
│   ├── database.py        # Configuración de BD
│   └── schemas.py         # Schemas Pydantic
├── tests/                 # Tests unitarios
│   ├── test_api.py        # Tests de la API
│   └── test_game_logic.py # Tests de lógica del juego
├── settings.py            # Configuración centralizada
├── requirements.txt       # Dependencias Python
└── scores.db             # Base de datos SQLite
```

---

## Instalación y Ejecución

### 1. Clonar el repositorio

```bash
git clone <repo-url>
cd pong-leaderboard
```

### 2. Crear entorno virtual

```bash
python3 -m venv venv
```

### 3. Activar el entorno

```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. (Opcional) Crear archivo .env

```bash
cp .env.example .env
```

### 6. Ejecutar el backend

```bash
python -m uvicorn api.main:app --reload
```

La API estará disponible en `http://localhost:8000`

### 7. Ejecutar el juego (en otra terminal)

```bash
python game/main.py
```

---

## Cómo Jugar

1. Al iniciar el juego, presiona **ENTER** para comenzar
2. Configura el nombre, letra identificadora y color de cada jugador
3. Define la cantidad de goles para ganar el partido
4. **Jugador izquierdo**: teclas `w` (arriba) / `s` (abajo)
5. **Jugador derecho**: teclas `↑` (arriba) / `↓` (abajo)
6. El primer jugador en llegar a la cantidad de goles establecidos gana

### Sistema de Puntuación

Cada gol de diferencia en la victoria vale **100 puntos**.

| Resultado | Diferencia | Puntos |
|----------|------------|--------|
| 12-7 | 5 | 500 |
| 12-3 | 9 | 900 |
| 5-2 | 3 | 300 |

Solo el ganador envía su puntuación al leaderboard.

---

## Endpoints de la API

### POST /score

Guarda una nueva puntuación.

```bash
curl -X POST http://localhost:8000/score \
  -H "Content-Type: application/json" \
  -d '{"player": "Kevin", "score": 500}'
```

**Rate Limiting**: 10 requests por minuto por IP.

### GET /scores

Obtiene el top 10 de puntuaciones.

```bash
curl http://localhost:8000/scores
```

### POST /seed

Pobla la base de datos con datos de ejemplo.

```bash
curl -X POST http://localhost:8000/seed
```

### GET /health

Health check endpoint.

```bash
curl http://localhost:8000/health
```

### Documentación interactiva

Accedé a `http://localhost:8000/docs` para probar la API.

---

## Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| `DATABASE_URL` | URL de la base de datos | `sqlite:///./scores.db` |
| `API_HOST` | Host del servidor | `0.0.0.0` |
| `API_PORT` | Puerto del servidor | `8000` |

---

## Testing

### Ejecutar tests

```bash
pytest
```

### Ejecutar con coverage

```bash
pytest --cov=api --cov=game --cov-report=term-missing
```

### Coverage actual

| Módulo | Cobertura |
|--------|-----------|
| api/database.py | 100% |
| api/main.py | 94% |
| api/models.py | 100% |
| api/schemas.py | 97% |
| game/collision.py | 100% |
| game/config.py | 90% |
| **TOTAL** | **27%** |

> **Nota**: La cobertura del juego es baja porque los tests unitarios no cubren el código visual de turtle (main.py, paddle.py, etc). Solo se testa la lógica de colisiones y puntuación.

---

## Funcionalidades

- ✅ Juego Pong clásico con gráficos Turtle
- ✅ Movimiento fluido de paletas
- ✅ Rebote de pelota con detección de colisiones
- ✅ Sistema de puntuación dinámico (diferencia × 100)
- ✅ Integración automática juego → API
- ✅ Backend REST con FastAPI
- ✅ Almacenamiento persistente en SQLite
- ✅ Menú de inicio y reinicio
- ✅ Limpieza de pantalla al reiniciar partida
- ✅ Validación de input con Pydantic
- ✅ Sanitización de nombres de jugador
- ✅ Rate limiting (10 req/min)
- ✅ Manejo centralizado errores
- ✅ Configuración en variables de entorno
- ✅ 36 tests unitarios

---

## Mejoras Futuras

- 🌐 Modo multiplayer online
- 🎨 Interfaz web para el juego
- 📊 Dashboard en tiempo real del leaderboard
- 👥 Sistema de usuarios y autenticación
- 📱 Versión móvil
- 🔄 Historial de partidas por jugador

---

## Autor

**Kevin Andrés Betancourt López**

---

## Licencia

MIT License
