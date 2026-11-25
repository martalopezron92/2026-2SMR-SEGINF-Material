# Práctica técnica · UD01
## Parte guiada — Montaje del laboratorio y primeros pasos con Nmap

> **IMPORTANTE:** este documento es la **parte guiada y NO evaluable**. Sirve para montar el laboratorio y aprender a usar las herramientas con ayuda. **No se entrega**, pero es **obligatorio** haberla realizado antes de pasar al Documento 2 (la parte evaluable).

| | |
|---|---|
| **Módulo** | Seguridad Informática · 2º SMR |
| **Instrumento** | Práctica técnica (40 % de la UD01) — **esta parte no puntúa** |
| **Duración orientativa** | 2 sesiones (montaje + práctica guiada) |
| **Equipo anfitrión** | Linux Mint 21 o 22 (montaje por terminal) |

> **Qué vas a hacer:** montar un pequeño "laboratorio" con dos máquinas virtuales aisladas y practicar las **primeras fases de una auditoría de caja negra** (footprinting y fingerprinting) con **Nmap**, tal y como se explica en la UD01. **No se ataca ni se explota nada:** solo se observa y se analiza, igual que hace un auditor antes de emitir su informe.

---

## 0. Normas éticas y legales (OBLIGATORIO leer y firmar)

Las técnicas de esta práctica **solo son legales sobre sistemas propios o con autorización expresa por escrito**. Usarlas contra equipos o redes ajenas sin permiso es un **delito** (arts. 197 bis y 264 del Código Penal) y contradice el principio que estudiamos: la diferencia entre un PenTest y un ataque real es **la autorización**.

En esta práctica:

- Todo se hace en **máquinas virtuales propias**, en una **red aislada sin salida a Internet**.
- **Nunca** se escanean equipos del instituto, de casa, redes WiFi públicas ni direcciones de Internet.
- La práctica se queda en **reconocimiento y análisis**; no se ejecutan exploits ni se modifica ningún sistema.


---

## 1. Preparación del laboratorio en Linux Mint (paso a paso por terminal)

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

Todo el montaje se hace desde la **terminal de Linux Mint** (el equipo físico, al que llamamos **anfitrión**). Para abrirla: menú → *Terminal*, o pulsa **`Ctrl` + `Alt` + `T`**.

> **Cómo leer esta guía:**
> - Cada bloque gris es un comando. **Escríbelo (o cópialo) y pulsa `Intro`**. Debajo tienes explicado qué hace.
> - En la terminal se pega con **`Ctrl` + `Shift` + `V`** (no con `Ctrl` + `V`).
> - Lo que va entre `< >` hay que **cambiarlo** por tu dato (sin los símbolos `< >`).
> - Cuando un comando empieza por **`sudo`**, se ejecuta como administrador y te pedirá **tu contraseña** de Linux Mint. Al escribirla **no se ve nada en pantalla**: es normal, escríbela y pulsa `Intro`.
> - La tecla **`Tab`** autocompleta nombres de archivos y carpetas. Úsala: evita errores de escritura.

### 1.1. Comprobaciones previas

Antes de instalar nada, comprueba que tu equipo puede con el laboratorio.

```bash
lscpu | grep -i virtualiz
```

Muestra si el procesador admite **virtualización por hardware**. Debe aparecer `VT-x` (Intel) o `AMD-V` (AMD). Si no sale nada, hay que activarla en la BIOS/UEFI del equipo (avisa al profesor/a).

```bash
free -h
```

Muestra la **memoria RAM**. En la fila `Mem:`, columna `total`, necesitas **al menos 8 GB** para tener las dos máquinas encendidas a la vez con soltura (con 4 GB funciona, pero muy justo).

```bash
df -h ~
```

Muestra el **espacio libre** en tu carpeta personal (`~` significa "mi carpeta personal"). Mira la columna `Disp`: necesitas **unos 30 GB libres** (las imágenes descargadas + las descomprimidas).

### 1.2. Instalar VirtualBox (versión oficial de Oracle)

**a) ¿Ya tienes VirtualBox? Compruébalo primero**

```bash
VBoxManage --version
```

- Si muestra un número que empieza por **7.1 o 7.2** (por ejemplo `7.2.22r175245`), **ya lo tienes instalado: sáltate este apartado** y ve directamente a 1.3.
- Si dice `VBoxManage: orden no encontrada`, sigue con los pasos de abajo.

> **⚠️ No instales el VirtualBox de los repositorios de Linux Mint/Ubuntu** (`sudo apt install virtualbox`). Es una versión antigua (7.0) que **no funciona con los núcleos recientes**: falla al instalarse (`Bad return status for module build`) y, si ya tenías el VirtualBox de Oracle, **lo desinstala**. Usa siempre el de Oracle, como se explica aquí.

**b) Instalar las herramientas para compilar el módulo de VirtualBox**

```bash
sudo apt update
sudo apt install -y build-essential dkms linux-headers-$(uname -r) wget gpg
```

- `sudo apt update` actualiza la **lista de programas** disponibles. No instala nada, solo "refresca el catálogo".
- La segunda línea instala lo que VirtualBox necesita para crear su **módulo del núcleo** (*kernel*), la pieza que le permite usar el hardware: el compilador (`build-essential`), `dkms` y las **cabeceras del núcleo** que estás usando (`$(uname -r)` se sustituye solo por tu versión del núcleo). La opción `-y` responde "sí" automáticamente.

**c) Añadir la clave de Oracle**

```bash
wget -O- https://www.virtualbox.org/download/oracle_vbox_2016.asc | sudo gpg --dearmor --yes --output /usr/share/keyrings/oracle-virtualbox-2016.gpg
```

Descarga la **clave pública** de Oracle y la guarda en el sistema. Con ella, `apt` comprobará que los paquetes de VirtualBox están **firmados por Oracle** y no han sido manipulados (autenticidad e integridad, otra vez la UD01).

