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

## Uso en iPad (app a-Shell)

El iPad no tiene Terminal ni permite instalar librerías compiladas. Se usa la app
gratuita **a-Shell** (App Store), que trae Python 3 y `pip` para paquetes en Python puro.

1. Instala **a-Shell** desde la App Store y ábrela.
2. Copia y pega estos comandos, uno por línea:

```sh
pip install --no-deps garminconnect
pip install requests ua-generator
curl -L -o conectar_garmin.py https://raw.githubusercontent.com/jls75/00.-garmin-claude/claude/garmin-watch-connection-1mgry5/conectar_garmin.py
python3 conectar_garmin.py
```

3. Escribe el email y luego la contraseña cuando te lo pida a-Shell. El código MFA
   también se pide ahí si lo tienes activado.

`pip` avisará de que falta `curl_cffi`. Es normal: esa dependencia es código compilado y
no existe para iPad, y la librería funciona sin ella. Las siguientes veces basta con
`python3 conectar_garmin.py`.

### Plan B si Garmin bloquea el login desde el iPad
Sin `curl_cffi`, Cloudflare puede bloquear el inicio de sesión aunque la contraseña sea
correcta. En ese caso:
1. Haz el login **una sola vez** en un Mac/PC con `./instalar_y_conectar.sh`.
2. Pasa al iPad el archivo `~/.garminconnect/garmin_tokens.json` (AirDrop o iCloud Drive)
   y guárdalo en la carpeta de a-Shell (en Archivos: *En mi iPad › a-Shell*), dentro de una
   subcarpeta `garmin`.
3. En a-Shell: `python3 conectar_garmin.py --tokens garmin`

A partir de ahí el iPad renueva los tokens solo, sin volver a pedir la contraseña.
Trata ese archivo como una contraseña: da acceso a tu cuenta de Garmin.

## Notas
- Requiere Python 3.10+.
- El reloj se sincroniza con Garmin Connect desde la app del móvil o Garmin Express; esta
  librería lee los datos de tu cuenta en la nube de Garmin.
- Para cerrar sesión: borra `~/.garminconnect/garmin_tokens.json`.
- Opciones: `--tokens <carpeta>` o la variable `GARMINTOKENS` (otra ruta de tokens), `GARMIN_EMAIL` (evita teclear el email).
