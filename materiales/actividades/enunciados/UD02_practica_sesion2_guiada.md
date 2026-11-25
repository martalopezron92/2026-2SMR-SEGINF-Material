# Práctica guiada · UD02 · Sesión 2
## Clave pública, cifrado y firma digital con GPG (por parejas)

| | |
|---|---|
| **Módulo** | Seguridad Informática · 2º SMR |
| **Tipo** | Práctica guiada **no evaluable** (te prepara para la prueba práctica) |
| **Modalidad** | Por parejas (persona **A** y persona **B**), cada una en su equipo |
| **Duración** | 70 minutos |
| **Equipo** | Kali Linux (máquina virtual de la UD01) o Windows con Gpg4win (Kleopatra) |
| **Criterios que trabaja** | RA4.d, RA4.f, RA4.g |

> **Objetivo:** cada persona crea su par de claves, intercambia su clave pública con su pareja y se envían un mensaje **cifrado** (confidencialidad) y **firmado** (autenticación, integridad y no repudio). **En la prueba práctica tendrás que hacer lo mismo con la clave pública del profesor/a.**

Recuerda la regla de la sesión:

| Quiero… | Uso la clave… |
|---|---|
| Cifrar para mi pareja | **pública de mi pareja** |
| Descifrar lo que me llega | **mi privada** |
| Firmar | **mi privada** |
| Verificar la firma de mi pareja | **pública de mi pareja** |

Trabaja en la carpeta de la sesión anterior: `cd ~/ud02`

---

## Paso 1 · Generar tu par de claves (10 min)

```bash
gpg --full-generate-key
```

Responde:

| Pregunta | Respuesta |
|---|---|
| Tipo de clave | La opción por defecto **(ECC, firmar y cifrar)**. También vale RSA de 3072 bits. |
| Validez | `1y` (un año). En un caso real nunca se deja sin caducidad. |
| Nombre real | Tu nombre y primer apellido |
| Dirección de correo | Tu correo del centro |
| Comentario | `2SMR` |
| Frase de contraseña | Una que **recuerdes**. Protege tu clave privada. |

Comprueba tus claves:

```bash
gpg --list-keys            # claves públicas que tienes (la tuya y las que importes)
gpg --list-secret-keys     # claves privadas (solo la tuya)
```

Verás `pub` (clave principal, para firmar `[SC]`), `sub` (subclave para cifrar `[E]`) y una **huella** (*fingerprint*) de 40 caracteres.

> **Windows (Kleopatra):** *Archivo → Nuevo par de claves → Crear un par de claves OpenPGP personal*. Rellena nombre y correo. En *Configuración avanzada* puedes ver el algoritmo y la caducidad.

**Captura 1:** salida de `gpg --list-keys` con tu clave.

---

## Paso 2 · Exportar tu clave pública y dársela a tu pareja (10 min)

```bash
gpg --armor --export tu_correo@centro.es > clave_publica_TUNOMBRE.asc
cat clave_publica_TUNOMBRE.asc
```

`--armor` la guarda en texto (empieza por `-----BEGIN PGP PUBLIC KEY BLOCK-----`) para poder enviarla por correo o pegarla en cualquier sitio. **Se puede compartir sin miedo: es pública.**

Pásale el archivo `.asc` a tu pareja (aula virtual, correo, USB o carpeta compartida).

> ⚠️ **Nunca** exportes ni compartas tu clave privada (`--export-secret-keys`).

**Kleopatra:** clic derecho sobre tu clave → *Exportar…*

---

## Paso 3 · Importar la clave de tu pareja y comprobar la huella (10 min)

```bash
gpg --import clave_publica_PAREJA.asc
gpg --list-keys
gpg --fingerprint correo_pareja@centro.es
```

**¿Cómo sé que esa clave es de verdad de mi pareja y no de alguien que se hace pasar por ella?**
Comprobando la **huella** por otro canal: leedla en voz alta, cara a cara. Si coincide, la clave es auténtica.

Cuando hayáis comprobado la huella, **firma la clave de tu pareja** para indicar que confías en ella:

```bash
gpg --sign-key correo_pareja@centro.es
```

> Esta es la idea de la **red de confianza** de PGP. En los certificados X.509 (HTTPS, DNIe), en lugar de comprobar la huella cada persona, es una **Autoridad de Certificación** la que garantiza la identidad.

**Kleopatra:** *Importar…* → seleccionar el `.asc` → *Certificar* tras comprobar la huella.

**Captura 2:** la huella de la clave de tu pareja.

---

## Paso 4 · Enviar un mensaje cifrado y firmado (15 min)

Escribe un mensaje para tu pareja:

```bash
echo "Hola, soy TUNOMBRE. La reunión es el jueves a las 10 en el aula 2." > mensaje_para_PAREJA.txt
```

**Cifrar (para la pareja) y firmar (con tu privada) a la vez:**

```bash
gpg --armor --encrypt --sign -r correo_pareja@centro.es -o mensaje_para_PAREJA.asc mensaje_para_PAREJA.txt
```