**d) Añadir el repositorio de Oracle**

```bash
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/oracle-virtualbox-2016.gpg] https://download.virtualbox.org/virtualbox/debian noble contrib" | sudo tee /etc/apt/sources.list.d/virtualbox.list
```

Crea el archivo `virtualbox.list`, que le dice a `apt` que hay un **repositorio** (almacén de programas) nuevo: el de Oracle, firmado con la clave del paso anterior.

> `noble` es el nombre de la versión de Ubuntu en la que se basa **Linux Mint 22**. Si tienes **Linux Mint 21**, cambia `noble` por `jammy`. Para saberlo: `grep UBUNTU_CODENAME /etc/os-release`.

**e) Instalar VirtualBox 7.2**

```bash
sudo apt update
sudo apt install -y virtualbox-7.2
```

Vuelve a refrescar el catálogo (ahora incluye el repositorio de Oracle) e instala **VirtualBox 7.2**: la ventana gráfica, la herramienta de terminal `VBoxManage` y su módulo del núcleo. Al terminar, **lee los últimos mensajes**: no debe aparecer ningún `error`.

> **Si durante la instalación aparece una pantalla azul hablando de "Secure Boot" (arranque seguro):** te pide crear una contraseña. Invéntate una sencilla (por ejemplo `12345678`), apúntala y continúa. Al **reiniciar** el equipo saldrá una pantalla azul (*MOK management*): elige **Enroll MOK → Continue → Yes**, escribe esa contraseña y reinicia. Si no lo haces, VirtualBox no podrá arrancar máquinas.

**f) Dar permiso a tu usuario**

```bash
sudo usermod -aG vboxusers $USER
```

Añade tu usuario (`$USER` se sustituye solo por tu nombre de usuario) al grupo **`vboxusers`**, que es el grupo de usuarios autorizados a usar VirtualBox por completo. Para que el cambio tenga efecto, **cierra la sesión y vuelve a entrar** (o reinicia el equipo).

**g) Comprueba que ha funcionado**

```bash
VBoxManage --version
```

Debe mostrar un número de versión que empieza por `7.2` (por ejemplo `7.2.22r175245`). **`VBoxManage`** es la herramienta de terminal de VirtualBox: con ella vamos a hacer todo lo demás.

> **Si al usar VirtualBox sale `Kernel driver not installed`:** ejecuta `sudo /sbin/vboxconfig`, que vuelve a crear y cargar el módulo del núcleo. Lee el final de lo que muestra: si habla de Secure Boot, mira el recuadro de arriba.

### 1.3. Crear la carpeta del laboratorio

```bash
mkdir -p ~/labSI
cd ~/labSI
```

- `mkdir -p ~/labSI` crea (*make directory*) una carpeta llamada `labSI` dentro de tu carpeta personal. La opción `-p` evita un error si ya existía.
- `cd ~/labSI` entra (*change directory*) en esa carpeta. A partir de aquí, todo lo que descarguemos se guardará en ella.

> **Si el aula ya tiene las imágenes descargadas** (en una carpeta compartida o en un USB), cópialas a `~/labSI` y **sáltate los apartados 1.4 y 1.5 hasta el paso de descomprimir**.

### 1.4. Descargar y descomprimir Kali Linux

**a) Instalar el descompresor de archivos `.7z`**

```bash
sudo apt install -y p7zip-full
```

Kali se distribuye comprimido en formato **`.7z`**. Este paquete instala el programa `7z` para descomprimirlo.

**b) Averiguar el nombre exacto del archivo**

Kali saca una versión nueva cada pocos meses, así que el nombre del archivo cambia. Abre en el navegador `https://cdimage.kali.org/current/` y busca el archivo que termina en **`-virtualbox-amd64.7z`**. Por ejemplo: `kali-linux-2026.3-virtualbox-amd64.7z`.

Guarda ese nombre **sin el `.7z`** en una **variable** de la terminal (así no tienes que escribirlo entero cada vez):

```bash
KALI=kali-linux-2026.3-virtualbox-amd64
```

Cambia `2026.3` por la versión que hayas visto en la web. **Ojo:** sin espacios alrededor del `=`. Para comprobar lo que has guardado:

```bash
echo $KALI
```

> La variable solo existe **en esa ventana de terminal**. Si la cierras, vuelve a escribir la línea `KALI=...`.

**c) Descargar**

```bash
wget https://cdimage.kali.org/current/$KALI.7z
```

`wget` descarga un archivo de Internet a la carpeta en la que estás. Verás una barra de progreso. Ocupa unos **3–4 GB**, así que tardará un rato.

**d) Comprobar que el archivo no está dañado ni manipulado (integridad)**

```bash
wget https://cdimage.kali.org/current/SHA256SUMS
grep $KALI.7z SHA256SUMS | sha256sum -c -
```

- El primer comando descarga `SHA256SUMS`, una lista oficial con la **huella digital (hash SHA-256)** de cada archivo de Kali.
- El segundo busca (`grep`) la línea de nuestro archivo y se la pasa (`|`) a `sha256sum -c`, que calcula la huella del archivo descargado y la compara con la oficial.
- Debe responder **`... .7z: La suma coincide`** (o `OK`). Si dice que **no coincide**, la descarga está corrupta: bórrala y vuelve a descargarla.

> **Esto es seguridad informática:** acabas de garantizar la **integridad** del archivo (uno de los principios de la UD01). Un archivo modificado por un atacante tendría una huella distinta.

**e) Descomprimir**

```bash
7z x $KALI.7z
```

`7z x` extrae (*extract*) el contenido manteniendo las carpetas. Se crea una carpeta con el mismo nombre que contiene dos archivos: uno **`.vbox`** (la configuración de la máquina) y uno **`.vdi`** (su disco duro). Compruébalo:

```bash
ls $KALI
```

### 1.5. Descargar y descomprimir Metasploitable 2

