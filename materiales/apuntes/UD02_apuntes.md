# UD02. Criptografía · Apuntes esenciales

> **Duración:** 2 sesiones de 2 h (teoría + práctica)
> **RA implicado:** RA4 (privacidad de la información transmitida)
> **Criterios de evaluación:** RA4.d, RA4.f, RA4.g

Estos apuntes recogen **lo básico y fundamental** de la unidad. Para ampliar, tienes los documentos de la carpeta UD02 (criptografía clásica, moderna, hash y firma electrónica).

| Apartado | Contenido | Sesión |
|---|---|---|
| 1 | ¿Qué es la criptografía y para qué sirve? | 1 |
| 2 | Criptografía clásica: César y Vigenère | 1 |
| 3 | Criptografía simétrica | 1 |
| 4 | Criptografía asimétrica y cifrado híbrido | 2 |
| 5 | Funciones hash | 1 |
| 6 | Firma digital | 2 |
| 7 | Certificados digitales, CA, HTTPS y DNIe | 2 |
| 8 | Resumen: qué herramienta para qué objetivo | 2 |

---

## 1. ¿Qué es la criptografía y para qué sirve?

<!-- content: UD02-C01 -->
*Criterios de evaluación: RA4.d*

La **criptografía** es la técnica que transforma un mensaje para que **solo pueda entenderlo quien tenga la clave**. Si alguien intercepta el mensaje (por ejemplo, escuchando el tráfico de la red con un *sniffer*), verá datos sin sentido.

### 1.1. Vocabulario básico

| Término | Significado | Ejemplo |
|---|---|---|
| **Texto claro** (texto plano) | El mensaje original, legible. | `HOLA MUNDO` |
| **Criptograma** (texto cifrado) | El mensaje ya cifrado. | `KROD PXQGR` |
| **Algoritmo** | El método o la "receta" para cifrar. Suele ser público. | César, AES, RSA |
| **Clave** | El dato secreto que usa el algoritmo. | Desplazar 3 letras |
| **Cifrar** | Pasar de texto claro a criptograma usando la clave. | |
| **Descifrar** | Pasar de criptograma a texto claro usando la clave. | |
| **Criptoanálisis** | Intentar romper un cifrado **sin conocer la clave**. | Fuerza bruta, análisis de frecuencias |
| **Esteganografía** | Ocultar que existe un mensaje (no cifrarlo). | Texto escondido dentro de una imagen |

> **Principio de Kerckhoffs:** la seguridad debe depender **solo del secreto de la clave**, no de que el algoritmo sea secreto. Por eso AES o RSA son públicos y aun así son seguros.

### 1.2. Objetivos (servicios de seguridad)

| Objetivo | Pregunta que responde | Herramienta criptográfica |
|---|---|---|
| **Confidencialidad** | ¿Puede leerlo alguien no autorizado? | Cifrado (simétrico o asimétrico) |
| **Integridad** | ¿Se ha modificado por el camino? | Funciones hash |
| **Autenticación** | ¿Quién lo envía de verdad? | Firma digital, certificados |
| **No repudio** | ¿Puede el emisor negar que lo envió? | Firma digital |

---

## 2. Criptografía clásica: César y Vigenère

<!-- content: UD02-C01 -->
*Criterios de evaluación: RA4.d*

Los métodos clásicos son de dos tipos:

- **Transposición:** se cambian las letras **de orden** (las mismas letras, desordenadas).
- **Sustitución:** cada letra se **cambia por otra**.

En esta unidad usamos el **alfabeto de 26 letras sin Ñ** (el que usa CyberChef).

```
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
0 1 2 3 4 5 6 7 8 9 10 ...                       25
```

### 2.1. Cifrado César (sustitución monoalfabética)

Cada letra se desplaza **k posiciones** en el alfabeto. La clave es el número **k**. Al llegar a la Z se vuelve a empezar por la A.

**Ejemplo** con k = 3: `A→D`, `B→E`, …, `X→A`, `Y→B`, `Z→C`

```
Texto claro:  H O L A   M U N D O
Criptograma:  K R O D   P X Q G R
```

Para **descifrar**, se desplaza k posiciones hacia la **izquierda**.

**¿Por qué es inseguro?**

