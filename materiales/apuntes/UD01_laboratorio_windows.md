# Práctica técnica · UD01 · Documento 1 de 2 (versión Windows)
## Parte guiada — Montaje del laboratorio y primeros pasos con Nmap

> **IMPORTANTE:** este documento es la **parte guiada y NO evaluable**. Sirve para montar el laboratorio y aprender a usar las herramientas con ayuda. **No se entrega**, pero es **obligatorio** haberla realizado antes de pasar al Documento 2 (la parte evaluable).

| | |
|---|---|
| **Módulo** | Seguridad Informática · 2º SMR |
| **Instrumento** | Práctica técnica (40 % de la UD01) — **esta parte no puntúa** |
| **Duración orientativa** | 2 sesiones (montaje + práctica guiada) |
| **Equipo anfitrión** | Windows 10 u 11 (64 bits) |

> **Qué vas a hacer:** montar un pequeño "laboratorio" con dos máquinas virtuales aisladas y practicar las **primeras fases de una auditoría de caja negra** (footprinting y fingerprinting) con **Nmap**, tal y como se explica en la UD01. **No se ataca ni se explota nada:** solo se observa y se analiza, igual que hace un auditor antes de emitir su informe.

---

## 0. Normas éticas y legales (OBLIGATORIO leer y firmar)

Las técnicas de esta práctica **solo son legales sobre sistemas propios o con autorización expresa por escrito**. Usarlas contra equipos o redes ajenas sin permiso es un **delito** (arts. 197 bis y 264 del Código Penal) y contradice el principio que estudiamos: la diferencia entre un PenTest y un ataque real es **la autorización**.

En esta práctica:

- Todo se hace en **máquinas virtuales propias**, en una **red aislada sin salida a Internet**.
- **Nunca** se escanean equipos del instituto, de casa, redes WiFi públicas ni direcciones de Internet.
- La práctica se queda en **reconocimiento y análisis**; no se ejecutan exploits ni se modifica ningún sistema.

---

## Cómo usar esta guía

- Ve **en orden**, apartado por apartado. No te saltes pasos: cada uno depende del anterior.
- Al final de cada apartado hay un recuadro **✅ Comprueba**. **No sigas** hasta que se cumpla lo que dice.
- Las palabras en **negrita** son botones, menús o textos que vas a ver en pantalla.
- Lo que va en `letra de código` hay que **escribirlo exactamente igual** (mayúsculas, espacios y guiones incluidos).
- Lo que va entre `< >` hay que **cambiarlo** por tu dato, sin los símbolos `< >`. Ejemplo: `ping <IP_del_objetivo>` → `ping 10.10.10.10`.
- Los menús de VirtualBox pueden cambiar un poco según la versión. Si no encuentras un botón exactamente como aquí, busca uno parecido o pregunta.
- Si algo falla, mira el apartado **1.12. Si algo falla** antes de preguntar.

---

## 1. Preparación del laboratorio en Windows (paso a paso)

Vamos a usar **dos** máquinas virtuales dentro de **VirtualBox**:

- **Kali Linux** → será nuestra máquina de auditoría (el "auditor").
- **Metasploitable 2** → será la máquina objetivo. Es un sistema **vulnerable a propósito**, creado para practicar de forma legal. No contiene datos reales.

Ambas estarán en una **red interna aislada**, sin conexión a Internet, para que nada salga del laboratorio.

```
        ┌─────────── Red interna "labSI" (aislada) ───────────┐
        │                                                     │
   [ Kali Linux ]  ◄───── observa / escanea ─────►  [ Metasploitable 2 ]
      (auditor)                                        (objetivo)
        │                                                     │
        └─────────────  SIN salida a Internet  ───────────────┘
```

Tu ordenador con Windows es el **anfitrión** (el equipo físico). Las dos máquinas virtuales son los **invitados**: funcionan "dentro" de él.

### 1.1. Comprobaciones previas

**a) ¿Está activada la virtualización?**

1. Pulsa a la vez **`Ctrl` + `Shift` + `Esc`** para abrir el **Administrador de tareas**.
2. Si ves una ventana pequeña, pulsa **Más detalles** (abajo a la izquierda).
3. Ve a la pestaña **Rendimiento** (en Windows 11 es el icono de la gráfica, en la barra de la izquierda) y haz clic en **CPU**.
4. Abajo a la derecha busca **Virtualización**. Debe poner **Habilitado**.

> Si pone **Deshabilitado**, hay que activarla en la BIOS/UEFI del ordenador (opción *Intel Virtualization Technology*, *VT-x* o *SVM Mode*). **Avisa al profesor/a**: sin esto no se puede hacer la práctica.