```bash
wget -O metasploitable-linux-2.0.0.zip "https://sourceforge.net/projects/metasploitable/files/Metasploitable2/metasploitable-linux-2.0.0.zip/download"
```

Descarga Metasploitable 2 desde SourceForge (unos **830 MB**). La opción **`-O`** indica con qué nombre guardar el archivo (si no, se llamaría `download`). La dirección va entre comillas para que la terminal no interprete ningún carácter raro.

```bash
unzip metasploitable-linux-2.0.0.zip
```

Descomprime el `.zip`. Se crea la carpeta **`Metasploitable2-Linux`**. Dentro, el archivo importante es **`Metasploitable.vmdk`**: es el **disco duro** de la máquina, ya instalado y listo.

```bash
ls Metasploitable2-Linux
```

> Si te dice `unzip: orden no encontrada`, instálalo con `sudo apt install -y unzip`.

### 1.6. Registrar Kali en VirtualBox

```bash
VBoxManage registervm ~/labSI/$KALI/$KALI.vbox
```

**`registervm`** "da de alta" en VirtualBox una máquina que ya existe (Kali viene ya creada y configurada; solo hay que decirle a VirtualBox dónde está). Hay que darle la **ruta completa** al archivo `.vbox`; por eso empieza por `~/labSI/...`.

```bash
VBoxManage list vms
```

Lista todas las máquinas registradas. Debe aparecer una con un nombre parecido a `"kali-linux-2026.3-virtualbox-amd64"`. Para trabajar más cómodo, **cámbiale el nombre a `Kali`**:

```bash
VBoxManage modifyvm "<nombre_que_aparece_en_la_lista>" --name Kali
```

Por ejemplo: `VBoxManage modifyvm "kali-linux-2026.3-virtualbox-amd64" --name Kali`. **`modifyvm`** cambia la configuración de una máquina; `--name` le pone un nombre nuevo.

**Ajusta la memoria** según la RAM de tu equipo (lo viste con `free -h`):

```bash
VBoxManage modifyvm Kali --memory 4096 --cpus 2
```

- `--memory 4096` → 4 GB de RAM para Kali. Si tu equipo tiene **8 GB o menos**, pon `--memory 2048` (2 GB).
- `--cpus 2` → 2 núcleos de procesador.

### 1.7. Crear la máquina Metasploitable 2

Metasploitable no viene como máquina de VirtualBox, solo trae el disco. Así que **creamos una máquina vacía y le conectamos ese disco**. Son cuatro comandos:

**a) Crear la máquina**

```bash
VBoxManage createvm --name Metasploitable2 --ostype Ubuntu --register
```

- `createvm` crea una máquina nueva.
- `--name Metasploitable2` → su nombre.
- `--ostype Ubuntu` → le decimos que el sistema es **Ubuntu de 32 bits** (Metasploitable 2 está basado en Ubuntu 8.04). Así VirtualBox elige un hardware virtual compatible.
- `--register` → la da de alta en VirtualBox directamente.

**b) Asignar memoria**

```bash
VBoxManage modifyvm Metasploitable2 --memory 512 --cpus 1
```

Metasploitable es un sistema muy ligero: con **512 MB** de RAM y 1 procesador va sobrado.

**c) Añadir una controladora de disco**

```bash
VBoxManage storagectl Metasploitable2 --name "IDE" --add ide
```

Un ordenador necesita una **controladora** a la que enchufar el disco duro. Este comando añade a la máquina una controladora de tipo **IDE** (el tipo clásico, que Metasploitable reconoce sin problemas) y la llama `IDE`.

**d) Conectar el disco `.vmdk`**

```bash
VBoxManage storageattach Metasploitable2 --storagectl "IDE" --port 0 --device 0 --type hdd --medium ~/labSI/Metasploitable2-Linux/Metasploitable.vmdk
```

"Enchufa" el disco descargado a la controladora `IDE`, en la primera posición (`--port 0 --device 0`), indicando que es un disco duro (`--type hdd`). **No hay que instalar nada:** el sistema ya está dentro del disco.

### 1.8. Configurar la RED INTERNA AISLADA (paso crítico)

Este es el paso más importante para que la práctica sea **legal y segura**. Con las dos máquinas **apagadas**:

```bash
VBoxManage modifyvm Kali --nic1 intnet --intnet1 labSI --nic2 none
VBoxManage modifyvm Metasploitable2 --nic1 intnet --intnet1 labSI --nic2 none
```

| Opción | Qué significa |
|---|---|
| `--nic1 intnet` | La **tarjeta de red 1** (*NIC 1*) se conecta a una **red interna** (*internal network*). |
| `--intnet1 labSI` | El **nombre** de esa red interna es `labSI`. Tiene que ser **exactamente igual** en las dos máquinas para que se vean. |
| `--nic2 none` | Nos aseguramos de que **no hay una segunda tarjeta** que pudiera dar salida a Internet. |

> **Muy importante:** con "Red interna" las máquinas se ven entre sí pero **no tienen acceso a Internet ni a la red del instituto**. Esto mantiene la práctica dentro de la ley. **Nunca** cambies Metasploitable a `nat` ni a `bridged` (adaptador puente): es un sistema vulnerable a propósito y quedaría expuesto.

**Darles IP automática (servidor DHCP del laboratorio)**

Una red interna de VirtualBox está "vacía": nadie reparte direcciones IP. Creamos un pequeño **servidor DHCP virtual** que solo da servicio dentro de `labSI`:

```bash
VBoxManage dhcpserver add --network=labSI --server-ip=10.10.10.1 --netmask=255.255.255.0 --lower-ip=10.10.10.10 --upper-ip=10.10.10.50 --enable
```

| Opción | Qué significa |
|---|---|
| `dhcpserver add` | Crea un servidor DHCP de VirtualBox. |
| `--network=labSI` | Solo funcionará en nuestra red interna `labSI`. |
| `--server-ip=10.10.10.1` | IP del propio servidor DHCP. |
| `--netmask=255.255.255.0` | Máscara de red: la red es `10.10.10.0/24`. |
| `--lower-ip` / `--upper-ip` | Rango de IP que repartirá: de `10.10.10.10` a `10.10.10.50`. |
| `--enable` | Lo deja activado. |

