# Conexión de mi reloj Garmin con python-garminconnect

Conecta tu cuenta de Garmin Connect (y los datos de tu reloj) a tu ordenador usando
[python-garminconnect](https://github.com/cyberjunky/python-garminconnect) (v0.3.x).

## Uso (una sola vez)

**macOS / Linux** — en la Terminal:

```bash
git clone -b claude/garmin-watch-connection-1mgry5 https://github.com/jls75/00.-garmin-claude.git
cd 00.-garmin-claude
./instalar_y_conectar.sh
```

**Windows**: clona el repo y haz doble clic en `instalar_y_conectar.bat`.

El script:
1. Crea un entorno virtual `.venv` e instala `garminconnect`.
2. Te pide **en la Terminal** el email y la contraseña (oculta, vía `getpass`).
   Si tienes verificación en dos pasos, te pide también el código MFA.
3. Guarda **solo tokens** (no la contraseña) en `~/.garminconnect/garmin_tokens.json`.
4. Muestra tu nombre, relojes vinculados y el resumen de hoy (pasos, FC reposo, Body Battery…).

Las siguientes veces basta con `./.venv/bin/python conectar_garmin.py`: reutiliza los
tokens y no vuelve a pedir contraseña.

## Notas
- Requiere Python 3.10+.
- El reloj se sincroniza con Garmin Connect desde la app del móvil o Garmin Express; esta
  librería lee los datos de tu cuenta en la nube de Garmin.
- Para cerrar sesión: borra `~/.garminconnect/garmin_tokens.json`.
- Variables opcionales: `GARMIN_EMAIL` (evita teclear el email), `GARMINTOKENS` (otra ruta de tokens).
