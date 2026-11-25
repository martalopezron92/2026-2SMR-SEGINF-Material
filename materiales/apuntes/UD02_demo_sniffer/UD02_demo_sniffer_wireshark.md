# Demo en clase · UD02 · Sesión 1
## Qué ve un sniffer: HTTP frente a HTTPS

| | |
|---|---|
| **Tipo** | Demostración del profesor/a (proyectada) |
| **Duración** | 10–15 minutos, al empezar la sesión 1, como motivación |
| **Equipo** | Kali Linux (máquina virtual de la UD01) con Wireshark y Python 3, que ya vienen instalados |
| **Criterio que motiva** | RA4.d (aplicar medidas para evitar la monitorización de redes) |
| **Archivos** | `servidor_login.py` (en esta misma carpeta) |

> **Objetivo:** que el alumnado **vea con sus propios ojos** que una contraseña enviada por HTTP viaja en claro y cualquiera que capture el tráfico la puede leer, mientras que con HTTPS solo se ven datos cifrados. Es la razón de ser de toda la unidad.

> **Legalidad:** todo ocurre **dentro de tu propia máquina** (interfaz *loopback*, `127.0.0.1`). No se captura tráfico de nadie más. Recuérdalo en clase: capturar el tráfico de una red ajena sin autorización es delito (art. 197 del Código Penal), igual que el escaneo de la UD01.

---

## 1. Preparación (5 minutos, antes de clase)

Copia `servidor_login.py` a una carpeta de Kali, por ejemplo `~/demo_sniffer`, y genera un certificado **autofirmado** para la parte HTTPS:

```bash
cd ~/demo_sniffer
openssl req -x509 -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 30 -subj "/CN=127.0.0.1"
```

Abre **dos terminales** y deja los dos servidores en marcha:

```bash
# Terminal 1: servidor HTTP (sin cifrar)
python3 servidor_login.py

# Terminal 2: servidor HTTPS (cifrado)
python3 servidor_login.py --https
```

Comprueba que en el navegador de Kali se abren `http://127.0.0.1:8080` y `https://127.0.0.1:8443`. El script solo escucha en `127.0.0.1` y no guarda nada.

---

## 2. Parte A · Login por HTTP (5 minutos)

1. Abre **Wireshark** (`sudo wireshark` o desde el menú de Kali).
2. Elige la interfaz **Loopback: lo** y pulsa la aleta azul para empezar a capturar.
3. En la barra de filtro escribe y pulsa Intro:

   ```
   http.request.method == "POST"
   ```

4. En el navegador, entra en `http://127.0.0.1:8080` y haz login con:
   - Usuario: `ana`
   - Contraseña: `Secreta123`
5. En Wireshark aparece un paquete `POST /login`. Selecciónalo y, en el panel inferior, despliega **HTML Form URL Encoded**: se ven `usuario = ana` y `password = Secreta123`.
6. Para que se vea aún más claro: clic derecho sobre el paquete → **Seguir → Secuencia TCP** (*Follow → TCP Stream*). Aparece la petición completa en texto, con la contraseña en claro.

**Pregunta para la clase:** *¿Quién más podría ver esto en una red real?* (Cualquiera en la misma wifi abierta, el dueño del router, un equipo comprometido de la red, el proveedor de Internet…)

---

## 3. Parte B · Login por HTTPS (5 minutos)

1. Cambia el filtro de Wireshark a:

   ```
   tcp.port == 8443
   ```

2. En el navegador, entra en `https://127.0.0.1:8443`.
   - El navegador mostrará un **aviso de seguridad** (*"La conexión no es privada"* / *"Advertencia: riesgo potencial de seguridad"*). Es lo esperado: el certificado es **autofirmado** y no lo ha firmado ninguna CA de confianza. Acepta el riesgo **solo porque es tu propio servidor de prueba**.
3. Haz el mismo login (`ana` / `Secreta123`).
4. En Wireshark ya no aparece ningún `POST`. Se ven paquetes **TLS**: `Client Hello`, `Server Hello`, intercambio de claves y luego **Application Data**.
5. Clic derecho → **Seguir → Secuencia TCP**: solo caracteres sin sentido. **La contraseña no aparece por ningún lado.**

**Pregunta para la clase:** *¿Qué ha cambiado?* (El navegador y el servidor han acordado una clave y todo el tráfico va cifrado → es lo que veremos en la unidad: cifrado simétrico, asimétrico, híbrido y certificados.)

---

## 4. Cierre (2 minutos): conectar con la unidad

| Lo que hemos visto | Dónde se explica |
|---|---|
| Un sniffer captura todo el tráfico que pasa por la interfaz | Apuntes §1 |
| Con HTTP los datos viajan en **texto claro** | Apuntes §1 (confidencialidad) |
| HTTPS cifra los datos: **AES** con una clave de sesión acordada con criptografía **asimétrica** | Apuntes §3, §4.2 y §7.3 (cifrado híbrido) |
| El aviso del navegador ante un certificado **autofirmado** | Apuntes §7 (certificados y CA) |
| Ojo: el candado no impide el phishing | Apuntes §7.3 |

> **Idea para recordar:** el cifrado **no impide** que capturen tus datos, pero hace que lo capturado **no sirva para nada** sin la clave.

---

## 5. Si algo falla

| Problema | Solución |
|---|---|
| Wireshark no muestra la interfaz `lo` o da el error *"You don't have permission to capture on that device"* / *"Please check to make sure you have sufficient permissions"* | Ejecuta `sudo dpkg-reconfigure wireshark-common` y responde **Sí** (*Yes*) a si los usuarios sin privilegios pueden capturar. Después `sudo usermod -aG wireshark $USER` y **cierra sesión y vuelve a entrar** (o, para no cerrar sesión, `newgrp wireshark` y lanza `wireshark` desde ese mismo terminal). Comprueba con `groups` que aparece `wireshark`. Solución rápida para la demo: `sudo wireshark`. |
| `Address already in use` al lanzar el servidor | Ya hay uno en marcha: ciérralo con Ctrl+C o usa `pkill -f servidor_login.py`. |
| El servidor HTTPS da `FileNotFoundError: cert.pem` | Genera el certificado (apartado 1) en la **misma carpeta** que el script. |
| No aparece el POST en Wireshark | Comprueba que capturas en **Loopback: lo** y que entras por `127.0.0.1:8080`, no por `localhost` en otro puerto. |
| Prefieres hacerlo en Windows | Instala Wireshark con **Npcap** marcando *Support loopback traffic* y captura en *Adapter for loopback traffic capture*. El script funciona igual con `python servidor_login.py`; para el certificado necesitas OpenSSL (incluido con Git for Windows). |

### Variante para que lo haga el alumnado (opcional)

Si hay tiempo en la práctica de la sesión 1, cada alumno/a puede repetir la demo en su propia Kali (todo en `127.0.0.1`, sin riesgo) y añadir dos capturas: el POST con la contraseña en claro y el flujo TLS ilegible.