**Comprueba que todo está bien configurado** (esta comprobación es obligatoria):

```bash
VBoxManage showvminfo Kali --machinereadable | grep -E '^nic1|^intnet1'
VBoxManage showvminfo Metasploitable2 --machinereadable | grep -E '^nic1|^intnet1'
```

`showvminfo` muestra toda la configuración de una máquina; con `grep` filtramos solo las líneas de la red. En **las dos** debe salir:

```
nic1="intnet"
intnet1="labSI"
```

Si en alguna sale `nic1="nat"` o `nic1="bridged"`, **repite el paso** antes de arrancar nada.

```bash
VBoxManage list dhcpservers
```

Debe aparecer un servidor con `NetworkName: labSI` y `Enabled: Yes`.

### 1.9. Guardar una "foto" de las máquinas (instantánea)

```bash
VBoxManage snapshot Metasploitable2 take limpio --description "Recién montada"
VBoxManage snapshot Kali take limpio --description "Recién montada"
```

Una **instantánea** (*snapshot*) guarda el estado exacto de la máquina. Si algo se estropea, puedes volver a él en segundos con:

```bash
VBoxManage snapshot Metasploitable2 restore limpio
```

(con la máquina apagada). Es la versión "de laboratorio" de una **copia de seguridad**.

### 1.10. Arrancar y obtener las direcciones IP

**a) Arranca Metasploitable 2**

```bash
VBoxManage startvm Metasploitable2
```

`startvm` enciende la máquina y abre su ventana. Espera a que termine de arrancar (salen muchas líneas de texto) y aparezca `metasploitable login:`.

- usuario: `msfadmin` · contraseña: `msfadmin` (al escribir la contraseña no se ve nada, es normal).
- Escribe `ifconfig` y busca en el bloque **`eth0`** la línea `inet addr:`. Deberías ver algo como `10.10.10.10`. **Anótala: es la IP del objetivo.**

> **Ratón "atrapado":** si haces clic dentro de la ventana de una máquina y el ratón no sale, pulsa la tecla **`Ctrl` derecha** (la "tecla anfitrión" de VirtualBox).

**b) Arranca Kali Linux** (desde la terminal de Linux Mint, no desde Metasploitable)

```bash
VBoxManage startvm Kali
```

- Usuario y contraseña por defecto: `kali` / `kali`.
- Si el teclado no escribe bien los símbolos, abre una terminal en Kali y escribe `setxkbmap es` para ponerlo en español.
- En la terminal de Kali escribe:

```bash
ip a
```

Busca la interfaz **`eth0`** y la línea `inet`, por ejemplo `10.10.10.11/24`. **Anota la IP de Kali.**

> **Si alguna máquina no tiene IP** (en `eth0` no aparece ninguna `inet`): revisa el apartado 1.8 y, después, en esa máquina ejecuta `sudo dhclient eth0` para pedir IP de nuevo. Si sigue sin funcionar, avisa al profesor/a.

### 1.11. Comprobar que se "ven" (y que NO salen a Internet)

Desde la terminal de **Kali**, comprueba la conexión con el objetivo:

```bash
ping -c 4 <IP_del_objetivo>
```

`ping` envía mensajes de prueba; `-c 4` envía solo 4. Si ves 4 líneas `64 bytes from ...` y `0% packet loss`, las máquinas se comunican.

Ahora comprueba que el laboratorio **está aislado**:

```bash
ping -c 4 8.8.8.8
```

Esta vez **debe fallar** (`Network is unreachable` o `100% packet loss`). Eso confirma que Kali **no tiene salida a Internet**: el laboratorio está cerrado.

Si el primer ping funciona y el segundo falla, el laboratorio está listo. **Haz una captura de pantalla** de los dos pings (la necesitarás en la parte evaluable).

### 1.12. Apagar las máquinas al terminar

- En **Metasploitable**: `sudo halt` (contraseña `msfadmin`).
- En **Kali**: menú de usuario → *Shut Down*, o en su terminal `sudo poweroff`.
- Si alguna se queda colgada, desde la terminal de Linux Mint:

```bash
VBoxManage controlvm Metasploitable2 poweroff
```

`controlvm ... poweroff` equivale a "tirar del cable": úsalo solo si no responde.

### 1.13. Si algo falla

| Mensaje o síntoma | Causa probable | Solución |
|---|---|---|
| Al instalar: `Error! Bad return status for module build` y `dpkg: error al procesar el paquete virtualbox-dkms` | Se ha instalado el VirtualBox **antiguo de los repositorios de Ubuntu** (7.0), que no compila en núcleos recientes. Si tenías el de Oracle, además lo ha desinstalado. | Quita el antiguo: `sudo apt remove --purge virtualbox virtualbox-qt virtualbox-dkms` y después `sudo apt autoremove`. Luego instala el de Oracle siguiendo **1.2 b–g** (`sudo apt install -y virtualbox-7.2`). |
| `Kernel driver not installed (rc=-1908)` | El módulo del núcleo de VirtualBox no está creado o no está cargado. | Ejecuta `sudo /sbin/vboxconfig`. Si falla, comprueba que tienes las cabeceras: `sudo apt install -y linux-headers-$(uname -r)` y repite. Si menciona **Secure Boot**, reinicia y acepta la pantalla azul **Enroll MOK** (ver 1.2). |
| `VT-x is disabled in the BIOS` / `AMD-V is disabled` | La virtualización está desactivada en el equipo. | Activarla en la BIOS/UEFI (*Intel Virtualization Technology* o *SVM Mode*). |
| `VT-x is being used by another hypervisor` (`VERR_VMX_IN_VMX_ROOT_MODE`) | Está cargado **KVM**, otro sistema de virtualización. | `sudo modprobe -r kvm_intel kvm` (Intel) o `sudo modprobe -r kvm_amd kvm` (AMD) y vuelve a arrancar la máquina. |
| `VBoxManage: orden no encontrada` | VirtualBox no está instalado (o se desinstaló). | Repite el apartado 1.2 (versión de Oracle). |
| `createvm`: *Guest OS type 'Ubuntu' is invalid* | Tu versión de VirtualBox usa otro nombre de sistema. | Mira los nombres con `VBoxManage list ostypes \| grep -i ubuntu` y usa uno de los que salgan (sirve también `Ubuntu_64`). |
| `registervm`: *path must be absolute* o *file not found* | Ruta mal escrita. | Usa la tecla `Tab` para autocompletar y comprueba con `ls ~/labSI/$KALI`. Recuerda volver a definir la variable `KALI` si cerraste la terminal. |
| La suma SHA-256 **no coincide** | Descarga incompleta o dañada. | `rm $KALI.7z` y descarga de nuevo. |
| Una máquina no recibe IP | Red o DHCP mal configurados. | Comprueba el apartado 1.8 (`showvminfo` y `list dhcpservers`) y ejecuta `sudo dhclient eth0` dentro de la máquina. |
| Todo va muy lento | Poca RAM en el anfitrión. | Baja Kali a `--memory 2048` (con la máquina apagada) y cierra otros programas. |

