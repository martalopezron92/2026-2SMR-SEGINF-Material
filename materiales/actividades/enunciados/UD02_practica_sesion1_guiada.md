# Práctica guiada · UD02 · Sesión 1
## Cifrado clásico, cifrado simétrico y hash

| | |
|---|---|
| **Módulo** | Seguridad Informática · 2º SMR |
| **Tipo** | Práctica guiada **no evaluable** (te prepara para la prueba práctica) |
| **Modalidad** | Individual |
| **Duración** | 50 minutos |
| **Equipo** | Kali Linux (máquina virtual de la UD01) o Windows con Gpg4win |
| **Criterios que trabaja** | RA4.d |

> **Objetivo:** al terminar sabrás cifrar y descifrar con César y Vigenère, cifrar un archivo con contraseña (AES) y comprobar la integridad de un archivo con su hash. **Todo esto se pide en la prueba práctica**, así que guarda tus notas y capturas.

Crea una carpeta de trabajo para la práctica:

```bash
# Kali
mkdir ~/ud02 && cd ~/ud02
```

```powershell
# Windows (PowerShell)
mkdir $HOME\ud02 ; cd $HOME\ud02
```

---

## Parte A · Cifrados clásicos con CyberChef (15 min)

Abre **CyberChef** en el navegador: `https://gchq.github.io/CyberChef/`

La pantalla tiene 4 zonas: **Operations** (izquierda, buscador de operaciones), **Recipe** (receta: las operaciones que arrastras), **Input** (entrada) y **Output** (salida).

### A.1. Cifrar con César

1. Busca la operación **`ROT13`** y arrástrala a la receta. Aunque se llama ROT13, tiene un campo **Amount** que es la clave *k* del César.
2. Cambia **Amount** a `3`.
3. Escribe en *Input*: `HOLA MUNDO`
4. Comprueba que la salida es `KROD PXQGR`.

### A.2. Descifrar un César con la clave

Para descifrar se desplaza hacia atrás 3 posiciones, que es lo mismo que avanzar 23 (26 − 3 = 23). Pon **Amount** a `23`.

**Descifra:** `DWDFDU DO DPDQHFHU` (clave 3).

### A.3. Romper un César sin la clave (fuerza bruta)

No sabes la clave de este mensaje:

```
SH JSHCL LZ LS ZLJYLAV
```

1. Pon el mensaje en *Input* y la operación ROT13.
2. Ve cambiando **Amount** de 1 a 25 hasta que salga un texto con sentido.
3. Apunta la clave y el mensaje.

> **Pista profesional:** CyberChef tiene una operación **`ROT13 Brute Force`** que muestra las 25 posibilidades a la vez. Pruébala.

### A.4. Vigenère

1. Quita ROT13 de la receta y añade **`Vigenère Encode`**. Clave: `LIMON`.
2. Cifra `ATACAR AL AMANECER` y comprueba que sale `LBMQNC IX OZLVQQRC`.
3. Ahora usa **`Vigenère Decode`** con la clave `CLAVE` para descifrar:

```
NL FDVOL DDKKEAG KCCAIXKKA ZP PZ RZTWOIJ
```

**Captura 1:** CyberChef con la receta y el mensaje descifrado de A.3 o A.4.

---

## Parte B · Cifrado simétrico de un archivo con GPG (15 min)

`gpg -c` (*c* de *symmetric*) cifra un archivo con una **contraseña**. Internamente usa **AES**.

### B.1. Crear un archivo y cifrarlo

**Kali:**

```bash
echo "Contraseña del wifi del taller: Ribera2026!" > secreto.txt
cat secreto.txt
gpg -c --cipher-algo AES256 secreto.txt
```

**Windows (PowerShell, con Gpg4win instalado):**

```powershell
"Contraseña del wifi del taller: Ribera2026!" | Out-File -Encoding utf8 secreto.txt
Get-Content secreto.txt
gpg -c --cipher-algo AES256 secreto.txt
```

Te pedirá una **frase de contraseña** dos veces. Se crea el archivo `secreto.txt.gpg`.

> En Windows también se puede hacer con **Kleopatra** (botón *Firmar/Cifrar* → *Cifrar con contraseña*) o con **7-Zip** (*Añadir al archivo* → *Cifrado AES-256*).

### B.2. Comprobar que no se puede leer

```bash
ls -l secreto.txt*
cat secreto.txt.gpg        # Windows: Get-Content secreto.txt.gpg
file secreto.txt.gpg       # solo Kali: indica el algoritmo usado
```