1. **Fuerza bruta:** solo hay **25 claves posibles**. Se prueban todas en segundos.
2. **Análisis de frecuencias:** cada letra se cambia siempre por la misma. En castellano las letras más frecuentes son **E** y **A**. Si en el criptograma la letra que más se repite es la H, probablemente H = E, y así sale la clave (k = 3).

### 2.2. Cifrado Vigenère (sustitución polialfabética)

La clave es una **palabra**. Cada letra de la clave indica el desplazamiento para una letra del mensaje (A = 0, B = 1, C = 2, …). La clave se repite a lo largo del mensaje. Los espacios no consumen letras de la clave.

**Ejemplo** con clave `LIMON` (L = 11, I = 8, M = 12, O = 14, N = 13):

```
Texto claro:  A T A C A R   A L   A M A N E C E R
Clave:        L I M O N L   I M   O N L I M O N L
Criptograma:  L B M Q N C   I X   O Z L V Q Q R C
```

Una misma letra (la A) se cifra como L, M, N, I, O… según su posición. Esto **dificulta el análisis de frecuencias** y lo hace más seguro que César, aunque hoy también se rompe con ordenador.

> **Idea clave:** cuanto más grande es el número de claves posibles (**espacio de claves**), más difícil es la fuerza bruta. Los algoritmos modernos tienen claves de 128 o 256 bits: 2^128 posibilidades, imposible de probar.

---

## 3. Criptografía simétrica (de clave secreta)

<!-- content: UD02-C02 -->
*Criterios de evaluación: RA4.d*

Se usa **la misma clave para cifrar y para descifrar**. Emisor y receptor deben compartir esa clave secreta.

```
          clave K                       clave K
Texto claro ──► [ CIFRAR ] ──► criptograma ──► [ DESCIFRAR ] ──► Texto claro
   (Ana)                       (viaja por la red)                    (Luis)
```

| Algoritmo | Clave | Situación |
|---|---|---|
| DES | 56 bits | **Obsoleto**, se rompe por fuerza bruta. |
| 3DES | 112/168 bits | Obsoleto, lento. |
| **AES** | 128, 192 o 256 bits | **Estándar actual.** Lo usan WPA2/WPA3, HTTPS, BitLocker, 7-Zip, GPG… |
| ChaCha20 | 256 bits | Moderno, muy usado en móviles. |

**Ventajas:** muy **rápido**, sirve para cifrar grandes cantidades de datos (discos, archivos, vídeo).

**Inconvenientes:**

1. **Distribución de la clave:** ¿cómo le hago llegar la clave a la otra persona sin que nadie la intercepte? Si la mando por el mismo canal que el mensaje, quien intercepte uno intercepta los dos.
2. **Número de claves:** necesito una clave distinta con cada persona. Para *n* personas hacen falta *n·(n−1)/2* claves (con 100 personas, ¡4.950 claves!).

> **Práctica:** `gpg -c archivo` cifra un archivo con una contraseña usando AES (sesión 1).

---

## 4. Criptografía asimétrica (de clave pública) y cifrado híbrido

<!-- content: UD02-C03 -->
*Criterios de evaluación: RA4.d*

Cada persona tiene **un par de claves** relacionadas matemáticamente:

| Clave | Quién la tiene | Para qué se usa |
|---|---|---|
| **Pública** | Cualquiera. Se publica o se reparte. | **Cifrar** mensajes para su dueño y **verificar** sus firmas. |
| **Privada** | **Solo su dueño.** Nunca se comparte. | **Descifrar** lo que le envían y **firmar**. |

Lo que se cifra con una clave solo se puede descifrar con la otra del mismo par. A partir de la clave pública **no se puede calcular** la privada.

### 4.1. Enviar un mensaje confidencial

Ana quiere mandar un mensaje secreto a Luis:

```
Ana cifra con la clave PÚBLICA de Luis ──► criptograma ──► Luis descifra con su clave PRIVADA
```

Solo Luis puede leerlo, porque solo él tiene su clave privada. **Se resuelve el problema de la distribución de claves:** la clave pública puede ir por cualquier canal.

> **Regla para recordar:** *para que algo sea secreto, cifro con la clave pública del destinatario.*

| Algoritmo | Comentario |
|---|---|
| **RSA** | El más conocido. Claves de 2048–4096 bits. |
| **ECC** (curvas elípticas, p. ej. Ed25519/Curve25519) | Misma seguridad con claves mucho más cortas. Es el que genera GPG por defecto. |