### Resumen: todos los comandos del montaje

Para tenerlo a mano (cambia la versión de Kali por la actual):

```bash
# 1.2 Instalar VirtualBox de Oracle (sáltalo si "VBoxManage --version" ya muestra 7.1 o 7.2)
sudo apt update
sudo apt install -y build-essential dkms linux-headers-$(uname -r) wget gpg p7zip-full unzip
wget -O- https://www.virtualbox.org/download/oracle_vbox_2016.asc | sudo gpg --dearmor --yes --output /usr/share/keyrings/oracle-virtualbox-2016.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/oracle-virtualbox-2016.gpg] https://download.virtualbox.org/virtualbox/debian noble contrib" | sudo tee /etc/apt/sources.list.d/virtualbox.list   # Mint 21: jammy
sudo apt update
sudo apt install -y virtualbox-7.2
sudo usermod -aG vboxusers $USER        # después: cerrar sesión y volver a entrar

# 1.3 Carpeta del laboratorio
mkdir -p ~/labSI && cd ~/labSI

# 1.4 Kali
KALI=kali-linux-2026.3-virtualbox-amd64
wget https://cdimage.kali.org/current/$KALI.7z
wget https://cdimage.kali.org/current/SHA256SUMS
grep $KALI.7z SHA256SUMS | sha256sum -c -
7z x $KALI.7z

# 1.5 Metasploitable 2
wget -O metasploitable-linux-2.0.0.zip "https://sourceforge.net/projects/metasploitable/files/Metasploitable2/metasploitable-linux-2.0.0.zip/download"
unzip metasploitable-linux-2.0.0.zip

# 1.6 Registrar Kali
VBoxManage registervm ~/labSI/$KALI/$KALI.vbox
VBoxManage modifyvm "$KALI" --name Kali   # si el nombre de la lista es otro, usa ese
VBoxManage modifyvm Kali --memory 4096 --cpus 2

# 1.7 Crear Metasploitable 2
VBoxManage createvm --name Metasploitable2 --ostype Ubuntu --register
VBoxManage modifyvm Metasploitable2 --memory 512 --cpus 1
VBoxManage storagectl Metasploitable2 --name "IDE" --add ide
VBoxManage storageattach Metasploitable2 --storagectl "IDE" --port 0 --device 0 --type hdd --medium ~/labSI/Metasploitable2-Linux/Metasploitable.vmdk

# 1.8 Red interna aislada + DHCP
VBoxManage modifyvm Kali --nic1 intnet --intnet1 labSI --nic2 none
VBoxManage modifyvm Metasploitable2 --nic1 intnet --intnet1 labSI --nic2 none
VBoxManage dhcpserver add --network=labSI --server-ip=10.10.10.1 --netmask=255.255.255.0 --lower-ip=10.10.10.10 --upper-ip=10.10.10.50 --enable
VBoxManage showvminfo Kali --machinereadable | grep -E '^nic1|^intnet1'
VBoxManage showvminfo Metasploitable2 --machinereadable | grep -E '^nic1|^intnet1'

# 1.9 Instantáneas
VBoxManage snapshot Metasploitable2 take limpio
VBoxManage snapshot Kali take limpio

# 1.10 Arrancar
VBoxManage startvm Metasploitable2
VBoxManage startvm Kali
```

---

## 2. Práctica guiada con Nmap (NO evaluable)

> Objetivo: aprender a usar **Nmap** paso a paso. Sigue las instrucciones y ve observando qué devuelve cada comando. Esta parte **no puntúa**: es para aprender.

Nmap es la herramienta de **fingerprinting** que cita la UD01: sirve para descubrir qué equipos hay, qué puertos tienen abiertos y qué servicios y versiones ejecutan.

### Antes de empezar: puertos, servicios y estados

Para entender lo que te va a mostrar Nmap necesitas tener claros tres conceptos: **puerto**, **servicio** y **estado de un puerto**. Léelo con calma: lo vas a necesitar en toda la práctica y en el informe evaluable.

#### ¿Qué es un puerto?

La **dirección IP** identifica a **un equipo** dentro de la red. Pero un mismo equipo puede ofrecer muchas cosas a la vez: páginas web, correo, transferencia de archivos, acceso remoto... Para saber a cuál de ellas va dirigido cada mensaje se usan los **puertos**.

> **Comparación:** la IP es la dirección de un edificio y el puerto es el número de la puerta. Para entregar un paquete en el sitio correcto hacen falta las dos cosas.