**b) ¿Cuánta memoria RAM tienes?**

En la misma ventana, haz clic en **Memoria**. Arriba a la derecha verás el total (por ejemplo `8,0 GB`).

- **8 GB o más:** perfecto.
- **4 GB:** funciona, pero muy justo. Cierra todos los programas (sobre todo el navegador) mientras uses las máquinas.

**c) ¿Tienes espacio en el disco?**

1. Abre el **Explorador de archivos** (**`Windows` + `E`**).
2. Haz clic en **Este equipo**.
3. Mira el disco **`C:`**: necesitas **al menos 30 GB libres**.

**d) Anota tus datos**

| Dato | Tu equipo |
|---|---|
| Virtualización | Habilitado / Deshabilitado |
| Memoria RAM total | ______ GB |
| Espacio libre en `C:` | ______ GB |

> ✅ **Comprueba:** virtualización **Habilitado**, al menos 4 GB de RAM y 30 GB libres. Si no, avisa al profesor/a antes de seguir.

### 1.2. Instalar VirtualBox

> **¿Ya tienes VirtualBox?** Pulsa la tecla **`Windows`**, escribe `VirtualBox` y mira si aparece **Oracle VirtualBox**. Si aparece, ábrelo y ve a **Ayuda → Acerca de VirtualBox**: si la versión empieza por **7.1 o 7.2**, **sáltate este apartado** y ve a 1.3.

**a) Descargar el instalador**

1. Abre el navegador y entra en `https://www.virtualbox.org/wiki/Downloads`.
2. En **VirtualBox Platform Packages**, haz clic en **Windows hosts**.
3. Se descarga un archivo parecido a `VirtualBox-7.2.x-xxxxxx-Win.exe` en tu carpeta **Descargas**.

> Descarga VirtualBox **solo de la web oficial**. Un instalador descargado de otra página podría estar modificado y contener malware.

**b) Instalarlo**

1. Ve a **Descargas** y haz **doble clic** en el instalador.
2. Si Windows pregunta **¿Quieres permitir que esta aplicación haga cambios en el dispositivo?**, pulsa **Sí**.
3. En la bienvenida, pulsa **Siguiente** (*Next*).
4. Acepta la licencia (**I accept the terms...**) y pulsa **Siguiente**.
5. En la pantalla de componentes, **deja todo como está** y pulsa **Siguiente**.
6. Pueden aparecer estos avisos. Así se responden:

| Aviso que aparece | Qué significa | Qué hacer |
|---|---|---|
| **Warning: Network Interfaces** | Durante la instalación tu conexión de red se cortará unos segundos. | Pulsa **Sí** (*Yes*). |
| **Missing Dependencies Python Core / win32api** | Faltan unos complementos de programación que **no necesitamos**. | Pulsa **Sí** (*Yes*) para continuar. |
| **Microsoft Visual C++ 2019 Redistributable** es necesario | Falta una librería de Windows. | Descárgala de `https://aka.ms/vs/17/release/vc_redist.x64.exe`, instálala y vuelve a ejecutar el instalador de VirtualBox. |
| **¿Desea instalar este software de dispositivo?** (Oracle) | Son los controladores de red y USB de VirtualBox. | Pulsa **Instalar**. |

7. Pulsa **Instalar** (*Install*) y espera a que termine la barra.
8. Deja marcada la casilla **Start Oracle VirtualBox after installation** y pulsa **Finalizar**.

> ✅ **Comprueba:** se abre la ventana de **Oracle VirtualBox Manager**, de momento sin ninguna máquina.

### 1.3. Crear la carpeta del laboratorio

1. Abre el **Explorador de archivos** (**`Windows` + `E`**).
2. Entra en el disco **`C:`**.
3. Clic derecho en un hueco vacío → **Nuevo → Carpeta**.
4. Llámala exactamente `labSI` y pulsa **`Intro`**.

Aquí guardaremos todas las descargas. La ruta de la carpeta es **`C:\labSI`**.