**Inconveniente:** es **muy lento** (cientos o miles de veces más que AES). No sirve para cifrar archivos grandes.

### 4.2. Cifrado híbrido: lo mejor de los dos

En la práctica (HTTPS, GPG, WhatsApp…) se combinan los dos sistemas:

1. Se genera una **clave simétrica aleatoria** (clave de sesión).
2. El mensaje se cifra con esa clave usando **AES** (rápido).
3. La clave de sesión se cifra con la **clave pública** del destinatario (seguro).
4. Se envían ambas cosas. El destinatario descifra la clave de sesión con su **privada** y con ella descifra el mensaje.

> **Resumen:** la asimétrica sirve para **intercambiar la clave** de forma segura; la simétrica, para **cifrar los datos**.

---

## 5. Funciones hash (resumen)

<!-- content: UD02-C04 -->
*Criterios de evaluación: RA4.d*

Una **función hash** convierte cualquier dato (una palabra o un archivo de 4 GB) en una **huella de longitud fija**. Por ejemplo, SHA-256 siempre da 256 bits (64 caracteres hexadecimales).

```
$ echo -n "hola" | sha256sum
b221d9dbb083a7f33428d7c2a3c3198ae925614d70210e28716ccaa7cd4ddb79  -
```

**Propiedades:**

| Propiedad | Qué significa |
|---|---|
| **Longitud fija** | Da igual el tamaño de la entrada, la salida mide siempre lo mismo. |
| **Unidireccional** | A partir del hash **no se puede** obtener el dato original. **No es cifrado:** no hay clave ni se puede "descifrar". |
| **Efecto avalancha** | Un cambio mínimo (una letra, un bit) produce un hash **completamente distinto**. |
| **Resistencia a colisiones** | Es prácticamente imposible encontrar dos entradas distintas con el mismo hash. |

| Algoritmo | Situación |
|---|---|
| MD5 (128 bits) | **Roto**: se pueden fabricar colisiones. Solo para detectar errores accidentales. |
| SHA-1 (160 bits) | **Roto** desde 2017. No usar. |
| **SHA-256 / SHA-512** (familia SHA-2), SHA-3 | **Recomendados.** |

**Usos:**

- **Comprobar la integridad** de un archivo descargado: se compara el hash calculado con el que publica la web oficial. Si coinciden, el archivo no se ha modificado.
- **Guardar contraseñas**: el sistema guarda el hash, no la contraseña.
- **Firma digital** (apartado 6).

> **Práctica:** `sha256sum archivo` (Linux) o `Get-FileHash archivo` (PowerShell).

---

## 6. Firma digital

<!-- content: UD02-C05 -->
*Criterios de evaluación: RA4.f, RA4.g*

La **firma digital** usa la criptografía asimétrica "al revés": se firma con la clave **privada** y cualquiera verifica con la clave **pública**. Garantiza:

- **Autenticación:** el mensaje lo ha firmado el dueño de la clave privada.
- **Integridad:** el documento no se ha modificado después de firmarlo.
- **No repudio:** el firmante no puede negar haberlo firmado.

> La firma digital **no da confidencialidad**: un documento firmado se puede leer. Si además queremos que sea secreto, hay que **firmar y cifrar**.

### 6.1. Cómo funciona

**Firmar (Ana):**

1. Calcula el **hash** del documento.
2. Cifra ese hash con su **clave privada** → eso es la **firma**.
3. Envía el documento + la firma.

**Verificar (Luis):**

1. Descifra la firma con la **clave pública de Ana** → obtiene el hash original.
2. Calcula él mismo el hash del documento recibido.
3. Si **los dos hashes coinciden**, la firma es válida: lo firmó Ana y no se ha modificado.

```
FIRMAR:     documento ─► hash ─► cifrar con PRIVADA de Ana ─► firma
VERIFICAR:  firma ─► descifrar con PÚBLICA de Ana ─► hash A
            documento ─► hash ─► hash B          ¿hash A = hash B?
```

### 6.2. Resumen de qué clave se usa

| Quiero… | Uso la clave… |
|---|---|
| Cifrar un mensaje para Luis | **pública de Luis** |
| Descifrar un mensaje que me envían | **mi privada** |
| Firmar un documento | **mi privada** |
| Verificar la firma de Ana | **pública de Ana** |

### 6.3. Firma electrónica en la ley

