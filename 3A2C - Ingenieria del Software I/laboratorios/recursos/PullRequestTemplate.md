# TÍTULO BREVE Y DESCRIPTIVO

<!-- Ej: feat(api): add /games/join endpoint (PROJ-123) -->

[TIPO] área: breve-descripción (TICKET)

---

## Descripción

<!-- En 2–5 párrafos explica:
 - Qué problema arregla o qué feature agrega.
 - Resumen de la solución aplicada.
 - Por qué esta solución (decisiones importantes / alternativas descartadas).
-->

* **Problema / motivo:**
* **Cambios realizados:**
* **Decisiones relevantes:**

## Referencias

* Issue / Ticket: `IP-123` (link)
* Branch relacionada(s): `feature_IP-123-...`
* PRs dependientes / relacionados (si aplica): #NNN

## Checklist de preparación (obligatorio)

* [ ] Actualicé mi branch desde `develop` (`git merge origin/develop`) y resolví conflictos.
* [ ] Los tests locales pasan: `./test` .
* [ ] Formato aplicados: Equivalente a `prettier` para Python (autopep8).
* [ ] Coverage alcanzado: **>= 90%** en backend .
* [ ] Añadí tests que cubran nuevos paths (Si usan nuevos path, testeenlos, muchas horas perdimos con los paths) y edge-cases (unit / integration / e2e según corresponda, aunque no hemos hecho ninguna de estos hasta la fecha 04/10).
* [ ] Actualicé la documentación relevante si es necesario (README, API docs (endpoints,websocoket)).
* [ ] Actualizar  `requirements.txt` en caso de serlo necesario.

## Cambios técnicos importantes

* **Endpoints añadidos/modificados:**

  * `POST /games/:id/join` — breve descripción


* **Breaking changes:** (si aplica) describir y documentar plan de migración

## Cómo probar manualmente (pasos)

1. `git swich feature_IP-123-...`
2. Levantar entorno virtual de python: ` python -m venv venv` -> `source venv/bing/activate `
3. Instalar los requerimientos `pip install -r requirements.txt`
4. Ejecutar tests : `pytest`
5. (Opcional) Probar endpoint (Utilizando CURL pj.)

### Revisar cobertura

1. Ejecucion `pytest --cov=src --cov-report=html`.
2. Visualizar con `firefox htmlcov/index.html` o cualquier metodo para abrir un .html.

## Archivos sugeridos para revisar (orden recomendado)

1. `api/controllers/games.py` — lógica del endpoint
2. `services/game_service.py` — reglas de negocio y transacciones
3. `repositories/game_repo.py` — queries y locks
4. `migrations/*.sql` — cambios en DB
5. `tests/test_games_join.py` — tests principales

> Sugerencia: indicar un orden ayuda a revisores menos experimentados y acelera la revisión.

## Evidencia / Antes y después (opcional, pero estaria bueno)

* Adjunta screenshots, gifs, logs o sample responses JSON relevantes.
* Adjuntar salida de tests/coverage si relevante.
> No, antes-despues de codigo, sino de cosas mas visibles y claras

## Consideraciones de validacion (opcional)

* Validaciones aplicadas: sanitización y autorización (ej: `player_id` validado y autorizado).