> **¿Por qué en `C:\` y no en el Escritorio?** Porque la ruta es corta y sin espacios ni tildes, lo que evita errores en VirtualBox.

> **Si el aula ya tiene las imágenes descargadas** (en una carpeta compartida o en un USB), cópialas a `C:\labSI` y **sáltate las descargas** de los apartados 1.4 y 1.5 (pero haz igualmente la comprobación SHA-256 y la descompresión).

### 1.4. Descargar, comprobar y descomprimir Kali Linux

**a) Descargar**

1. Entra en `https://www.kali.org/get-kali/`.
2. Haz clic en **Virtual Machines**.
3. Busca el recuadro de **VirtualBox** (64-bit) y pulsa el **botón de descarga** (la flecha hacia abajo).
4. Se descarga un archivo parecido a `kali-linux-2026.3-virtualbox-amd64.7z` (unos **3–4 GB**; tardará un rato).
5. Cuando termine, **mueve** el archivo de **Descargas** a **`C:\labSI`**.

**b) Comprobar que el archivo no está dañado ni manipulado (integridad)**

Kali publica la **huella digital (hash SHA-256)** de cada archivo. Si nuestro archivo tiene la misma huella, es idéntico al original.

1. En la página de descargas de Kali, junto al botón de descarga hay un icono o enlace **sum** / **SHA256**. Púlsalo y verás una cadena larga de letras y números. **Cópiala** y pégala en el **Bloc de notas**.
2. Abre **`C:\labSI`** en el Explorador de archivos.
3. Haz **clic en la barra de direcciones** (donde pone `C:\labSI`), escribe `powershell` y pulsa **`Intro`**. Se abre una ventana azul (o negra) de **PowerShell** ya situada en esa carpeta.
4. Escribe este comando (usa la tecla **`Tab`** para completar el nombre del archivo después de escribir `.\kali`) y pulsa **`Intro`**:

```powershell
Get-FileHash .\kali-linux-2026.3-virtualbox-amd64.7z -Algorithm SHA256
```

| Parte del comando | Qué significa |
|---|---|
| `Get-FileHash` | "Calcula la huella (hash) de un archivo". |
| `.\kali-linux-...7z` | El archivo: `.\` significa "en esta carpeta". |
| `-Algorithm SHA256` | Usa el algoritmo **SHA-256**. |

5. Compara la columna **Hash** con la que copiaste de la web. Fíjate en los **primeros y los últimos 6 caracteres** (no importan mayúsculas o minúsculas).
   - **Iguales:** el archivo está bien.
   - **Distintos:** la descarga está dañada. Bórrala y descárgala de nuevo.

> **Esto es seguridad informática:** acabas de garantizar la **integridad** del archivo (uno de los principios de la UD01). Un archivo modificado por un atacante tendría una huella distinta.

**c) Descomprimir**

El archivo está comprimido en formato **`.7z`**.

- **Windows 11:** clic derecho sobre el archivo → **Extraer todo...** → en el destino deja `C:\labSI` → **Extraer**.
- **Windows 10** (o si no aparece *Extraer todo*): instala **7-Zip** desde `https://www.7-zip.org` (elige la versión **64-bit x64**). Después: clic derecho sobre el archivo → **7-Zip → Extraer aquí** (en Windows 11, primero **Mostrar más opciones**).

Tarda unos minutos. Se crea una carpeta llamada `kali-linux-2026.3-virtualbox-amd64` con **dos archivos** dentro:

| Archivo | Qué es |
|---|---|
| `...vbox` | La **configuración** de la máquina (memoria, red, etc.). |
| `...vdi` | El **disco duro** de la máquina, con Kali ya instalado. |

> ✅ **Comprueba:** dentro de `C:\labSI\kali-linux-...` ves un archivo `.vbox` y uno `.vdi` (el `.vdi` ocupa más de 10 GB). Cuando lo veas, puedes **borrar el `.7z`** para recuperar espacio.

> Si no ves la extensión (`.vbox`, `.vdi`), en el Explorador ve a **Vista → Mostrar → Extensiones de nombre de archivo** (Windows 11) o marca **Vista → Extensiones de nombre de archivo** (Windows 10).

### 1.5. Descargar y descomprimir Metasploitable 2

1. Entra en `https://sourceforge.net/projects/metasploitable/files/Metasploitable2/`.
2. Haz clic en **`metasploitable-linux-2.0.0.zip`**. Espera unos segundos y empezará la descarga (unos **830 MB**).
3. Mueve el archivo a **`C:\labSI`**.
4. Clic derecho sobre él → **Extraer todo...** → destino `C:\labSI` → **Extraer**.

Se crea la carpeta **`Metasploitable2-Linux`**. Dentro, el archivo importante es **`Metasploitable.vmdk`**: es el **disco duro** de la máquina, ya instalado y listo.

> ✅ **Comprueba:** existe `C:\labSI\Metasploitable2-Linux\Metasploitable.vmdk`.

### 1.6. Añadir Kali a VirtualBox