- Un puerto es un **número entre 0 y 65 535**.
- Se escribe detrás de la IP, separado por dos puntos: `10.10.10.10:80` significa "el puerto 80 del equipo 10.10.10.10".
- Existen dos protocolos de transporte, y **cada uno tiene sus propios puertos**:

| Protocolo | Cómo funciona | Ejemplos de uso |
|---|---|---|
| **TCP** | Antes de enviar datos **establece una conexión** (el "saludo en tres pasos": `SYN` → `SYN-ACK` → `ACK`) y comprueba que todo llega bien y en orden. Es fiable, pero algo más lento. | Web, SSH, FTP, correo |
| **UDP** | Envía los datos **sin conexión previa** y sin confirmar que llegan. Es más rápido, pero menos fiable. | DNS, DHCP, vídeo en directo, juegos en línea |

Por eso Nmap escribe `80/tcp` o `53/udp`: el puerto 80 de TCP y el puerto 80 de UDP son puertas distintas. **Por defecto Nmap solo revisa TCP**; para UDP hay que pedirlo expresamente (`sudo nmap -sU`), y es mucho más lento.

Los puertos se agrupan en **tres rangos**:

| Rango | Nombre | Para qué se usan |
|---|---|---|
| 0 – 1023 | **Puertos bien conocidos** (*well-known ports*) | Servicios clásicos y estandarizados (web, correo, FTP...). En Linux solo el administrador puede poner un servicio a escuchar en ellos. |
| 1024 – 49 151 | **Puertos registrados** | Aplicaciones concretas: bases de datos, servidores de juegos, programas de gestión... |
| 49 152 – 65 535 | **Puertos dinámicos o privados** | Los usa tu propio equipo de forma temporal, como "puerto de origen", cuando se conecta a otro. |

Algunos puertos bien conocidos que conviene **memorizar**:

| Puerto | Servicio | Para qué sirve |
|---|---|---|
| 21/tcp | FTP | Transferir archivos (**sin cifrar**) |
| 22/tcp | SSH | Acceso remoto a la terminal (cifrado) |
| 23/tcp | Telnet | Acceso remoto a la terminal (**sin cifrar**, obsoleto) |
| 25/tcp | SMTP | Envío de correo |
| 53/udp y 53/tcp | DNS | Traducir nombres (`www.ejemplo.com`) a direcciones IP |
| 80/tcp | HTTP | Páginas web (**sin cifrar**) |
| 443/tcp | HTTPS | Páginas web (cifradas) |
| 3389/tcp | RDP | Escritorio remoto de Windows |

> Que un servicio vaya **sin cifrar** significa que todo lo que viaja por él, **incluidos usuarios y contraseñas**, lo puede leer cualquiera que capture el tráfico de la red.

#### ¿Qué es un servicio?

Un **servicio** es un **programa que se queda funcionando en segundo plano, "escuchando" en un puerto**, a la espera de que alguien se conecte. Cuando decimos que un puerto está abierto, en realidad queremos decir que **hay un servicio escuchando detrás**.

Fíjate en que hay que distinguir tres cosas distintas:

| Concepto | Ejemplo | Explicación |
|---|---|---|
| **Tipo de servicio (protocolo)** | `http` | El "idioma" que se habla en ese puerto. |
| **Programa (producto)** | `Apache httpd` | El software concreto que ofrece ese servicio. Para un mismo protocolo hay varios programas: Apache, Nginx e IIS son todos servidores web. |
| **Versión** | `2.4.58` | La edición concreta de ese programa. |

**¿Por qué importa tanto la versión?** Porque las **vulnerabilidades** afectan a **versiones concretas de programas concretos**. Si un servidor tiene una versión antigua y sin actualizar, es muy probable que tenga fallos ya publicados (con su código **CVE**) que cualquiera puede consultar... y aprovechar. Por eso tanto un atacante como un auditor quieren saber **exactamente** qué programa y qué versión hay detrás de cada puerto.

Además, **cada servicio abierto es una puerta más que hay que vigilar**. Un principio básico de seguridad es tener activos **solo los servicios imprescindibles**; a esto se le llama **reducir la superficie de ataque**.

#### Estados de un puerto

Nmap clasifica cada puerto que revisa en uno de estos estados:

| Estado | Qué significa | Comparación |
|---|---|---|
| `open` (abierto) | Hay un servicio escuchando que **acepta conexiones**. Es lo que más nos interesa. | Llamas a la puerta y alguien abre. |
| `closed` (cerrado) | El equipo responde, pero **no hay ningún servicio** en ese puerto. | Llamas y alguien contesta desde dentro: "aquí no vive nadie". |
| `filtered` (filtrado) | Nmap **no recibe respuesta**: normalmente un **cortafuegos** está bloqueando el paso, así que no puede saber si está abierto o cerrado. | Llamas y no contesta nadie: no sabes si no hay nadie o si un portero no te deja ni llegar a la puerta. |

> A veces verás estados combinados como `open|filtered`: significa que Nmap duda entre los dos (es habitual en los escaneos UDP).

#### ¿Qué cabe esperar al escanear Metasploitable 2?

Metasploitable 2 es una máquina **hecha vulnerable a propósito** para practicar. Es justo lo contrario de un servidor bien configurado, así que cuando la escanees:

- Verás **muchísimos puertos abiertos** (más de veinte). Un servidor real suele tener solo unos pocos: un servidor web bien configurado puede tener abiertos únicamente el 22, el 80 y el 443.
- Encontrarás servicios **muy variados** en la misma máquina: transferencia de archivos, acceso remoto, web, correo, bases de datos, compartición de archivos...
- Algunos de esos servicios son **inseguros por diseño** (envían las contraseñas sin cifrar) y hoy no deberían estar activos en ningún servidor.
- Las **versiones** son **muy antiguas** (de hace más de quince años) y nunca se han actualizado. Muchas tienen vulnerabilidades conocidas, y alguna incluso contiene una **puerta trasera** (*backdoor*).
- El sistema operativo que estime Nmap será un **Linux antiguo**.
- Los puertos que no aparecen en la lista estarán **`closed`**, no `filtered`, porque Metasploitable **no tiene cortafuegos**.

