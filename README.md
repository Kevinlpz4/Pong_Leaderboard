# 🎮 Pong Leaderboard

Un juego Pong clásico desarrollado en Python con un backend FastAPI y almacenamiento en SQLite. Los puntuaciones de los partidos se guardan en una base de datos y pueden consultarse a través de una REST API.

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

### 5. Ejecutar el backend

```bash
python -m uvicorn api.main:app --reload
```

La API estará disponible en `http://localhost:8000`

### 6. Ejecutar el juego (en otra terminal)

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

### POST /seed

Pobla la base de datos con datos de ejemplo (top 10 inicial).

```bash
curl -X POST http://localhost:8000/seed
```

### POST /score

Guarda una nueva puntuación.

```bash
curl -X POST http://localhost:8000/score \
  -H "Content-Type: application/json" \
  -d '{"player": "Kevin", "score": 500}'
```

### GET /scores

Obtiene el top 10 de puntuaciones.

```bash
curl http://localhost:8000/scores
```

### Documentación interactiva

Accedé a `http://localhost:8000/docs` para probar la API desde Swagger UI.

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

---

## Mejoras Futuras

- 🌐 Modo multiplayer online
- 🎨 Interfaz web para el juego
- 📊 Dashboard en tiempo real del leaderboard
- 👥 Sistema de usuarios y autenticación
- 📱 Version móvil
- 🔄 Historial de partidas por jugador

---

## Autor

**Kevin Andrés Betancourt López**

---

## Licencia

MIT License
