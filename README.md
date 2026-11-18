# LexyBotEstado

Muestra en tu **perfil personal de Discord** una Rich Presence personalizada parecida a la captura de referencia:

- **Jugando a:** Grand Theft Auto VI
- **Descripción:** Jugando en PlayStation 5
- **Estado:** PS5 | GTA VI
- **Tiempo transcurrido:** 357044 horas iniciales (configurable, simuladas)
- **Imagen:** portada opcional del juego, mediante un asset de tu aplicación de Discord

> **Importante:** el texto de PlayStation 5 es personalizado. No genera el indicador oficial "Jugando en PlayStation" ni comprueba que tengas una PS5 o GTA VI. No se utiliza un self-bot, token de usuario ni contraseña.

## Requisitos

- Una computadora con **Windows, macOS o Linux**, Python 3.10+ y la **aplicación de Discord de escritorio** iniciada con tu cuenta.
- No funciona por sí solo en Discord web, en una página de GitHub ni en Android/Termux. Puedes **ver** el estado desde Discord móvil, pero necesitas que el programa esté ejecutándose donde haya un cliente de Discord con RPC local.
- El repositorio **no necesita un token de bot**.

## Instalación

1. Entra en [Discord Developer Portal](https://discord.com/developers/applications) y crea una aplicación nueva. Copia su **Application ID** (número). No necesitas crear un bot.
2. Descarga el proyecto o clónalo:
   ```bash
   git clone https://github.com/Yamekiteelyeso/LexyBotEstado.git
   cd LexyBotEstado
   ```
3. Instala Python y la dependencia:
   ```bash
   python -m pip install -r requirements.txt
   ```
4. Copia `config.example.json` a `config.json`. En Windows:
   ```bat
   copy config.example.json config.json
   ```
   En macOS/Linux:
   ```bash
   cp config.example.json config.json
   ```
5. Abre `config.json` y sustituye `PON_AQUI_TU_APPLICATION_ID` por el ID numérico de tu aplicación. **Nunca pegues tu token de Discord.**
6. Comprueba que la configuración esté bien:
   ```bash
   python main.py --check
   ```
7. Abre Discord de escritorio y ejecuta:
   ```bash
   python main.py
   ```

En Windows puedes hacer doble clic en `iniciar.bat`, que instala la dependencia y crea la configuración si falta. **Debes rellenar el Application ID antes de activar la presencia.**

## Imagen del GTA VI

Para mostrar una imagen grande, súbela en la sección **Rich Presence / Art Assets** de tu aplicación del Developer Portal (usa una imagen que puedas utilizar). Ponle una clave, por ejemplo `gta6`. Después cambia en `config.json`:

```json
"large_image": "gta6"
```

Si está vacía, Discord mostrará la actividad sin portada personalizada.

## Personalización

Edita `config.json`:

| Campo | Función |
| --- | --- |
| `game` | Nombre de la actividad, por defecto Grand Theft Auto VI |
| `details` | Texto Jugando en PlayStation 5 |
| `state` | Texto secundario PS5 / GTA VI |
| `elapsed_hours` | Horas iniciales simuladas (usa `0` para un contador real desde el inicio) |
| `large_image` | Clave de la imagen subida a Discord |
| `refresh_seconds` | Intervalo de actualización; mínimo 15 segundos |
| `retry_seconds` | Reintento si se cierra o reinicia Discord |

El contador es una simulación; **no mide horas reales de juego**. Discord puede elegir cómo mostrar la hora y el nombre, y su interfaz puede cambiar. Si el nombre personalizado no aparece, revisa el nombre de la aplicación en el Developer Portal.

## Solución de problemas

- **Application ID inválido:** copia el **Application ID**, no el public key ni bot token.
- **No encuentra Discord:** abre la aplicación de escritorio y vuelve a ejecutar el programa.
- **No aparece el juego:** en Discord activa la visualización de actividad en los ajustes de privacidad/actividad. Verifica también que no haya otra actividad que esté reemplazando la tuya.
- **No aparece la imagen:** revisa que la clave de Art Assets coincida exactamente con `large_image`.
- **Se apaga al cerrar el programa o la PC:** es normal. El RPC funciona mientras el proceso y Discord están activos.

Detén la actividad con **Ctrl+C**. El código solo establece una Rich Presence local, no modifica cuentas ni servidores.