Kali ya viene como máquina de VirtualBox: solo hay que decirle a VirtualBox dónde está.

1. Abre **Oracle VirtualBox**.
2. Menú **Máquina → Añadir...** (o el botón **Añadir** de la barra superior).
3. Ve a `C:\labSI\kali-linux-...` y selecciona el archivo **`.vbox`**. Pulsa **Abrir**.
4. Aparece en la lista de la izquierda una máquina llamada `kali-linux-2026.3-virtualbox-amd64` (o parecido).

**Cambiarle el nombre y ajustar la memoria:**

1. Haz clic sobre la máquina de Kali y pulsa **Configuración** (el engranaje).
2. **General → Básico → Nombre:** escribe `Kali`.
3. **Sistema → Placa base → Memoria base:**
   - Si tu equipo tiene **más de 8 GB** de RAM: `4096 MB`.
   - Si tiene **8 GB o menos**: `2048 MB`.
4. **Sistema → Procesador:** `2` CPU.
5. Pulsa **Aceptar**.

> Si en la ventana de Configuración no ves todas las opciones, arriba a la derecha cambia de **Básico** a **Experto**.

> ✅ **Comprueba:** en la lista de la izquierda aparece **Kali**, apagada.

### 1.7. Crear la máquina Metasploitable 2

Metasploitable no viene como máquina de VirtualBox, solo trae el disco. Así que **creamos una máquina vacía y le conectamos ese disco**.

1. Pulsa **Nueva** (el icono de la estrella azul).
2. **Nombre y sistema operativo:**
   - **Nombre:** `Metasploitable2`
   - **Carpeta:** déjala como está.
   - **Imagen ISO:** **déjalo vacío** (no vamos a instalar nada).
   - **Tipo:** `Linux`
   - **Subtipo** (si aparece): `Ubuntu`
   - **Versión:** `Ubuntu (32-bit)`. Si no aparece, elige `Ubuntu (64-bit)`; también funciona.
   - Pulsa **Siguiente**.
3. **Hardware:**
   - **Memoria base:** `512 MB`
   - **Procesadores:** `1`
   - Pulsa **Siguiente**.
4. **Disco duro virtual:**
   - Elige **Usar un archivo de disco duro virtual existente**.
   - Pulsa el **icono de la carpeta** a la derecha. Se abre el **Selector de medio**.
   - Pulsa **Añadir**, ve a `C:\labSI\Metasploitable2-Linux`, selecciona **`Metasploitable.vmdk`** y pulsa **Abrir**.
   - Selecciona `Metasploitable.vmdk` en la lista y pulsa **Seleccionar** (o **Elegir**).
   - Pulsa **Siguiente**.
5. Revisa el **Resumen** y pulsa **Terminar**.

> **No hay que instalar nada:** el sistema ya está dentro del disco.

> ✅ **Comprueba:** en la lista aparece **Metasploitable2**, apagada. Si la seleccionas, en el panel de la derecha, en **Almacenamiento**, aparece `Metasploitable.vmdk`.

### 1.8. Configurar la RED INTERNA AISLADA (paso crítico)

Este es el paso más importante para que la práctica sea **legal y segura**. Hazlo **en las dos máquinas**, con las dos **apagadas**.

**a) Kali**

1. Selecciona **Kali** → **Configuración** → **Red**.
2. Pestaña **Adaptador 1**:
   - Marca **Habilitar adaptador de red**.
   - **Conectado a:** `Red interna`
   - **Nombre:** escribe exactamente `labSI` (`lab` en minúsculas y `SI` en mayúsculas).
3. Revisa las pestañas **Adaptador 2, 3 y 4**: las tres deben tener **desmarcado** *Habilitar adaptador de red*.
4. Pulsa **Aceptar**.

**b) Metasploitable2**

Repite exactamente lo mismo: **Configuración → Red → Adaptador 1 → Red interna → Nombre `labSI`**, y adaptadores 2, 3 y 4 deshabilitados.

> **Muy importante:** con **Red interna** las máquinas se ven entre sí pero **no tienen acceso a Internet ni a la red del instituto**. Esto mantiene la práctica dentro de la ley. **Nunca** cambies Metasploitable a **NAT** ni a **Adaptador puente**: es un sistema vulnerable a propósito y quedaría expuesto.

**c) Dar IP automática a las máquinas (servidor DHCP del laboratorio)**

Una red interna de VirtualBox está "vacía": nadie reparte direcciones IP. Vamos a crear un pequeño **servidor DHCP virtual** que solo funciona dentro de `labSI`. Esto **no tiene botón** en la ventana de VirtualBox, así que se hace con un comando:

