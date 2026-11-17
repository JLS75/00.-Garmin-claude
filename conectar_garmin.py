#!/usr/bin/env python3
"""Conecta tu cuenta Garmin Connect (y tu reloj) usando python-garminconnect.

- La contraseña se pide en la Terminal con getpass (no se muestra ni se guarda).
- Tras el primer login se guardan solo tokens en ~/.garminconnect (permisos 600),
  así que las siguientes ejecuciones no vuelven a pedir contraseña ni código MFA.
"""
from __future__ import annotations

import os
import sys
from datetime import date
from getpass import getpass
from pathlib import Path

try:
    from garminconnect import (
        Garmin,
        GarminConnectAuthenticationError,
        GarminConnectConnectionError,
        GarminConnectTooManyRequestsError,
    )
except ImportError:
    sys.exit("Falta la librería. Ejecuta primero: ./instalar_y_conectar.sh "
             "(o pip install -r requirements.txt)")

TOKENSTORE = os.getenv("GARMINTOKENS", str(Path.home() / ".garminconnect"))


def pedir_mfa() -> str:
    return input("Código de verificación (MFA) que te ha enviado Garmin: ").strip()


def conectar() -> Garmin:
    # 1) Intento con tokens guardados (sin contraseña)
    if (Path(TOKENSTORE).expanduser() / "garmin_tokens.json").exists():
        try:
            api = Garmin()
            api.login(TOKENSTORE)
            print(f"✔ Sesión restaurada desde {TOKENSTORE}")
            return api
        except Exception as e:  # tokens caducados o inválidos
            print(f"Los tokens guardados no sirven ({type(e).__name__}); "
                  "hay que iniciar sesión de nuevo.")

    # 2) Login con credenciales pedidas en la Terminal
    email = os.getenv("GARMIN_EMAIL") or input("Email de Garmin Connect: ").strip()
    password = getpass("Contraseña de Garmin Connect (no se mostrará): ")
    if not email or not password:
        raise GarminConnectAuthenticationError("Email y contraseña son obligatorios")
    Path(TOKENSTORE).expanduser().mkdir(mode=0o700, parents=True, exist_ok=True)
    api = Garmin(email=email, password=password, prompt_mfa=pedir_mfa)
    del password
    api.login(TOKENSTORE)  # guarda los tokens en TOKENSTORE
    print(f"✔ Login correcto. Tokens guardados en {TOKENSTORE}")
    return api


def mostrar_resumen(api: Garmin) -> None:
    print(f"\n👤 Usuario: {api.get_full_name()}")

    dispositivos = api.get_devices() or []
    print(f"\n⌚ Dispositivos vinculados ({len(dispositivos)}):")
    for d in dispositivos:
        nombre = d.get("displayName") or d.get("productDisplayName") or "?"
        print(f"   - {nombre} | modelo: {d.get('productDisplayName', '?')} "
              f"| firmware: {d.get('currentFirmwareVersion', '?')}")

    try:
        ultimo = api.get_device_last_used() or {}
        if ultimo:
            print(f"   Último usado: {ultimo.get('lastUsedDeviceName', '?')} "
                  f"(sincronizado: {ultimo.get('lastUsedDeviceUploadTime', '?')})")
    except Exception:
        pass

    hoy = date.today().isoformat()
    s = api.get_user_summary(hoy) or {}
    print(f"\n📊 Resumen de hoy ({hoy}):")
    print(f"   Pasos: {s.get('totalSteps')} / objetivo {s.get('dailyStepGoal')}")
    print(f"   Calorías totales: {s.get('totalKilocalories')}")
    print(f"   FC reposo: {s.get('restingHeartRate')} ppm")
    print(f"   Body Battery actual: {s.get('bodyBatteryMostRecentValue')}")
    print(f"   Estrés medio: {s.get('averageStressLevel')}")


def main() -> int:
    try:
        api = conectar()
        mostrar_resumen(api)
        print("\n✅ Tu reloj Garmin está conectado a este ordenador.")
        return 0
    except GarminConnectAuthenticationError as e:
        print(f"❌ Error de autenticación: {e}")
    except GarminConnectTooManyRequestsError:
        print("❌ Garmin ha limitado los intentos (429). Espera un rato y reintenta.")
    except GarminConnectConnectionError as e:
        print(f"❌ Error de conexión con Garmin: {e}")
    except (KeyboardInterrupt, EOFError):
        print("\nCancelado.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