Verás caracteres sin sentido. `file` mostrará algo como *"PGP symmetric key encrypted data - AES with 256-bit key"*.

### B.3. Simular el envío y descifrar

Borra el original (como si el archivo cifrado hubiera viajado por la red hasta otra persona):

```bash
rm secreto.txt             # Windows: Remove-Item secreto.txt
```

GPG guarda la contraseña en memoria unos minutos (el *gpg-agent*). Para que te la vuelva a pedir, ciérralo y descifra:

```bash
gpgconf --kill gpg-agent
gpg -o secreto_recuperado.txt -d secreto.txt.gpg
cat secreto_recuperado.txt
```

**Captura 2:** el archivo cifrado ilegible y el archivo recuperado.

### B.4. Piensa

- ¿Qué pasa si escribes mal la contraseña? Pruébalo.
- Si le envías `secreto.txt.gpg` a un compañero por correo, **¿cómo le haces llegar la contraseña?** ¿Sería seguro mandarla en el mismo correo? (→ problema de la distribución de claves).

---

## Parte C · Integridad con funciones hash (20 min)

### C.1. Calcular un hash

```bash
# Kali
echo "Pago: 100 EUR" > pago.txt
sha256sum pago.txt
```

```powershell
# Windows
"Pago: 100 EUR" | Out-File -Encoding ascii pago.txt
Get-FileHash pago.txt -Algorithm SHA256
```

Apunta el hash. Mide siempre **64 caracteres hexadecimales**, sea cual sea el tamaño del archivo.

### C.2. Efecto avalancha

Cambia **un solo carácter** (100 → 900) y vuelve a calcular el hash:

```bash
echo "Pago: 900 EUR" > pago.txt
sha256sum pago.txt
```

Compara los dos hashes. ¿Se parecen en algo?

También en CyberChef: operación **`SHA2`** (tamaño 256). Escribe `hola` y después `Hola`.

| Entrada | SHA-256 |
|---|---|
| `hola` | `b221d9dbb083a7f33428d7c2a3c3198ae925614d70210e28716ccaa7cd4ddb79` |
| `Hola` | `e633f4fc79badea1dc5db970cf397c8248bac47cc3acf9915ba60b5d76b0e88f` |

### C.3. Comprobar una descarga (caso real)

Las webs de software publican el hash oficial de sus archivos. Por ejemplo, la página de descargas de Kali Linux muestra el **SHA256sum** de cada imagen ISO.

El profesor/a os deja en el aula virtual un archivo `programa.zip` y el hash publicado en la web. Calcula el hash del archivo descargado y compáralo:

```bash
sha256sum programa.zip
# o comprobación automática:
echo "HASH_PUBLICADO  programa.zip" | sha256sum -c
```

Si sale `programa.zip: OK`, el archivo es íntegro. Si sale `FAILED`, **no lo uses**: se ha corrompido o lo han manipulado.

> Si no hay archivo en el aula virtual, haz la prueba con tu propio `secreto.txt.gpg`: calcula su hash, ábrelo con un editor, cambia un carácter y vuelve a comprobar.

**Captura 3:** los dos hashes distintos de `pago.txt` y la comprobación `OK` / `FAILED`.

### C.4. Piensa

- ¿Se puede "descifrar" un hash para obtener el texto original? ¿Por qué?
- ¿Por qué no se recomienda MD5 para comprobar si alguien ha manipulado un archivo?

---

## Para repasar (autoevaluación)

1. ¿Cuántas claves hay que probar como máximo para romper un César?
2. ¿Por qué Vigenère resiste mejor el análisis de frecuencias que César?
3. ¿Qué algoritmo ha usado `gpg -c` en esta práctica? ¿Es simétrico o asimétrico?
4. ¿Qué objetivo de seguridad garantiza el cifrado? ¿Y el hash?

> **Opcional:** si el profesor/a lo pide como evidencia de trabajo, sube tus 3 capturas y las respuestas a un repositorio `2SMR-SEGINF-XXX-UD02-S1` siguiendo la guía de GitHub de la UD01.

---

### Soluciones de la parte A (para comprobar)

- A.2: `ATACAR AL AMANECER`
- A.3: clave **7** → `LA CLAVE ES EL SECRETO`
- A.4: `LA FIRMA DIGITAL GARANTIZA EL NO REPUDIO`