1. Pulsa la tecla **`Windows`**, escribe `cmd` y abre **Símbolo del sistema** (no hace falta como administrador).
2. Escribe este comando para entrar en la carpeta de VirtualBox y pulsa **`Intro`**:

```bat
cd "C:\Program Files\Oracle\VirtualBox"
```

`cd` significa "cambiar de carpeta". Las comillas son necesarias porque la ruta tiene espacios.

3. Escribe este comando **en una sola línea** (puedes copiarlo y pegarlo con clic derecho) y pulsa **`Intro`**:

```bat
VBoxManage dhcpserver add --network=labSI --server-ip=10.10.10.1 --netmask=255.255.255.0 --lower-ip=10.10.10.10 --upper-ip=10.10.10.50 --enable
```

| Parte del comando | Qué significa |
|---|---|
| `VBoxManage` | Herramienta de VirtualBox para usar desde comandos. |
| `dhcpserver add` | Crea un servidor DHCP. |
| `--network=labSI` | Solo funcionará en nuestra red interna `labSI`. |
| `--server-ip=10.10.10.1` | IP del propio servidor DHCP. |
| `--netmask=255.255.255.0` | Máscara de red: la red es `10.10.10.0/24`. |
| `--lower-ip` / `--upper-ip` | Rango de IP que repartirá: de `10.10.10.10` a `10.10.10.50`. |
| `--enable` | Lo deja activado. |

Si no sale nada, **ha funcionado** (en los comandos, "sin mensaje" suele significar "sin errores").

4. Comprueba que existe:

```bat
VBoxManage list dhcpservers
```

Debe aparecer un bloque con `NetworkName: labSI` y `Enabled: Yes`.

5. **Comprobación final de la red** de las dos máquinas:

```bat
VBoxManage showvminfo Kali --machinereadable | findstr /b "nic1 intnet1"
VBoxManage showvminfo Metasploitable2 --machinereadable | findstr /b "nic1 intnet1"
```

`showvminfo` muestra toda la configuración de una máquina y `findstr` filtra solo las líneas de la red. En **las dos** debe salir:

```
nic1="intnet"
intnet1="labSI"
```

> ✅ **Comprueba:** las dos máquinas muestran `nic1="intnet"` e `intnet1="labSI"`, y el servidor DHCP de `labSI` está `Enabled: Yes`. Si alguna muestra `nat` o `bridged`, **repite el paso a o b** antes de arrancar nada.

### 1.9. Guardar una "foto" de las máquinas (instantánea)

Una **instantánea** (*snapshot*) guarda el estado exacto de la máquina. Si algo se estropea, puedes volver a él en segundos. Es la versión "de laboratorio" de una **copia de seguridad**.

1. En la lista de la izquierda, junto al nombre **Metasploitable2**, pulsa el **icono de menú** (tres rayas **≡**) → **Instantáneas**.
2. Pulsa **Tomar** (icono de la cámara).
3. **Nombre:** `limpio`. **Descripción:** `Recién montada`. Pulsa **Aceptar**.
4. Repite con **Kali**.

> Para volver a una instantánea: máquina **apagada** → **Instantáneas** → selecciona `limpio` → **Restaurar**.

### 1.10. Arrancar y obtener las direcciones IP

> **Ratón "atrapado":** si haces clic dentro de la ventana de una máquina y el ratón no sale, pulsa la tecla **`Ctrl` derecha** (la "tecla anfitrión" de VirtualBox). Lo mismo con el teclado.

**a) Arranca Metasploitable 2**

1. Selecciona **Metasploitable2** y pulsa **Iniciar** (la flecha verde).
2. Se abre una ventana negra con muchas líneas de texto. Espera hasta que aparezca `metasploitable login:`.
3. Escribe el usuario `msfadmin` y pulsa **`Intro`**.
4. Escribe la contraseña `msfadmin` y pulsa **`Intro`**. **Al escribir la contraseña no se ve nada en pantalla**: es normal.
5. Escribe:

```bash
ifconfig
```

6. Busca el bloque **`eth0`** y la línea `inet addr:`. Verás algo como `10.10.10.10`.

**Anota la IP del objetivo:** `________________`

> Metasploitable usa el teclado **inglés**. Si una tecla no sale como esperas, recuerda que el usuario y la contraseña solo tienen letras: escríbelos con cuidado.

**b) Arranca Kali Linux**