> **Si algo no cuadra:** si Nmap dice `Host seems down`, te salen 0 puertos abiertos o todos aparecen como `filtered`, lo más probable es que hayas escrito mal la IP o que Metasploitable no esté encendida o no esté conectada a la red `labSI`. Repasa los apartados 1.10 y 1.11.

> **Ojo:** aquí no te damos la lista de puertos y servicios de Metasploitable. Descubrirla e **interpretarla** es precisamente tu trabajo en el **Documento 2** (parte evaluable).

**Paso 1 · Descubrir si el objetivo está activo**

```bash
nmap -sn <IP_del_objetivo>
```

`-sn` solo comprueba si la máquina responde, sin mirar puertos. Deberías ver "Host is up".

**Paso 2 · Ver qué puertos están abiertos**

```bash
nmap <IP_del_objetivo>
```

Nmap mostrará una lista de puertos abiertos (por ejemplo 21, 22, 23, 80...). Cada puerto abierto es un **servicio** accesible, y por tanto una posible **vía de entrada**.

**Paso 3 · Averiguar servicios y versiones (fingerprinting)**

```bash
nmap -sV <IP_del_objetivo>
```

`-sV` intenta averiguar **qué programa y qué versión** hay detrás de cada puerto (por ejemplo `vsftpd 2.3.4`, `Apache 2.2.8`). Esta información es clave: conociendo la versión exacta se pueden buscar vulnerabilidades conocidas (CVE), que es lo que estudiamos en la UD01.

**Paso 4 · Intentar identificar el sistema operativo**

```bash
sudo nmap -O <IP_del_objetivo>
```

`-O` intenta adivinar el sistema operativo del objetivo.

### Cómo interpretar los resultados de Nmap

Ejecutar Nmap es fácil; lo que distingue a un auditor es **saber leer lo que devuelve**. Vamos a desmontar la salida de `nmap -sV` línea a línea. Tu salida tendrá **muchas más líneas** en la tabla y algunos datos distintos (hora, tiempos, número de puertos...):

```
Starting Nmap 7.95 ( https://nmap.org ) at 2026-11-18 10:15 CET
Nmap scan report for 10.10.10.10
Host is up (0.00045s latency).
Not shown: ??? closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 2.3.4
80/tcp open  http    Apache httpd 2.2.8 ((Ubuntu) DAV/2)
...
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 15.32 seconds
```

#### Las líneas de alrededor de la tabla

| Línea | Qué te dice |
|---|---|
| `Starting Nmap 7.95 ... at ...` | Versión de Nmap y **fecha y hora** del escaneo. En un informe es una evidencia importante: demuestra **cuándo** se hizo. |
| `Nmap scan report for 10.10.10.10` | A qué equipo corresponde el resultado. **Comprueba siempre que es la IP de Metasploitable.** |
| `Host is up (0.00045s latency)` | El equipo está activo. La **latencia** es lo que tarda en responder; en una red interna es casi cero. |
| `Not shown: ... closed tcp ports` | Por defecto Nmap revisa **1000 puertos**, pero no lista los cerrados para no llenar la pantalla. Te dice cuántos ha ocultado y por qué: `conn-refused` o `reset` significa que el equipo contestó "aquí no hay nadie". |
| `Service Info:` | Datos extra que Nmap ha deducido de los servicios: sistema operativo, nombre del equipo... |
| `MAC Address: 08:00:27:...` | Solo aparece si ejecutas Nmap con `sudo`. Es la dirección física de la tarjeta de red. Si el fabricante que indica es *Oracle VirtualBox*, estás ante una **máquina virtual**. |
| `Nmap done: 1 IP address (1 host up) scanned in ... seconds` | Resumen final: cuántas IP se han revisado, cuántas estaban activas y cuánto ha tardado. |

#### La tabla, columna a columna

| Columna | Ejemplo | Cómo leerla |
|---|---|---|
| `PORT` | `21/tcp` | **Número de puerto / protocolo** (TCP o UDP). |
| `STATE` | `open` | El **estado** del puerto (`open`, `closed`, `filtered`). Casi siempre verás `open`, porque los cerrados se ocultan. |
| `SERVICE` | `ftp` | El **tipo de servicio**. **Cuidado:** sin `-sV` es solo una **suposición** a partir del número de puerto (Nmap consulta una lista: "el 21 suele ser FTP"). Con `-sV` lo ha **comprobado** hablando con el servicio. Si aparece con interrogación (`http?`), Nmap no está seguro. |
| `VERSION` | `vsftpd 2.3.4` | Solo aparece con `-sV`. Indica el **programa** y su **versión**, y a veces información extra entre paréntesis. Si está vacía, Nmap no ha conseguido identificarlo. |

Ejemplo de cómo "traducir" una línea completa:

```
80/tcp open  http    Apache httpd 2.2.8 ((Ubuntu) DAV/2)
```

> "En el **puerto 80** (protocolo **TCP**) hay un servicio **abierto** que habla **HTTP**, es decir, un **servidor web**. El programa es **Apache httpd**, versión **2.2.8**, preparado para **Ubuntu** y con el módulo **DAV/2** activado."

#### La salida de `sudo nmap -O`

| Línea | Qué te dice |
|---|---|
| `Device type: general purpose` | Tipo de dispositivo: un equipo de propósito general (no un router, una impresora...). |
| `Running: Linux 2.6.X` | **Familia** del sistema operativo y versión aproximada del núcleo. |
| `OS details: ...` | Estimación más detallada, normalmente un **rango** de versiones. |
| `Network Distance: 1 hop` | A cuántos "saltos" (routers) está el objetivo. **1 salto** = está en tu misma red. |

> Recuerda que `-O` es una **estimación**: Nmap la deduce de cómo responde el equipo a ciertos paquetes. Nunca la presentes en un informe como una certeza.

