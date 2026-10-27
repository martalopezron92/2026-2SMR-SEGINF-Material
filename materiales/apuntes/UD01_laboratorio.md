# Práctica técnica · UD01 · Documento 1 de 2
## Parte guiada — Montaje del laboratorio y primeros pasos con Nmap

> **IMPORTANTE:** este documento es la **parte guiada y NO evaluable**. Sirve para montar el laboratorio y aprender a usar las herramientas con ayuda. **No se entrega**, pero es **obligatorio** haberla realizado antes de pasar al Documento 2 (la parte evaluable).

| | |
|---|---|
| **Módulo** | Seguridad Informática · 2º SMR |
| **Instrumento** | Práctica técnica (40 % de la UD01) — **esta parte no puntúa** |
| **Duración orientativa** | 2 sesiones (montaje + práctica guiada) |

> **Qué vas a hacer:** montar un pequeño "laboratorio" con dos máquinas virtuales aisladas y practicar las **primeras fases de una auditoría de caja negra** (footprinting y fingerprinting) con **Nmap**, tal y como se explica en la UD01. **No se ataca ni se explota nada:** solo se observa y se analiza, igual que hace un auditor antes de emitir su informe.

---

## 0. Normas éticas y legales (OBLIGATORIO leer y firmar)

Las técnicas de esta práctica **solo son legales sobre sistemas propios o con autorización expresa por escrito**. Usarlas contra equipos o redes ajenas sin permiso es un **delito** (arts. 197 bis y 264 del Código Penal) y contradice el principio que estudiamos: la diferencia entre un PenTest y un ataque real es **la autorización**.

En esta práctica:

- Todo se hace en **máquinas virtuales propias**, en una **red aislada sin salida a Internet**.
- **Nunca** se escanean equipos del instituto, de casa, redes WiFi públicas ni direcciones de Internet.
- La práctica se queda en **reconocimiento y análisis**; no se ejecutan exploits ni se modifica ningún sistema.

> **Declaración del alumno/a:** "He leído estas normas y me comprometo a usar lo aprendido solo sobre sistemas propios o autorizados, con fines de aprendizaje y defensa."
>
> Nombre y apellidos: ___________________________ Fecha: _______ Firma: _______

*(Esta hoja se entrega firmada —escaneada o fotografiada— dentro del repositorio de la parte evaluable. Sin ella no se realiza la práctica.)*

---

## 1. Preparación del laboratorio (guía paso a paso)

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

### 1.1. Instalar VirtualBox

1. Descarga **VirtualBox** desde la web oficial `https://www.virtualbox.org` (versión para tu sistema operativo).
2. Instálalo aceptando las opciones por defecto. Si pregunta por instalar controladores de red, acéptalo.

### 1.2. Descargar las máquinas virtuales

- **Kali Linux:** en `https://www.kali.org/get-kali/` elige **"Virtual Machines" → VirtualBox**. Descargas un archivo comprimido (`.7z`) que ya contiene la máquina lista. Descomprímelo.
- **Metasploitable 2:** descárgalo desde SourceForge (`https://sourceforge.net/projects/metasploitable/`). Obtienes un `.zip` con un archivo `.vmdk` (el disco de la máquina).

> Si el aula ya tiene las imágenes descargadas en una carpeta común, usa esas y te saltas este paso.

### 1.3. Importar Kali en VirtualBox

1. Abre VirtualBox → menú **Archivo → Importar servicio virtualizado** (si Kali viene como `.ova`) **o** **Máquina → Añadir** y selecciona el archivo `.vbox` de la carpeta descomprimida.
2. Deja la configuración por defecto (2 GB de RAM como mínimo, mejor 4 GB) y finaliza.

### 1.4. Crear la máquina Metasploitable 2

1. VirtualBox → **Nueva**.
   - Nombre: `Metasploitable2`
   - Tipo: **Linux**, Versión: **Ubuntu (64-bit)**
   - Memoria: 512 MB es suficiente.
2. En "Disco duro" elige **"Usar un archivo de disco duro virtual existente"** y selecciona el `.vmdk` descargado.
3. Finaliza. **No** necesitas instalar nada: la máquina ya está lista.

### 1.5. Configurar la RED INTERNA AISLADA (paso crítico)

Haz esto **en las dos máquinas** (con las máquinas apagadas):

1. Selecciona la máquina → **Configuración → Red**.
2. En **Adaptador 1**:
   - "Conectado a:" → **Red interna**
   - "Nombre:" → escribe exactamente `labSI` (el mismo nombre en las dos máquinas).
3. Acepta.

> **Muy importante:** con "Red interna" las máquinas se ven entre sí pero **no tienen acceso a Internet ni a la red del instituto**. Esto mantiene la práctica dentro de la ley. No cambies esto a "NAT" ni a "Adaptador puente".

### 1.6. Arrancar y obtener las direcciones IP

1. **Arranca Metasploitable 2.** Cuando pida usuario, entra con:
   - usuario: `msfadmin` · contraseña: `msfadmin`
   - Escribe `ifconfig` y anota su dirección IP (algo como `192.168.x.x` o `10.0.x.x`). Es la **IP del objetivo**.
2. **Arranca Kali Linux.** Usuario y contraseña por defecto: `kali` / `kali`.
   - Abre una terminal y escribe `ip a`. Anota la IP de Kali.

> Si las máquinas no tienen IP automática, pregunta al profesor/a cómo asignar una IP fija dentro de la misma red (por ejemplo `10.10.10.1` para Kali y `10.10.10.2` para el objetivo).

### 1.7. Comprobar que se "ven"

Desde la terminal de **Kali**, comprueba la conexión con el objetivo:

```bash
ping -c 4 <IP_del_objetivo>
```

Si recibes respuesta, el laboratorio está listo. **Haz una captura de pantalla** (la necesitarás en la parte evaluable).

---

## 2. Práctica guiada con Nmap (NO evaluable)

> Objetivo: aprender a usar **Nmap** paso a paso. Sigue las instrucciones y ve observando qué devuelve cada comando. Esta parte **no puntúa**: es para aprender.

Nmap es la herramienta de **fingerprinting** que cita la UD01: sirve para descubrir qué equipos hay, qué puertos tienen abiertos y qué servicios y versiones ejecutan.

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

Observa, comenta en clase lo que ves y practica los comandos hasta que entiendas qué hace cada uno. Cuando lo tengas claro, pasa al **Documento 2: parte evaluable (informe de auditoría)**.

---

## Anexo para el profesorado · notas de montaje

- **Metasploitable 2** debe permanecer **siempre** en red interna. Nunca en NAT ni puente: es un sistema deliberadamente vulnerable.
- Alternativas al objetivo si se prefiere algo más ligero: una VM con **Metasploitable 2** es la recomendada por su variedad de servicios y por existir CVE bien documentados (p. ej. vsftpd 2.3.4 → CVE-2011-2523; Samba → CVE-2007-2447). También sirve cualquier VM Linux antigua preparada por el centro.
- Para buscar CVE sin salida a Internet en las VM, se puede habilitar el buscador en los equipos del aula (no en las VM) o proporcionar un listado offline de CVE de los servicios de Metasploitable 2.
- Tiempos orientativos: sesión 1 montaje del laboratorio; sesión 2 parte guiada; sesiones 3–4 parte autónoma e informe (Documento 2).