1. Vuelve a la ventana de VirtualBox, selecciona **Kali** y pulsa **Iniciar**.
2. Espera a que aparezca la pantalla de inicio de sesión.
3. Usuario `kali`, contraseña `kali`.
4. Abre una **terminal**: icono de la pantalla negra en la barra superior (o clic derecho en el escritorio → **Open Terminal Here**).
5. Si el teclado no escribe bien los símbolos, pon el teclado en español:

```bash
setxkbmap es
```

6. Escribe:

```bash
ip a
```

7. Busca la interfaz **`eth0`** y la línea `inet`. Verás algo como `10.10.10.11/24` (el `/24` no forma parte de la IP).

**Anota la IP de Kali:** `________________`

> **Si alguna máquina no tiene IP** (en `eth0` no aparece ninguna `inet`): revisa el apartado 1.8 y, después, en esa máquina ejecuta `sudo dhclient eth0` (contraseña `kali` en Kali o `msfadmin` en Metasploitable) para pedir IP de nuevo. Si sigue sin funcionar, avisa al profesor/a.

### 1.11. Comprobar que se "ven" (y que NO salen a Internet)

Todo esto se hace en la **terminal de Kali**.

**a) ¿Kali ve al objetivo?**

```bash
ping -c 4 <IP_del_objetivo>
```

`ping` envía mensajes de prueba; `-c 4` envía solo 4. Debes ver 4 líneas `64 bytes from ...` y, al final, `0% packet loss` (0 % de paquetes perdidos).

**b) ¿El laboratorio está aislado?**

```bash
ping -c 4 8.8.8.8
```

`8.8.8.8` es un servidor de Internet. Esta vez **debe fallar**: `Network is unreachable` o `100% packet loss`. Eso confirma que Kali **no tiene salida a Internet**.

> ✅ **Comprueba:** el primer `ping` **funciona** y el segundo **falla**. Si es así, el laboratorio está listo.

**Haz una captura de pantalla** de los dos `ping` (la necesitarás en la parte evaluable). En Windows: **`Windows` + `Shift` + `S`**, selecciona la zona y pega la imagen en Paint o guárdala desde la notificación.

### 1.12. Si algo falla

| Mensaje o síntoma | Causa probable | Solución |
|---|---|---|
| `VT-x is not available` / `AMD-V is disabled in the BIOS` | La virtualización está desactivada en el ordenador. | Activarla en la BIOS/UEFI (*Intel Virtualization Technology* o *SVM Mode*). Avisa al profesor/a. |
| La máquina va **lentísima** y abajo a la derecha de su ventana sale una **tortuga verde** | Windows tiene activado **Hyper-V** o el **Aislamiento del núcleo**, y VirtualBox no puede usar el procesador directamente. | Avisa al profesor/a (ver anexo del profesorado). |
| No aparece el botón o la opción que dice la guía | Tu versión de VirtualBox coloca el menú en otro sitio. | En **Configuración**, cambia de **Básico** a **Experto** (arriba a la derecha). |
| No encuentro el `.vbox` al **Añadir** Kali | El archivo no se ha descomprimido bien o no ves las extensiones. | Repite 1.4 c y activa **Mostrar extensiones** en el Explorador. |
| `Failed to open... Metasploitable.vmdk` / *UUID already exists* | El disco ya estaba registrado (por ejemplo, de un intento anterior). | **Archivo → Herramientas → Gestor de medios virtuales**, quita `Metasploitable.vmdk` de la lista (**Liberar** y **Eliminar**, sin borrar el archivo) y repite 1.7. |
| `"VBoxManage" no se reconoce como un comando interno o externo` | No estás en la carpeta de VirtualBox. | Repite `cd "C:\Program Files\Oracle\VirtualBox"` (con comillas). |
| `dhcpserver add`: *already exists* | Ya creaste el servidor DHCP antes. | No pasa nada: ya está hecho. Compruébalo con `VBoxManage list dhcpservers`. |
| La Hash de Kali **no coincide** | Descarga incompleta o dañada. | Borra el `.7z` y descárgalo de nuevo. |
| Una máquina no recibe IP | Red o DHCP mal configurados. | Repite las comprobaciones de 1.8 y ejecuta `sudo dhclient eth0` dentro de la máquina. |
| El ratón o el teclado no salen de la máquina | La máquina los ha "capturado". | Pulsa **`Ctrl` derecho**. |
| En Kali, los símbolos del teclado salen cambiados | Teclado en inglés. | `setxkbmap es` en la terminal de Kali. |

### 1.13. Apagar las máquinas al terminar