El Reglamento europeo **eIDAS** (y en España la Ley 6/2020) distingue:

| Tipo | Ejemplo | Valor |
|---|---|---|
| **Simple** | Escribir tu nombre al final de un correo, una firma escaneada. | Bajo. |
| **Avanzada** | Firma con un certificado digital (p. ej. certificado FNMT en el ordenador). Identifica al firmante y detecta cambios. | Alto. |
| **Cualificada** | Avanzada + certificado cualificado + dispositivo seguro (p. ej. el **DNIe**). | **Equivale a la firma manuscrita.** |

---

## 7. Certificados digitales, CA, HTTPS y DNIe

<!-- content: UD02-C06 -->
*Criterios de evaluación: RA4.f, RA4.g*

**Problema:** si alguien me pasa una clave pública diciendo "es la de mi banco", ¿cómo sé que es verdad y no la de un atacante?

**Solución:** el **certificado digital**, un documento electrónico que **une una clave pública con una identidad** (persona, empresa o web) y que está **firmado por una Autoridad de Certificación (CA)** de confianza.

### 7.1. Qué contiene un certificado (estándar X.509)

- Datos del **titular** (nombre, DNI/CIF, dominio web…).
- La **clave pública** del titular.
- **Emisor**: la CA que lo firma.
- **Periodo de validez** (desde / hasta).
- Número de serie y algoritmos usados.
- La **firma digital de la CA**.

### 7.2. Autoridades de Certificación (CA)

Una **CA** es una entidad de confianza que comprueba la identidad del solicitante y firma su certificado. Ejemplos: **FNMT-RCM** (Fábrica Nacional de Moneda y Timbre), **Dirección General de la Policía** (DNIe), Let's Encrypt, DigiCert.

El navegador y el sistema operativo traen una lista de **CA raíz de confianza**. Si un certificado está firmado por una de ellas (directamente o mediante CA intermedias), se considera válido. Un certificado puede **revocarse** antes de caducar (si se pierde la clave privada, por ejemplo).

### 7.3. HTTPS: el candado del navegador

Cuando entras en `https://...`:

1. El servidor envía su **certificado**.
2. El navegador comprueba que lo firma una CA de confianza, que no ha caducado y que el dominio coincide.
3. Se acuerda una **clave de sesión** usando criptografía asimétrica.
4. Todo el tráfico se cifra con esa clave simétrica (AES o ChaCha20). → **Cifrado híbrido.**

> **Ojo:** el candado indica que **la conexión está cifrada** y que el certificado corresponde a ese dominio, **no** que la web sea honrada. Una web de *phishing* también puede tener HTTPS. Revisa siempre el dominio.

### 7.4. DNIe y certificado FNMT

- El **DNI electrónico** lleva un chip con dos certificados: uno de **autenticación** y otro de **firma** (firma cualificada). Se usa con un lector o por NFC y un PIN.
- El **certificado de persona física de la FNMT** se instala en el navegador u ordenador y permite hacer trámites (Hacienda, Seguridad Social, sede electrónica del ayuntamiento…).
- **Cl@ve** es un sistema de identificación de la Administración que no necesita certificado (usuario + PIN o app).

---

## 8. Resumen: qué herramienta para qué objetivo

| Objetivo | Herramienta | Clave |
|---|---|---|
| Confidencialidad de grandes datos | Cifrado simétrico (AES) | Secreta compartida |
| Intercambiar una clave / mensaje secreto sin clave previa | Cifrado asimétrico (RSA/ECC) | Pública del destinatario |
| Integridad | Hash (SHA-256) | Ninguna |
| Autenticación, integridad y no repudio | Firma digital | Privada del firmante (verifica la pública) |
| Saber que una clave pública es de quien dice | Certificado digital firmado por una CA | — |

### Herramientas que usaremos

| Herramienta | Para qué |
|---|---|
| **CyberChef** (`https://gchq.github.io/CyberChef/`) | Cifrados clásicos, hashes, codificaciones, desde el navegador. |
| **GnuPG** (`gpg`) | Cifrado simétrico, asimétrico y firma. En Kali ya viene instalado. En Windows: **Gpg4win** (incluye `gpg` y la interfaz **Kleopatra**). |
| `sha256sum` / `Get-FileHash` | Calcular hashes en Linux / Windows. |
| Navegador | Ver el certificado de una web (clic en el candado). |