| Opción | Qué hace |
|---|---|
| `--encrypt` / `-e` | Cifra con la **clave pública** del destinatario (`-r`). |
| `--sign` / `-s` | Firma con **tu clave privada** (te pide tu frase de contraseña). |
| `--armor` / `-a` | Salida en texto (`.asc`) en vez de binario (`.gpg`). |
| `-o` | Archivo de salida. |

Mira el resultado (`cat mensaje_para_PAREJA.asc`): empieza por `-----BEGIN PGP MESSAGE-----` y es ilegible.

> GPG usa **cifrado híbrido**: genera una clave de sesión aleatoria, cifra el mensaje con ella (AES) y cifra la clave de sesión con la pública de tu pareja.

Envía el `.asc` a tu pareja.

**Kleopatra:** *Firmar/Cifrar…* → marcar *Firmar como* (tu clave) y *Cifrar para* (la clave de tu pareja).

---

## Paso 5 · Descifrar y verificar el mensaje recibido (10 min)

```bash
gpg -d mensaje_para_TUNOMBRE.asc
```

GPG usa tu **clave privada** para descifrar (te pide la frase de contraseña) y la **pública de tu pareja** para verificar la firma. Debe aparecer:

```
gpg: encrypted with cv25519 key, ID ..., created ...
      "Tu Nombre (2SMR) <tu_correo@centro.es>"
Hola, soy PAREJA. La reunión es el jueves a las 10 en el aula 2.
gpg: Signature made ...
gpg: Good signature from "Nombre Pareja (2SMR) <correo_pareja@centro.es>"
```

> Si no firmaste la clave de tu pareja en el paso 3, verás además el aviso *"WARNING: This key is not certified with a trusted signature!"*. La firma es correcta, pero GPG te recuerda que no has confirmado la identidad del dueño de la clave.

**Captura 3:** el mensaje descifrado con `Good signature`.

### 5.1. ¿Y si alguien modifica el mensaje? (experimento)

Firma un documento **sin cifrarlo** (firma en claro, se puede leer):

```bash
echo "Autorizo el pago de 100 EUR" > autorizacion.txt
gpg --clearsign autorizacion.txt
cat autorizacion.txt.asc
gpg --verify autorizacion.txt.asc
```

Ahora edita `autorizacion.txt.asc` con `nano` y cambia `100` por `900`. Verifica otra vez:

```bash
gpg --verify autorizacion.txt.asc
```

Debe salir **`BAD signature`**. La firma detecta cualquier modificación (**integridad**).

**Captura 4:** `Good signature` antes y `BAD signature` después.

---

## Paso 6 · Certificados digitales en el navegador (5 min)

1. Entra en `https://www.sede.fnmt.gob.es` (o en la web de tu banco o de la Agencia Tributaria).
2. Haz clic en el **candado** (o en el icono de ajustes junto a la URL) → *La conexión es segura* → *El certificado es válido* / *Más información → Ver certificado*.
3. Apunta:

| Campo | Valor |
|---|---|
| Emitido para (titular / dominio) | |
| Emitido por (CA) | |
| Válido desde / hasta | |
| Algoritmo de la clave pública | |
| Jerarquía (CA raíz → intermedia → web) | |

4. Prueba la web `https://expired.badssl.com`. ¿Qué te dice el navegador? ¿Por qué?

**Captura 5:** el certificado de la web.

---

## Para repasar (autoevaluación)

1. Si quieres que solo tu pareja pueda leer un mensaje, ¿con qué clave lo cifras?
2. ¿Qué clave usa GPG para verificar la firma de tu pareja?
3. ¿Por qué hay que comprobar la huella de una clave pública antes de usarla?
4. Un documento firmado pero no cifrado, ¿es confidencial?
5. ¿Qué papel tiene la CA en el certificado de una web?
6. ¿Qué significa que en el experimento 5.1 salga `BAD signature`?

> **Opcional:** si el profesor/a lo pide como evidencia de trabajo, sube tus capturas y respuestas a un repositorio `2SMR-SEGINF-XXX-UD02-S2`.

---

### Chuleta de comandos GPG

| Acción | Comando |
|---|---|
| Generar par de claves | `gpg --full-generate-key` |
| Listar claves públicas / privadas | `gpg --list-keys` / `gpg --list-secret-keys` |
| Ver huella | `gpg --fingerprint correo` |
| Exportar mi clave pública | `gpg --armor --export micorreo > mi_clave.asc` |
| Importar una clave pública | `gpg --import clave.asc` |
| Cifrado simétrico (contraseña) | `gpg -c --cipher-algo AES256 archivo` |
| Cifrar para alguien | `gpg -a -e -r correo archivo` |
| Cifrar y firmar | `gpg -a -e -s -r correo -o salida.asc archivo` |
| Firmar en claro | `gpg --clearsign archivo` |
| Firma separada | `gpg -a --detach-sign archivo` → `archivo.asc` |
| Descifrar / verificar | `gpg -d archivo.asc` · `gpg --verify firma.asc [archivo]` |
| Olvidar contraseñas en memoria | `gpgconf --kill gpg-agent` |