- En **Metasploitable**: escribe `sudo halt` y la contraseña `msfadmin`.
- En **Kali**: menú de usuario (arriba a la derecha) → **Shut Down**, o en su terminal `sudo poweroff`.
- Si alguna se queda colgada: en VirtualBox, clic derecho sobre la máquina → **Cerrar → Apagar**. Es como "tirar del cable": úsalo solo si no responde.

---

## 2. Práctica guiada con Nmap (NO evaluable)

> **Objetivo:** aprender a usar **Nmap** paso a paso. Sigue las instrucciones y ve observando qué devuelve cada comando. Esta parte **no puntúa**: es para aprender. Todo se hace en la **terminal de Kali**, con las **dos máquinas encendidas**.

**Nmap** (*Network Mapper*) es la herramienta de **fingerprinting** que cita la UD01: sirve para descubrir qué equipos hay, qué puertos tienen abiertos y qué servicios y versiones ejecutan. Kali ya lo trae instalado.

> **Recuerda:** sustituye `<IP_del_objetivo>` por la IP de Metasploitable que anotaste en 1.10 (por ejemplo `10.10.10.10`). **Nunca** escribas otra dirección.

### Antes de empezar: dos conceptos

| Concepto | Explicación sencilla |
|---|---|
| **Puerto** | Una "puerta" numerada por la que un equipo ofrece un servicio. Por ejemplo, las páginas web suelen usar el puerto **80** y el acceso remoto seguro (SSH), el **22**. Hay 65 535 puertos posibles. |
| **Servicio** | El programa que "atiende" detrás de un puerto abierto (un servidor web, un servidor FTP...). Cada uno tiene su **versión**, y algunas versiones tienen fallos conocidos. |

### Paso 1 · Descubrir si el objetivo está activo

```bash
nmap -sn <IP_del_objetivo>
```

- `nmap` → el programa.
- `-sn` → "solo comprueba si la máquina responde", **sin mirar puertos**. Es la forma más discreta de saber si un equipo está encendido.

**Qué debes ver:** una línea con **`Host is up`** ("el equipo está activo").

> **Pregúntate:** ¿en qué se parece esto al `ping` del apartado 1.11?

### Paso 2 · Ver qué puertos están abiertos

```bash
nmap <IP_del_objetivo>
```

Sin opciones, Nmap revisa los **1000 puertos más habituales**. Tarda unos segundos.

**Qué debes ver:** una tabla como esta (la tuya tendrá **muchas más líneas**):

```
PORT   STATE SERVICE
21/tcp open  ftp
22/tcp open  ssh
80/tcp open  http
...
```

| Columna | Qué significa |
|---|---|
| `PORT` | Número de puerto y protocolo (`tcp`). |
| `STATE` | `open` = abierto: hay un servicio escuchando. |
| `SERVICE` | El servicio que **suele** usar ese puerto (Nmap lo **supone** por el número; todavía no lo ha comprobado). |

Cada puerto abierto es un **servicio** accesible, y por tanto una posible **vía de entrada**. Un servidor bien protegido solo tiene abiertos los puertos que de verdad necesita.

> **Pregúntate:** ¿cuántos puertos abiertos tiene el objetivo? ¿Te parece que son muchos para un servidor?

### Paso 3 · Averiguar servicios y versiones (fingerprinting)

```bash
nmap -sV <IP_del_objetivo>
```

- `-sV` → *Service Version*: Nmap "habla" con cada puerto abierto para averiguar **qué programa y qué versión** hay detrás. Tarda más que el paso 2 (puede llegar a un par de minutos): espera sin cerrar nada.

**Qué debes ver:** la misma tabla, pero con una columna nueva, **`VERSION`**, por ejemplo:

```
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 2.3.4
80/tcp open  http    Apache httpd 2.2.8 ((Ubuntu) DAV/2)
...
```

Esta información es **clave**: conociendo la versión exacta de un programa se pueden buscar **vulnerabilidades conocidas (CVE)**, que es lo que estudiamos en la UD01. Una versión antigua suele significar fallos que ya son públicos.

> **Pregúntate:** ¿qué diferencia hay entre la columna `SERVICE` del paso 2 y la columna `VERSION` de este paso?

### Paso 4 · Intentar identificar el sistema operativo

```bash
sudo nmap -O <IP_del_objetivo>
```

- `-O` (letra **O** mayúscula, no el número cero) → intenta **adivinar el sistema operativo** del objetivo por cómo responde a ciertos paquetes.
- `sudo` → este tipo de escaneo necesita permisos de administrador. Te pedirá la contraseña de Kali (`kali`); al escribirla no se ve nada.