#### Piensa como un auditor

Para **cada** puerto abierto que encuentres, hazte estas preguntas:

1. **¿Es necesario este servicio?** Si nadie lo usa, debería estar desactivado.
2. **¿Va cifrado?** Si no, las contraseñas viajan a la vista de cualquiera.
3. **¿La versión es actual o antigua?** Si es antigua, busca si tiene vulnerabilidades conocidas (**CVE**).
4. **¿Qué podría pasar si alguien lo aprovechara?** Leer datos, entrar en el sistema, tirar el servicio...

*Ejemplo ficticio (no es de Metasploitable):* en un escaneo aparece `3389/tcp open ms-wbt-server`. Es el **Escritorio remoto de Windows** (RDP). Si ese servidor no necesita que nadie se conecte desde fuera, ese puerto abierto es un riesgo innecesario: lo correcto sería **desactivarlo** o, como mínimo, **limitar con el cortafuegos** quién puede conectarse.

#### Errores típicos al interpretar

- **Fiarse de `SERVICE` sin haber usado `-sV`.** Un servicio puede estar escuchando en un puerto que no es el suyo habitual; solo `-sV` lo comprueba.
- **Pensar que `open` significa "vulnerable".** Un puerto abierto es una **posible** vía de entrada; que sea vulnerable depende del programa, de su versión y de su configuración.
- **Pensar que Nmap lo ha revisado todo.** Sin opciones solo mira los **1000 puertos TCP más habituales** de los 65 535 posibles. Para revisarlos todos se usa `-p-` (tarda bastante más).
- **Presentar la estimación del sistema operativo como un dato seguro.**

Observa, comenta en clase lo que ves y practica los comandos hasta que entiendas qué hace cada uno. Cuando lo tengas claro, pasa al **Documento 2: parte evaluable (informe de auditoría)**.

---

## Anexo · Alternativa con la ventana de VirtualBox

Si en algún paso prefieres usar la interfaz gráfica (se abre con el comando `virtualbox` o desde el menú de Linux Mint), estos son los equivalentes. **Las normas de red son las mismas.**

| Paso por terminal | Equivalente en la ventana de VirtualBox |
|---|---|
| `registervm` (1.6) | **Máquina → Añadir** y selecciona el archivo `.vbox` de Kali. |
| `createvm` + `storageattach` (1.7) | **Nueva** → Nombre `Metasploitable2`, Tipo **Linux**, Versión **Ubuntu (32-bit)**, 512 MB → **Usar un archivo de disco duro virtual existente** → selecciona `Metasploitable.vmdk`. |
| `--nic1 intnet --intnet1 labSI` (1.8) | Máquina apagada → **Configuración → Red → Adaptador 1** → "Conectado a: **Red interna**", "Nombre: `labSI`". En las dos máquinas. |
| `dhcpserver add` (1.8) | No tiene equivalente gráfico: este comando hay que ejecutarlo en la terminal (o asignar IP fija a mano, ver anexo del profesorado). |
| `snapshot ... take` (1.9) | Máquina → icono de menú **≡ → Instantáneas → Tomar**. |
| `startvm` (1.10) | Selecciona la máquina → **Iniciar**. |

---

## Anexo para el profesorado · notas de montaje

- **Metasploitable 2** debe permanecer **siempre** en red interna. Nunca en NAT ni puente: es un sistema deliberadamente vulnerable.
- Alternativas al objetivo si se prefiere algo más ligero: una VM con **Metasploitable 2** es la recomendada por su variedad de servicios y por existir CVE bien documentados (p. ej. vsftpd 2.3.4 → CVE-2011-2523; Samba → CVE-2007-2447). También sirve cualquier VM Linux antigua preparada por el centro.
- Para buscar CVE sin salida a Internet en las VM, se puede habilitar el buscador en los equipos del aula (no en las VM) o proporcionar un listado offline de CVE de los servicios de Metasploitable 2.
- Tiempos orientativos: sesión 1 montaje del laboratorio; sesión 2 parte guiada; sesiones 3–4 parte autónoma e informe (Documento 2).
- **Equipos anfitriones con Linux Mint:** la guía está pensada para Linux Mint 22 (base Ubuntu 24.04 *noble*; en Mint 21 se usa `jammy`) con **VirtualBox 7.2 del repositorio oficial de Oracle**. **No** usar el paquete `virtualbox` de los repositorios de Ubuntu: es la 7.0, su módulo DKMS no compila en núcleos recientes (comprobado con un núcleo 7.0 en un portátil del aula) y además desinstala el `virtualbox-7.2` de Oracle si estaba instalado. Instalar VirtualBox requiere permisos de administrador (`sudo`); si el alumnado no los tiene, conviene dejar instalado VirtualBox (y aceptada la clave MOK si el equipo usa **Secure Boot**) antes de la sesión 1.
- **Imágenes precargadas:** para no saturar la conexión del aula (Kali ocupa 3–4 GB por equipo), se recomienda dejar `kali-linux-XXXX-virtualbox-amd64.7z`, `SHA256SUMS` y `metasploitable-linux-2.0.0.zip` en una carpeta compartida o USB. El alumnado puede seguir haciendo la comprobación SHA-256 sobre la copia local.
- **Sin DHCP:** si se prefiere no usar `VBoxManage dhcpserver`, se puede asignar IP fija. En Metasploitable: `sudo ifconfig eth0 10.10.10.2 netmask 255.255.255.0`. En Kali: `sudo ip addr add 10.10.10.1/24 dev eth0` (en ese caso, no usar la `.1` en el servidor DHCP). Ambas se pierden al reiniciar.
- **Limpieza al final del curso:** `VBoxManage unregistervm Metasploitable2 --delete` y `VBoxManage unregistervm Kali --delete` borran las máquinas y sus discos; `VBoxManage dhcpserver remove --network=labSI` elimina el DHCP del laboratorio.