**Qué debes ver:** al final, líneas como `Running:` y `OS details:` con una estimación (por ejemplo, una versión de **Linux 2.6.x**). Es una **estimación**, no una certeza.

### Paso 5 · Guardar los resultados en un archivo (para tu informe)

Un auditor siempre **guarda las evidencias**. Prueba a repetir el paso 3 guardando el resultado:

```bash
nmap -sV <IP_del_objetivo> -oN escaneo_versiones.txt
```

- `-oN escaneo_versiones.txt` → además de mostrarlo en pantalla, guarda el resultado en el archivo `escaneo_versiones.txt` (formato normal, legible).

Para ver el archivo:

```bash
cat escaneo_versiones.txt
```

### Resumen de lo aprendido

| Comando | Para qué sirve | Fase de la auditoría |
|---|---|---|
| `nmap -sn <IP>` | Saber si el equipo está activo. | Descubrimiento (footprinting) |
| `nmap <IP>` | Ver los puertos abiertos. | Fingerprinting |
| `nmap -sV <IP>` | Ver servicios y **versiones**. | Fingerprinting |
| `sudo nmap -O <IP>` | Estimar el sistema operativo. | Fingerprinting |
| `... -oN archivo.txt` | Guardar los resultados como evidencia. | Documentación |

Observa, comenta en clase lo que ves y practica los comandos hasta que entiendas qué hace cada uno. Cuando lo tengas claro, **apaga las máquinas** (apartado 1.13) y pasa al **Documento 2: parte evaluable (informe de auditoría)**.

---

## Anexo para el profesorado · notas de montaje (Windows)

- **Metasploitable 2** debe permanecer **siempre** en red interna. Nunca en NAT ni puente: es un sistema deliberadamente vulnerable.
- **VirtualBox:** la guía está pensada para **VirtualBox 7.1/7.2** sobre Windows 10/11 de 64 bits. Instalarlo requiere permisos de administrador; si el alumnado no los tiene, conviene dejarlo instalado antes de la sesión 1.
- **Hyper-V, WSL2 y "Integridad de memoria":** si están activos, VirtualBox funciona en modo compatibilidad (icono de **tortuga verde**) y las máquinas van muy lentas o no arrancan. Para desactivarlos (requiere administrador y reiniciar):
  - **Seguridad de Windows → Seguridad del dispositivo → Aislamiento del núcleo → Integridad de memoria: Desactivado.**
  - En un **Símbolo del sistema como administrador**: `bcdedit /set hypervisorlaunchtype off`. Para revertirlo: `bcdedit /set hypervisorlaunchtype auto`.
  - Valorar el impacto antes de hacerlo en equipos donde se use WSL2, Docker Desktop o el Subsistema de Android.
- **Imágenes precargadas:** para no saturar la conexión del aula (Kali ocupa 3–4 GB por equipo), se recomienda dejar el `.7z` de Kali, su hash SHA-256 y `metasploitable-linux-2.0.0.zip` en una carpeta compartida o USB. El alumnado puede hacer igualmente la comprobación con `Get-FileHash`.
- **Sin DHCP:** si se prefiere no usar `VBoxManage dhcpserver`, se puede asignar IP fija. En Metasploitable: `sudo ifconfig eth0 10.10.10.2 netmask 255.255.255.0`. En Kali: `sudo ip addr add 10.10.10.3/24 dev eth0`. Ambas se pierden al reiniciar.
- Alternativas al objetivo si se prefiere algo más ligero: una VM con **Metasploitable 2** es la recomendada por su variedad de servicios y por existir CVE bien documentados (p. ej. vsftpd 2.3.4 → CVE-2011-2523; Samba → CVE-2007-2447). También sirve cualquier VM Linux antigua preparada por el centro.
- Para buscar CVE sin salida a Internet en las VM, se puede habilitar el buscador en los equipos del aula (no en las VM) o proporcionar un listado offline de CVE de los servicios de Metasploitable 2.
- Tiempos orientativos: sesión 1 montaje del laboratorio; sesión 2 parte guiada; sesiones 3–4 parte autónoma e informe (Documento 2).
- **Limpieza al final del curso:** en VirtualBox, clic derecho sobre cada máquina → **Eliminar → Borrar todos los archivos**; y en un Símbolo del sistema (desde `C:\Program Files\Oracle\VirtualBox`): `VBoxManage dhcpserver remove --network=labSI`. Después se puede borrar `C:\labSI`.
