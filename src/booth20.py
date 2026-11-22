#!/usr/bin/env python3
"""
Photo booth - version 20.

Novedades respecto a booth19:
    - El espejo muestra los pasos UNO POR UNO y grandes ("Paso 1 de 3:
      Escanea este codigo...", "Paso 2: toca Conectar...", "Paso 3: toca
      Tomar foto y mira aqui"), cada uno en espanol y luego en ingles,
      con "Un telefono a la vez" fijo.
    - La bienvenida del telefono va en tres pantallas con "Siguiente".
    - Al terminar la sesion o al recoger la hoja se pide desconectarse del
      Wi-Fi PhotoBooth: el Wi-Fi interno de la Pi aguanta pocos telefonos
      a la vez (~8) y los que se quedan conectados le quitan lugar a los
      siguientes.
    - La cola de impresion recuerda 300 trabajos en vez de 40: con el
      modo manual, las hojas viejas ya no desaparecen del admin.
    - Mientras alguien usa el espejo los codigos siguen ocultos.

Novedades de booth19 respecto a booth18:
    - Seguro anti-bloqueo: si el espejo pasa mas de 20 s en cuenta
      regresiva o capturando (camara colgada), se libera solo, intenta
      reiniciar la camara y lo anota en el registro ("ATORADO") y en el
      diagnostico del admin. Una captura que llega tarde le entrega la
      foto a su dueno pero ya no le quita el turno al siguiente. Antes,
      un cuelgue dejaba el espejo bloqueado hasta liberarlo a mano.
    - La pantalla dice de frente que hacer, en espanol e ingles:
      libre "1 Escanea · 2 Tomate tu foto · 3 Elige e imprime / Un
      telefono a la vez"; en uso "EN USO · Espera tu turno / No escanees
      todavia · Siguiente turno en N s", con los codigos ocultos; al
      terminar "Listo, tu foto ya esta en tu telefono".
    - QR pequeno fijo al pie: "Ya estas conectado? Escanea aqui", que
      lleva directo a la pagina sin depender del portal.
    - Telefono: bienvenida con los tres pasos y "No vuelvas a escanear"
      una sola vez; "Espera tu turno: tu boton se prende solo. No
      escanees otra vez."; aviso de fin de turno mas grande.

Novedades de booth18 respecto a booth17:
    - iPhone: guardar fotos. La ventanita del portal no deja guardar y,
      al cerrarse, iOS se salia de la red. Ahora:
        * al iPhone que ya entro se le contesta "Success" a su sonda, asi
          la ventanita muestra "Listo" y el telefono sigue en la red;
        * el visor trae "Abrir en Safari para guardar", que abre la MISMA
          sesion en Safari;
        * en Safari, escribir 10.42.0.1 lleva a la sesion de ese telefono
          aunque no traiga cookie (se reconoce por su IP).
      La pantalla del espejo y la vista previa del admin no cambian.

Novedades de booth17 respecto a booth16:
    - El QR de ayuda vuelve a salir para quien se DESCONECTA y regresa
      sin que se le abra la pagina (pasaba mucho con Samsung). El espejo
      ahora lee de la antena cuanto lleva conectado cada telefono
      (iw station dump), que se reinicia al reconectar; los leases y la
      tabla ARP duran horas y no lo notaban. Quien entro y se guardo el
      telefono SIN desconectarse sigue sin encender el aviso, igual que
      el admin y la impresora. Si la antena no se puede leer, se usa el
      metodo de booth16.

Novedades de booth16 respecto a booth15:
    - En iPhone ya se puede imprimir la hoja, descartar y terminar la
      sesion: la ventanita del portal de iOS no muestra confirm() ni
      alert() y los cancela solos. Ahora las confirmaciones van dentro
      de la pagina, en el idioma del telefono.
    - La hoja impresa es VERTICAL, igual que el papel: cuatro fotos
      verticales en 2x2. Cada foto se recorta al centro para parecerse
      a lo que se ve en el espejo a 1-2 metros (ver "Hoja de la
      sesion"), y lleva un banner del evento mucho mas grande, que se
      lee en la copia impresa.

Novedades de booth15 respecto a booth14:
    - El QR de ayuda sale SOLO para quien se conecto al Wi-Fi del espejo
      y nunca abrio la pagina del booth. Antes salia tambien por cada
      invitado que, ya atendido, se guardaba el telefono conectado, y
      con una fiesta llena habria estado encendido casi toda la noche.
    - Cuenta como "entro" solo una pagina del booth pedida a la IP del
      espejo. Las sondas del sistema y las apps que piden cosas por HTTP
      a otros dominios no cuentan.
    - El aparato del operador que entra al admin con el PIN no enciende
      el QR de ayuda aunque luego cierre la pagina.
    - Un aparato que pasa cinco minutos conectado sin entrar nunca se da
      por fijo (reloj, tablet, impresora sin configurar) y no vuelve a
      contar aunque se desconecte y regrese.

Novedades de booth14 respecto a booth13:
    - Hoja de la sesion: el invitado elige hasta 4 fotos y salen juntas
      en UNA hoja horizontal de 6x4, en cuadricula de 2x2, cada foto con
      su marco y lineas de corte en cruz. Una sola hoja por sesion.
    - Al terminar de tomarse fotos sale la pregunta "Te gustaria
      imprimir tus fotos? / Hasta 4 fotos diferentes por sesion", en
      espanol o en ingles segun el telefono. Tambien sale si intenta
      terminar la sesion sin haber impreso.
    - Candados en el servidor: solo fotos de la propia sesion, sin
      repetir, hasta el tope y una hoja por visita. Se quito la
      impresion de fotos sueltas.
    - El telefono dice "se esta imprimiendo" durante 60 segundos antes
      de decir que la hoja ya salio: CUPS la da por hecha al recibirla.
    - Modo manual: sin impresora conectada a la Pi, aprobar solo marca
      la hoja como lista y la cola ofrece Descargar para imprimirla con
      la app de Canon.
    - La impresora conectada al Wi-Fi del espejo ya no cuenta como
      telefono atorado ni enciende el QR de ayuda.

Novedades de booth13 respecto a booth12:
    - La lista de ranuras ya no se redibuja mientras el operador tiene
      algo a medias. Se refrescaba cada cuatro segundos para enterarse
      de los cambios hechos desde otro telefono, y al hacerlo borraba
      el archivo recien elegido antes de que diera tiempo a picar
      Subir.
    - Lo que se sube a una ranura se reconoce por su contenido y no por
      la extension del nombre. La galeria de Android manda los archivos
      llamados "1000012345", sin extension, y un GIF valido acababa
      rechazado por como se llamaba.
    - La foto se voltea en el archivo y no en la pantalla. Voltearla
      con CSS daba la vuelta a la imagen entera, y desde que lleva el
      marco pegado eso dejaba el nombre del evento escrito al reves, en
      la pantalla y en el papel.
    - El aviso de los telefonos atorados cuenta desde la ultima senal
      de vida y no desde que el telefono aparecio en la red. Antes, una
      direccion que hubiera pedido una pagina quedaba dada por resuelta
      para siempre, asi que quien volvia al espejo por segunda vez no
      disparaba el aviso nunca: su telefono se reconecta solo y Android
      ya no le saca el portal de esa red.
    - Los telefonos conectados se cuentan por la tabla de vecinos del
      sistema y no solo por los archivos de leases de NetworkManager.
      En la Pi de verdad esos archivos no estaban donde la documentacion
      dice, asi que el aviso para los telefonos atorados nunca llegaba
      a salir. La tabla de vecinos no depende de rutas.
    - Guardar la foto en iPhone. Safari ignora el atributo download y
      navega a la imagen; si desde ahi se usa el boton de compartir del
      navegador, lo que se manda es la DIRECCION y no la foto, y esa
      direccion es un 10.42.x.x que solo existe dentro de la red del
      espejo. La API de compartir lo arreglaria, pero solo existe en
      HTTPS. Asi que en iOS la foto se abre en un visor propio que
      lleva al gesto que si funciona ahi, y avisa de no compartir desde
      el navegador.
    - Descartar una foto desde el telefono. Sale de la galeria de quien
      se la tomo y de la cola si todavia esperaba el visto bueno; el
      archivo se queda en disco para el operador.
    - Tres tipos de letra a elegir y color propio para cada parte de la
      pantalla: la etiqueta, el nombre, el subtitulo, la fecha, los
      filetes, el texto del centro y el pie. Cada parte sin color
      propio hereda el de siempre, asi que cambiar el acento sigue
      cambiandolo todo de un golpe. La letra elegida se usa tambien en
      el pie de las fotos impresas, y el admin ensena la pantalla de
      verdad encogida para no tener que ir a mirar el espejo.
    - Marco con los datos del evento al pie de cada foto. Ademas de
      convertir la copia en un recuerdo, cuadra la proporcion: el
      sensor entrega 16:9 y una hoja de 4x6 es 3:2, asi que sin barra
      la impresora dejaba dos bandas blancas de casi dos centimetros.
      La barra se dimensiona para dejar la foto en 3:2 exacto, de modo
      que llena el papel sin recortar un solo pixel. La foto sin marco
      se conserva en fotos/originales.
    - El telefono pregunta al ritmo que hace falta y no siempre igual.
      Con cincuenta invitados, medio segundo fijo son cien peticiones
      por segundo, y la mayoria no sirven de nada: solo la cuenta
      regresiva necesita ritmo. Baja a menos de un tercio.
    - La vista previa de la camara en /admin se para cuando la pestana
      no esta a la vista. Durante la fiesta ese panel se queda abierto
      en el bolsillo del operador, pidiendo ocho capturas por segundo
      que nadie mira.
    - El espejo se suelta por inactividad real, no por un reloj fijo.
      Los quince segundos se reinician cada vez que el dueno dispara,
      imprime o descarga; mirar la foto no cuenta, y esa distincion es
      la que mantiene el espejo libre, porque mirar no genera ninguna
      peticion. El telefono avisa antes, con un boton de "sigo aqui",
      para que nadie tenga que disparar solo por no perder el turno.
    - Separadas dos cosas que antes eran la misma. El boton del
      telefono cierra la sesion de verdad (suelta el espejo, tira la
      visita y borra la cookie, asi el siguiente que use ese telefono
      empieza limpio), mientras que el aviso que manda el navegador al
      bloquearse la pantalla solo suelta el espejo. Si hicieran lo
      mismo, guardarse el telefono en la bolsa costaria las fotos.
    - La broma entra, sale y cambia de pieza con un fundido por negro.
      Un corte seco entre el espejito y la cara mataba el efecto, y el
      negro es ademas lo que el panel hace mejor: por un instante
      vuelve a ser un espejo antes de revelar.
    - Cinco ranuras de broma en vez de una imagen, cada una con intro
      (GIF o video en bucle, sin sonido) y remate, para la broma de dos
      tiempos: el espejo "habla" y luego "responde".
    - Las claves de configuracion de versiones viejas se descartan al
      cargar, en vez de arrastrarse para siempre en los archivos JSON.

Novedades de la version 12:
    - El espejo se suelta en cuanto la foto esta tomada. Antes el turno
      duraba 90 segundos contados desde el ultimo disparo, y no se
      refrescaban al mirar: quien se tomaba su foto y guardaba el
      telefono dejaba el espejo muerto minuto y medio. Ahora las fotos
      viven aparte del espejo (ver `visitas`), asi que la persona sigue
      viendolas e imprimiendolas desde su telefono mientras el siguiente
      ya se esta tomando la suya.
    - El turno se agarra al disparar, no al conectarse. Cincuenta
      telefonos pueden tener la pagina abierta sin bloquear nada; el
      espejo es del primero que pica el boton. Y el que llega mientras
      esta ocupado no ve un rechazo: su boton se habilita solo.
    - Aviso automatico para los telefonos que se conectan y no abren el
      portal cautivo (Samsung, sobre todo). El espejo cruza los leases
      del DHCP con las paginas que ha servido, y solo cuando detecta a
      alguien atorado ensena un codigo en el centro de la pantalla.
    - Cinco bromas de dos tiempos. Cada ranura tiene una intro (GIF o
      video en bucle, sin sonido) y un remate (la foto), cada una con
      su boton: el espejo "habla" primero y "responde" cuando el
      operador decide, sin pasar por negro entre las dos.
    - El texto del centro de la pantalla se edita y se puede quitar.
    - El codigo QR dejo de llevar un token de sesion y apunta a
      /entrar, asi que no se quema al usarse: antes, quien le tomaba
      una foto a la pantalla o tardaba en escanear se encontraba un
      "ese codigo ya no sirve".

Novedades de la version 11:
    - Portal cautivo. El telefono abre la pagina solo al conectarse a
      la red del espejo, sin que nadie teclee una direccion. Se atienden
      las sondas de Android, iOS y Windows, y el DNS del modo compartido
      se secuestra para que cualquier nombre caiga en el booth.
    - El codigo QR puede llevar las credenciales del wifi en el formato
      que leen iOS y Android de fabrica: un escaneo conecta y abre.
    - Sala de espera para quien llega con el espejo ocupado.
    - La direccion del punto de acceso tiene preferencia sobre la del
      cable, que era lo que hacia que el QR apuntara a la red de casa
      cuando la Pi estaba conectada por Ethernet para trabajar.

Novedades de la version 10:
    - Diagnostico en vivo en /admin: camara, impresora, papel, disco,
      direccion, red propia o ajena, tiempo encendida. Pensado para
      resolver problemas el dia del evento sin abrir una terminal.
    - Mantenimiento: apagar la Pi, borrar todas las fotos, y exportar e
      importar la configuracion para pasarla a otra tarjeta.
    - Resolucion de captura configurable; de fabrica 3 MP, que sobra
      para imprimir 4x6 y pesa la cuarta parte que los 12 MP nativos.

Novedades de la version 9:
    - Impresion de fotos. El invitado la pide desde su telefono y recibe
      un numero de recogida; el operador ve la cola con miniaturas en
      /admin y aprueba o descarta cada una. Se habla con CUPS por el
      comando `lp`, sin librerias extra, asi que funciona igual con la
      impresora de verdad que con la impresora PDF virtual (cups-pdf)
      que sirve para ensayar sin hardware.
    - Contador de hojas restantes, con aviso cuando se esta acabando.
    - El admin descubre solo las impresoras que CUPS ve, para no tener
      que escribir el nombre a mano.
    - El PIN de administracion se cambia desde la propia pagina; deja de
      estar enterrado en el codigo.
    - La pantalla decia "Libre" / "Free" cuando el espejo estaba
      desocupado, que en una fiesta se lee como "gratis". Ahora dice
      "Disponible" / "Available".

Novedades de la version 8:
    - Arreglada la deteccion de IP, que sin internet devolvia 127.0.0.1
      y habria hecho que el QR apuntara a localhost en modo punto de
      acceso. Ahora se lee de la interfaz y se recalcula en cada QR.
    - El panel de admin muestra la direccion actual del espejo.

Novedades de la version 7:
    - Filetes decorativos configurables: arriba, abajo, ambos o ninguno.
      Tipografia clasica de invitacion: filete, etiqueta, nombre,
      filete, fecha.
    - Mas espacio en los campos de texto del evento.

Novedades de la version 6:
    - Arquitectura de camara corregida. Antes el sensor estaba en modo
      still permanente: la vista previa saturaba ese canal y la captura
      se quedaba esperando. Ahora corre en modo video (rapido, ligero)
      y solo cambia a still en el instante del disparo.
    - Acceso a la camara protegido por un candado propio, para que la
      previsualizacion no se cruce con una captura en curso.

Uso:
    python3 -m venv --system-site-packages ~/booth-venv
    ~/booth-venv/bin/pip install flask "qrcode[pil]"
    ~/booth-venv/bin/python booth20.py

    Espejo:          http://<ip>:8000/
    Administracion:  http://<ip>:8000/admin
"""

import base64
import glob
import io
import json
import os
import re
import secrets
import shlex
import shutil
import socket
import subprocess
import threading
import time
from datetime import datetime
from pathlib import Path

import qrcode
from PIL import Image, ImageDraw, ImageFont
from flask import (Flask, jsonify, make_response, redirect, render_template_string,
                   request, send_from_directory, url_for)
from werkzeug.serving import make_server

from picamera2 import Picamera2

# ---------------------------------------------------------------
# Configuracion tecnica (esto si vive en el codigo)
# ---------------------------------------------------------------

# La version publica no contiene un PIN conocido. Si no hay ~/pin.txt,
# el primer arranque toma PHOTOBOOTH_ADMIN_PIN o genera uno aleatorio.
# Consultar el PIN localmente con: cat ~/pin.txt (NO subirlo al repositorio).
PIN_INICIAL_ENTORNO = os.environ.get("PHOTOBOOTH_ADMIN_PIN", "")

FOTOS_DIR = Path.home() / "fotos"
ARCHIVO_CALIBRACION = Path.home() / "calibracion.json"
ARCHIVO_EVENTO = Path.home() / "evento.json"
ARCHIVO_PIN = Path.home() / "pin.txt"
ARCHIVO_BROMAS = Path.home() / "booth_bromas.json"
DIR_BROMAS = Path.home() / "booth_bromas"
ARCHIVO_IMPRESION = Path.home() / "impresion.json"

# Resolucion de captura. Los 12 MP nativos del sensor son mas de lo
# que cualquier salida necesita: la Selphy imprime a 300 dpi, asi que
# una foto de 4x6 pulgadas son 1200x1800 pixeles. Capturar de mas solo
# gasta RAM, tiempo de captura y disco, y en una Pi 3B llega a estorbar.
# Estas son las opciones que ofrece el panel de admin.
RESOLUCIONES = {
    "alta":  (4608, 2592),   # 12 MP nativos
    "media": (2304, 1296),   # 3 MP, de sobra para imprimir 4x6
    "baja":  (1536,  864),   # 1.3 MP, para equipo lento
}
RESOLUCION_PREVIA = (800, 450)
PUERTO = 8000

# El portal cautivo solo funciona desde el puerto 80: es ahi donde los
# telefonos preguntan si la red tiene internet. Escuchar en los dos
# deja la direccion corta (10.42.0.1, sin puerto) para quien la teclee,
# y no rompe nada de lo que ya apunta al 8000.
PUERTO_PORTAL = 80

SEGUNDOS_CUENTA = 3
MOSTRAR_RESULTADO = 8
ESPEJAR_RESULTADO = True

# Cuanto tiempo se queda el espejo apartado despues de una foto.
#
# Hasta booth11 el turno duraba 90 segundos contados desde el ultimo
# disparo, y no se refrescaban al mirar: quien se tomaba su foto y
# guardaba el telefono dejaba el espejo muerto minuto y medio. Con
# cincuenta invitados eso es mas de una hora de cola inventada.
#
# Ahora el espejo solo esta apartado mientras hace falta. En cuanto
# acaba de ensenar la foto, el dueno conserva una ventana corta para
# disparar otra vez -- quien quiere tres tomas seguidas no tiene que
# pelearlas -- y si no la usa, queda libre. Las fotos ya tomadas NO
# dependen de eso: viven en la visita del telefono (ver `visitas`) y
# se pueden ver e imprimir mucho despues, sin bloquear a nadie.
# El espejo se suelta cuando pasan estos segundos sin que el dueno
# HAGA algo: disparar, imprimir o descargar. Mirar la foto no cuenta, y
# esa es la distincion importante: mirar no genera ninguna peticion y
# es justo lo que la gente hace despues de tomarse la foto. Si mirar
# extendiera el turno, el espejo volveria a quedarse apartado minutos.
#
# El reloj se reinicia con cada accion, asi que quien quiere tres tomas
# seguidas no las pelea, y quien ya acabo no bloquea a nadie.
INACTIVIDAD_ESPEJO = 15
# Si el espejo pasa mas de esto en cuenta regresiva o capturando, algo se
# colgo (casi siempre la camara): se suelta solo en vez de quedarse
# bloqueado hasta que alguien entre al admin.
LIMITE_ATORADO = 20
ESPERA_CAMARA = 10      # lo mas que se espera por la camara para disparar
AVISO_ANTES = 7         # desde aqui el telefono avisa, con boton de seguir
GRACIA_LATIDO = 5       # sin senales de vida del dueno, se suelta ya
VIDA_VISITA = 20 * 60   # cuanto recuerda el espejo las fotos de alguien

# Deteccion de telefonos atorados.
#
# Hay telefonos -- Samsung entre ellos -- que se conectan a la red del
# espejo y no abren el portal cautivo. El invitado se queda mirando un
# "conectado sin internet" sin saber que le falta un paso. En vez de
# llenar la pantalla de instrucciones para todos, el espejo cruza dos
# listas: quien esta conectado (los leases del DHCP) y quien ha pedido
# alguna pagina. La resta es la gente atorada, y solo entonces aparece
# el aviso.
#
# Los diez segundos de abajo salen de una cuenta asimetrica. El flujo
# normal -- escanear, conectar, que salte el portal, que cargue -- tarda
# entre cinco y nueve segundos, asi que diez deja poco margen y de vez
# en cuando el aviso saldra para alguien que ya iba a entrar. No
# importa: aparece un codigo en una pantalla que estaba vacia y
# desaparece en cuanto esa persona entra. Equivocarse por tarde es mucho
# peor: a los veinte segundos de no ver nada, la gente se va.
#
# El tope de arriba existe porque esto es un espejo antes que una
# pantalla: la gente se para enfrente a mirarse, y un codigo plantado
# en el centro les tapa la cara. El aviso es para quien acaba de
# intentar entrar y no pudo, no para los cincuenta telefonos que van a
# estar conectados toda la noche con la pagina cerrada.
#
# Cinco minutos conectado sin entrar es el limite de "esta persona
# todavia esta ahi esperando". Pasado eso, se fue a bailar y el centro
# vuelve a ser espejo.
#
# Desde booth14 solo cuenta quien NUNCA ha abierto la pagina: el que ya
# entro y se guardo el telefono no enciende el aviso, ni el admin, ni
# la impresora. Ver cuantos_atorados().
VENTANA_ATORADO = (10, 300)     # segundos desde que el telefono se conecto
LEASES_DHCP = "/var/lib/NetworkManager/dnsmasq-*.leases"
# Pedir cualquiera de estas rutas a la IP del espejo prueba que esa
# persona ya llego a la pagina del booth (o al admin).
PREFIJOS_ENTRADA = ("/entrar", "/s/", "/api/", "/fotos/", "/admin")

SEGUNDOS_ALTERNA = 4.5      # cada cuanto cambia de idioma el texto del QR

AVISO_POCAS_HOJAS = 15      # a partir de aqui el admin avisa
MAX_COLA_VISIBLE = 300      # cuantos trabajos recuerda la pagina

# ---------------------------------------------------------------

FOTOS_DIR.mkdir(exist_ok=True)
app = Flask(__name__)


# ---------------------------------------------------------------
# PIN de administracion
#
# Vive en su propio archivo y no dentro de evento.json, para que no
# pueda colarse por accidente a ninguna plantilla publica.
# Si alguna vez se olvida: borrar ~/pin.txt y vuelve a ser el de
# fabrica.
# ---------------------------------------------------------------

def leer_pin():
    """Carga un PIN existente o crea uno aleatorio de 8 digitos localmente.

    El archivo queda solo para el usuario y no se escribe el valor en logs.
    """
    try:
        p = ARCHIVO_PIN.read_text().strip()
        if 4 <= len(p) <= 8 and p.isascii() and p.isdigit():
            return p
    except FileNotFoundError:
        pass
    except Exception as e:
        raise RuntimeError(f"No se pudo leer {ARCHIVO_PIN}") from e

    p = PIN_INICIAL_ENTORNO.strip()
    if not (4 <= len(p) <= 8 and p.isascii() and p.isdigit()):
        p = str(secrets.randbelow(90_000_000) + 10_000_000)
    if not escribir_pin(p):
        raise RuntimeError(f"No se pudo crear {ARCHIVO_PIN}; revisar permisos")
    return p


def escribir_pin(nuevo):
    nuevo = "".join(c for c in nuevo if c.isascii() and c.isdigit())
    if not 4 <= len(nuevo) <= 8:
        return False
    try:
        # Crear con permisos 0600; nunca escribir en una ruta del repositorio.
        import os as _os
        fd = _os.open(str(ARCHIVO_PIN), _os.O_WRONLY | _os.O_CREAT | _os.O_TRUNC, 0o600)
        try:
            _os.fchmod(fd, 0o600)
            with _os.fdopen(fd, "w") as out:
                out.write(nuevo)
        except Exception:
            try:
                _os.close(fd)
            except OSError:
                pass
            raise
        return True
    except Exception as e:
        print(f"No se pudo guardar el PIN: {e}")
        return False

pin_admin = leer_pin()
# Token de sesion distinto del PIN y sin valor fijo.
sesion_admin = secrets.token_urlsafe(32)


def cookie_admin_valida():
    cookie = request.cookies.get("admin", "")
    return bool(cookie) and secrets.compare_digest(cookie, sesion_admin)


def poner_cookie_admin(respuesta):
    respuesta.set_cookie("admin", sesion_admin, max_age=60 * 60 * 12,
                         httponly=True, samesite="Strict")
    return respuesta


# ---------------------------------------------------------------
# Configuracion del evento (editable desde /admin)
# ---------------------------------------------------------------

EVENTO_FABRICA = {
    "nombre": "Photo Booth",
    "subtitulo": "",
    "etiqueta_es": "",
    "etiqueta_en": "",
    "fecha": "",
    "acento": "#b9a48a",
    "idioma_espejo": "bilingue",   # bilingue | es | en
    "lineas": "abajo",             # ninguna | arriba | abajo | ambas
    # Que codigo ensena la pantalla:
    #   wifi   -> conecta al telefono a la red del espejo (recomendado)
    #   enlace -> lleva directo a la pagina, pero solo sirve si el
    #             telefono ya esta en la red
    "modo_qr": "wifi",
    # Estos dos solo arman el codigo QR; no configuran el punto de
    # acceso, que vive en NetworkManager. Tienen que coincidir con el.
    "wifi_ssid": "PhotoBooth",
    # Requiere configurar la clave real en el admin o via entorno.
    # Nunca debe publicarse una contrasena real del AP.
    "wifi_clave": os.environ.get("PHOTOBOOTH_WIFI_PASSWORD", ""),
    # El texto del centro de la pantalla mientras nadie se esta
    # tomando la foto. Vacio = se usa el traducido ("Cuando quieras").
    # Con centro_visible apagado no aparece nada, que es lo que mas
    # respeta el espejo: en negro, el panel es un espejo de verdad.
    "centro_visible": True,
    "centro_texto": "",
    # clasica | moderna | marcada
    "tipografia": "clasica",
    # Color propio de cada parte de la pantalla. Vacio = hereda (ver
    # PARTES_COLOR); asi cambiar el acento sigue cambiandolo todo.
    "color_etiqueta": "",
    "color_nombre": "",
    "color_subtitulo": "",
    "color_fecha": "",
    "color_lineas": "",
    "color_centro": "",
    "color_pie": "",
    # La barra con los datos del evento al pie de cada foto. Ademas de
    # convertir la foto en un recuerdo, cuadra la proporcion: el sensor
    # da 16:9 y el papel 4x6 es 3:2, asi que sin la barra la copia sale
    # con bandas blancas arriba y abajo. Con ella, llena el papel.
    "marco_activo": True,
    "marco_fondo": "#101014",
    # Vacio = se usa el color de acento del evento
    "marco_tinta": "",
}

evento = dict(EVENTO_FABRICA)
version_evento = 1                 # sube al guardar; la pantalla se recarga


def fundir(fabrica, guardado):
    """Mezcla lo guardado con lo de fabrica, descartando lo que sobra.

    Las claves que ya no existen en esta version se tiran en vez de
    arrastrarse. Sin esto, el archivo de una version vieja le deja
    ajustes fantasma a la nueva: no hacen nada, no se pueden cambiar
    desde /admin, y aparecen en el respaldo de configuracion como si
    todavia significaran algo.
    """
    if not isinstance(guardado, dict):
        return dict(fabrica)
    return {**fabrica, **{k: v for k, v in guardado.items() if k in fabrica}}


def cargar_evento():
    global evento
    if ARCHIVO_EVENTO.exists():
        try:
            evento = fundir(EVENTO_FABRICA,
                            json.loads(ARCHIVO_EVENTO.read_text()))
        except Exception as e:
            print(f"No se pudo leer el evento: {e}")


def guardar_evento():
    global version_evento
    try:
        ARCHIVO_EVENTO.write_text(json.dumps(evento, indent=2, ensure_ascii=False))
        version_evento += 1
        return True
    except Exception as e:
        print(f"No se pudo guardar el evento: {e}")
        return False


cargar_evento()



# ---------------------------------------------------------------
# Bromas
#
# Cada ranura tiene dos piezas y su propio boton, porque la broma que
# se quiere hacer es de dos tiempos: primero el espejo "habla" -- un
# GIF o un video en bucle -- y cuando el operador decide, el espejo
# "responde" con una foto. Entre las dos no se pasa por negro.
#
# La intro va en bucle y sin sonido: asi arranca sola en cualquier
# navegador, sin permisos de reproduccion automatica, y se queda ahi el
# tiempo que haga falta.
#
# Los GIF animados y los videos se guardan tal cual. Solo las fotos
# fijas pasan por PIL: convertir un GIF animado a JPEG lo dejaria en un
# solo cuadro, que es exactamente lo que no se quiere.
# ---------------------------------------------------------------

RANURAS = ("a", "b", "c", "d", "e")
PIEZAS = ("intro", "remate")
EXT_VIDEO = {".mp4", ".webm", ".mov", ".m4v"}
EXT_IMAGEN = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
LIMITE_PIEZA = 48 * 1024 * 1024

# Los primeros bytes de un video, para reconocerlo sin abrirlo. La
# posicion importa: en los MP4 la marca viene despues del tamano de la
# primera caja.
FIRMAS_VIDEO = (
    (4, b"ftyp"),                   # mp4, m4v, mov
    (0, b"\x1a\x45\xdf\xa3"),     # webm, mkv
)
# Formatos de imagen que un navegador pinta sin ayuda. Los animados de
# esta lista se guardan intactos; el resto se normaliza a JPEG.
ANIMABLES = {"GIF", "WEBP", "APNG"}

# Un video de un minuto en 1080p cabe de sobra; el tope esta para que
# nadie llene la tarjeta subiendo una pelicula por error.
app.config["MAX_CONTENT_LENGTH"] = LIMITE_PIEZA + (2 * 1024 * 1024)


def que_llego(datos, nombre=""):
    """Decide que es un archivo mirando su contenido, no su nombre.

    La extension no sirve para esto: la galeria de Android manda los
    archivos con nombres como "1000012345", sin extension ninguna, y
    un GIF perfectamente valido acababa rechazado por como se llamaba.
    El nombre solo se usa al final, para conservar la extension de un
    video cuando ya se sabe que es un video.

    Devuelve (tipo, formato, extension) o (None, None, None).
    """
    try:
        img = Image.open(io.BytesIO(datos))
        fmt = (img.format or "").upper()
        if fmt:
            animada = getattr(img, "is_animated", False)
            if animada and fmt in ANIMABLES:
                return "imagen", fmt, "." + fmt.lower()
            # Las fijas se reencodan a JPEG mas adelante
            return "imagen", fmt, ".jpg"
    except Exception:
        pass

    for pos, firma in FIRMAS_VIDEO:
        if datos[pos:pos + len(firma)] == firma:
            ext = Path(nombre).suffix.lower()
            return "video", "VIDEO", (ext if ext in EXT_VIDEO else ".mp4")

    return None, None, None


def bromas_fabrica():
    return {
        letra: {
            "nombre": f"Broma {letra.upper()}",
            # Segundos antes de quitarse sola. 0 = se queda hasta que la
            # quites, que es lo normal para una broma: el ritmo lo pone
            # quien la cuenta, no un reloj.
            "tope": 0,
            "piezas": {p: None for p in PIEZAS},
        }
        for letra in RANURAS
    }


bromas = bromas_fabrica()


def cargar_bromas():
    global bromas
    if not ARCHIVO_BROMAS.exists():
        return
    try:
        guardadas = json.loads(ARCHIVO_BROMAS.read_text())
    except Exception as e:
        print(f"No se pudieron leer las bromas: {e}")
        return

    nuevas = bromas_fabrica()
    for letra in RANURAS:
        g = guardadas.get(letra)
        if not isinstance(g, dict):
            continue
        nuevas[letra]["nombre"] = str(g.get("nombre") or
                                      nuevas[letra]["nombre"])[:40]
        try:
            nuevas[letra]["tope"] = max(0, min(600, int(g.get("tope", 0))))
        except (TypeError, ValueError):
            pass
        for p in PIEZAS:
            pieza = (g.get("piezas") or {}).get(p)
            # Una pieza cuyo archivo ya no esta se olvida: asi el admin
            # no ensena botones que no van a pintar nada.
            if (isinstance(pieza, dict) and pieza.get("archivo")
                    and (DIR_BROMAS / pieza["archivo"]).exists()):
                nuevas[letra]["piezas"][p] = {
                    "archivo": pieza["archivo"],
                    "tipo": ("video" if pieza.get("tipo") == "video"
                             else "imagen"),
                }
    bromas = nuevas


def guardar_bromas():
    try:
        ARCHIVO_BROMAS.write_text(
            json.dumps(bromas, indent=2, ensure_ascii=False))
        return True
    except Exception as e:
        print(f"No se pudieron guardar las bromas: {e}")
        return False


DIR_BROMAS.mkdir(exist_ok=True)
cargar_bromas()


# ---------------------------------------------------------------
# Tipografia
#
# Tres estilos y no tres nombres de fuente: lo que cambia el caracter
# de una pantalla no es solo la familia, sino el peso y el espaciado
# entre letras. Una serif de invitacion, una sans ligera con aire y una
# sans compacta con fuerza se distinguen de lejos; tres familias
# parecidas, no.
#
# Cada una lista varias fuentes en orden. El navegador usa la primera
# que exista, y PIL hace lo mismo con los archivos para el marco de la
# foto, asi que la pantalla y la copia impresa salen a juego sin
# depender de que la Pi tenga una fuente concreta instalada.
# ---------------------------------------------------------------

TIPOGRAFIAS = {
    "clasica": {
        "nombre": "Clasica",
        "pista": "Serif de invitacion. La de siempre.",
        "css": '"Noto Serif", "Liberation Serif", "DejaVu Serif", '
               'Georgia, serif',
        "peso": "600",
        "espaciado": "0",
        "ttf": (
            "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        ),
    },
    "moderna": {
        "nombre": "Moderna",
        "pista": "Sans ligera, con las letras separadas. Mas sobria.",
        "css": '"Noto Sans", "Liberation Sans", "DejaVu Sans", '
               'system-ui, sans-serif',
        "peso": "300",
        "espaciado": "0.06em",
        "ttf": (
            "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ),
    },
    "marcada": {
        "nombre": "Marcada",
        "pista": "Sans compacta y pesada. Se lee desde el otro lado del salon.",
        "css": '"DejaVu Sans Condensed", "Liberation Sans Narrow", '
               '"Noto Sans", "DejaVu Sans", sans-serif',
        "peso": "700",
        "espaciado": "-0.01em",
        "ttf": (
            "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ),
    },
}


def tipografia():
    """La elegida, o la clasica si el valor guardado no existe."""
    return TIPOGRAFIAS.get(evento.get("tipografia", "clasica"),
                           TIPOGRAFIAS["clasica"])


# Las partes de la pantalla que pueden llevar color propio. El segundo
# valor es de donde sale el color cuando el campo se deja vacio:
# "acento" toma el del evento y un codigo se usa tal cual. Dejarlo en
# blanco es lo normal; los campos existen para el evento que trae
# colores definidos y quiere que el espejo los siga.
PARTES_COLOR = (
    ("color_etiqueta",  "acento",  "Texto de arriba"),
    ("color_nombre",    "#ffffff", "Nombre del evento"),
    ("color_subtitulo", "#ffffff", "Subtitulo"),
    ("color_fecha",     "#8a8a8a", "Fecha"),
    ("color_lineas",    "acento",  "Filetes y borde"),
    ("color_centro",    "#777777", "Texto del centro"),
    ("color_pie",       "#8a8a8a", "Texto junto al codigo QR"),
)


def color_de(clave):
    """El color de una parte: el suyo, o el que herede."""
    propio = str(evento.get(clave, "")).strip()
    if propio.startswith("#") and len(propio) == 7:
        return propio
    for k, respaldo, _ in PARTES_COLOR:
        if k == clave:
            if respaldo == "acento":
                ac = str(evento.get("acento", "")).strip()
                return ac if ac.startswith("#") else "#b9a48a"
            return respaldo
    return "#ffffff"


def colores_pantalla():
    return {k: color_de(k) for k, _, _ in PARTES_COLOR}

# ---------------------------------------------------------------
# Impresion
#
# Se habla con CUPS por la linea de comandos (`lp`, `lpstat`) en vez de
# con pycups. Son dos llamadas y evita una dependencia que habria que
# compilar en la Pi; ademas el mismo codigo sirve para la impresora de
# verdad y para la impresora PDF virtual con la que se ensaya.
#
# El invitado pide la copia y recibe un numero de recogida. El operador
# la aprueba desde /admin. Esa aprobacion existe por una razon muy
# concreta: en una fiesta la gente se toma fotos que no quiere en papel,
# y cada hoja cuesta dinero y 47 segundos de impresora.
# ---------------------------------------------------------------

IMPRESION_FABRICA = {
    "activa": False,        # si no, el telefono ni siquiera ve el boton
    "impresora": "",        # nombre tal como lo conoce CUPS
    "aprobar": True,        # el operador da el visto bueno
    "opciones": "-o fit-to-page",
    "hojas": -1,            # restantes. -1 = no llevar la cuenta, 0 = se acabo
    "copias_sesion": 4,     # fotos maximas en la hoja de cada sesion
    # Modo manual: la impresora no va conectada a la Pi. Aprobar una foto
    # no la manda a CUPS; solo la marca lista y el operador la descarga
    # desde la cola y la imprime por su cuenta (p. ej. la app de Canon
    # por Wi-Fi). Existe porque la CP1500 no tiene driver para Linux.
    "manual": False,
}

impresion = dict(IMPRESION_FABRICA)


def cargar_impresion():
    global impresion
    if ARCHIVO_IMPRESION.exists():
        try:
            impresion = fundir(IMPRESION_FABRICA,
                               json.loads(ARCHIVO_IMPRESION.read_text()))
            # Antes era "copias por turno" y admitia hasta 10; ahora son
            # las fotos de la hoja y no caben mas de 4.
            impresion["copias_sesion"] = min(4, max(1, int(
                impresion.get("copias_sesion", 4))))
        except Exception as e:
            print(f"No se pudo leer la configuracion de impresion: {e}")


def guardar_impresion():
    try:
        ARCHIVO_IMPRESION.write_text(
            json.dumps(impresion, indent=2, ensure_ascii=False))
        return True
    except Exception as e:
        print(f"No se pudo guardar la configuracion de impresion: {e}")
        return False


cargar_impresion()


candado_cola = threading.Lock()
candado_recogida = threading.Lock()
cola = []                  # trabajos, el mas reciente al final
_ultima_recogida = 0


def impresoras_disponibles():
    """Nombres que CUPS conoce.

    Se usa `lpstat -e` y no `lpstat -p` a proposito: -e devuelve solo
    los nombres, uno por linea, mientras que -p los envuelve en texto
    traducido al idioma del sistema y habria que adivinar el formato.
    """
    try:
        salida = subprocess.run(["lpstat", "-e"], capture_output=True,
                                text=True, timeout=4).stdout
        return [l.strip() for l in salida.splitlines() if l.strip()]
    except Exception:
        return []


def siguiente_recogida():
    """Numero nuevo de recogida.

    Se pide una sola vez por turno, no una por foto: si alguien imprime
    dos fotos y se lleva los numeros 07 y 08, en el momento de la entrega
    se arma justo el enredo que el numero venia a evitar. Una persona,
    un numero, aunque sean tres fotos.

    Lleva candado propio y no el de la cola porque se pide con el candado
    del estado ya tomado; siendo el ultimo eslabon, no hay manera de que
    dos hilos se queden esperandose.
    """
    global _ultima_recogida
    with candado_recogida:
        _ultima_recogida += 1
        return _ultima_recogida


def encolar(archivo, recogida):
    """Mete una foto en la cola con el numero del turno que la pidio."""
    with candado_cola:
        trabajo = {
            "id": secrets.token_urlsafe(6),
            "archivo": archivo,
            "recogida": recogida,
            "estado": "espera" if impresion["aprobar"] else "cola",
            "detalle": "",
            "pedida": time.time(),
        }
        cola.append(trabajo)
        del cola[:-MAX_COLA_VISIBLE]
        return trabajo


def enviar_a_impresora(trabajo):
    """Manda el archivo a CUPS. Devuelve (ok, detalle)."""
    if impresion.get("manual"):
        # Nada que mandar: la foto queda lista para que el operador la
        # descargue. Se valida que exista para no aprobar un hueco.
        if not (FOTOS_DIR / trabajo["archivo"]).exists():
            return False, "la foto ya no esta"
        return True, "descargala e imprimela a mano"

    destino = impresion.get("impresora", "").strip()
    if not destino:
        return False, "no hay impresora elegida"

    ruta = FOTOS_DIR / trabajo["archivo"]
    if not ruta.exists():
        return False, "la foto ya no esta"

    cmd = ["lp", "-d", destino]
    try:
        cmd += shlex.split(impresion.get("opciones", ""))
    except ValueError:
        return False, "las opciones de impresion estan mal escritas"
    cmd.append(str(ruta))

    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        return False, "la impresora no contesto"
    except Exception as e:
        return False, str(e)

    if r.returncode != 0:
        return False, (r.stderr or r.stdout).strip()[:120] or "fallo al imprimir"
    return True, (r.stdout or "").strip()[:120]


def trabajador_impresion():
    """Toma de la cola lo que ya esta aprobado y lo manda, de uno en uno.

    De uno en uno a proposito: la Selphy tarda unos tres cuartos de
    minuto por hoja y encimarle trabajos solo sirve para que el operador
    pierda la cuenta de que salio y que no.
    """
    while True:
        pendiente = None
        with candado_cola:
            for t in cola:
                if t["estado"] == "cola":
                    t["estado"] = "imprimiendo"
                    pendiente = t
                    break

        if pendiente is None:
            time.sleep(1)
            continue

        ok, detalle = enviar_a_impresora(pendiente)

        with candado_cola:
            pendiente["estado"] = "lista" if ok else "error"
            pendiente["detalle"] = detalle
            pendiente["lista_en"] = time.time()
            if ok and impresion.get("hojas", 0) > 0:
                impresion["hojas"] -= 1
                guardar_impresion()


threading.Thread(target=trabajador_impresion, daemon=True).start()


# ---------------------------------------------------------------
# Camara y calibracion
# ---------------------------------------------------------------

camara = Picamera2()

# Dos configuraciones. La camara vive en modo video, que es rapido y
# barato de sondear para la vista previa; solo cambia a still durante
# el instante de la captura. Dejarla en still permanente hace que el
# sensor corra a 14 fps y que la previsualizacion ahogue a la captura.
CONFIG_VIDEO = camara.create_video_configuration(
    main={"size": RESOLUCION_PREVIA, "format": "RGB888"}
)

camara.configure(CONFIG_VIDEO)
camara.start()
time.sleep(1)

# Serializa todo acceso a la camara: sin esto, un sondeo de la vista
# previa puede colarse en medio de una captura.
candado_camara = threading.Lock()

# Ultimo veredicto sobre la camara. Se actualiza en cada captura y en
# cada cuadro de la vista previa, y es lo que el panel de admin enseña:
# asi el operador se entera de que el cable se solto sin tener que
# descubrirlo cuando alguien ya se puso a posar.
salud_camara = {"ok": True, "error": ""}


def marcar_camara(ok, error=""):
    salud_camara["ok"] = ok
    salud_camara["error"] = str(error)[:120]

# Las configuraciones de captura se arman una vez por tamano y se
# guardan: construirlas cuesta poco, pero se piden en el momento del
# disparo y ahi cada milisegundo se nota.
_still_cache = {}


def config_still():
    nombre = calibracion.get("resolucion", "media")
    if nombre not in RESOLUCIONES:
        nombre = "media"
    if nombre not in _still_cache:
        _still_cache[nombre] = camara.create_still_configuration(
            main={"size": RESOLUCIONES[nombre]}
        )
    return _still_cache[nombre]


def tomar_foto(ruta):
    """Captura cambiando de modo solo durante el disparo.

    No espera para siempre por la camara: si otra captura se quedo
    colgada con ella, falla a los ESPERA_CAMARA segundos en vez de
    sumarse al bloqueo.
    """
    try:
        if not candado_camara.acquire(timeout=ESPERA_CAMARA):
            raise RuntimeError("la camara no responde (ocupada)")
        try:
            camara.switch_mode_and_capture_file(config_still(), str(ruta))
        finally:
            candado_camara.release()
    except Exception as e:
        marcar_camara(False, e)
        raise
    marcar_camara(True)


def cuadro_previa():
    """Devuelve un cuadro de la vista previa como imagen PIL."""
    try:
        with candado_camara:
            img = camara.capture_image("main")
    except Exception as e:
        marcar_camara(False, e)
        raise
    marcar_camara(True)
    return img


CALIBRACION_FABRICA = {
    "brillo": 0.0,          # ExposureValue, -3 a 3
    "saturacion": 1.0,
    "contraste": 1.0,
    "nitidez": 1.0,
    "enfoque_auto": True,
    "enfoque": 2.0,         # dioptrias: 0 = infinito, 10 = muy cerca
    "color_auto": True,
    "tono": 0.0,            # -1 frio, +1 calido
    "resolucion": "media",  # alta | media | baja, ver RESOLUCIONES
}

calibracion = dict(CALIBRACION_FABRICA)


def cargar_calibracion():
    global calibracion
    if ARCHIVO_CALIBRACION.exists():
        try:
            calibracion = fundir(CALIBRACION_FABRICA,
                                 json.loads(ARCHIVO_CALIBRACION.read_text()))
        except Exception as e:
            print(f"No se pudo leer la calibracion: {e}")


def guardar_calibracion():
    try:
        ARCHIVO_CALIBRACION.write_text(json.dumps(calibracion, indent=2))
        return True
    except Exception as e:
        print(f"No se pudo guardar la calibracion: {e}")
        return False


def aplicar_calibracion(bloqueada=False):
    """Aplica controles; bloqueada=True solo si ya se posee el lock."""
    c = {
        "ExposureValue": float(calibracion["brillo"]),
        "Saturation": float(calibracion["saturacion"]),
        "Contrast": float(calibracion["contraste"]),
        "Sharpness": float(calibracion["nitidez"]),
    }

    if calibracion["enfoque_auto"]:
        c["AfMode"] = 2
    else:
        c["AfMode"] = 0
        c["LensPosition"] = float(calibracion["enfoque"])

    if calibracion["color_auto"]:
        c["AwbEnable"] = True
    else:
        t = float(calibracion["tono"])
        c["AwbEnable"] = False
        c["ColourGains"] = (2.0 + t * 0.8, 2.0 - t * 0.8)

    try:
        if bloqueada:
            camara.set_controls(c)
        else:
            with candado_camara:
                camara.set_controls(c)
    except Exception as e:
        print(f"Error al aplicar calibracion: {e}")


cargar_calibracion()
aplicar_calibracion()


# NetworkManager reparte 10.42.x.x cuando una conexion usa
# ipv4.method shared, que es justo como esta armado el punto de acceso.
# Encontrar una direccion en ese rango es la senal de que el espejo
# esta dando su propia red.
PREFIJO_AP = "10.42."


# Las direcciones se releen cada pocos segundos en vez de en cada
# consulta: la pantalla pregunta por el QR varias veces por segundo y
# cada telefono conectado hace lo mismo, asi que sin esto la Pi se
# pasaria el evento lanzando subprocesos para averiguar algo que casi
# nunca cambia. Tres segundos es suficiente para que el cambio de red
# se note de inmediato a ojo.
_ips_cache = {"cuando": 0.0, "lista": []}
TTL_IPS = 3.0


def ips_propias():
    """Direcciones IPv4 de la maquina, sin la de loopback."""
    ahora = time.time()
    if ahora - _ips_cache["cuando"] < TTL_IPS:
        return _ips_cache["lista"]
    try:
        salida = subprocess.run(["hostname", "-I"], capture_output=True,
                                text=True, timeout=1).stdout.split()
        lista = [ip for ip in salida
                 if ":" not in ip and not ip.startswith("127.")]
    except Exception:
        lista = _ips_cache["lista"]
    _ips_cache["cuando"] = ahora
    _ips_cache["lista"] = lista
    return lista


def ip_local():
    """Direccion por la que los invitados pueden alcanzar al espejo.

    Se consulta cada vez, no una sola vez al arrancar: cambia al pasar
    de cliente de wifi a punto de acceso, y el QR tiene que seguir ese
    cambio sin reiniciar nada.

    El orden importa y se aprendio probando. Si el espejo esta dando su
    propia red, esa direccion manda sobre cualquier otra, aunque haya un
    cable conectado: los telefonos de los invitados estan colgados del
    punto de acceso y no saben llegar a ninguna otra parte. Antes se
    preguntaba primero por la ruta por defecto, y con el cable puesto el
    QR apuntaba a una direccion que desde la fiesta no existe.
    """
    propias = ips_propias()

    # 1) La del punto de acceso, si lo hay
    for ip in propias:
        if ip.startswith(PREFIJO_AP):
            return ip

    # 2) La de la ruta por defecto (hay internet o puerta de enlace)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.3)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        if ip and not ip.startswith("127."):
            return ip
    except Exception:
        pass

    # 3) Lo que haya
    if propias:
        return propias[0]

    return "127.0.0.1"


def base_url():
    return f"http://{ip_local()}:{PUERTO}"


# ---------------------------------------------------------------
# Diagnostico
#
# Lo que el operador necesita saber de un vistazo, desde el telefono y
# con el salon lleno. La idea es que una llamada pase de "no funciona"
# a "dice que la camara no esta", que es lo unico que vuelve arreglable
# un problema a distancia.
# ---------------------------------------------------------------

# Si el puerto 80 se pudo abrir. Se llena al arrancar y el panel de
# admin lo ensena, porque sin el los telefonos no abren la pagina solos
# y conviene enterarse antes de la fiesta y no durante.
portal_activo = {"ok": False, "error": "todavia sin arrancar"}


def espacio_disco():
    """Devuelve (libres_mb, porcentaje_usado) de donde viven las fotos."""
    try:
        u = shutil.disk_usage(FOTOS_DIR)
        return int(u.free / 1048576), int(u.used * 100 / u.total)
    except Exception:
        return -1, -1


def fotos_guardadas():
    try:
        return sum(1 for _ in FOTOS_DIR.glob("*.jpg"))
    except Exception:
        return -1


def encendida_desde():
    """Minutos que lleva prendida la Pi."""
    try:
        return int(float(Path("/proc/uptime").read_text().split()[0]) / 60)
    except Exception:
        return -1


def diagnostico():
    ip = ip_local()
    destino = impresion.get("impresora", "").strip()
    conectadas = impresoras_disponibles()
    libres, usado = espacio_disco()

    with candado_cola:
        pendientes = sum(1 for t in cola
                         if t["estado"] in ("espera", "cola", "imprimiendo"))

    return {
        "camara_ok": salud_camara["ok"],
        "camara_error": salud_camara["error"],
        "impresora": destino,
        # En modo manual no hay impresora que vigilar: se da por buena
        # para que el diagnostico no avise de un fallo que no existe.
        "impresora_ok": bool(impresion.get("manual"))
                        or (bool(destino) and destino in conectadas),
        "impresion_activa": bool(impresion.get("activa")),
        "hojas": impresion.get("hojas", -1),
        "pendientes": pendientes,
        "ip": ip,
        # 10.42.x.x es el rango que reparte NetworkManager en modo
        # compartido: si la IP cae ahi, el espejo esta dando su propia
        # red y no colgado de un router ajeno.
        "red_propia": ip.startswith("10.42."),
        "disco_libre_mb": libres,
        "disco_usado_pct": usado,
        "fotos": fotos_guardadas(),
        "minutos_encendida": encendida_desde(),
        "portal_ok": portal_activo["ok"],
        "portal_error": portal_activo["error"],
        "modo_qr": evento.get("modo_qr", "wifi"),
        "conectados": len(_dhcp_desde),
        "leases_ok": salud_leases["encontrado"],
        "estaciones_ok": salud_estaciones["ok"],
        "atorones": atorones["n"],
        "atoron_ultimo": atorones["ultimo"],
        "leases_fuente": salud_leases["archivo"],
        "leases_error": (salud_leases["error"]
                         or ("" if salud_leases["encontrado"]
                             else "sin tabla de vecinos ni leases")),
        "atorados": cuantos_atorados(),
        "visitas": len(visitas),
        "fase": estado["fase"],
        "marco_activo": bool(evento.get("marco_activo")),
        "tipografia": tipografia()["nombre"],
        "fuente_archivo": fuente_usada["archivo"],
        "fuente_pobre": fuente_usada["respaldo_feo"],
        "piezas_listas": sum(
            1 for letra in RANURAS for p in PIEZAS
            if bromas[letra]["piezas"][p] is not None),
        "show_activo": bool(estado["show"]),
    }


# ---------------------------------------------------------------
# Textos
# ---------------------------------------------------------------

T = {
    "es": {
        "tomar": "Tomar foto",
        "otra": "Tomar otra",
        "terminar": "Terminar mi sesion",
        "sigo": "Sigo aqui",
        "aviso_espejo": "El espejo pasa al siguiente en {s} s",
        "confirmar_fin": "Terminas tu sesion? Ya no vas a poder descargar "
                         "ni imprimir estas fotos desde este telefono.",
        "cerrada_t": "Sesion terminada",
        "cerrada_p": "Descon\u00e9ctate del Wi-Fi PhotoBooth para recuperar tu "
                     "internet y dejarle lugar a otros invitados.",
        "listo": "Listo para disparar",
        "espera_otro": "Alguien est\u00e1 usando el espejo. Espera tu turno: "
                       "tu bot\u00f3n se prende solo. No escanees otra vez.",
        "espera_otro_viejo": "Alguien se esta tomando su foto. Tu boton se "
                       "prende solo en cuanto acabe.",
        "mira": "Mira al espejo:",
        "capturando": "Capturando...",
        "fotos": "foto(s) tuyas",
        "sigue_tuyo": "Tus fotos se quedan aqui aunque pase el siguiente.",
        "guardar_pista": "Manten presionada una foto para guardarla en tu galeria",
        "descargar": "Descargar",
        "guardar": "Guardar",
        "descartar": "Descartar",
        "confirmar_descartar": "Quitar esta foto? Dejaras de verla aqui y ya "
                               "no se va a poder imprimir.",
        # El visor de iOS
        "ios_t": "Manten presionada la foto de arriba",
        "ios_p": "y elige \"Anadir a Fotos\".",
        "ios_safari": "Abrir en Safari para guardar",
        "ios_safari_p": "Si no se guarda aqui: toca \u00abListo\u00bb arriba, "
                        "abre Safari y escribe 10.42.0.1",
        "ios_ojo": "No uses el boton de compartir del navegador: manda un "
                   "enlace que solo funciona aqui, no la foto. Guardala "
                   "primero y compartela desde tu galeria.",
        "cerrar": "Cerrar",
        "otro_idioma": "English",
        # impresion
        "imprimir": "Imprimir",
        "pedida": "Pedida",
        "recogida": "Numero {n}",
        "recogida_pista": "Recoge tu foto con el encargado del espejo y di tu numero.",
        "sin_papel": "Ya no hay papel",
        "tope_copias": "Ya pediste tus impresiones de este turno",
        # hoja de la sesion
        "elegir": "Elegir",
        "elegida": "\u2713 Elegida",
        "barra_cuenta": "{k} de {n} fotos elegidas",
        "imprimir_hoja": "Imprimir mi hoja",
        "confirmar_hoja": "Se imprime UNA sola hoja por sesion con las {k} "
                          "fotos elegidas. Despues ya no se puede cambiar. "
                          "Imprimir?",
        "max_fotos": "Maximo {n} fotos por hoja",
        "pop_t": "\u00bfTe gustar\u00eda imprimir tus fotos?",
        "pop_s": "Hasta {n} fotos diferentes por sesi\u00f3n",
        "pop_s2": "Todas salen juntas en una sola hoja.",
        "pop_si": "S\u00ed, elegir fotos",
        "pop_no": "Ahora no",
        "pop_fin": "Terminar sin imprimir",
        "hoja_auto": "Tu hoja se est\u00e1 imprimiendo. Rec\u00f3gela en "
                     "la impresora en un minuto.",
        "hoja_lista_auto": "Tu hoja ya sali\u00f3. Rec\u00f3gela en la "
                           "impresora. Cuando termines, descon\u00e9ctate del Wi-Fi PhotoBooth.",
        "hoja_operador": "N\u00famero {n}: recoge tu hoja con el encargado "
                         "y di tu n\u00famero. Cuando termines, descon\u00e9ctate del Wi-Fi PhotoBooth.",
        "hoja_error": "La impresora tuvo un problema. Avisa al encargado "
                      "(n\u00famero {n}).",
        "hoja_falla": "No se pudo armar tu hoja. Intenta otra vez.",
        "cancelar": "Cancelar",
        "entendido": "Entendido",
        # pantalla del espejo
        "esp_titulo": "Llevate tu foto",
        "esp_sub": "Escanea el codigo con tu telefono",
        "esp_sub_wifi": "Escanea para conectarte y tomarte la foto",
        "esp_listo": "Cuando quieras",
        "esp_libre": "Disponible",
        "esp_uso": "En uso",
        "esp_pasos": "1 Escanea \u00b7 2 T\u00f3mate tu foto \u00b7 3 Elige e imprime",
        "esp_uno": "Un tel\u00e9fono a la vez",
        "esp_uso_t": "EN USO \u00b7 Espera tu turno",
        "esp_uso_s": "No escanees todav\u00eda",
        "esp_uso_seg": "No escanees todav\u00eda \u00b7 Siguiente turno en {s} s",
        "esp_hecho_t": "\u00a1Listo! Tu foto ya est\u00e1 en tu tel\u00e9fono",
        "esp_hecho_s": "Ya no escanees: todo sigue en tu tel\u00e9fono",
        "esp_conectado": "\u00bfYa est\u00e1s conectado? Escanea aqu\u00ed",
        "esp_p1": "\u2190 Escanea este c\u00f3digo con tu c\u00e1mara",
        "esp_p2": "Toca \u00abConectar\u00bb y se abre la p\u00e1gina del espejo",
        "esp_p3": "En tu tel\u00e9fono toca \u00abTomar foto\u00bb y mira aqu\u00ed",
        "esp_paso": "Paso {k} de 3 \u00b7 Un tel\u00e9fono a la vez",
        "bien1": "1 de 3\n\nToca \u00abTomar foto\u00bb y mira al espejo.",
        "bien2": "2 de 3\n\nElige hasta {n} fotos e impr\u00edmelas juntas en una sola hoja.",
        "bien3": "3 de 3\n\nNo vuelvas a escanear: todo pasa en esta p\u00e1gina."
                 " Cuando termines, descon\u00e9ctate del Wi-Fi PhotoBooth.",
        "siguiente": "Siguiente",
        "bien": "1. Toca \u00abTomar foto\u00bb\n2. Mira al espejo\n"
                "3. Elige hasta {n} fotos e impr\u00edmelas\n\n"
                "No vuelvas a escanear: todo pasa en esta p\u00e1gina.",
        # aviso para quien se conecto y no abrio nada
        "atorado_t": "Te conectaste y no paso nada?",
        "atorado_s": "Escanea este codigo",
    },
    "en": {
        "tomar": "Take photo",
        "otra": "Take another",
        "terminar": "End my session",
        "sigo": "I am still here",
        "aviso_espejo": "The mirror moves on in {s} s",
        "confirmar_fin": "End your session? You will not be able to download "
                         "or print these photos from this phone.",
        "cerrada_t": "Session ended",
        "cerrada_p": "Disconnect from the PhotoBooth Wi-Fi to get your internet "
                     "back and make room for other guests.",
        "listo": "Ready to shoot",
        "espera_otro": "Someone is using the mirror. Wait your turn: your "
                       "button turns on by itself. Don't scan again.",
        "espera_otro_viejo": "Someone is taking their photo. Your button turns "
                       "back on by itself as soon as they finish.",
        "mira": "Look at the mirror:",
        "capturando": "Capturing...",
        "fotos": "photo(s) of yours",
        "sigue_tuyo": "Your photos stay here even after the next person goes.",
        "guardar_pista": "Press and hold a photo to save it to your gallery",
        "descargar": "Download",
        "guardar": "Save",
        "descartar": "Discard",
        "confirmar_descartar": "Remove this photo? It will disappear from "
                               "here and can no longer be printed.",
        # El visor de iOS
        "ios_t": "Press and hold the photo above",
        "ios_p": "and choose \"Add to Photos\".",
        "ios_safari": "Open in Safari to save",
        "ios_safari_p": "If it does not save here: tap \u201cDone\u201d at the top, "
                        "open Safari and type 10.42.0.1",
        "ios_ojo": "Do not use the browser share button: it sends a link "
                   "that only works here, not the photo. Save it first and "
                   "share it from your gallery.",
        "cerrar": "Close",
        "otro_idioma": "Espanol",
        # impresion
        "imprimir": "Print",
        "pedida": "Requested",
        "recogida": "Number {n}",
        "recogida_pista": "Pick your photo up with the attendant and give them your number.",
        "sin_papel": "Out of paper",
        "tope_copias": "You already requested your prints for this turn",
        # hoja de la sesion
        "elegir": "Select",
        "elegida": "\u2713 Selected",
        "barra_cuenta": "{k} of {n} photos selected",
        "imprimir_hoja": "Print my sheet",
        "confirmar_hoja": "Only ONE sheet is printed per session, with the "
                          "{k} selected photos. You cannot change it "
                          "afterwards. Print?",
        "max_fotos": "Up to {n} photos per sheet",
        "pop_t": "Would you like to print your photos?",
        "pop_s": "Up to {n} different pictures per session",
        "pop_s2": "They all print together on one sheet.",
        "pop_si": "Yes, choose photos",
        "pop_no": "Not now",
        "pop_fin": "End without printing",
        "hoja_auto": "Your sheet is printing. Pick it up at the printer "
                     "in about a minute.",
        "hoja_lista_auto": "Your sheet is ready. Pick it up at the printer. When you're done, disconnect from the PhotoBooth Wi-Fi.",
        "hoja_operador": "Number {n}: pick up your sheet from the attendant "
                         "and give them your number. When you're done, disconnect from the PhotoBooth Wi-Fi.",
        "hoja_error": "The printer had a problem. Tell the attendant "
                      "(number {n}).",
        "hoja_falla": "Your sheet could not be made. Please try again.",
        "cancelar": "Cancel",
        "entendido": "OK",
        # pantalla del espejo
        "esp_titulo": "Take your photo home",
        "esp_sub": "Scan the code with your phone",
        "esp_sub_wifi": "Scan to connect and take your photo",
        "esp_listo": "Whenever you're ready",
        "esp_libre": "Available",
        "esp_uso": "In use",
        "esp_pasos": "1 Scan \u00b7 2 Take your photo \u00b7 3 Pick & print",
        "esp_uno": "One phone at a time",
        "esp_uso_t": "IN USE \u00b7 Wait your turn",
        "esp_uso_s": "Don't scan yet",
        "esp_uso_seg": "Don't scan yet \u00b7 Next turn in {s} s",
        "esp_hecho_t": "Done! Your photo is on your phone",
        "esp_hecho_s": "No need to scan again: it's all on your phone",
        "esp_conectado": "Already connected? Scan here",
        "esp_p1": "\u2190 Scan this code with your camera",
        "esp_p2": "Tap \u201cJoin\u201d and the mirror page opens",
        "esp_p3": "On your phone tap \u201cTake photo\u201d and look here",
        "esp_paso": "Step {k} of 3 \u00b7 One phone at a time",
        "bien1": "1 of 3\n\nTap \u201cTake photo\u201d and look at the mirror.",
        "bien2": "2 of 3\n\nPick up to {n} photos and print them together on one sheet.",
        "bien3": "3 of 3\n\nDon't scan again: everything happens on this page."
                 " When you're done, disconnect from the PhotoBooth Wi-Fi.",
        "siguiente": "Next",
        "bien": "1. Tap \u201cTake photo\u201d\n2. Look at the mirror\n"
                "3. Pick up to {n} photos and print them\n\n"
                "Don't scan again: everything happens on this page.",
        # aviso para quien se conecto y no abrio nada
        "atorado_t": "Did you connect but nothing happened?",
        "atorado_s": "Scan this code",
    },
}


def idioma():
    pedido = request.args.get("lang")
    if pedido in T:
        return pedido
    return request.accept_languages.best_match(["es", "en"]) or "en"


# ---------------------------------------------------------------
# Estado compartido
# ---------------------------------------------------------------

candado = threading.Lock()

# Quien tiene el espejo AHORA. Esto dura segundos, no minutos.
estado = {
    "fase": "libre",        # libre | cuenta | capturando | resultado | gracia
    "dueno": None,          # token de quien lo esta usando
    "cuenta_fin": 0,
    "resultado_fin": 0,
    "accion": 0,            # ultima vez que el dueno HIZO algo
    "foto": None,           # la que se esta ensenando en el espejo
    # La pieza que esta tapando la pantalla, si hay alguna:
    #   {"ranura": "a", "pieza": "intro", "fin": 0}
    # fin = 0 quiere decir que se queda hasta que la quiten.
    "show": None,
}

# Las fotos de cada telefono, que sobreviven a que el espejo se suelte.
#
# Esta separacion es la que permite soltar el espejo en cuanto la foto
# esta tomada: la persona sigue viendo sus fotos y pidiendo copias desde
# su telefono mientras el siguiente ya se esta tomando la suya. Hasta
# booth11 las fotos vivian dentro del estado del espejo y se borraban al
# liberar, asi que habia que elegir entre soltar el espejo pronto o
# dejarle a la persona sus fotos. Ahora no hay que elegir.
visitas = {}        # token -> {"fotos": [], "recogida": None, "visto": t}
_token_por_ip = {}  # ip -> ultima sesion que abrio ese telefono

_qr_cache = {"url": None, "png": None}


def nuevo_token():
    return secrets.token_urlsafe(8)


def nueva_visita(token=None):
    """Apunta el telefono que acaba de abrir la pagina, o lo recupera.

    Todas las lecturas y escrituras de `visitas` pasan por `candado`,
    asi que esto se llama con el candado ya tomado.
    """
    token = token or nuevo_token()
    v = visitas.get(token)
    if v is None:
        v = {"fotos": [], "recogida": None, "visto": time.time()}
        visitas[token] = v
    else:
        v["visto"] = time.time()
    return token, v


def soltar_espejo():
    """Deja el espejo libre para el siguiente.

    No toca las visitas: quien acaba de tomarse la foto se queda con
    ella en la mano aunque el espejo ya sea de alguien mas.
    """
    estado["fase"] = "libre"
    estado["dueno"] = None
    estado["foto"] = None
    estado["cuenta_fin"] = 0
    estado["resultado_fin"] = 0
    estado["accion"] = 0


def marcar_accion(token):
    """Reinicia el reloj del espejo si quien actuo es su dueno.

    Una sola puerta para las tres acciones que cuentan (disparar,
    imprimir, descargar), para que no se olvide ninguna al anadir otra.
    Se llama con el candado tomado.
    """
    if token == estado["dueno"]:
        estado["accion"] = time.time()


def olvidar_visitas():
    """Tira las visitas viejas para que la memoria no crezca sin freno."""
    limite = time.time() - VIDA_VISITA
    for tok in [t for t, v in visitas.items() if v["visto"] < limite]:
        if tok != estado["dueno"]:
            del visitas[tok]


with candado:
    soltar_espejo()


def _qr_png(texto):
    """Dibuja un QR y lo devuelve en base64, guardando el ultimo.

    La pantalla pide el codigo varias veces por segundo; redibujarlo
    cada vez seria tirar CPU que la camara necesita.
    """
    if _qr_cache["url"] == texto:
        return _qr_cache["png"]
    img = qrcode.make(texto, box_size=10, border=2)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    png = base64.b64encode(buf.getvalue()).decode()
    _qr_cache["url"] = texto
    _qr_cache["png"] = png
    return png


def _escapar_wifi(s):
    """El formato WIFI: usa ; , : y \\ como separadores."""
    for c in ("\\", ";", ",", ":", '"'):
        s = s.replace(c, "\\" + c)
    return s


def texto_qr_wifi():
    """Credenciales en el formato que leen iOS y Android nativamente."""
    ssid = str(evento.get("wifi_ssid", "")).strip()
    if not ssid:
        return None
    clave = str(evento.get("wifi_clave", ""))
    if not clave:
        return None  # No anunciar una red abierta por error de configuracion.
    tipo = "WPA"
    return (f"WIFI:T:{tipo};S:{_escapar_wifi(ssid)};"
            f"P:{_escapar_wifi(clave)};;")


def qr_para_pantalla():
    """El codigo que toca ensenar segun como este configurado el evento.

    Con el punto de acceso andando, lo util es el codigo de wifi: un
    escaneo conecta el telefono y el portal cautivo abre la pagina sola.
    El codigo de enlace sigue disponible para quien ya este en la red.
    """
    if evento.get("modo_qr", "wifi") == "wifi":
        texto = texto_qr_wifi()
        if texto:
            return _qr_png(texto)
    return qr_enlace()


_qr_enlace = {"url": None, "png": None}


def qr_enlace_cache():
    """El QR de /entrar, hecho una sola vez: la pantalla lo pide 3 veces
    por segundo y armarlo cada vez no tiene caso."""
    url = f"{base_url()}/entrar"
    if _qr_enlace["url"] != url:
        _qr_enlace["png"] = _qr_png(url)
        _qr_enlace["url"] = url
    return _qr_enlace["png"]


def qr_enlace():
    """QR que lleva a la pagina, sin token.

    Hasta booth11 el codigo llevaba el token de la siguiente sesion, y
    se quemaba al usarse: quien le tomaba una foto a la pantalla o
    tardaba en escanear se encontraba un "ese codigo ya no sirve". Ahora
    apunta a /entrar, que le reparte un token propio a cada telefono. El
    mismo codigo sirve para todos y no caduca nunca.
    """
    return _qr_png(f"{base_url()}/entrar")



# ---------------------------------------------------------------
# El marco de la foto
#
# Una copia impresa que no dice de que fiesta es, es una foto. Con el
# nombre y la fecha al pie es un recuerdo, y es lo que justifica el
# papel. Como el software ya guarda esos datos para la pantalla, aqui
# solo se usan.
#
# De paso resuelve un problema de formato: el sensor entrega 16:9 y el
# papel 4x6 es 3:2. Sin barra, la impresora deja dos bandas blancas de
# casi dos centimetros. La barra se dimensiona para que la foto
# compuesta quede en 3:2 exacto, asi que llena el papel sin recortar ni
# un pixel de la imagen.
# ---------------------------------------------------------------

PROPORCION_PAPEL = 3 / 2        # 4x6 pulgadas
MARCO_MIN = 0.07                # minimo de la altura, si ya viene en 3:2
ORIGINALES_DIR = FOTOS_DIR / "originales"
ORIGINALES_DIR.mkdir(exist_ok=True)

# Respaldos comunes, por si la tipografia elegida no tiene ninguno de
# sus archivos en esta Pi.
FUENTES_RESPALDO = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "/usr/share/fonts/truetype/piboto/Piboto-Regular.ttf",
)
_fuentes = {}
fuente_usada = {"archivo": "", "respaldo_feo": False}


def fuente_marco(tam, estilo=None):
    """La fuente de la tipografia elegida, al tamano pedido.

    Se recuerda cual se acabo usando para que el diagnostico pueda
    decirlo: si la Pi no tiene la fuente del estilo elegido, la foto
    sale igual pero con otra letra, y conviene enterarse antes de
    imprimir cien copias.
    """
    estilo = estilo or evento.get("tipografia", "clasica")
    clave = (estilo, tam)
    if clave in _fuentes:
        return _fuentes[clave]

    candidatas = tuple(TIPOGRAFIAS.get(estilo, {}).get("ttf", ()))
    carga = None
    for ruta in candidatas + FUENTES_RESPALDO:
        if Path(ruta).exists():
            try:
                carga = ImageFont.truetype(ruta, tam)
                fuente_usada["archivo"] = Path(ruta).name
                fuente_usada["respaldo_feo"] = False
                break
            except Exception:
                continue
    if carga is None:
        carga = ImageFont.load_default()
        fuente_usada["archivo"] = "(la de PIL)"
        fuente_usada["respaldo_feo"] = True
    _fuentes[clave] = carga
    return carga


def _color(txt, respaldo):
    """Convierte #rrggbb en una tupla, o devuelve el respaldo."""
    t = str(txt or "").strip().lstrip("#")
    if len(t) == 6:
        try:
            return tuple(int(t[i:i + 2], 16) for i in (0, 2, 4))
        except ValueError:
            pass
    return respaldo


def texto_marco():
    """Las dos lineas de la barra: titulo y pie."""
    titulo = str(evento.get("nombre", "")).strip()
    sub = str(evento.get("subtitulo", "")).strip()
    fecha = str(evento.get("fecha", "")).strip()
    pie = " · ".join([p for p in (sub, fecha) if p])
    return titulo, pie


def espejar_foto(ruta):
    """Voltea la foto como se veria en un espejo.

    Se hace sobre el archivo y no con CSS en la pantalla porque la
    pantalla volteaba la imagen entera: con el marco pegado, el nombre
    del evento salia escrito al reves, y asi se imprimia.
    """
    with Image.open(ruta) as img:
        img.transpose(Image.FLIP_LEFT_RIGHT).save(ruta, "JPEG", quality=92)


def aplicar_marco(ruta, destino=None):
    """Compone la foto con la barra y la guarda.

    La barra se calcula para dejar el resultado en 3:2. Si la foto ya
    viniera en esa proporcion o mas alta, se usa una barra minima en
    vez de deformar nada.
    """
    destino = destino or ruta
    titulo, pie = texto_marco()

    with Image.open(ruta) as img:
        foto = img.convert("RGB")

    an, al = foto.size
    alto_total = max(int(round(an / PROPORCION_PAPEL)), al + int(al * MARCO_MIN))
    barra = alto_total - al

    fondo = _color(evento.get("marco_fondo"), (16, 16, 20))
    tinta = _color(evento.get("marco_tinta") or evento.get("acento"),
                   (185, 164, 138))

    lienzo = Image.new("RGB", (an, alto_total), fondo)
    lienzo.paste(foto, (0, 0))
    d = ImageDraw.Draw(lienzo)

    # Filete del color de acento entre la foto y la barra
    grosor = max(1, int(an * 0.0012))
    d.rectangle([0, al, an, al + grosor], fill=tinta)

    # El texto se centra en el alto de la barra. Los tamanos salen de la
    # barra y no de numeros fijos, para que se vea igual en cualquier
    # resolucion de captura.
    hay_pie = bool(pie)
    t_tit = int(barra * (0.34 if hay_pie else 0.42))
    t_pie = int(barra * 0.19)
    hueco = int(barra * 0.10)

    f_tit = fuente_marco(t_tit)
    f_pie = fuente_marco(t_pie)

    # Se mide con el recuadro completo y no solo con su borde inferior:
    # textbbox empieza en el hueco del ascendente, asi que tomar solo
    # [3] cuenta un espacio en blanco que no esta ahi y baja el texto.
    bb_tit = d.textbbox((0, 0), titulo or " ", font=f_tit)
    bb_pie = d.textbbox((0, 0), pie or " ", font=f_pie)
    alto_tit = bb_tit[3] - bb_tit[1]
    alto_pie = (bb_pie[3] - bb_pie[1]) if hay_pie else 0
    alto_texto = alto_tit + (hueco + alto_pie if hay_pie else 0)
    y = al + grosor + (barra - grosor - alto_texto) // 2

    if titulo:
        d.text(((an - (bb_tit[2] - bb_tit[0])) // 2 - bb_tit[0], y - bb_tit[1]),
               titulo, font=f_tit,
               fill=_color(color_de("color_nombre"), (242, 242, 245)))
    if hay_pie:
        d.text(((an - (bb_pie[2] - bb_pie[0])) // 2 - bb_pie[0],
                y + alto_tit + hueco - bb_pie[1]),
               pie, font=f_pie, fill=tinta)

    lienzo.save(destino, "JPEG", quality=92)
    return True


# ---------------------------------------------------------------
# Hoja de la sesion
#
# Cada sesion imprime UNA hoja de 4x6 con las fotos que el invitado
# elige (hasta impresion["copias_sesion"], maximo 4). La Selphy tarda lo
# mismo en una hoja con una foto que con cuatro, y el cartucho trae 108
# hojas: asi alcanza para toda la fiesta.
#
# Hoja VERTICAL de 4x6, igual que el papel de la Selphy, con cuatro
# fotos VERTICALES en una cuadricula de 2x2. Cada foto lleva su propio
# banner con el nombre del evento, grande para que se lea en la copia
# impresa. Lineas en cruz para cortar la hoja en cuatro.
#
# La camara toma la foto acostada (16:9) y el espejo esta de pie, asi
# que cada foto se recorta al centro para parecerse a lo que el invitado
# ve en el reflejo. La cuenta, para alguien parado entre 1 y 2 metros:
#
#   - Un espejo plano deja ver, en el plano de quien se mira, una franja
#     del DOBLE de su ancho, sin importar la distancia: con el cristal
#     del Mirror (~0.56 m) son ~1.12 m de ancho.
#   - El IMX708 normal tiene ~66 grados de campo horizontal y ~41 de
#     vertical: a 1.5 m ve ~1.95 x 1.12 m.
#   - Para llenar una celda vertical sin deformar, el limite lo pone la
#     altura de la camara: a 1.5 m alcanza para ~0.94 m de ancho, que es
#     menos que lo que muestra el espejo. Asi que la foto usa toda la
#     altura y el centro del ancho (~48%).
#
# Si la camara se cambia por la de lente ancho, o el espejo se usa a
# otra distancia, basta con ajustar las tres constantes de abajo.
# ---------------------------------------------------------------

HOJA_ANCHO, HOJA_ALTO = 1200, 1800   # 4x6 vertical a 300 dpi
MAX_FOTOS_HOJA = 4
HOJA_COLS, HOJA_FILAS = 2, 2
HOJA_MARGEN = 24            # borde exterior, en pixeles
HOJA_HUECO = 24             # entre columnas
HOJA_HUECO_FILA = 24        # entre filas
HOJA_LINEA = (205, 205, 205)
HOJA_BANNER = 0.22          # alto del banner, fraccion de la celda
# Lo que tarda la Selphy en sacar la hoja. CUPS da el trabajo por hecho
# en cuanto lo recibe, asi que el telefono espera esto antes de decir
# que ya salio.
SEGUNDOS_IMPRESION = 60

ESPEJO_ANCHO_M = 0.56       # ancho del cristal
DISTANCIA_M = 1.5           # donde se para la gente (entre 1 y 2 m)
CAMARA_HFOV = 66.0          # campo horizontal de la camara, en grados


def _celda_hoja():
    """Ancho y alto de cada celda de la hoja."""
    w = (HOJA_ANCHO - 2 * HOJA_MARGEN - HOJA_HUECO * (HOJA_COLS - 1)) // HOJA_COLS
    h = (HOJA_ALTO - 2 * HOJA_MARGEN - HOJA_HUECO_FILA * (HOJA_FILAS - 1)) // HOJA_FILAS
    return w, h


def _recorte_espejo(img, aspecto):
    """Recorta img a ancho/alto = aspecto como se veria en el espejo.

    Ancho buscado: lo que el espejo deja ver a DISTANCIA_M, como
    fraccion de lo que ve la camara. Si para eso habria que salirse de la
    foto por arriba o por abajo, manda la altura. Siempre al centro: la
    camara va centrada en el espejo.
    """
    import math
    ancho_cam = 2 * DISTANCIA_M * math.tan(math.radians(CAMARA_HFOV / 2))
    frac = min(1.0, 2 * ESPEJO_ANCHO_M / ancho_cam)
    w = img.width * frac
    h = w / aspecto
    if h > img.height:
        h = img.height
        w = h * aspecto
    x = (img.width - w) / 2
    y = (img.height - h) / 2
    return img.crop((int(x), int(y), int(x + w), int(y + h)))


def _foto_sin_marco(nombre):
    """La foto sin barra y ya volteada como la vio el invitado."""
    original = ORIGINALES_DIR / nombre
    if original.exists():
        with Image.open(original) as img:
            foto = img.convert("RGB")
        # La original se guarda tal como salio del sensor, sin voltear
        if ESPEJAR_RESULTADO:
            foto = foto.transpose(Image.FLIP_LEFT_RIGHT)
        return foto
    # Sin marco no hay original aparte: la de la galeria ya es la foto sola
    with Image.open(FOTOS_DIR / nombre) as img:
        return img.convert("RGB")


def _fuente_que_quepa(texto, tam, ancho, d):
    """La fuente del evento al tamano pedido, o mas chica si no cabe."""
    while tam > 12:
        f = fuente_marco(tam)
        bb = d.textbbox((0, 0), texto or " ", font=f)
        if bb[2] - bb[0] <= ancho:
            return f
        tam -= 2
    return fuente_marco(tam)


def _celda_con_banner(foto, cw, ch):
    """Una foto vertical con su banner del evento abajo."""
    fondo = _color(evento.get("marco_fondo"), (16, 16, 20))
    if not evento.get("marco_activo"):
        return _recorte_espejo(foto, cw / ch).resize((cw, ch), Image.LANCZOS)

    tinta = _color(evento.get("marco_tinta") or evento.get("acento"),
                   (212, 175, 55))
    titulo, pie = texto_marco()
    banner = int(ch * HOJA_BANNER)
    alto_foto = ch - banner

    celda = Image.new("RGB", (cw, ch), fondo)
    celda.paste(_recorte_espejo(foto, cw / alto_foto)
                .resize((cw, alto_foto), Image.LANCZOS), (0, 0))
    d = ImageDraw.Draw(celda)
    grosor = 4
    d.rectangle([0, alto_foto, cw, alto_foto + grosor], fill=tinta)

    util = cw - 40
    f_tit = _fuente_que_quepa(titulo, int(banner * 0.33), util, d)
    f_pie = _fuente_que_quepa(pie, int(banner * 0.18), util, d)
    bt = d.textbbox((0, 0), titulo or " ", font=f_tit)
    bp = d.textbbox((0, 0), pie or " ", font=f_pie)
    alto_t = bt[3] - bt[1]
    alto_p = (bp[3] - bp[1]) if pie else 0
    hueco = int(banner * 0.08) if pie else 0
    y = alto_foto + grosor + (banner - grosor - alto_t - hueco - alto_p) // 2
    if titulo:
        d.text(((cw - (bt[2] - bt[0])) // 2 - bt[0], y - bt[1]), titulo,
               font=f_tit,
               fill=_color(color_de("color_nombre"), (245, 245, 248)))
    if pie:
        d.text(((cw - (bp[2] - bp[0])) // 2 - bp[0],
                y + alto_t + hueco - bp[1]), pie, font=f_pie, fill=tinta)
    return celda


def componer_hoja(nombres, destino):
    """Arma la hoja de 4x6 con las fotos elegidas y la guarda en destino."""
    lienzo = Image.new("RGB", (HOJA_ANCHO, HOJA_ALTO), (255, 255, 255))
    d = ImageDraw.Draw(lienzo)
    cw, ch = _celda_hoja()

    # Lineas de corte en cruz
    xc, yc = HOJA_ANCHO // 2, HOJA_ALTO // 2
    d.line([(xc, 0), (xc, HOJA_ALTO)], fill=HOJA_LINEA, width=2)
    d.line([(0, yc), (HOJA_ANCHO, yc)], fill=HOJA_LINEA, width=2)

    for i, nombre in enumerate(nombres[:HOJA_COLS * HOJA_FILAS]):
        fila, col = divmod(i, HOJA_COLS)
        x = HOJA_MARGEN + col * (cw + HOJA_HUECO)
        y = HOJA_MARGEN + fila * (ch + HOJA_HUECO_FILA)
        lienzo.paste(_celda_con_banner(_foto_sin_marco(nombre), cw, ch), (x, y))

    lienzo.save(destino, "JPEG", quality=94, dpi=(300, 300))
    return destino

# ---------------------------------------------------------------
# Telefonos atorados
#
# Un telefono que se conecta a la red del espejo y no abre el portal
# cautivo deja a su dueno mirando un "conectado sin internet" sin
# ninguna pista de que le falta un paso. Pasa en Samsung de forma
# consistente, y la causa esta del lado del telefono: sondea por HTTPS,
# donde no hay forma de interceptarlo sin un certificado valido.
#
# No se puede arreglar desde el servidor, pero si se puede DETECTAR, y
# eso basta para resolverlo bien: el espejo sabe quien esta conectado
# (los leases del DHCP) y quien ha pedido alguna pagina. La resta es la
# gente atorada, y solo cuando hay alguien asi aparece el aviso en la
# pantalla. El resto del tiempo el centro queda limpio.
# ---------------------------------------------------------------

candado_red = threading.Lock()
_dhcp_desde = {}        # ip -> primera vez que la vimos conectada
_http_vistas = {}       # ip -> ultima vez que pidio una pagina
salud_leases = {"encontrado": False, "archivo": "", "error": ""}


def _ips_por_leases():
    """Las direcciones que dnsmasq apunto al repartirlas."""
    ips = set()
    archivos = glob.glob(LEASES_DHCP)
    for ruta in archivos:
        try:
            for linea in Path(ruta).read_text().splitlines():
                partes = linea.split()
                if len(partes) >= 3 and partes[2].startswith(PREFIJO_AP):
                    ips.add(partes[2])
        except Exception:
            continue
    return ips, bool(archivos)


def _ips_por_vecinos():
    """Las direcciones que la Pi tiene enfrente, segun la tabla ARP.

    Esta es la fuente buena y la de los leases es el complemento: no
    depende de donde guarde los archivos esta version de
    NetworkManager, que es justo lo que fallo en la Pi de verdad. Un
    telefono conectado aparece aqui en cuanto habla con el espejo, sin
    importar quien le haya dado la direccion.
    """
    ips = set()
    try:
        salida = subprocess.run(["ip", "neigh", "show"], capture_output=True,
                                text=True, timeout=3).stdout
    except Exception:
        return ips, False

    for linea in salida.splitlines():
        partes = linea.split()
        if not partes or not partes[0].startswith(PREFIJO_AP):
            continue
        # FAILED e INCOMPLETE son direcciones que no contestan: estan
        # en la tabla pero no hay nadie ahi.
        if partes[-1] in ("FAILED", "INCOMPLETE"):
            continue
        ips.add(partes[0])
    return ips, True


def _estaciones_ap():
    """MAC -> segundos que lleva asociada a la antena del espejo.

    Es la unica fuente que se reinicia cuando un telefono se desconecta y
    vuelve: los leases duran horas y la tabla ARP guarda direcciones
    "STALE" mucho despues de que el telefono se fue. Devuelve None si no
    se puede leer (sin iw, o sin interfaz en modo AP), y entonces se usa
    el metodo anterior.
    """
    try:
        dev = subprocess.run(["iw", "dev"], capture_output=True,
                             text=True, timeout=3).stdout
    except Exception:
        return None
    ifaces, actual = [], None
    for linea in dev.splitlines():
        linea = linea.strip()
        if linea.startswith("Interface "):
            actual = linea.split()[1]
        elif linea == "type AP" and actual:
            ifaces.append(actual)
    if not ifaces:
        return None
    est = {}
    for iface in ifaces:
        try:
            salida = subprocess.run(["iw", "dev", iface, "station", "dump"],
                                    capture_output=True, text=True,
                                    timeout=3).stdout
        except Exception:
            continue
        mac = None
        for linea in salida.splitlines():
            linea = linea.strip()
            if linea.startswith("Station "):
                mac = linea.split()[1].lower()
            elif linea.startswith("connected time:") and mac:
                try:
                    est[mac] = int(linea.split()[2])
                except (IndexError, ValueError):
                    pass
    return est


def _mac_a_ip():
    """MAC -> IP, con la tabla ARP y los leases."""
    m = {}
    for ruta in glob.glob(LEASES_DHCP):
        try:
            for linea in Path(ruta).read_text().splitlines():
                partes = linea.split()
                if len(partes) >= 3 and partes[2].startswith(PREFIJO_AP):
                    m[partes[1].lower()] = partes[2]
        except Exception:
            continue
    try:
        salida = subprocess.run(["ip", "neigh", "show"], capture_output=True,
                                text=True, timeout=3).stdout
        for linea in salida.splitlines():
            partes = linea.split()
            if (partes and partes[0].startswith(PREFIJO_AP)
                    and "lladdr" in partes):
                m[partes[partes.index("lladdr") + 1].lower()] = partes[0]
    except Exception:
        pass
    return m


_conectado_desde = {}       # ip -> cuando empezo SU conexion actual
salud_estaciones = {"ok": False}


def revisar_estaciones():
    """Apunta cuando empezo la conexion actual de cada telefono."""
    est = _estaciones_ap()
    if est is None:
        salud_estaciones["ok"] = False
        return
    ahora = time.time()
    macs = _mac_a_ip()
    nuevo = {}
    for mac, segundos in est.items():
        ip = macs.get(mac)
        if ip:
            nuevo[ip] = ahora - segundos
    with candado_red:
        _conectado_desde.clear()
        _conectado_desde.update(nuevo)
    salud_estaciones["ok"] = True


def revisar_dhcp():
    """Apunta desde cuando esta conectado cada telefono.

    Se guarda la primera vez que *nosotros* lo vemos, y no ningun sello
    del sistema: el de los leases es la hora de caducidad, y la
    duracion la decide NetworkManager, asi que restarla seria adivinar.
    """
    ahora = time.time()
    vecinos, hay_tabla = _ips_por_vecinos()
    leases, hay_archivos = _ips_por_leases()
    ips = vecinos | leases

    if not hay_tabla and not hay_archivos:
        # Sin ninguna de las dos fuentes el aviso no sale, que es el
        # lado seguro. Pero queda apuntado: si el operador ve cero
        # telefonos con diez conectados, el diagnostico le dice por que.
        salud_leases.update(encontrado=False,
                            error="no hay tabla de vecinos ni leases")
        return

    salud_leases.update(
        encontrado=True, error="",
        archivo=("tabla de vecinos" if hay_tabla else "") +
                (" + leases" if hay_archivos and hay_tabla else
                 ("leases" if hay_archivos else "")))

    with candado_red:
        for ip in ips:
            _dhcp_desde.setdefault(ip, ahora)
        for ip in [i for i in _dhcp_desde if i not in ips]:
            del _dhcp_desde[ip]         # se desconecto


_ip_imp = {"t": 0.0, "nombre": None, "ip": None}
_ips_admin = set()      # aparatos que entraron al admin: no son invitados


def ip_impresora():
    """La IP de la impresora elegida, si va por la red del espejo.

    La impresora se conecta al Wi-Fi como un telefono mas, pero nunca
    abre una pagina: sin esto contaria como telefono atorado y sacaria
    el QR de ayuda. Se pregunta a CUPS cada minuto, no en cada peticion.
    """
    nombre = impresion.get("impresora", "").strip()
    ahora = time.time()
    if nombre == _ip_imp["nombre"] and ahora - _ip_imp["t"] < 60:
        return _ip_imp["ip"]
    ip = None
    if nombre:
        try:
            salida = subprocess.run(["lpstat", "-v", nombre],
                                    capture_output=True, text=True,
                                    timeout=4).stdout
            m = re.search(r"://([^/:\s]+)", salida)
            if m:
                ip = socket.gethostbyname(m.group(1))
        except Exception:
            ip = None
    _ip_imp.update(t=ahora, nombre=nombre, ip=ip)
    return ip


_ips_entraron = set()   # aparatos que ya abrieron la pagina del booth
_entro_en = {}          # ip -> ultima vez que abrio una pagina del booth
_ips_fijas = set()      # aparatos que pasaron el tope sin entrar nunca


def cuantos_atorados():
    """Telefonos que se conectaron al Wi-Fi y NUNCA abrieron el booth.

    Es el unico caso para el que existe el QR de ayuda: alguien escaneo
    el QR del Wi-Fi, quedo conectado, y el portal no se le abrio. No
    cuentan:
      - quien ya entro alguna vez a la pagina (aunque luego se guarde el
        telefono con la red conectada),
      - el aparato del operador que entro al admin,
      - la impresora elegida en el admin,
      - cualquier aparato que lleve conectado mas del tope sin entrar
        nunca: a esas alturas no es un invitado esperando, es algo fijo
        (una impresora sin configurar, un reloj, una tablet), y se le
        deja de contar aunque se desconecte y vuelva.

    El reloj cuenta desde que el aparato aparecio en la red.
    """
    ahora = time.time()
    pronto, tarde = VENTANA_ATORADO
    impresora = ip_impresora()
    if salud_estaciones["ok"]:
        # Metodo bueno: cuenta desde que empezo la conexion ACTUAL. Quien
        # entro, se guardo el telefono y sigue conectado no cuenta; quien
        # se desconecto y volvio sin que se le abriera la pagina, si.
        with candado_red:
            n = 0
            for ip, inicio in _conectado_desde.items():
                if ip == impresora or ip in _ips_admin:
                    continue
                if _entro_en.get(ip, 0) >= inicio - 2:
                    continue            # ya abrio la pagina en esta conexion
                if pronto <= ahora - inicio <= tarde:
                    n += 1
            return n
    # Respaldo si no se puede leer la antena: el metodo de booth15/16
    with candado_red:
        n = 0
        for ip, desde in _dhcp_desde.items():
            if (ip == impresora or ip in _ips_admin or ip in _ips_entraron
                    or ip in _ips_fijas):
                continue
            conectado = ahora - desde
            if conectado > tarde:
                _ips_fijas.add(ip)
            elif conectado >= pronto:
                n += 1
        return n


@app.before_request
def apuntar_visitante():
    """Cualquier peticion prueba que ese telefono si abrio la pagina.

    Con esto, quien ya se tomo su foto y cerro el navegador no vuelve a
    contar como atorado aunque siga conectado a la red.
    """
    ip = request.remote_addr
    # Solo cuentan como "entro" las paginas del booth pedidas a la
    # direccion del espejo. Con el DNS secuestrado, cualquier app del
    # telefono que pida algo por HTTP a otro dominio tambien llega aqui,
    # y eso no quiere decir que la persona haya visto la pagina. Las
    # sondas del portal cautivo tampoco cuentan: las manda el sistema
    # solo, sin que nadie abra nada.
    a_la_pi = request.host.split(":")[0].startswith(PREFIJO_AP)
    entro = a_la_pi and request.path.startswith(PREFIJOS_ENTRADA)
    if ip:
        # El aparato del operador (con la cookie del admin) no es un
        # invitado: aunque se quede callado con la pagina cerrada, nunca
        # debe encender el QR de ayuda.
        es_admin = (cookie_admin_valida()
                    or (request.path == "/admin"
                        and request.method == "POST"
                        and request.form.get("pin") == pin_admin))
        with candado_red:
            _http_vistas[ip] = time.time()
            if es_admin:
                _ips_admin.add(ip)
            if entro:
                _ips_entraron.add(ip)
                _entro_en[ip] = time.time()


def capturar_ahora(dueno):
    """Dispara y le entrega la foto a quien la pidio.

    El token llega por argumento y no se lee del estado a proposito:
    entre el disparo y el obturador pasan tres segundos, y en ese rato
    el espejo pudo cambiar de manos. La foto es de quien pico el boton.
    """
    nombre = datetime.now().strftime("%Y%m%d-%H%M%S-%f")[:-3] + ".jpg"
    ruta = FOTOS_DIR / nombre
    mi_id = secrets.token_hex(4)

    with candado:
        # Si el seguro ya solto el espejo mientras se esperaba la cuenta,
        # esta captura ya no le toca a nadie.
        if estado["dueno"] != dueno or estado["fase"] != "cuenta":
            return
        estado["fase"] = "capturando"
        estado["captura_id"] = mi_id
        estado["captura_ini"] = time.time()

    try:
        tomar_foto(ruta)
    except Exception as e:
        print(f"Error al capturar: {e}")
        with candado:
            # La camara fallo, pero el dueno sigue siendo el dueno: se
            # le devuelve la ventana para que vuelva a intentar.
            if estado.get("captura_id") == mi_id:
                estado["fase"] = "espera"
                estado["accion"] = time.time()
                estado["captura_id"] = None
        return

    # El orden importa: primero la original tal como salio del sensor,
    # luego el volteo, y el texto al final para que se lea del derecho.
    try:
        if evento.get("marco_activo"):
            shutil.copy2(ruta, ORIGINALES_DIR / nombre)
        if ESPEJAR_RESULTADO:
            espejar_foto(ruta)
        if evento.get("marco_activo"):
            aplicar_marco(ruta)
    except Exception as e:
        # Que falle esto no puede costar la foto
        print(f"No se pudo preparar la foto: {e}")

    with candado:
        v = visitas.get(dueno)
        if v is not None:
            v["fotos"].append(nombre)
            v["visto"] = time.time()
        if estado.get("captura_id") != mi_id:
            # Tardo tanto que el seguro ya le dio el espejo a otro. La foto
            # es de su dueno igual, pero no se le quita el turno a nadie.
            return
        estado["captura_id"] = None
        estado["foto"] = nombre
        estado["fase"] = "resultado"
        estado["resultado_fin"] = time.time() + MOSTRAR_RESULTADO
        # La foto recien tomada ES una accion: el reloj de los quince
        # segundos empieza a contar desde aqui, no desde el disparo.
        estado["accion"] = time.time()


atorones = {"n": 0, "ultimo": ""}


def reiniciar_camara():
    """Intenta revivir la camara despues de un cuelgue, sin tumbar el booth."""
    if not candado_camara.acquire(timeout=ESPERA_CAMARA):
        print("ATORADO: la camara sigue ocupada; reinicia el booth si no se "
              "recupera (sudo systemctl restart photobooth)")
        marcar_camara(False, "colgada: reinicia el booth")
        return
    try:
        try:
            camara.stop()
        except Exception:
            pass
        camara.configure(CONFIG_VIDEO)
        camara.start()
        aplicar_calibracion(bloqueada=True)
        marcar_camara(True)
        print("ATORADO: camara reiniciada")
    except Exception as e:
        marcar_camara(False, e)
        print(f"ATORADO: no se pudo reiniciar la camara: {e}")
    finally:
        candado_camara.release()


def vigilante():
    ultima_limpieza = 0.0
    ultimo_dhcp = 0.0

    while True:
        time.sleep(0.5)
        ahora = time.time()

        with candado:
            fase = estado["fase"]

            # Una pieza con tope se quita sola. Sin tope se queda: el
            # ritmo de una broma lo pone quien la cuenta.
            show = estado["show"]
            if show and show["fin"] and ahora > show["fin"]:
                estado["show"] = None

            if fase == "resultado" and ahora > estado["resultado_fin"]:
                # Acabo de ensenar la foto en el espejo. El dueno sigue
                # siendo el dueno mientras haga algo.
                estado["fase"] = "espera"
                # Los quince segundos empiezan AQUI, no cuando se tomo
                # la foto: los ocho que el espejo estuvo ensenandola la
                # persona los paso mirando al frente, no su telefono.
                # Contarlos le dejaria la mitad del tiempo para decidir
                # si imprime.
                estado["accion"] = ahora
                fase = "espera"

            # Seguro anti-bloqueo: nada se queda en cuenta regresiva o
            # capturando mas de LIMITE_ATORADO segundos.
            atorado = None
            if fase == "cuenta" and ahora > estado["cuenta_fin"] + LIMITE_ATORADO:
                atorado = "la cuenta regresiva no termino"
            elif (fase == "capturando" and ahora - estado.get("captura_ini", ahora)
                    > LIMITE_ATORADO):
                atorado = "la camara no respondio"
            if atorado:
                print(f"ATORADO: {atorado}; se libera el espejo")
                atorones["n"] += 1
                atorones["ultimo"] = (datetime.now().strftime("%H:%M")
                                      + " · " + atorado)
                estado["captura_id"] = None
                soltar_espejo()
                fase = "libre"
                if atorado == "la camara no respondio":
                    marcar_camara(False, "no respondio; reiniciando")
                    threading.Thread(target=reiniciar_camara,
                                     daemon=True).start()

            if fase == "espera":
                v = visitas.get(estado["dueno"])
                callado = v is None or (ahora - v["visto"]) > GRACIA_LATIDO
                quieto = (ahora - estado["accion"]) > INACTIVIDAD_ESPEJO
                # Dos motivos para soltarlo: llevan quince segundos sin
                # hacer nada, o el telefono dejo de dar senales de vida
                # (cerro la pestana, bloqueo la pantalla, se fue). Lo
                # segundo pasa casi siempre y es lo que hace que el
                # espejo este libre de verdad en una fiesta.
                if quieto or callado:
                    soltar_espejo()

            if ahora - ultima_limpieza > 60:
                ultima_limpieza = ahora
                olvidar_visitas()

        # Fuera del candado: leer archivos no debe trabar el estado.
        if ahora - ultimo_dhcp > 3:
            ultimo_dhcp = ahora
            revisar_dhcp()
            revisar_estaciones()


threading.Thread(target=vigilante, daemon=True).start()


# ---------------------------------------------------------------
# Pantalla del espejo
# ---------------------------------------------------------------

ESPEJO = """
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ ev.nombre }}</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    /* La familia de los textos grandes la elige el operador; la de los
       textos chicos se queda neutra para que siempre se lean. */
    --titulo: {{ tipo.css|safe }};
    --peso: {{ tipo.peso }};
    --tracking: {{ tipo.espaciado }};
    --sans: "Noto Sans", "DejaVu Sans", system-ui, sans-serif;
    --acento: {{ ev.acento }};
    --c-etiqueta:  {{ col.color_etiqueta }};
    --c-nombre:    {{ col.color_nombre }};
    --c-subtitulo: {{ col.color_subtitulo }};
    --c-fecha:     {{ col.color_fecha }};
    --c-lineas:    {{ col.color_lineas }};
    --c-centro:    {{ col.color_centro }};
    --c-pie:       {{ col.color_pie }};
  }
  html, body { height: 100%; background: #000; color: #fff;
               font-family: var(--sans); overflow: hidden; cursor: none; }
  #marco { position: fixed; inset: 1.4vh; border: 1px solid var(--c-lineas);
           border-radius: 3px; pointer-events: none; }
  #pantalla { height: 100%; display: flex; flex-direction: column;
              justify-content: space-between; align-items: center;
              padding: 6vh 5vw; }

  #cabecera { text-align: center; }
  #etiqueta { font-size: 1.3vh; letter-spacing: 0.26em; text-transform: uppercase;
              color: var(--c-etiqueta); margin-bottom: 1.6vh; min-height: 1.6vh; }
  #evento, #subtitulo { font-family: var(--titulo); font-weight: var(--peso);
                        letter-spacing: var(--tracking);
                        font-size: 4.6vh; line-height: 1.12; }
  #evento { color: var(--c-nombre); }
  #subtitulo { color: var(--c-subtitulo); }
  .linea { width: 3.4vh; height: 1px; background: var(--c-lineas);
           margin: 2.2vh auto; }
  #fecha { font-size: 1.3vh; letter-spacing: 0.22em; color: var(--c-fecha); }

  #centro { flex: 1; width: 100%; display: flex; align-items: center;
            justify-content: center; }
  #cuenta { font-size: 26vh; font-weight: 300; line-height: 1;
            font-variant-numeric: tabular-nums; }
  #listo { position: relative; height: 4vh; width: 100%; }
  #listo .f { position: absolute; inset: 0; font-family: var(--titulo);
              font-size: 2.6vh; color: var(--c-centro); text-align: center;
              opacity: 0; transition: opacity 0.9s ease-in-out; }
  #listo .f.on { opacity: 1; }
  #foto { max-width: 100%; max-height: 46vh; border-radius: 4px; }

  /* Aviso para quien se conecto a la red y no abrio nada. Vive en el
     centro, que el resto del tiempo esta vacio a proposito, y sale
     solo cuando el espejo detecta a alguien atorado. */
  #ayuda { text-align: center; }
  #ayuda .qr { background: #fff; padding: 1.2vh; border-radius: 3px;
               line-height: 0; display: inline-block; }
  #ayuda .qr img { width: 22vh; height: 22vh; display: block; }
  #ayudatxt { position: relative; height: 8vh; margin-top: 2.6vh; }
  #ayudatxt .a { position: absolute; inset: 0; opacity: 0;
                 transition: opacity 0.9s ease-in-out; }
  #ayudatxt .a.on { opacity: 1; }
  #ayudatxt .t { font-family: var(--titulo); font-size: 2.6vh; color: #e8e8e8; }
  #ayudatxt .s { font-size: 1.6vh; color: #8a8a8a; margin-top: 0.9vh;
                 letter-spacing: 0.04em; }

  #pie { display: flex; align-items: center; gap: 2.4vh; width: 100%; }
  #qr { background: #fff; padding: 1vh; border-radius: 3px;
        line-height: 0; flex-shrink: 0; }
  #qr img { width: 12vh; height: 12vh; display: block; }

  /* Las dos frases se apilan y se cruzan con un fundido suave */
  #frases { position: relative; height: 5.6vh; flex: 1; }
  .frase { position: absolute; inset: 0; text-align: left;
           opacity: 0; transition: opacity 0.9s ease-in-out; }
  .frase.on { opacity: 1; }
  .frase .t { font-size: 2vh; margin-bottom: 0.7vh; color: var(--c-nombre); }
  .frase .s { font-size: 1.45vh; color: var(--c-pie); line-height: 1.5; }

  /* Mientras alguien usa el espejo los codigos se ocultan: es la senal
     mas clara de "no escanees todavia". El texto queda a la vista. */
  #pie.en_uso #qr, #pie.en_uso #qr2 { visibility: hidden; }
  #pie.en_uso .frase .t { color: {{ ev.acento }}; font-weight: 600; }
  #frases { height: 11.5vh; }
  .frase .t { font-size: 2.2vh; line-height: 1.3; }
  .frase .s { font-size: 1.6vh; }
  #qr2 { flex: none; width: 10vh; text-align: center; }
  #qr2 .cq { background: #fff; padding: 0.6vh; border-radius: 3px;
             display: inline-block; }
  #qr2 img { width: 8vh; height: 8vh; display: block; }
  #qr2 .l { position: relative; height: 3.6vh; margin-top: 0.6vh; }
  #qr2 .q2 { position: absolute; inset: 0; font-size: 1.1vh; line-height: 1.25;
             color: var(--c-pie); opacity: 0; transition: opacity .6s; }
  #qr2 .q2.on { opacity: 1; }

  #flash { position: fixed; inset: 0; background: #fff; opacity: 0;
           pointer-events: none; transition: opacity 0.18s ease-out; }
  #flash.on { opacity: 1; transition: none; }

  /* La pieza de la broma tapa todo lo demas mientras dura.

     Entra y sale con un fundido, y entre una pieza y otra pasa por
     negro: un corte seco entre el espejito y la cara mata el efecto,
     y el negro es ademas lo que el panel hace mejor -- por un instante
     vuelve a ser un espejo de verdad antes de revelar.

     Se oculta con opacity y visibility en vez de display para que la
     transicion exista; display no se puede animar. */
  #show { position: fixed; inset: 0; background: #000; z-index: 40;
          display: flex; align-items: center; justify-content: center;
          opacity: 0; visibility: hidden;
          transition: opacity .45s ease, visibility 0s linear .45s; }
  #show.on { opacity: 1; visibility: visible;
             transition: opacity .45s ease, visibility 0s; }
  #show.tapado img, #show.tapado video { opacity: 0; }
  /* width/height al 100% con object-fit y no max-*: con max-* una
     imagen mas chica que el panel se queda de su tamano, y en un
     panel de 1080x1920 un GIF de 600 px seria una estampilla en medio
     de un mar negro. Asi siempre llena lo que puede sin deformarse ni
     recortarse. */
  #show img, #show video { width: 100%; height: 100%;
                           object-fit: contain; display: block;
                           transition: opacity .45s ease; }

  .oculto { display: none !important; }
</style>
</head>
<body>
  <div id="marco"></div>
  <div id="flash"></div>
  <div id="show">
    <img id="showimg" class="oculto" alt="">
    <!-- muted y loop no son adorno: un video sin sonido arranca solo
         en cualquier navegador, sin tener que darle permiso de
         reproduccion automatica a Chromium -->
    <video id="showvid" class="oculto" loop muted playsinline></video>
  </div>

  <div id="pantalla">
    <div id="cabecera">
      {% if ev.lineas in ('arriba', 'ambas') %}<div class="linea"></div>{% endif %}
      {% if etiqueta %}<div id="etiqueta">{{ etiqueta }}</div>{% endif %}
      <div id="evento">{{ ev.nombre }}</div>
      {% if ev.subtitulo %}<div id="subtitulo">{{ ev.subtitulo }}</div>{% endif %}
      {% if ev.lineas in ('abajo', 'ambas') %}<div class="linea"></div>{% endif %}
      {% if ev.fecha %}<div id="fecha">{{ ev.fecha }}</div>{% endif %}
    </div>

    <div id="centro">
      <div id="cuenta" class="oculto"></div>

      {% if ev.centro_visible %}
      <div id="listo" class="oculto">
        {% if ev.centro_texto %}
        {# Texto puesto a mano por el operador: uno solo, sin alternar #}
        <div class="f on">{{ ev.centro_texto }}</div>
        {% else %}
        {% for L in idiomas %}
        <div class="f" data-i="{{ loop.index0 }}">{{ T[L].esp_listo }}</div>
        {% endfor %}
        {% endif %}
      </div>
      {% endif %}

      <div id="ayuda" class="oculto">
        <div class="qr"><img id="ayudaimg" alt=""></div>
        <div id="ayudatxt">
          {% for L in idiomas %}
          <div class="a" data-i="{{ loop.index0 }}">
            <div class="t">{{ T[L].atorado_t }}</div>
            <div class="s">{{ T[L].atorado_s }}</div>
          </div>
          {% endfor %}
        </div>
      </div>

      <img id="foto" class="oculto">
    </div>

    <div id="pie">
      <div id="qr"><img id="qrimg" alt=""></div>
      <div id="frases">
        {% for L in idiomas %}
        <div class="frase" data-i="{{ loop.index0 }}">
          <div class="t" data-libre="{{ T[L].esp_p1 }}"
               data-p1="{{ T[L].esp_p1 }}" data-p2="{{ T[L].esp_p2 }}"
               data-p3="{{ T[L].esp_p3 }}"
               data-uso="{{ T[L].esp_uso_t }}"
               data-hecho="{{ T[L].esp_hecho_t }}">{{ T[L].esp_p1 }}</div>
          <div class="s" data-libre="{{ T[L].esp_uno }}"
               data-paso="{{ T[L].esp_paso }}"
               data-uso="{{ T[L].esp_uso_s }}"
               data-usoseg="{{ T[L].esp_uso_seg }}"
               data-hecho="{{ T[L].esp_hecho_s }}">{{ T[L].esp_uno }}</div>
        </div>
        {% endfor %}
      </div>
      {% if qr_wifi %}
      <div id="qr2">
        <div class="cq"><img id="qr2img" alt=""></div>
        <div class="l">
          {% for L in idiomas %}
          <div class="q2" data-i="{{ loop.index0 }}">{{ T[L].esp_conectado }}</div>
          {% endfor %}
        </div>
      </div>
      {% endif %}
    </div>
  </div>

<script>
const cuenta = document.getElementById('cuenta');
const listo  = document.getElementById('listo');     // null si esta apagado
const ayuda  = document.getElementById('ayuda');
const foto   = document.getElementById('foto');
const qrimg  = document.getElementById('qrimg');
const ayudaimg = document.getElementById('ayudaimg');
const pie    = document.getElementById('pie');
const flash  = document.getElementById('flash');
const show   = document.getElementById('show');
const showimg = document.getElementById('showimg');
const showvid = document.getElementById('showvid');

const N_IDIOMAS = {{ idiomas|length }};
const VERSION   = {{ version }};

let qrActual = null, qrAyudaActual = null, showActual = null;

/* Cuanto dura el fundido. Tiene que coincidir con el CSS de arriba. */
const FUNDIDO = 450;
let cambiandoShow = false;

function dormir(ms) {
  return new Promise(function (r) { setTimeout(r, ms); });
}

function ponerPieza(p) {
  if (p.tipo === 'video') {
    showimg.classList.add('oculto');
    showimg.removeAttribute('src');
    showvid.classList.remove('oculto');
    showvid.src = p.src;
    showvid.play().catch(function () {});
  } else {
    /* Al quitar el video se pausa: en bucle seguiria decodificando
       cuadros detras de la pantalla y la Pi los necesita para la
       camara. */
    showvid.pause();
    showvid.classList.add('oculto');
    showvid.removeAttribute('src');
    showimg.classList.remove('oculto');
    showimg.src = p.src;
  }
}

async function pintarShow(s) {
  /* La pantalla pregunta tres veces por segundo y el fundido dura casi
     uno: sin este cerrojo, dos cambios se pisarian a media transicion. */
  if (cambiandoShow) return;

  if (s.show) {
    if (showActual === s.show.src) { show.classList.add('on'); return; }
    cambiandoShow = true;
    if (showActual !== null) {
      // Ya habia una pieza: se va a negro antes de traer la siguiente
      show.classList.add('tapado');
      await dormir(FUNDIDO);
    } else {
      show.classList.add('tapado');
    }
    showActual = s.show.src;
    ponerPieza(s.show);
    show.classList.add('on');
    // Un respiro para que el navegador tenga el cuadro antes de revelarlo
    await dormir(80);
    show.classList.remove('tapado');
    cambiandoShow = false;
  } else if (showActual !== null) {
    cambiandoShow = true;
    showActual = null;
    show.classList.remove('on');
    await dormir(FUNDIDO);
    showvid.pause();
    showvid.removeAttribute('src');
    showimg.removeAttribute('src');
    cambiandoShow = false;
  }
}
let faseAnterior = null, iFrase = 0, faseActual = 'libre';

/* El texto del centro se puede apagar desde /admin, asi que `listo`
   puede no existir. Se filtran los nulos una vez y no hay que andar
   preguntando en cada giro. */
const capas = [cuenta, listo, ayuda, foto].filter(Boolean);

function mostrar(el) {
  capas.forEach(x => x.classList.add('oculto'));
  if (el) el.classList.remove('oculto');
}

function dispararFlash() {
  flash.classList.add('on');
  requestAnimationFrame(() => requestAnimationFrame(
    () => flash.classList.remove('on')));
}

// Alterna entre idiomas con fundido. Con un solo idioma, se queda fijo.
function pintarFrase() {
  document.querySelectorAll('.frase, #listo .f[data-i], #ayudatxt .a[data-i], #qr2 .q2')
    .forEach(el => el.classList.toggle('on', +el.dataset.i === iFrase));
}

let quedaEspejo = null;
/* Los pasos salen uno por uno: cada paso se dice en todos los idiomas y
   luego pasa al siguiente. Con un solo idioma, cambia en cada vuelta. */
let iPaso = 1;
function pintarEstado() {
  const vista = faseActual === 'libre' ? 'libre'
              : faseActual === 'resultado' ? 'hecho' : 'uso';
  document.querySelectorAll('.frase .t, .frase .s').forEach(el => {
    let txt = el.dataset[vista];
    if (vista === 'libre') {
      if (el.dataset.p1) txt = el.dataset['p' + iPaso];
      else if (el.dataset.paso) txt = el.dataset.paso.replace('{k}', iPaso);
    }
    if (vista === 'uso' && el.dataset.usoseg && quedaEspejo !== null) {
      txt = el.dataset.usoseg.replace('{s}', quedaEspejo);
    }
    if (el.textContent !== txt) el.textContent = txt;
  });
}

setInterval(() => {
  iFrase = (iFrase + 1) % N_IDIOMAS;
  if (iFrase === 0) iPaso = iPaso % 3 + 1;
  pintarEstado();
  pintarFrase();
}, {{ alterna }});
pintarFrase();
pintarEstado();

async function tick() {
  let s;
  try {
    s = await (await fetch('/api/estado')).json();
  } catch (e) { return; }

  // La configuracion cambio desde /admin: recarga para aplicarla
  if (s.version_evento !== VERSION) { location.reload(); return; }

  /* La pieza de la broma manda sobre todo lo demas: el operador la
     dispara en un momento concreto. El fundido lo lleva pintarShow. */
  pintarShow(s);

  if (s.qr && s.qr !== qrActual) {
    qrimg.src = 'data:image/png;base64,' + s.qr;
    qrActual = s.qr;
  }
  const qr2img = document.getElementById('qr2img');
  if (qr2img && s.qr_enlace && qr2img.dataset.v !== s.qr_enlace.slice(-24)) {
    qr2img.src = 'data:image/png;base64,' + s.qr_enlace;
    qr2img.dataset.v = s.qr_enlace.slice(-24);
  }
  if (s.qr_ayuda && s.qr_ayuda !== qrAyudaActual) {
    ayudaimg.src = 'data:image/png;base64,' + s.qr_ayuda;
    qrAyudaActual = s.qr_ayuda;
  }

  if (s.fase === 'capturando' && faseAnterior !== 'capturando') dispararFlash();
  faseAnterior = s.fase;

  pie.classList.toggle('en_uso', s.fase !== 'libre');
  faseActual = s.fase;
  quedaEspejo = (s.queda_espejo === undefined) ? null : s.queda_espejo;
  pintarEstado();

  switch (s.fase) {
    case 'libre':
      /* Si hay alguien conectado que no ha abierto nada, el centro se
         usa para ayudarlo. Si no, queda como estaba: en negro, que es
         cuando el panel de verdad funciona como espejo. */
      mostrar(s.atorados > 0 && qrAyudaActual ? ayuda : listo);
      break;
    case 'espera':     mostrar(listo); break;
    case 'cuenta':
      mostrar(cuenta);
      cuenta.textContent = s.restante > 0 ? s.restante : '';
      break;
    case 'capturando': mostrar(null); break;
    case 'resultado':
      /* La foto ya viene volteada del servidor: voltearla aqui tambien
         pondria el nombre del evento al reves. */
      mostrar(foto);
      if (!foto.src.endsWith(s.foto)) foto.src = '/fotos/' + s.foto;
      break;
  }
}

setInterval(tick, 350);
tick();
</script>
</body>
</html>
"""


# ---------------------------------------------------------------
# Control en el movil
# ---------------------------------------------------------------

MOVIL = """
<!doctype html>
<html lang="{{ lang }}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ ev.nombre }}</title>
<style>
  * { box-sizing: border-box; }
  body { font-family: system-ui, sans-serif; margin: 0; padding: 20px;
         background: #111; color: #eee; }
  header { display: flex; justify-content: space-between;
           align-items: flex-start; margin-bottom: 18px; }
  h1 { font-size: 17px; font-weight: 500; margin: 0; }
  #idioma { font-size: 13px; color: {{ ev.acento }}; text-decoration: none;
            border: 1px solid #333; border-radius: 6px; padding: 5px 10px;
            white-space: nowrap; }

  button { width: 100%; padding: 18px; font-size: 17px; border: none;
           border-radius: 10px; font-weight: 600; margin-bottom: 10px; }
  #btn { background: {{ ev.acento }}; color: #111; }
  #btn:disabled { background: #333; color: #777; }
  #fin { background: transparent; color: #888; border: 1px solid #333;
         font-size: 15px; font-weight: 400; padding: 13px; }

  /* El aviso de que el espejo va a pasar al siguiente. Lleva su propio
     boton porque, sin el, la unica forma de no perder el turno seria
     disparar, y la gente acabaria tomando fotos que no quiere. */
  #aviso { display: none; background: #3a2a00; color: #fc3; padding: 16px;
           border-radius: 10px; font-size: 17px; font-weight: 600;
           margin-bottom: 14px;
           align-items: center; gap: 10px; }
  #aviso.on { display: flex; }
  #aviso span { flex: 1; line-height: 1.4; }
  #aviso button { width: auto; margin: 0; padding: 9px 14px; font-size: 14px;
                  background: #fc3; color: #241a00; white-space: nowrap; }

  /* Visor para iPhone.

     Safari ignora el atributo download de los enlaces: en vez de
     guardar, navega a la imagen, y si desde ahi se usa el boton de
     compartir del navegador se manda la DIRECCION y no la foto --
     una direccion 10.42.x.x que solo existe dentro de la red del
     espejo y que nadie puede abrir despues. La API de compartir del
     navegador arreglaria esto, pero solo existe en HTTPS y el booth
     va en HTTP dentro de su propia red.

     Asi que la salida no es tecnica sino de interfaz: ensenar la foto
     grande y llevar al gesto que en iOS si funciona. */
  #visor { display: none; position: fixed; inset: 0; z-index: 60;
           background: #000; padding: 16px; overflow-y: auto; }
  #visor.on { display: block; }
  #visor img { width: 100%; border-radius: 8px; display: block;
               margin-bottom: 18px; }
  #visor .vt { font-size: 17px; font-weight: 600; text-align: center;
               margin-bottom: 4px; }
  #visor .vp { font-size: 15px; color: #aaa; text-align: center;
               margin-bottom: 18px; }
  #visor .safari { display: block; text-align: center; padding: 16px;
                   border-radius: 10px; margin-bottom: 8px; font-size: 17px;
                   font-weight: 600; text-decoration: none;
                   background: {{ ev.acento }}; color: #111; }
  #visor .vojo { background: #3a2a00; color: #fc3; padding: 12px;
                 border-radius: 8px; font-size: 13px; line-height: 1.5;
                 margin-bottom: 18px; }

  #cerrada { display: none; text-align: center; padding: 40px 10px; }
  #cerrada h2 { font-size: 19px; font-weight: 500; margin: 0 0 12px; }
  #cerrada p { color: #888; font-size: 15px; line-height: 1.6; margin: 0; }

  #estado { font-size: 13px; color: #888; min-height: 34px;
            margin-bottom: 14px; line-height: 1.45; }

  #galeria { margin-top: 20px; }
  #galeria img { width: 100%; border-radius: 8px; margin-bottom: 8px;
                 display: block; }
  .foto { margin-bottom: 20px; }
  .pista { font-size: 12px; color: #777; text-align: center; margin-bottom: 18px; }

  .acciones { display: flex; gap: 8px; }
  .acciones > * { flex: 1; margin: 0; display: block; text-align: center;
                  padding: 12px; border: 1px solid #333; border-radius: 8px;
                  color: {{ ev.acento }}; text-decoration: none;
                  font-size: 15px; font-weight: 400; background: transparent; }
  .acciones button:active { background: #1c1c1c; }

  .recogida { flex: 1; border: 1px solid {{ ev.acento }}; border-radius: 8px;
              padding: 12px; text-align: center; font-size: 15px;
              color: {{ ev.acento }}; }
  .recogida small { display: block; font-size: 11px; color: #777;
                    margin-top: 2px; }
  .nopapel { flex: 1; border: 1px solid #333; border-radius: 8px; padding: 12px;
             text-align: center; font-size: 14px; color: #666; }
  /* Descartar es destructivo y poco frecuente: no compite con los
     otros dos botones, pero esta a la mano.

     El width:auto no sobra: los botones del movil llevan width:100%
     general, y con flex-basis en auto ese 100% se vuelve su tamano
     base. Sin esto, Descartar se come tres cuartas partes de la fila. */
  .acciones .tirar { flex: 0 0 auto; width: auto; padding: 12px 15px;
                     color: #a77; border-color: #3a2a2a; font-size: 14px; }

  /* Hoja de la sesion: elegir fotos y mandarlas juntas */
  .acciones .elegida { background: {{ ev.acento }}; color: #111;
                       border-color: {{ ev.acento }}; font-weight: 600; }
  .foto.sel img { outline: 3px solid {{ ev.acento }}; outline-offset: -3px; }
  #barra { display: none; position: sticky; bottom: 0; z-index: 40;
           background: #111; padding: 12px 0 4px; border-top: 1px solid #222; }
  #barra.on { display: block; }
  #barra .cuenta { font-size: 13px; color: #aaa; text-align: center;
                   margin-bottom: 8px; }
  #barra button { background: {{ ev.acento }}; color: #111; margin: 0; }
  #barra button:disabled { background: #333; color: #777; }
  #hojainfo { display: none; border: 1px solid {{ ev.acento }};
              color: {{ ev.acento }}; border-radius: 10px; padding: 14px;
              font-size: 15px; line-height: 1.45; text-align: center;
              margin-bottom: 18px; }
  #hojainfo.on { display: block; }
  #hojainfo.mal { border-color: #a55; color: #e77; }

  /* La pregunta de si quiere imprimir */
  #pop, #dlg { display: none; position: fixed; inset: 0; z-index: 70;
         background: rgba(0,0,0,.78); padding: 20px;
         align-items: center; justify-content: center; }
  #pop.on, #dlg.on { display: flex; }
  #dlg { z-index: 80; }
  #pop .caja, #dlg .caja { background: #1a1a1a; border: 1px solid #333;
               border-radius: 14px; padding: 24px 20px 14px; width: 100%;
               max-width: 380px; text-align: center; }
  #pop h2 { font-size: 20px; font-weight: 600; margin: 0 0 10px;
            line-height: 1.3; }
  #pop .sub { font-size: 16px; color: {{ ev.acento }}; margin: 0 0 4px; }
  #pop .sub2 { font-size: 13px; color: #888; margin: 0 0 20px; }
  #dlg p { font-size: 16px; line-height: 1.45; margin: 0 0 20px;
           white-space: pre-line; }
  #dlg .si { background: {{ ev.acento }}; color: #111; }
  #dlg .no { background: transparent; color: #999; border: 1px solid #333;
             font-weight: 400; font-size: 15px; padding: 13px; }
  #pop .si { background: {{ ev.acento }}; color: #111; }
  #pop .no { background: transparent; color: #999; border: 1px solid #333;
             font-weight: 400; font-size: 15px; padding: 13px; }
</style>
</head>
<body>
  <header>
    <h1>{{ ev.nombre }}</h1>
    <a id="idioma" href="?lang={{ otro_lang }}">{{ t.otro_idioma }}</a>
  </header>

  <div id="aviso"><span></span><button onclick="seguir()">{{ t.sigo }}</button></div>
  <div id="estado"></div>

  <div id="vivo">
    <button id="btn" onclick="disparar()">{{ t.tomar }}</button>
    <button id="fin" onclick="terminar()">{{ t.terminar }}</button>
  </div>

  <div id="cerrada">
    <h2>{{ t.cerrada_t }}</h2>
    <p>{{ t.cerrada_p }}</p>
  </div>

  <div id="hojainfo"></div>
  <div id="galeria"></div>
  <div id="barra">
    <div class="cuenta"></div>
    <button id="btnhoja" onclick="imprimirHoja()">{{ t.imprimir_hoja }}</button>
  </div>

  <!-- Confirmaciones dentro de la pagina: la ventanita del portal de
       iPhone no muestra confirm() ni alert(), los cancela solos. -->
  <div id="dlg">
    <div class="caja">
      <p id="dlgtxt"></p>
      <button class="si" id="dlgsi"></button>
      <button class="no" id="dlgno"></button>
    </div>
  </div>

  <div id="pop">
    <div class="caja">
      <h2>{{ t.pop_t }}</h2>
      <p class="sub" id="popsub"></p>
      <p class="sub2">{{ t.pop_s2 }}</p>
      <button class="si" onclick="popSi()">{{ t.pop_si }}</button>
      <button class="no" id="popno" onclick="popNo()">{{ t.pop_no }}</button>
    </div>
  </div>

  <div id="visor">
    <img id="visorimg" alt="">
    <div class="vt">{{ t.ios_t }}</div>
    <div class="vp">{{ t.ios_p }}</div>
    <a class="safari" href="x-safari-{{ base }}/s/{{ token }}?lang={{ lang }}">{{ t.ios_safari }}</a>
    <div class="vp">{{ t.ios_safari_p }}</div>
    <div class="vojo">{{ t.ios_ojo }}</div>
    <button onclick="cerrarVisor()">{{ t.cerrar }}</button>
  </div>

<script>
const TOKEN = "{{ token }}";
const TXT = {{ t_json|safe }};
const btn = document.getElementById('btn');
const fin = document.getElementById('fin');
const aviso = document.getElementById('aviso');
const avisoTxt = aviso.querySelector('span');
const estado = document.getElementById('estado');
const galeria = document.getElementById('galeria');
const vivo = document.getElementById('vivo');
const cerrada = document.getElementById('cerrada');
const barra = document.getElementById('barra');
const btnhoja = document.getElementById('btnhoja');
const hojainfo = document.getElementById('hojainfo');
const pop = document.getElementById('pop');
const dlg = document.getElementById('dlg');

/* confirm() y alert() propios. La ventanita del portal cautivo de iOS
   no muestra los del navegador: confirm() devuelve false sin preguntar,
   asi que en iPhone ningun boton que pidiera confirmacion hacia nada. */
function preguntar(texto, siTxt) {
  return new Promise(function (listo) {
    document.getElementById('dlgtxt').textContent = texto;
    const si = document.getElementById('dlgsi');
    const no = document.getElementById('dlgno');
    si.textContent = siTxt;
    no.textContent = TXT.cancelar;
    no.style.display = '';
    si.onclick = function () { dlg.classList.remove('on'); listo(true); };
    no.onclick = function () { dlg.classList.remove('on'); listo(false); };
    dlg.classList.add('on');
  });
}
function avisarMovil(texto) {
  document.getElementById('dlgtxt').textContent = texto;
  const si = document.getElementById('dlgsi');
  si.textContent = TXT.entendido;
  document.getElementById('dlgno').style.display = 'none';
  si.onclick = function () { dlg.classList.remove('on'); };
  dlg.classList.add('on');
}
/* Bienvenida en tres pantallas, una idea por pantalla */
function bienvenida(k, n) {
  document.getElementById('dlgtxt').textContent =
    TXT['bien' + k].replace('{n}', n);
  const si = document.getElementById('dlgsi');
  si.textContent = k < 3 ? TXT.siguiente : TXT.entendido;
  document.getElementById('dlgno').style.display = 'none';
  si.onclick = function () {
    if (k < 3) bienvenida(k + 1, n);
    else dlg.classList.remove('on');
  };
  dlg.classList.add('on');
}
let ultimaLista = '', viva = true;

/* Hoja de la sesion. Las fotos elegidas viven solo en el telefono hasta
   que se pica Imprimir; el servidor vuelve a revisar todo. */
const elegidas = new Set();
let ultimoS = null;        // el ultimo estado, para repintar sin preguntar
let eraMio = false;        // para notar cuando el espejo pasa al siguiente
let popAlTerminar = false;

/* La pregunta sale una sola vez por sesion. Se recuerda en el telefono
   con try: en modo privado sessionStorage puede fallar, y entonces se
   recuerda solo mientras la pagina siga abierta. */
const CLAVE_POP = 'pop_' + TOKEN;
let popVisto = false;
let bienVista = false;
try { bienVista = sessionStorage.getItem('bien_' + TOKEN) === '1'; } catch (e) {}
try { popVisto = sessionStorage.getItem(CLAVE_POP) === '1'; } catch (e) {}
function marcarPopVisto() {
  popVisto = true;
  try { sessionStorage.setItem(CLAVE_POP, '1'); } catch (e) {}
}

/* Safari en iOS no descarga con el atributo download: navega a la
   imagen. Se detecta para ofrecer el camino que si funciona ahi. El
   segundo caso es el iPad reciente, que se hace pasar por Mac. */
const ES_IOS = /iPad|iPhone|iPod/.test(navigator.userAgent)
  || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);

const visor = document.getElementById('visor');
const visorimg = document.getElementById('visorimg');

function verFoto(f) {
  visorimg.src = '/fotos/' + f + '?d=1';
  visor.classList.add('on');
  window.scrollTo(0, 0);
}
function cerrarVisor() {
  visor.classList.remove('on');
  visorimg.removeAttribute('src');
}

async function descartar(f) {
  if (!(await preguntar(TXT.confirmar_descartar, TXT.descartar))) return;
  elegidas.delete(f);
  try {
    await fetch('/api/descartar/' + TOKEN, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ archivo: f })
    });
  } catch (e) {}
  ultimaLista = '';        // obliga a repintar la galeria
  programar(0);
}

async function disparar() {
  btn.disabled = true;           // que no se pique dos veces
  try {
    await fetch('/api/disparar/' + TOKEN, { method: 'POST' });
  } catch (e) {}
  programar(0);
}

/* "Sigo aqui": reinicia el reloj sin tomar otra foto. */
async function seguir() {
  aviso.classList.remove('on');
  try {
    await fetch('/api/seguir/' + TOKEN, { method: 'POST' });
  } catch (e) {}
  programar(0);
}

function puedeImprimir(s) {
  return !!(s && s.imprimir_activo && s.hay_papel && !s.hoja
            && s.fotos && s.fotos.length);
}

function abrirPop(alTerminar) {
  popAlTerminar = alTerminar;
  document.getElementById('popsub').textContent =
    TXT.pop_s.replace('{n}', ultimoS ? ultimoS.max_hoja : 4);
  document.getElementById('popno').textContent =
    alTerminar ? TXT.pop_fin : TXT.pop_no;
  pop.classList.add('on');
  marcarPopVisto();
}

function popSi() {
  pop.classList.remove('on');
  /* Si caben todas, se dejan elegidas de una vez: lo comun es querer
     todas, y quitar una cuesta menos que poner cinco. */
  if (ultimoS && elegidas.size === 0
      && ultimoS.fotos.length <= ultimoS.max_hoja) {
    ultimoS.fotos.forEach(f => elegidas.add(f));
  }
  pintar(ultimoS, true);
  galeria.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function popNo() {
  pop.classList.remove('on');
  if (popAlTerminar) cerrarSesion();
}

async function terminar() {
  if (puedeImprimir(ultimoS)) { abrirPop(true); return; }
  cerrarSesion();
}

async function cerrarSesion() {
  if (!(await preguntar(TXT.confirmar_fin, TXT.terminar))) return;
  try {
    const d = await (await fetch('/api/terminar/' + TOKEN,
                                 { method: 'POST' })).json();
    if (!d.ok) return;           // va una foto en camino: no se cierra
  } catch (e) { return; }
  viva = false;
  vivo.style.display = 'none';
  aviso.classList.remove('on');
  estado.textContent = '';
  galeria.innerHTML = '';
  cerrada.style.display = 'block';
}

/* Al cerrar la pestana o bloquear el telefono, soltar el espejo. Va a
   /api/suelto y NO a /api/terminar a proposito: este aviso llega
   tambien cuando la pantalla se apaga, y la gente se guarda el
   telefono, platica, y lo saca de nuevo para pedir su impresion.
   Cerrarle la sesion aqui seria quitarle sus fotos por bloquear el
   telefono. Se usa sendBeacon porque un fetch se cancela cuando la
   pagina ya se esta muriendo. */
window.addEventListener('pagehide', function () {
  if (!viva) return;
  try { navigator.sendBeacon('/api/suelto/' + TOKEN); } catch (e) {}
});

async function imprimirHoja() {
  const fotos = (ultimoS ? ultimoS.fotos : []).filter(f => elegidas.has(f));
  if (!fotos.length) return;
  if (!(await preguntar(TXT.confirmar_hoja.replace('{k}', fotos.length),
                        TXT.imprimir_hoja))) return;
  btnhoja.disabled = true;
  try {
    const r = await fetch('/api/imprimir_hoja/' + TOKEN, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ fotos: fotos })
    });
    const d = await r.json();
    if (!d.ok) {
      if (d.error === 'papel') avisarMovil(TXT.sin_papel);
      else if (d.error === 'tope')
        avisarMovil(TXT.max_fotos.replace('{n}', ultimoS.max_hoja));
      else if (d.error !== 'armando') avisarMovil(TXT.hoja_falla);
      btnhoja.disabled = false;
      return;
    }
  } catch (e) {
    btnhoja.disabled = false;
    return;
  }
  elegidas.clear();
  programar(0);   // que el aviso de la hoja salga ya
}

function alternar(f) {
  if (elegidas.has(f)) {
    elegidas.delete(f);
  } else if (ultimoS && elegidas.size >= ultimoS.max_hoja) {
    avisarMovil(TXT.max_fotos.replace('{n}', ultimoS.max_hoja));
    return;
  } else {
    elegidas.add(f);
  }
  pintar(ultimoS, true);
}

function dosDigitos(n) { return n < 10 ? '0' + n : '' + n; }

function avisoHoja(s) {
  const h = s.hoja;
  if (!h || !s.imprimir_activo) return ['', false];
  const n = dosDigitos(h.recogida);
  if (h.estado === 'error') return [TXT.hoja_error.replace('{n}', n), true];
  if (s.auto) {
    return [h.estado === 'lista' ? TXT.hoja_lista_auto : TXT.hoja_auto, false];
  }
  return [TXT.hoja_operador.replace('{n}', n), false];
}

/* Se redibuja solo cuando cambia algo que se ve: las fotos, lo elegido,
   la hoja, o si la impresion sigue disponible. */
function pintar(s, forzar) {
  if (!s) return;
  const mias = s.fotos.length;
  const lista = s.fotos.join(',') + '|' + Array.from(elegidas).join(',')
              + '|' + JSON.stringify(s.hoja) + '|' + s.imprimir_activo
              + '|' + s.hay_papel + '|' + s.mio + '|' + s.max_hoja;
  if (!forzar && lista === ultimaLista) return;
  ultimaLista = lista;

  galeria.innerHTML = mias
    ? (ES_IOS ? '' : '<div class="pista">' + TXT.guardar_pista + '</div>')
      + s.fotos.slice().reverse().map(f => tarjeta(f, s)).join('')
      + (s.mio ? '' : '<div class="pista">' + TXT.sigue_tuyo + '</div>')
    : '';

  const [txt, mal] = avisoHoja(s);
  hojainfo.textContent = txt;
  hojainfo.classList.toggle('on', !!txt);
  hojainfo.classList.toggle('mal', mal);

  const puede = puedeImprimir(s);
  barra.classList.toggle('on', puede);
  if (puede) {
    barra.querySelector('.cuenta').textContent = TXT.barra_cuenta
      .replace('{k}', elegidas.size).replace('{n}', s.max_hoja);
    btnhoja.disabled = elegidas.size === 0;
  }
}

function tarjeta(f, s) {
  /* El ?d=1 es lo que distingue descargar de mirar: solo el enlace de
     descarga lo lleva, asi que las miniaturas no reinician el reloj. */
  let acciones = ES_IOS
    ? '<button data-act="guardar" data-f="' + f + '">' + TXT.guardar
      + '</button>'
    : '<a href="/fotos/' + f + '?d=1" download>' + TXT.descargar + '</a>';

  if (puedeImprimir(s)) {
    const sel = elegidas.has(f);
    acciones += '<button data-act="elegir" data-f="' + f + '"'
              + (sel ? ' class="elegida"' : '') + '>'
              + (sel ? TXT.elegida : TXT.elegir) + '</button>';
  }

  acciones += '<button class="tirar" data-act="descartar" data-f="' + f
            + '">' + TXT.descartar + '</button>';

  return '<div class="foto' + (elegidas.has(f) ? ' sel' : '')
       + '"><img src="/fotos/' + f + '">'
       + '<div class="acciones">' + acciones + '</div></div>';
}

/* Un solo escuchador para toda la galeria. Meter el nombre del archivo
   dentro de un onclick obliga a escapar comillas en tres niveles --el
   archivo de Python, la plantilla y el JavaScript-- y eso ya costo un
   bug en este proyecto. Con data- no hay nada que escapar. */
galeria.addEventListener('click', function (e) {
  const b = e.target.closest('button[data-act]');
  if (!b) return;
  const f = b.dataset.f;
  if (b.dataset.act === 'elegir') alternar(f);
  else if (b.dataset.act === 'guardar') verFoto(f);
  else if (b.dataset.act === 'descartar') descartar(f);
});

async function tick() {
  if (!viva) return null;
  let s;
  try {
    s = await (await fetch('/api/estado?token=' + TOKEN)).json();
  } catch (e) { return null; }

  const mias = s.fotos.length;
  btn.textContent = mias ? TXT.otra : TXT.tomar;

  /* El aviso sale solo en los ultimos segundos y solo al dueno. */
  if (s.mio && s.queda !== null && s.queda <= {{ aviso }}) {
    avisoTxt.textContent = TXT.aviso_espejo.replace('{s}', s.queda);
    aviso.classList.add('on');
  } else {
    aviso.classList.remove('on');
  }

  if (s.fase === 'cuenta') {
    estado.textContent = TXT.mira + ' ' + s.restante;
    btn.disabled = true;
  } else if (s.fase === 'capturando') {
    estado.textContent = TXT.capturando;
    btn.disabled = true;
  } else if (!s.puedo) {
    /* Alguien mas lo tiene. No es un error ni un rechazo: el boton se
       prende solo en cuanto el otro acaba, sin que nadie recargue. */
    estado.textContent = TXT.espera_otro;
    btn.disabled = true;
  } else {
    estado.textContent = mias ? mias + ' ' + TXT.fotos : TXT.listo;
    btn.disabled = false;
  }

  ultimoS = s;
  /* Bienvenida: una sola vez por sesion, antes de su primera foto */
  if (!bienVista && !mias && s.puedo) {
    bienVista = true;
    try { sessionStorage.setItem('bien_' + TOKEN, '1'); } catch (e) {}
    bienvenida(1, s.max_hoja || 4);
  }
  /* Lo elegido que ya no existe (descartada) se olvida */
  for (const f of Array.from(elegidas))
    if (!s.fotos.includes(f)) elegidas.delete(f);

  /* La pregunta sale cuando el espejo pasa al siguiente: es la senal de
     que ya acabo de tomarse fotos. */
  if (eraMio && !s.mio && !popVisto && puedeImprimir(s)) abrirPop(false);
  eraMio = !!s.mio;

  pintar(s, false);
  return s;
}

/* Cada cuanto volver a preguntar.

   Con cincuenta invitados, preguntar dos veces por segundo cada uno son
   cien peticiones por segundo contra la Pi, y la mayoria no sirven de
   nada: quien esta mirando su foto o esperando turno no necesita
   enterarse de nada en medio segundo. Solo la cuenta regresiva pide
   ritmo, y de esa hay una a la vez. */
function ritmo(s) {
  if (!s) return 2000;                      // sin respuesta: no insistir
  if (s.fase === 'cuenta') return 300;      // hay que ver el numero bajar
  if (s.fase === 'capturando') return 400;
  if (s.mio) return 900;                    // es suyo: puede cambiar pronto
  return 2000;                              // mirando, o esperando turno
}

let proximo = null;
function programar(ms) {
  clearTimeout(proximo);
  proximo = setTimeout(ciclo, ms);
}
async function ciclo() {
  programar(ritmo(await tick()));
}

/* Al volver a la pagina, preguntar de inmediato: puede haber pasado
   mucho con la pantalla apagada. */
document.addEventListener('visibilitychange', function () {
  if (document.visibilityState === 'visible' && viva) programar(0);
});

ciclo();
</script>
</body>
</html>
"""






# ---------------------------------------------------------------
# Administracion
# ---------------------------------------------------------------

LOGIN = """
<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Administracion</title></head>
<body style="font-family:system-ui;background:#111;color:#eee;
             padding:60px 28px;max-width:420px;margin:0 auto">
  <h2 style="font-weight:500;font-size:20px;margin:0 0 20px">Administracion</h2>
  {% if error %}
  <div style="background:#3a1010;color:#f88;padding:11px;border-radius:8px;
              font-size:14px;margin-bottom:16px">PIN incorrecto</div>
  {% endif %}
  <form method="post">
    <input name="pin" type="password" inputmode="numeric" placeholder="PIN"
           autofocus style="width:100%;padding:16px;font-size:18px;
           border:1px solid #333;border-radius:10px;background:#1a1a1a;
           color:#eee;margin-bottom:12px;text-align:center;letter-spacing:0.3em">
    <button style="width:100%;padding:16px;font-size:16px;border:none;
            border-radius:10px;background:{{ acento }};color:#111;
            font-weight:600">Entrar</button>
  </form>
</body></html>
"""


ADMIN = """
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Administracion</title>
<style>
  * { box-sizing: border-box; }
  body { font-family: system-ui, sans-serif; margin: 0 auto;
         padding: 16px 16px 80px; background: #111; color: #eee;
         max-width: 560px; }
  h2 { font-size: 19px; font-weight: 500; margin: 0 0 4px; }
  .sub { font-size: 13px; color: #888; margin-bottom: 18px; }
  h3 { font-size: 15px; font-weight: 600; margin: 26px 0 12px;
       padding-bottom: 6px; border-bottom: 1px solid #2a2a2a; }

  #previa { width: 100%; border-radius: 10px; background: #000; display: block;
            margin-bottom: 6px; aspect-ratio: 16/9; object-fit: cover; }
  .pie_previa { font-size: 12px; color: #666; text-align: center;
                margin-bottom: 18px; }

  .ajuste { margin-bottom: 20px; }
  .fila { display: flex; justify-content: space-between;
          align-items: baseline; margin-bottom: 6px; }
  label { font-size: 15px; }
  .valor { font-size: 13px; color: {{ acento }};
           font-variant-numeric: tabular-nums; }
  .ayuda { font-size: 12px; color: #777; margin-top: 5px; line-height: 1.45; }
  .extremos { display: flex; justify-content: space-between;
              font-size: 11px; color: #666; margin-top: -4px; }

  input[type=range] { width: 100%; accent-color: {{ acento }}; height: 28px; }
  input[type=range]:disabled { opacity: 0.3; }

  input[type=text], input[type=number], select {
                     width: 100%; padding: 12px; font-size: 15px;
                     border: 1px solid #333; border-radius: 9px;
                     background: #1a1a1a; color: #eee; }
  input[type=number] { max-width: 150px; }
  /* El desplegable nativo se pinta claro sobre el panel oscuro si no se
     le quita la apariencia del sistema; la flechita se dibuja a mano. */
  select { appearance: none; -webkit-appearance: none; padding-right: 36px;
           background-image: linear-gradient(45deg, transparent 50%, #999 50%),
                             linear-gradient(135deg, #999 50%, transparent 50%);
           background-position: calc(100% - 20px) 21px,
                                calc(100% - 15px) 21px;
           background-size: 5px 5px, 5px 5px; background-repeat: no-repeat; }
  select option { background: #1a1a1a; color: #eee; }
  input[type=color] { width: 54px; height: 40px; padding: 2px;
                      border: 1px solid #333; border-radius: 8px;
                      background: #1a1a1a; }
  .campo { margin-bottom: 14px; }
  .campo label { display: block; font-size: 13px; color: #aaa;
                 margin-bottom: 6px; }

  .opciones { display: flex; gap: 7px; }
  .opciones label { flex: 1; text-align: center; padding: 11px 6px;
                    border: 1px solid #333; border-radius: 9px;
                    font-size: 13px; color: #aaa; cursor: pointer; }
  .opciones input { display: none; }
  .opciones input:checked + span { color: {{ acento }}; font-weight: 600; }

  .check { display: flex; align-items: center; gap: 9px;
           font-size: 14px; color: #bbb; margin-bottom: 8px; }
  .check input { width: 18px; height: 18px; accent-color: {{ acento }}; }

  .botones { display: flex; gap: 8px; margin-top: 8px; flex-wrap: wrap; }
  button { flex: 1; min-width: 130px; padding: 13px; font-size: 14px;
           border: 1px solid #333; border-radius: 9px; background: #1c1c1c;
           color: #ddd; font-weight: 500; }
  button.principal { background: {{ acento }}; color: #111;
                     border-color: {{ acento }}; font-weight: 600; }
  button.peligro { color: #d88; }
  /* Descargar un archivo necesita un enlace de verdad, no un boton,
     asi que se le da el mismo aspecto. */
  a.bot_a { flex: 1; min-width: 130px; padding: 13px; font-size: 14px;
            border: 1px solid #333; border-radius: 9px; background: #1c1c1c;
            color: #ddd; font-weight: 500; text-align: center;
            text-decoration: none; }

  #aviso { position: fixed; left: 16px; right: 16px; bottom: 16px;
           background: #1e3a1e; color: #9e9; padding: 13px; border-radius: 9px;
           font-size: 14px; text-align: center; display: none;
           max-width: 528px; margin: 0 auto; }

  .nota { background: #1a1a1a; border-left: 2px solid {{ acento }};
          padding: 11px 13px; font-size: 13px; color: #aaa;
          line-height: 1.5; margin-bottom: 18px; }

  .cfila { display: flex; align-items: center; gap: 10px;
           padding: 7px 0; border-bottom: 1px solid #222; }
  .cfila label { flex: 1; font-size: 13px; color: #bbb; margin: 0; }
  .cfila input[type=checkbox] { width: 17px; height: 17px;
                                accent-color: {{ acento }}; flex-shrink: 0; }
  .cfila input[type=color] { width: 46px; height: 32px; flex-shrink: 0; }
  .cfila input[type=color]:disabled { opacity: 0.25; }

  /* La pantalla del espejo va en vertical: se mete en un iframe a
     tamano real y se encoge, asi lo que se ve es la pagina de verdad y
     no una imitacion que se desactualiza. */
  .marco_pantalla { width: 100%; aspect-ratio: 9 / 16; overflow: hidden;
                    border-radius: 6px; background: #000; margin-top: 12px; }
  .marco_pantalla iframe { width: 1080px; height: 1920px; border: 0;
                           transform-origin: top left; }

  #marco_previa { width: 100%; border-radius: 6px; display: block;
                  background: #1a1a1a; margin-bottom: 3px; }

  /* ---- Bromas ---- */
  .ranura { border: 1px solid #2a2a2a; border-radius: 10px; padding: 12px;
            margin-bottom: 12px; }
  .ranura.viva { border-color: {{ acento }}; }
  .rcab { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
  .rletra { font-size: 12px; letter-spacing: 0.18em; color: {{ acento }};
            border: 1px solid #333; border-radius: 5px; padding: 4px 8px; }
  .rnombre { flex: 1; min-width: 0; }
  .rpieza { border-top: 1px solid #222; padding-top: 9px; margin-top: 9px; }
  .rpieza.puesta { border-left: 2px solid {{ acento }}; padding-left: 9px; }
  .rfila { display: flex; align-items: baseline; gap: 8px; margin-bottom: 7px; }
  .rfila b { font-size: 13px; font-weight: 600; }
  .rest { font-size: 11px; color: #777; overflow: hidden;
          text-overflow: ellipsis; white-space: nowrap; }
  .racc { display: flex; gap: 7px; flex-wrap: wrap; }
  .racc input[type=file] { flex: 1 1 100%; font-size: 12px; color: #999; }
  .racc button { min-width: 84px; padding: 10px; font-size: 13px; }
  .rtope { font-size: 12px; color: #888; margin-top: 11px;
           border-top: 1px solid #222; padding-top: 10px; }
  .rtope input { max-width: 74px; margin: 0 4px; padding: 7px; }
  #quitar_show { width: 100%; margin-bottom: 12px; }
  #quitar_show:disabled { opacity: 0.35; }
  #quitar_show.peligro { border-color: #a44; color: #fbb;
                         background: #2a1414; }

  /* ---- Cola de impresion ---- */
  #cola { margin-bottom: 22px; }
  .trab { display: flex; gap: 11px; align-items: center; background: #161616;
          border-radius: 9px; padding: 9px; margin-bottom: 8px; }
  .trab img { width: 76px; height: 57px; object-fit: cover;
              border-radius: 6px; flex: none; background: #000; }
  .trab .datos { flex: 1; min-width: 0; }
  .trab .num { font-size: 19px; font-weight: 600; color: {{ acento }};
               line-height: 1.1; }
  /* El estado puede ocupar dos lineas: cuando algo falla, el mensaje de
     la impresora es justo lo que hay que poder leer entero. */
  .trab .est { font-size: 12px; color: #888; margin-top: 3px;
               line-height: 1.35; word-break: break-word; }
  .trab .bots { display: flex; flex-direction: column; gap: 5px; flex: none; }
  .trab .bots button, .trab .bots a { padding: 8px 13px; font-size: 13px;
                       border: none; border-radius: 6px; font-weight: 500;
                       text-align: center; text-decoration: none; }
  .si { background: {{ acento }}; color: #111; }
  .no { background: #2a2a2a; color: #999; }

  .e_lista      { color: #7c7; }
  .e_error      { color: #e77; }
  .e_imprimiendo{ color: #fc3; }
  .e_descartada { color: #666; text-decoration: line-through; }

  .vacio { font-size: 13px; color: #666; padding: 14px 0; }
  .hojas { font-size: 13px; color: #888; margin-bottom: 12px; }
  .hojas b { color: #ddd; }
  .hojas.poco b { color: #fc3; }

  /* ---- Diagnostico ---- */
  #diag { background: #161616; border-radius: 11px; padding: 6px 14px 11px;
          margin-bottom: 22px; }
  .dir { padding: 11px 0 9px; border-bottom: 1px solid #262626;
         margin-bottom: 4px; }
  .dir b { font-size: 16px; color: #eee; word-break: break-all; }
  .dir .etq { font-size: 12px; color: #888; display: block; margin-bottom: 3px; }
  .dir .marca { display: inline-block; font-size: 11px; padding: 2px 7px;
                border-radius: 20px; margin-top: 6px; }
  .marca.propia { background: #1e3a1e; color: #9e9; }
  .marca.ajena  { background: #3a3220; color: #fc3; }

  .dg { display: flex; align-items: center; gap: 9px; padding: 7px 0;
        font-size: 14px; color: #ccc; }
  .pt { width: 9px; height: 9px; border-radius: 50%; flex: none; }
  .pt.ok    { background: #6c6; }
  .pt.mal   { background: #e66; }
  .pt.tibio { background: #fc3; }
  .dg .val { color: #888; margin-left: auto; font-size: 13px;
             text-align: right; }
</style>
</head>
<body>

<h2>Administracion</h2>
<div class="sub" id="cab_evento"></div>

<div id="diag"></div>

<h3>Fotos por imprimir</h3>
<div class="hojas" id="hojas"></div>
<div id="cola"></div>

<h3>Evento</h3>

<div class="campo">
  <label>Nombre (linea grande)</label>
  <input type="text" id="e_nombre" maxlength="60">
</div>
<div class="campo">
  <label>Segunda linea (opcional)</label>
  <input type="text" id="e_subtitulo" maxlength="60">
</div>
<div class="campo">
  <label>Texto chico de arriba, en espanol (opcional)</label>
  <input type="text" id="e_etiqueta_es" maxlength="70">
</div>
<div class="campo">
  <label>Texto chico de arriba, en ingles (opcional)</label>
  <input type="text" id="e_etiqueta_en" maxlength="70">
</div>
<div class="campo">
  <label>Fecha (opcional)</label>
  <input type="text" id="e_fecha" maxlength="40" placeholder="14 · 11 · 2026">
</div>

<div class="campo">
  <label>Idioma del texto junto al codigo QR</label>
  <div class="opciones">
    <label><input type="radio" name="idi" value="bilingue" id="idi_b">
           <span>Los dos, alternando</span></label>
    <label><input type="radio" name="idi" value="es" id="idi_es">
           <span>Solo espanol</span></label>
    <label><input type="radio" name="idi" value="en" id="idi_en">
           <span>Solo ingles</span></label>
  </div>
  <div class="ayuda">
    Con los dos, el texto cambia de idioma cada pocos segundos con un
    fundido suave. El control desde el telefono siempre se adapta solo
    al idioma de cada invitado.
  </div>
</div>

<div class="campo">
  <label>Filetes decorativos</label>
  <div class="opciones">
    <label><input type="radio" name="lin" value="ninguna" id="lin_n">
           <span>Ninguno</span></label>
    <label><input type="radio" name="lin" value="arriba" id="lin_a">
           <span>Arriba</span></label>
    <label><input type="radio" name="lin" value="abajo" id="lin_b">
           <span>Abajo</span></label>
    <label><input type="radio" name="lin" value="ambas" id="lin_d">
           <span>Los dos</span></label>
  </div>
  <div class="ayuda">
    Las lineas cortas del color del evento. Con los dos puestos queda
    la composicion clasica de invitacion: filete, texto chico, nombre,
    filete, fecha.
  </div>
</div>

<div class="campo">
  <label>Color</label>
  <input type="color" id="e_acento">
</div>

<div class="botones">
  <button class="principal" onclick="guardarEvento()">Guardar evento</button>
</div>

<h3>Texto del centro</h3>

<div class="check">
  <input type="checkbox" id="e_centro_visible">
  <label for="e_centro_visible">Mostrar texto en el centro de la pantalla</label>
</div>

<div class="campo">
  <label>Texto</label>
  <input type="text" id="e_centro_texto" maxlength="60"
         placeholder="Cuando quieras">
  <div class="ayuda">
    Vacio usa el texto de siempre, traducido y alternando entre
    idiomas. Si escribes algo aqui se usa tal cual y deja de alternar.
    Con la casilla apagada no sale nada: el centro queda en negro, que
    en un espejo no es un hueco sino la parte que de verdad refleja.
  </div>
</div>

<div class="botones">
  <button class="principal" onclick="guardarEvento()">Guardar texto</button>
</div>

<h3>Letra y colores</h3>

<div class="campo">
  <label>Tipo de letra</label>
  <div class="opciones">
    {% for clave, t in tipos.items() %}
    <label><input type="radio" name="tipo" value="{{ clave }}"
                  id="tipo_{{ clave }}"><span>{{ t.nombre }}</span></label>
    {% endfor %}
  </div>
  <div class="ayuda">
    {% for clave, t in tipos.items() %}
    <b>{{ t.nombre }}</b>: {{ t.pista }}<br>
    {% endfor %}
    Se usa en el nombre del evento y en el texto del centro, y tambien
    en el pie de las fotos impresas.
  </div>
</div>

<div class="campo">
  <label>Color de cada parte</label>
  <div class="ayuda" style="margin-bottom:9px">
    Sin palomita, esa parte usa el color de siempre: el de acento para
    los filetes y la etiqueta, blanco para los textos. Palomea solo lo
    que quieras cambiar.
  </div>
  {% for clave, respaldo, titulo in partes %}
  <div class="cfila">
    <input type="checkbox" id="u_{{ clave }}">
    <label for="u_{{ clave }}">{{ titulo }}</label>
    <input type="color" id="e_{{ clave }}">
  </div>
  {% endfor %}
</div>

<div class="botones">
  <button onclick="verPantalla()">Ver la pantalla</button>
  <button class="principal" onclick="guardarEvento()">Guardar letra y colores</button>
</div>

<div id="caja_pantalla" style="display:none">
  <div class="marco_pantalla"><iframe id="ifr_pantalla"></iframe></div>
  <div class="pie_previa">La pantalla del espejo, en chiquito</div>
</div>

<h3>Marco de la foto</h3>

<div class="check">
  <input type="checkbox" id="e_marco_activo">
  <label for="e_marco_activo">Poner los datos del evento al pie de cada foto</label>
</div>

<img id="marco_previa" alt="Como queda la foto">
<div class="pie_previa">Asi va a salir cada foto</div>

<div class="nota">
  La barra usa el <b>nombre</b>, el <b>subtitulo</b> y la <b>fecha</b> que
  pusiste arriba, en Evento. Ademas cuadra la foto con el papel: el
  sensor da 16:9 y una hoja de 4x6 es 3:2, asi que sin barra la
  impresora deja dos bandas blancas. Con ella, la copia llena la hoja y
  no se recorta nada de la imagen.
</div>

<div class="campo">
  <label>Color de la barra</label>
  <input type="color" id="e_marco_fondo">
</div>
<div class="campo">
  <label>Color del texto de abajo</label>
  <input type="color" id="e_marco_tinta">
  <div class="ayuda">
    El nombre siempre va en blanco. Este color es para la fecha y el
    filete; si no lo cambias, se usa el color de acento del evento.
  </div>
</div>

<div class="botones">
  <button onclick="verMarco()">Actualizar la muestra</button>
  <button class="principal" onclick="guardarEvento()">Guardar marco</button>
</div>

<h3>Bromas</h3>

<div class="nota">
  Cinco ranuras, cada una con dos piezas. La <b>intro</b> es un GIF o
  un video que se repite en bucle sin sonido -- el espejo "hablando" --
  y el <b>remate</b> es la foto que aparece cuando tu decides. Entre
  una y otra la pantalla no pasa por negro.
</div>

<button id="quitar_show" onclick="quitarShow()">Quitar de la pantalla</button>

<div id="bromas"></div>

<h3>Codigo QR</h3>

<div class="campo">
  <label>Que hace el codigo de la pantalla</label>
  <div class="opciones">
    <label><input type="radio" name="mqr" value="wifi" id="mqr_w">
           <span>Conecta a la red</span></label>
    <label><input type="radio" name="mqr" value="enlace" id="mqr_e">
           <span>Abre la pagina</span></label>
  </div>
  <div class="ayuda">
    <b>Conecta a la red</b> es lo recomendado para la fiesta: el
    invitado escanea una vez, su telefono se conecta al espejo y la
    pagina se le abre sola. <b>Abre la pagina</b> solo sirve para quien
    ya esta en la misma red, por ejemplo cuando pruebas desde tu casa.
  </div>
</div>

<div class="campo">
  <label>Nombre de la red (SSID)</label>
  <input type="text" id="e_wifi_ssid" maxlength="32">
</div>
<div class="campo">
  <label>Contrasena de la red</label>
  <input type="text" id="e_wifi_clave" maxlength="63">
  <div class="ayuda">
    Estos dos solo arman el codigo QR: <b>no configuran la red</b>. Si
    algun dia cambias el punto de acceso, cambialos aqui tambien, o el
    codigo va a mandar a los invitados a una red que no existe.
  </div>
</div>

<div class="botones">
  <button class="principal" onclick="guardarEvento()">Guardar codigo QR</button>
</div>

<h3>Camara</h3>

<img id="previa" alt="Vista de la camara">
<div class="pie_previa">Vista en vivo de la camara</div>

<div class="nota">
  Mueve los controles y mira el efecto arriba al instante.
  Cuando quede bien, pulsa Guardar ajustes.
</div>

<div class="botones">
  <button onclick="preset('auto')">Todo automatico</button>
  <button onclick="preset('oscuro')">Salon con poca luz</button>
  <button onclick="preset('cristal')">Detras del cristal</button>
</div>

<div class="campo" style="margin-top:18px">
  <label>Tamano de las fotos</label>
  <div class="opciones">
    <label><input type="radio" name="res" value="alta" id="res_a">
           <span>Alta</span></label>
    <label><input type="radio" name="res" value="media" id="res_m">
           <span>Normal</span></label>
    <label><input type="radio" name="res" value="baja" id="res_b">
           <span>Baja</span></label>
  </div>
  <div class="ayuda">
    <b>Normal</b> es la recomendada: alcanza de sobra para imprimir en
    4x6 y para que se vea bien en cualquier telefono. <b>Alta</b> usa
    los 12 megapixeles del sensor, tarda mas en cada disparo y llena el
    disco mas rapido; solo vale la pena si alguien va a ampliar las
    fotos. <b>Baja</b> es para equipo lento.
  </div>
</div>

<h3>Imagen</h3>

<div class="ajuste">
  <div class="fila"><label>Brillo</label><span class="valor" id="v_brillo"></span></div>
  <input type="range" id="brillo" min="-3" max="3" step="0.2">
  <div class="extremos"><span>Mas oscura</span><span>Mas clara</span></div>
  <div class="ayuda">Si las caras salen oscuras detras del cristal, sube esto.</div>
</div>

<div class="ajuste">
  <div class="fila"><label>Intensidad del color</label><span class="valor" id="v_saturacion"></span></div>
  <input type="range" id="saturacion" min="0" max="2" step="0.05">
  <div class="extremos"><span>Blanco y negro</span><span>Muy vivo</span></div>
</div>

<div class="ajuste">
  <div class="fila"><label>Contraste</label><span class="valor" id="v_contraste"></span></div>
  <input type="range" id="contraste" min="0" max="2" step="0.05">
  <div class="extremos"><span>Suave</span><span>Marcado</span></div>
</div>

<div class="ajuste">
  <div class="fila"><label>Nitidez</label><span class="valor" id="v_nitidez"></span></div>
  <input type="range" id="nitidez" min="0" max="4" step="0.1">
  <div class="extremos"><span>Suave</span><span>Dura</span></div>
</div>

<h3>Enfoque</h3>

<div class="check">
  <input type="checkbox" id="enfoque_auto">
  <label for="enfoque_auto">Enfoque automatico</label>
</div>

<div class="ajuste">
  <div class="fila"><label>Distancia</label><span class="valor" id="v_enfoque"></span></div>
  <input type="range" id="enfoque" min="0" max="10" step="0.1">
  <div class="extremos"><span>Lejos</span><span>Cerca</span></div>
  <div class="ayuda">
    Detras del cristal conviene apagar el automatico: la camara intenta
    enfocar el reflejo en vez de la persona. Apagalo y ajusta a mano
    hasta que se vea nitido a la distancia donde se para la gente.
  </div>
</div>

<h3>Color</h3>

<div class="check">
  <input type="checkbox" id="color_auto">
  <label for="color_auto">Color automatico</label>
</div>

<div class="ajuste">
  <div class="fila"><label>Tono</label><span class="valor" id="v_tono"></span></div>
  <input type="range" id="tono" min="-1" max="1" step="0.05">
  <div class="extremos"><span>Mas frio (azul)</span><span>Mas calido (naranja)</span></div>
  <div class="ayuda">
    Si la piel sale azulada o verdosa, muevelo hacia lo calido.
    El cristal suele tenir la imagen.
  </div>
</div>

<h3>Impresora</h3>

<div class="campo">
  <div class="check">
    <input type="checkbox" id="i_activa">
    <label for="i_activa">Dejar que los invitados pidan su foto impresa</label>
  </div>
  <div class="ayuda">
    Si esta apagado, el boton ni siquiera aparece en el telefono.
  </div>
</div>

<div class="campo">
  <div class="check">
    <input type="checkbox" id="i_manual">
    <label for="i_manual">Imprimir a mano (sin impresora conectada a la Pi)</label>
  </div>
  <div class="ayuda">
    Al aprobar una foto no se manda a ninguna impresora: queda lista y
    en la cola aparece el boton <b>Descargar</b> para imprimirla tu, por
    ejemplo con la app de Canon por Wi-Fi. Con esto encendido no hace
    falta elegir impresora.
  </div>
</div>

<div class="campo">
  <label>Impresora</label>
  <select id="i_impresora"></select>
  <div class="ayuda">
    Son las que el sistema encuentra conectadas. Si falta la tuya,
    revisa que este encendida y enchufada, y vuelve a cargar esta pagina.
  </div>
</div>

<div class="campo">
  <div class="check">
    <input type="checkbox" id="i_aprobar">
    <label for="i_aprobar">Aprobar cada foto antes de imprimirla</label>
  </div>
  <div class="ayuda">
    Si lo apagas, la hoja se imprime sola en cuanto el invitado la pide,
    sin que tengas que estar. Si lo dejas, cada hoja espera tu visto
    bueno en la cola.
  </div>
</div>

<div class="campo">
  <label>Hojas que quedan</label>
  <input type="number" id="i_hojas" min="-1" step="1">
  <div class="ayuda">
    Baja sola con cada foto impresa. Pon <b>-1</b> si no quieres llevar
    la cuenta. Al cambiar el cartucho, escribe las hojas nuevas aqui.
  </div>
</div>

<div class="campo">
  <label>Fotos por hoja (maximo 4)</label>
  <input type="number" id="i_copias" min="1" max="4" step="1">
  <div class="ayuda">
    Cada sesion imprime UNA sola hoja con las fotos que el invitado
    elija, hasta este numero. Las fotos se acomodan solas en la hoja.
  </div>
</div>

<div class="campo">
  <label>Opciones de impresion (avanzado)</label>
  <input type="text" id="i_opciones" maxlength="120">
  <div class="ayuda">
    Se pasan tal cual al sistema de impresion. Si las fotos salen con
    borde blanco o cortadas, aqui se corrige. Si no sabes que poner,
    dejalo como esta.
  </div>
</div>

<div class="botones">
  <button class="principal" onclick="guardarImp()">Guardar impresora</button>
  <button onclick="pruebaImp()">Imprimir hoja de prueba</button>
</div>

<h3>PIN de administracion</h3>

<div class="campo">
  <label>PIN nuevo (4 a 8 numeros)</label>
  <input type="text" id="pin_nuevo" inputmode="numeric" maxlength="8">
  <div class="ayuda">
    Si se te olvida, se recupera borrando el archivo <b>pin.txt</b> de la
    carpeta del usuario y vuelve a ser el de fabrica.
  </div>
</div>
<div class="botones">
  <button onclick="cambiarPin()">Cambiar PIN</button>
</div>

<h3>Guardar y herramientas</h3>
<div class="botones">
  <button class="principal" onclick="guardarCal()">Guardar ajustes</button>
  <button onclick="prueba()">Foto de prueba</button>
</div>
<div class="botones">
  <button class="peligro" onclick="restaurar()">Valores de fabrica</button>
  <button onclick="liberar()">Liberar sesion atorada</button>
</div>

<h3>Respaldo y mantenimiento</h3>

<div class="nota">
  Guarda tu configuracion en un archivo antes del evento. Si la tarjeta
  de memoria falla y tienes que cambiarla, con ese archivo recuperas
  todos tus ajustes en un minuto en vez de rehacerlos.
</div>

<div class="botones">
  <a class="bot_a" href="/admin/config/exportar">Guardar configuracion</a>
  <button onclick="document.getElementById('archivo_cfg').click()">
    Cargar configuracion
  </button>
</div>
<input type="file" id="archivo_cfg" accept=".json,application/json"
       style="display:none" onchange="importarCfg(this)">

<div class="botones" style="margin-top:18px">
  <button class="peligro" onclick="borrarFotos()">Borrar todas las fotos</button>
  <button class="peligro" onclick="apagar()">Apagar el espejo</button>
</div>
<div class="ayuda">
  Apaga siempre desde aqui antes de desconectar la corriente. Quitarle
  la luz de golpe es la causa numero uno de que una Raspberry Pi deje
  de arrancar.
</div>

<div id="aviso"></div>

<script>
const CAMPOS = ['brillo','saturacion','contraste','nitidez','enfoque','tono'];
const CASILLAS = ['enfoque_auto','color_auto'];
const E_TEXTO = ['nombre','subtitulo','etiqueta_es','etiqueta_en','fecha',
                 'wifi_ssid','wifi_clave','centro_texto'];
let enviando = false;

/* ---- Vista previa: pide un cuadro nuevo en cuanto llega el anterior,
   asi se adapta sola a lo rapido que vaya la red.

   Se para cuando la pestana no esta a la vista. Son ocho capturas por
   segundo, y durante la fiesta el admin se queda abierto en el bolsillo
   del operador: ahi estarian compitiendo por la camara y por la CPU con
   las fotos de los invitados, sin que nadie las mire. ---- */
const previa = document.getElementById('previa');
let previaViva = false;

function siguienteCuadro() {
  if (document.visibilityState !== 'visible') { previaViva = false; return; }
  previaViva = true;
  previa.src = '/admin/previa?t=' + Date.now();
}
previa.onload  = () => setTimeout(siguienteCuadro, 120);
previa.onerror = () => setTimeout(siguienteCuadro, 1000);

document.addEventListener('visibilitychange', function () {
  if (document.visibilityState === 'visible' && !previaViva) siguienteCuadro();
});

/* ---- Evento ---- */
function pintarEvento(ev) {
  E_TEXTO.forEach(k => document.getElementById('e_' + k).value = ev[k] || '');
  pintarColores(ev);
  document.getElementById('e_acento').value = ev.acento;
  document.getElementById('idi_b').checked  = ev.idioma_espejo === 'bilingue';
  document.getElementById('idi_es').checked = ev.idioma_espejo === 'es';
  document.getElementById('idi_en').checked = ev.idioma_espejo === 'en';
  document.getElementById('lin_n').checked = ev.lineas === 'ninguna';
  document.getElementById('lin_a').checked = ev.lineas === 'arriba';
  document.getElementById('lin_b').checked = ev.lineas === 'abajo';
  document.getElementById('lin_d').checked = ev.lineas === 'ambas';
  document.getElementById('mqr_w').checked = ev.modo_qr !== 'enlace';
  document.getElementById('mqr_e').checked = ev.modo_qr === 'enlace';
  document.getElementById('e_centro_visible').checked = !!ev.centro_visible;
  document.getElementById('e_marco_activo').checked = !!ev.marco_activo;
  document.getElementById('e_marco_fondo').value = ev.marco_fondo || '#101014';
  document.getElementById('e_marco_tinta').value =
    ev.marco_tinta || ev.acento || '#b9a48a';
  document.getElementById('cab_evento').textContent = ev.nombre;
}

function leerEvento() {
  const ev = {};
  E_TEXTO.forEach(k => ev[k] = document.getElementById('e_' + k).value);
  ev.acento = document.getElementById('e_acento').value;
  ev.idioma_espejo =
    document.querySelector('input[name=idi]:checked').value;
  ev.lineas =
    document.querySelector('input[name=lin]:checked').value;
  ev.modo_qr =
    document.querySelector('input[name=mqr]:checked').value;
  ev.centro_visible = document.getElementById('e_centro_visible').checked;
  ev.marco_activo = document.getElementById('e_marco_activo').checked;
  ev.marco_fondo = document.getElementById('e_marco_fondo').value;
  ev.marco_tinta = document.getElementById('e_marco_tinta').value;
  leerColores(ev);
  return ev;
}

async function guardarEvento() {
  const r = await fetch('/admin/evento', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(leerEvento())
  });
  const d = await r.json();
  pintarEvento(d.evento);
  avisar(d.ok ? 'Evento guardado' : 'No se pudo guardar');
  verMarco();          // el marco usa esos mismos datos
  if (pantallaVista) verPantalla();
}

/* ---- Calibracion ---- */
function pintarCal(c) {
  CAMPOS.forEach(k => {
    document.getElementById(k).value = c[k];
    document.getElementById('v_' + k).textContent = Number(c[k]).toFixed(2);
  });
  CASILLAS.forEach(k => document.getElementById(k).checked = c[k]);
  document.getElementById('enfoque').disabled = c.enfoque_auto;
  document.getElementById('tono').disabled = c.color_auto;
  document.getElementById('res_a').checked = c.resolucion === 'alta';
  document.getElementById('res_m').checked = c.resolucion === 'media';
  document.getElementById('res_b').checked = c.resolucion === 'baja';
}

function leerCal() {
  const c = {};
  CAMPOS.forEach(k => c[k] = parseFloat(document.getElementById(k).value));
  CASILLAS.forEach(k => c[k] = document.getElementById(k).checked);
  const res = document.querySelector('input[name=res]:checked');
  if (res) c.resolucion = res.value;
  return c;
}

async function enviarCal(c) {
  if (enviando) return;
  enviando = true;
  try {
    const r = await fetch('/admin/calibracion', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(c)
    });
    pintarCal((await r.json()).calibracion);
  } catch (e) {}
  enviando = false;
}

function cambioCal() {
  const c = leerCal();
  CAMPOS.forEach(k =>
    document.getElementById('v_' + k).textContent = Number(c[k]).toFixed(2));
  document.getElementById('enfoque').disabled = c.enfoque_auto;
  document.getElementById('tono').disabled = c.color_auto;
  enviarCal(c);
}

CAMPOS.forEach(k => document.getElementById(k).addEventListener('input', cambioCal));
CASILLAS.forEach(k => document.getElementById(k).addEventListener('change', cambioCal));
document.querySelectorAll('input[name=res]')
        .forEach(r => r.addEventListener('change', cambioCal));

function avisar(txt) {
  const a = document.getElementById('aviso');
  a.textContent = txt;
  a.style.display = 'block';
  setTimeout(() => a.style.display = 'none', 2600);
}

async function preset(cual) {
  const r = await fetch('/admin/preset/' + cual, { method: 'POST' });
  pintarCal((await r.json()).calibracion);
  avisar('Ajuste aplicado');
}

async function guardarCal() {
  const r = await fetch('/admin/guardar', { method: 'POST' });
  avisar((await r.json()).ok ? 'Ajustes guardados' : 'No se pudo guardar');
}

async function restaurar() {
  const r = await fetch('/admin/restaurar', { method: 'POST' });
  pintarCal((await r.json()).calibracion);
  avisar('Valores de fabrica');
}

async function liberar() {
  await fetch('/admin/liberar', { method: 'POST' });
  avisar('Sesion liberada');
}

async function prueba() {
  avisar('Tomando foto...');
  const r = await fetch('/admin/prueba', { method: 'POST' });
  const d = await r.json();
  if (d.ok) window.open('/fotos/' + d.archivo, '_blank');
  else avisar('Error: ' + d.error);
}

/* ---- Impresora ---- */
const ESTADOS = {
  espera:      ['Por aprobar',        ''],
  cola:        ['En cola',            ''],
  imprimiendo: ['Imprimiendo...',     'e_imprimiendo'],
  lista:       ['Lista para entregar','e_lista'],
  error:       ['No se pudo imprimir','e_error'],
  descartada:  ['Descartada',         'e_descartada'],
};

function pintarImpresion(i, impresoras) {
  document.getElementById('i_activa').checked  = i.activa;
  document.getElementById('i_aprobar').checked = i.aprobar;
  document.getElementById('i_manual').checked  = !!i.manual;
  document.getElementById('i_hojas').value     = i.hojas;
  document.getElementById('i_copias').value    = i.copias_sesion;
  document.getElementById('i_opciones').value  = i.opciones;

  const sel = document.getElementById('i_impresora');
  const lista = impresoras || [];
  sel.innerHTML = '<option value="">— ninguna —</option>'
    + lista.map(n => '<option value="' + n + '">' + n + '</option>').join('');
  /* Si la guardada ya no esta conectada, se deja visible para que se vea
     que falta, en vez de borrarla en silencio. */
  if (i.impresora && !lista.includes(i.impresora)) {
    sel.innerHTML += '<option value="' + i.impresora + '">'
                   + i.impresora + ' (no conectada)</option>';
  }
  sel.value = i.impresora || '';
}

function leerImpresion() {
  return {
    activa:   document.getElementById('i_activa').checked,
    aprobar:  document.getElementById('i_aprobar').checked,
    manual:   document.getElementById('i_manual').checked,
    impresora: document.getElementById('i_impresora').value,
    hojas:    parseInt(document.getElementById('i_hojas').value, 10),
    copias_sesion: parseInt(document.getElementById('i_copias').value, 10),
    opciones: document.getElementById('i_opciones').value,
  };
}

async function guardarImp() {
  const r = await fetch('/admin/impresion', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(leerImpresion())
  });
  const d = await r.json();
  pintarImpresion(d.impresion, d.impresoras);
  avisar(d.ok ? 'Impresora guardada' : 'No se pudo guardar');
}

async function pruebaImp() {
  avisar('Mandando hoja de prueba...');
  const d = await (await fetch('/admin/impresion/prueba',
                               { method: 'POST' })).json();
  if (d.ok && d.manual) {
    window.open('/fotos/' + d.archivo, '_blank');
    avisar('Modo manual: se abrio la ultima foto para imprimirla tu.');
    return;
  }
  avisar(d.ok ? 'Mandada. Revisa la impresora.' : 'Error: ' + d.error);
}

async function cambiarPin() {
  const campo = document.getElementById('pin_nuevo');
  const d = await (await fetch('/admin/pin', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ pin: campo.value })
  })).json();
  if (d.ok) { campo.value = ''; avisar('PIN cambiado'); }
  else avisar('El PIN debe ser de 4 a 8 numeros');
}

/* ---- Cola ---- */
function dosDigitos(n) { return n < 10 ? '0' + n : '' + n; }

function pintarCola(d) {
  const h = document.getElementById('hojas');
  if (d.impresion.hojas < 0) {
    h.textContent = 'No se esta llevando la cuenta de hojas.';
    h.classList.remove('poco');
  } else {
    h.innerHTML = 'Quedan <b>' + d.impresion.hojas + '</b> hojas.';
    h.classList.toggle('poco', d.impresion.hojas <= {{ aviso_hojas }});
  }

  const caja = document.getElementById('cola');
  if (!d.cola.length) {
    caja.innerHTML = '<div class="vacio">Nadie ha pedido fotos impresas.</div>';
    return;
  }

  /* Lo mas reciente arriba: durante la fiesta es lo que se atiende. */
  const manual = !!d.impresion.manual;
  caja.innerHTML = d.cola.slice().reverse().map(t => {
    let [txt, clase] = ESTADOS[t.estado] || [t.estado, ''];
    if (manual && t.estado === 'lista') txt = 'Aprobada: descargala e imprimela';
    const detalle = (t.estado === 'error' && t.detalle)
                    ? ': ' + t.detalle : '';
    /* El nombre del archivo lleva el numero de recogida delante, para
       que en la carpeta de descargas se sepa de quien es cada foto. */
    const bajar = '<a class="no" href="/fotos/' + t.archivo + '" download="'
                + dosDigitos(t.recogida) + '_' + t.archivo + '">Descargar</a>';
    let bots = '';
    if (t.estado === 'espera') {
      bots = '<button class="si" onclick="cola_ok(\\'' + t.id + '\\')">'
           + (manual ? 'Aprobar' : 'Imprimir') + '</button>'
           + '<button class="no" onclick="cola_no(\\'' + t.id + '\\')">Descartar</button>';
    } else if (t.estado === 'error') {
      bots = '<button class="si" onclick="cola_ok(\\'' + t.id + '\\')">Reintentar</button>'
           + '<button class="no" onclick="cola_no(\\'' + t.id + '\\')">Descartar</button>';
    } else if (t.estado === 'lista') {
      bots = '<button class="no" onclick="cola_ok(\\'' + t.id + '\\')">Otra copia</button>';
    }
    if (t.estado !== 'descartada') bots += bajar;
    return '<div class="trab">'
         + '<img src="/fotos/' + t.archivo + '">'
         + '<div class="datos"><div class="num">' + dosDigitos(t.recogida) + '</div>'
         + '<div class="est ' + clase + '">' + txt + detalle + '</div></div>'
         + '<div class="bots">' + bots + '</div></div>';
  }).join('');
}

async function cola_ok(id) {
  await fetch('/admin/cola/' + id + '/imprimir', { method: 'POST' });
  refrescarCola();
}

async function cola_no(id) {
  await fetch('/admin/cola/' + id + '/descartar', { method: 'POST' });
  refrescarCola();
}

async function refrescarCola() {
  try { pintarCola(await (await fetch('/admin/cola')).json()); }
  catch (e) {}
}

setInterval(refrescarCola, 2000);
refrescarCola();

/* ---- Diagnostico ---- */
function dgFila(estado, nombre, valor) {
  return '<div class="dg"><span class="pt ' + estado + '"></span>' + nombre
       + '<span class="val">' + valor + '</span></div>';
}

function tiempoLargo(min) {
  if (min < 0) return '—';
  if (min < 60) return min + ' min';
  return Math.floor(min / 60) + ' h ' + (min % 60) + ' min';
}

function pintarDiag(d) {
  let h = '<div class="dir"><span class="etq">Direccion del espejo</span>'
        + '<b>http://' + d.ip + ':{{ puerto }}</b><br>'
        + (d.red_propia
            ? '<span class="marca propia">Red propia del espejo</span>'
            : '<span class="marca ajena">Colgado de otra red</span>')
        + '</div>';

  h += dgFila(d.camara_ok ? 'ok' : 'mal', 'Camara',
              d.camara_ok ? 'funcionando'
                          : (d.camara_error || 'sin responder'));

  h += dgFila('ok', 'Codigo de la pantalla',
              d.modo_qr === 'enlace' ? 'abre la pagina' : 'conecta a la red');

  /* El puerto 80 es lo que hace que el telefono abra la pagina solo al
     conectarse. Sin el, el booth funciona pero cada invitado tiene que
     navegar a mano. */
  h += dgFila(d.portal_ok ? 'ok' : 'tibio', 'Apertura automatica',
              d.portal_ok ? 'activa' : 'apagada · falta el puerto 80');

  if (!d.impresion_activa) {
    h += dgFila('tibio', 'Impresion', 'apagada');
  } else {
    h += dgFila(d.impresora_ok ? 'ok' : 'mal', 'Impresora',
                d.impresora_ok ? d.impresora
                               : ((d.impresora || 'sin elegir') + ' · no conectada'));
    const pocas = {{ aviso_hojas }};
    h += dgFila(d.hojas < 0 ? 'ok' : (d.hojas === 0 ? 'mal'
                                     : (d.hojas <= pocas ? 'tibio' : 'ok')),
                'Papel',
                d.hojas < 0 ? 'sin contar' : (d.hojas + ' hojas'));
    if (d.pendientes)
      h += dgFila('tibio', 'Esperando aprobacion', d.pendientes);
  }

  const mb = d.disco_libre_mb;
  const disco = mb < 0 ? '—'
    : (mb > 1024 ? (mb / 1024).toFixed(1) + ' GB libres' : mb + ' MB libres');
  h += dgFila(mb < 0 ? 'tibio' : (mb < 500 ? 'mal' : (mb < 2048 ? 'tibio' : 'ok')),
              'Espacio', disco);

  h += dgFila('ok', 'Fotos guardadas', d.fotos < 0 ? '—' : d.fotos);

  /* Lo primero que hay que mirar si alguien se queja de que "no le
     abre nada": cuantos telefonos estan en la red y cuantos de esos
     no han pedido ni una pagina. */
  h += dgFila(d.leases_ok ? 'ok' : 'tibio', 'Telefonos en la red',
              d.leases_ok
                ? d.conectados + (d.leases_fuente
                                    ? ' · por ' + d.leases_fuente : '')
                : 'no se puede contar · ' + d.leases_error);
  if (d.atorados)
    h += dgFila('tibio', 'Conectados sin abrir nada',
                d.atorados + ' · la pantalla ya les muestra el codigo');

  /* Si la Pi no tiene la fuente del estilo elegido, la foto sale con
     otra letra sin avisar. Mejor enterarse antes de cien copias. */
  if (d.fuente_archivo)
    h += dgFila(d.fuente_pobre ? 'mal' : 'ok', 'Letra de las fotos',
                d.tipografia + ' · ' + d.fuente_archivo);

  h += dgFila(d.marco_activo ? 'ok' : 'tibio', 'Marco en las fotos',
              d.marco_activo ? 'puesto' : 'sin poner · las copias saldran '
                               + 'con bandas blancas');

  h += dgFila(d.show_activo ? 'tibio' : (d.piezas_listas ? 'ok' : 'tibio'),
              'Bromas',
              d.show_activo
                ? 'HAY UNA EN LA PANTALLA'
                : (d.piezas_listas
                    ? d.piezas_listas + ' pieza(s) cargada(s)'
                    : 'sin cargar'));

  h += dgFila('ok', 'Encendida hace', tiempoLargo(d.minutos_encendida));

  document.getElementById('diag').innerHTML = h;


}

async function refrescarDiag() {
  try { pintarDiag(await (await fetch('/admin/diagnostico')).json()); }
  catch (e) {}
}

setInterval(refrescarDiag, 5000);
refrescarDiag();

/* ---- Letra y colores ---- */
const CLAVES_COLOR = {{ claves_color|safe }};

/* Un <input type=color> nunca puede estar vacio, asi que la casilla de
   al lado es la que dice si esa parte lleva color propio o hereda. */
function pintarColores(ev) {
  CLAVES_COLOR.forEach(function (k) {
    const propio = (ev[k] || '').trim();
    const chk = document.getElementById('u_' + k);
    const col = document.getElementById('e_' + k);
    chk.checked = !!propio;
    col.disabled = !propio;
    // Sin color propio se ensena el que hereda, para que al palomear
    // no salte a un valor cualquiera.
    col.value = propio || heredado(k, ev);
  });
  const t = ev.tipografia || 'clasica';
  const r = document.getElementById('tipo_' + t);
  if (r) r.checked = true;
}

function heredado(k, ev) {
  if (k === 'color_etiqueta' || k === 'color_lineas')
    return ev.acento || '#b9a48a';
  if (k === 'color_fecha' || k === 'color_pie') return '#8a8a8a';
  if (k === 'color_centro') return '#777777';
  return '#ffffff';
}

function leerColores(ev) {
  CLAVES_COLOR.forEach(function (k) {
    ev[k] = document.getElementById('u_' + k).checked
      ? document.getElementById('e_' + k).value : '';
  });
  const r = document.querySelector('input[name=tipo]:checked');
  ev.tipografia = r ? r.value : 'clasica';
}

/* Palomear habilita el color de esa parte, y al reves */
CLAVES_COLOR.forEach(function (k) {
  document.getElementById('u_' + k).addEventListener('change', function () {
    document.getElementById('e_' + k).disabled = !this.checked;
  });
});

/* La pantalla de verdad, encogida. Bajo demanda y no siempre: es una
   pagina mas consultando al servidor, y durante la fiesta no hace
   falta que este ahi. */
let pantallaVista = false;
function verPantalla() {
  const caja = document.getElementById('caja_pantalla');
  const ifr = document.getElementById('ifr_pantalla');
  caja.style.display = 'block';
  const ancho = ifr.parentElement.clientWidth;
  ifr.style.transform = 'scale(' + (ancho / 1080) + ')';
  ifr.src = '/?t=' + Date.now();
  pantallaVista = true;
}

/* ---- Marco ---- */
function verMarco() {
  document.getElementById('marco_previa').src =
    '/admin/marco/previa?t=' + Date.now();
}
verMarco();

/* ---- Bromas ---- */
const PIEZAS = [['intro', 'Intro', 'GIF o video en bucle'],
                ['remate', 'Remate', 'la foto que aparece despues']];

function esc(t) {
  return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;')
                  .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function pintarBromas(d) {
  const quitar = document.getElementById('quitar_show');
  quitar.className = d.show ? 'peligro' : '';
  quitar.disabled = !d.show;

  let h = '';
  d.ranuras.forEach(function (r) {
    const enPantalla = d.show && d.show.ranura === r.letra;
    h += '<div class="ranura' + (enPantalla ? ' viva' : '') + '"'
       + ' data-ranura="' + r.letra + '">';
    h += '<div class="rcab"><span class="rletra">'
       + r.letra.toUpperCase() + '</span>'
       + '<input class="rnombre" maxlength="40" data-act="renombrar"'
       + ' value="' + esc(r.nombre) + '"></div>';

    PIEZAS.forEach(function (par) {
      const clave = par[0], titulo = par[1], pista = par[2];
      const p = r.piezas[clave];
      const puesta = enPantalla && d.show.pieza === clave;

      h += '<div class="rpieza' + (puesta ? ' puesta' : '') + '"'
         + ' data-pieza="' + clave + '">';
      h += '<div class="rfila"><b>' + titulo + '</b><span class="rest">'
         + (p ? (p.tipo === 'video' ? 'video' : 'imagen') + ' · '
                + esc(p.archivo)
              : pista)
         + '</span></div>';
      h += '<div class="racc">';
      h += '<input type="file" accept="video/*,image/*">';
      h += '<button data-act="subir">Subir</button>';
      if (p) {
        h += '<button class="principal" data-act="mostrar">Mostrar</button>';
        h += '<button data-act="borrar">Borrar</button>';
      }
      h += '</div></div>';
    });

    h += '<div class="rtope">Se quita sola despues de '
       + '<input type="number" min="0" max="600" data-act="tope"'
       + ' value="' + r.tope + '">'
       + ' s · <b>0</b> = se queda hasta que la quites</div>';
    h += '</div>';
  });
  document.getElementById('bromas').innerHTML = h;
}

/* Un solo listener para las cinco ranuras. Los botones se redibujan
   cada pocos segundos, asi que engancharlos uno por uno seria volver a
   engancharlos cada vez. */
const cajaBromas = document.getElementById('bromas');

function ubicar(el) {
  const ranura = el.closest('.ranura');
  const pieza = el.closest('.rpieza');
  return {
    letra: ranura ? ranura.dataset.ranura : null,
    pieza: pieza ? pieza.dataset.pieza : null,
    caja: pieza,
  };
}

cajaBromas.addEventListener('click', function (e) {
  const b = e.target.closest('button[data-act]');
  if (!b) return;
  const d = ubicar(b);
  if (b.dataset.act === 'subir') subirPieza(d.letra, d.pieza, d.caja);
  else if (b.dataset.act === 'mostrar') mostrarPieza(d.letra, d.pieza);
  else if (b.dataset.act === 'borrar') borrarPieza(d.letra, d.pieza);
});

cajaBromas.addEventListener('change', function (e) {
  const i = e.target;
  if (!i.dataset || !i.dataset.act) return;
  const d = ubicar(i);
  if (i.dataset.act === 'renombrar') ajustarRanura(d.letra, { nombre: i.value });
  else if (i.dataset.act === 'tope') ajustarRanura(d.letra, { tope: i.value });
});

document.getElementById('quitar_show')
  .addEventListener('click', quitarShow);

/* La lista se redibuja sola para enterarse de lo que se cambie desde
   otro telefono, pero redibujarla reconstruye los <input type=file> y
   eso BORRA el archivo que el operador acaba de elegir. Con cuatro
   segundos entre refrescos, elegir un archivo y no alcanzar el boton
   Subir era lo normal, no la excepcion. */
function aMedias() {
  if (cajaBromas.contains(document.activeElement)) return true;
  return Array.prototype.some.call(
    cajaBromas.querySelectorAll('input[type=file]'),
    function (i) { return i.files && i.files.length; });
}

async function refrescarBromas() {
  if (aMedias()) return;
  try { pintarBromas(await (await fetch('/admin/bromas')).json()); }
  catch (e) {}
}

async function subirPieza(letra, pieza, caja) {
  const campo = caja ? caja.querySelector('input[type=file]') : null;
  const f = campo && campo.files[0];
  if (!f) { avisar('Elige un archivo primero'); return; }
  const cuerpo = new FormData();
  cuerpo.append('archivo', f);
  avisar('Subiendo ' + f.name + '...');
  try {
    const d = await (await fetch(
      '/admin/bromas/' + letra + '/' + pieza + '/subir',
      { method: 'POST', body: cuerpo })).json();
    if (!d.ok) { avisar(d.error || 'No se pudo subir'); return; }
    avisar('Listo · ' + (d.formato || d.tipo));
    pintarBromas(d);
  } catch (e) { avisar('No se pudo subir'); }
  refrescarDiag();
}

async function mostrarPieza(letra, pieza) {
  try {
    const d = await (await fetch(
      '/admin/bromas/' + letra + '/' + pieza + '/mostrar',
      { method: 'POST' })).json();
    if (!d.ok) { avisar(d.error || 'No se pudo'); return; }
    pintarBromas(d);
  } catch (e) { avisar('No se pudo'); }
}

async function borrarPieza(letra, pieza) {
  if (!confirm('Se borra esa pieza de la ranura. Sigue?')) return;
  try {
    const d = await (await fetch(
      '/admin/bromas/' + letra + '/' + pieza + '/borrar',
      { method: 'POST' })).json();
    if (d.ok) pintarBromas(d);
  } catch (e) { avisar('No se pudo'); }
  refrescarDiag();
}

async function quitarShow() {
  try {
    const d = await (await fetch('/admin/bromas/quitar',
                                 { method: 'POST' })).json();
    if (d.ok) pintarBromas(d);
  } catch (e) { avisar('No se pudo'); }
}

async function ajustarRanura(letra, datos) {
  try {
    const d = await (await fetch('/admin/bromas/' + letra, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(datos)
    })).json();
    if (d.ok) pintarBromas(d);
  } catch (e) { avisar('No se pudo guardar'); }
}

/* La pantalla puede haber cambiado desde otro telefono, y el tope
   puede haber quitado la pieza sola: se revisa cada pocos segundos. */
setInterval(refrescarBromas, 4000);
refrescarBromas();

/* ---- Respaldo y mantenimiento ---- */
async function borrarFotos() {
  if (!confirm('Se borran TODAS las fotos guardadas y la cola de '
             + 'impresion. Esto no se puede deshacer.')) return;
  const d = await (await fetch('/admin/fotos/borrar',
                               { method: 'POST' })).json();
  avisar('Se borraron ' + d.borradas + ' fotos');
  refrescarDiag();
  refrescarCola();
}

async function apagar() {
  /* Ojo con el salto de linea: esta plantilla es una cadena de Python,
     y un \\n sencillo se convertiria en un salto de verdad que partiria
     la cadena de JavaScript en dos y tumbaria el script entero. */
  if (!confirm('Se va a apagar el espejo.\\n\\nEspera a que la luz verde '
             + 'de la Raspberry Pi deje de parpadear antes de '
             + 'desconectar la corriente.')) return;
  const d = await (await fetch('/admin/apagar', { method: 'POST' })).json();
  if (d.ok) {
    avisar('Apagando. Espera a que se apague la luz verde.');
  } else {
    avisar(d.error || 'No se pudo apagar');
    if (d.ayuda) alert(d.ayuda);
  }
}

async function importarCfg(input) {
  const f = input.files[0];
  input.value = '';
  if (!f) return;
  try {
    const datos = JSON.parse(await f.text());
    const d = await (await fetch('/admin/config/importar', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(datos)
    })).json();
    if (!d.ok) { avisar(d.error || 'No se pudo cargar'); return; }
    avisar('Configuracion cargada');
    /* Se recarga en vez de repintar: asi el desplegable de impresoras
       y todo lo demas quedan coherentes de un solo golpe. */
    setTimeout(() => location.reload(), 900);
  } catch (e) {
    avisar('Ese archivo no se pudo leer');
  }
}

pintarEvento({{ evento_json|safe }});
pintarCal({{ calibracion_json|safe }});
pintarImpresion({{ impresion_json|safe }}, {{ impresoras_json|safe }});
siguienteCuadro();
</script>
</body>
</html>
"""


PRESETS = {
    "auto": {"brillo": 0.0, "saturacion": 1.0, "contraste": 1.0, "nitidez": 1.0,
             "enfoque_auto": True, "enfoque": 2.0, "color_auto": True, "tono": 0.0},
    "oscuro": {"brillo": 1.2, "saturacion": 1.05, "contraste": 0.9, "nitidez": 1.0,
               "enfoque_auto": True, "enfoque": 2.0, "color_auto": True, "tono": 0.0},
    "cristal": {"brillo": 1.8, "saturacion": 1.15, "contraste": 1.1, "nitidez": 1.2,
                "enfoque_auto": False, "enfoque": 0.7, "color_auto": False, "tono": 0.35},
}


def autorizado():
    return cookie_admin_valida()


def idiomas_espejo():
    """Que idiomas muestra la pantalla, en orden."""
    modo = evento.get("idioma_espejo", "bilingue")
    if modo == "es":
        return ["es"]
    if modo == "en":
        return ["en"]
    return ["es", "en"]


# ---------------------------------------------------------------
# Rutas publicas
# ---------------------------------------------------------------

@app.route("/")
def espejo():
    # Quien escribe 10.42.0.1 en Safari llega aqui y no debe ver la
    # pantalla del espejo sino su sesion. El espejo mismo (127.0.0.1) y
    # la vista previa del admin (?t=) siguen viendo la pantalla.
    if (request.remote_addr not in ("127.0.0.1", "::1", ip_local())
            and not autorizado()):
        return al_portal()
    idis = idiomas_espejo()
    # La etiqueta de arriba sigue el mismo criterio que el resto
    partes = [evento.get(f"etiqueta_{L}", "") for L in idis]
    etiqueta = " · ".join([p for p in partes if p])

    return render_template_string(
        ESPEJO, ev=evento, T=T, idiomas=idis, etiqueta=etiqueta,
        version=version_evento,
        tipo=tipografia(), col=colores_pantalla(),
        alterna=int(SEGUNDOS_ALTERNA * 1000),
        qr_wifi=bool(evento.get("modo_qr", "wifi") == "wifi"
                     and texto_qr_wifi()),
    )


def con_cookie(respuesta, token):
    """Deja el token en una cookie para que recargar no borre las fotos."""
    respuesta.set_cookie("visita", token, max_age=VIDA_VISITA,
                         samesite="Lax")
    return respuesta


@app.route("/s/<token>")
def control(token):
    """La pagina del telefono.

    Abrirla ya NO aparta el espejo. Hasta booth11 si: el primero que se
    conectaba lo bloqueaba 90 segundos, asi que cincuenta telefonos con
    la red ya guardada, reconectandose solos, habrian hecho imposible
    la fiesta. Ahora el espejo se agarra al picar el boton de disparar.
    """
    lang = idioma()
    t = T[lang]

    with candado:
        token, _ = nueva_visita(token)
        _token_por_ip[request.remote_addr] = token

    pag = make_response(render_template_string(
        MOVIL, base=f"http://{ip_local()}:{PUERTO}", token=token, ev=evento, lang=lang, t=t, t_json=json.dumps(t),
        otro_lang=("en" if lang == "es" else "es"),
        aviso=AVISO_ANTES,
    ))
    return con_cookie(pag, token)


@app.route("/entrar")
def entrar():
    """Puerta de entrada: le reparte a cada telefono un token propio.

    El codigo QR de la pantalla apunta aqui y no a una sesion concreta,
    asi que no se quema al usarse ni caduca. Quien ya tiene cookie
    vuelve a la suya, con sus fotos; quien llega nuevo recibe una.
    """
    previo = request.cookies.get("visita")
    ip = request.remote_addr
    with candado:
        if previo and previo in visitas:
            token, _ = nueva_visita(previo)
        elif _token_por_ip.get(ip) in visitas:
            # Mismo telefono que llega sin cookie: de la ventanita del
            # portal a Safari, en iPhone. Se le devuelve su sesion.
            token, _ = nueva_visita(_token_por_ip[ip])
        else:
            token, _ = nueva_visita()

    return con_cookie(redirect(url_for("control", token=token)), token)


@app.route("/api/estado")
def api_estado():
    token = request.args.get("token")
    ahora = time.time()

    with candado:
        fase = estado["fase"]
        datos = {
            "fase": fase,
            "foto": estado["foto"],
            "show": pieza_en_pantalla(),
            "version_evento": version_evento,
            "restante": max(0, int(estado["cuenta_fin"] - ahora) + 1)
                        if fase == "cuenta" else 0,
        }
        if token is None:
            datos["qr"] = qr_para_pantalla()
            fotos = None
            # Lo que le falta al turno actual, para que la fila lo vea
            datos["queda_espejo"] = (
                max(0, int(INACTIVIDAD_ESPEJO - (ahora - estado["accion"])))
                if fase == "espera" else None)
        else:
            # Esta peticion ES el latido del telefono: mientras llegue,
            # la persona sigue ahi. Cuando deja de llegar y el espejo
            # esta en gracia, el vigilante lo suelta en segundos.
            _, v = nueva_visita(token)
            fotos = list(v["fotos"])
            hoja = v.get("hoja")
            datos["fotos"] = fotos
            datos["mio"] = (token == estado["dueno"])
            # Puede disparar si nadie lo tiene, o si ya es suyo y la
            # toma anterior termino.
            datos["puedo"] = (fase == "libre") or (
                token == estado["dueno"] and fase in ("resultado", "espera"))
            # Segundos antes de que el espejo pase al siguiente. Solo
            # para el dueno, y solo cuando el reloj corre de verdad.
            datos["queda"] = (
                max(0, int(INACTIVIDAD_ESPEJO - (ahora - estado["accion"])))
                if (token == estado["dueno"] and fase == "espera") else None)

    # Fuera del candado del estado: los otros candados son suyos y
    # cruzarlos seria la forma mas facil de trabarlo todo.
    if token is None:
        # Telefonos conectados que no han abierto nada. Solo con esto
        # la pantalla ensena el aviso, y solo mientras haga falta.
        perdidos = cuantos_atorados()
        datos["atorados"] = perdidos
        datos["qr_enlace"] = qr_enlace_cache()
        if perdidos:
            datos["qr_ayuda"] = qr_enlace()
    else:
        datos["imprimir_activo"] = bool(
            impresion.get("activa")
            and (impresion.get("manual")
                 or impresion.get("impresora", "").strip()))
        datos["hay_papel"] = impresion.get("hojas", -1) != 0
        datos["max_hoja"] = impresion.get("copias_sesion", MAX_FOTOS_HOJA)
        # Sin aprobacion ni modo manual, la hoja sale sola: el telefono
        # manda a la impresora y no al encargado.
        datos["auto"] = not (impresion.get("aprobar")
                             or impresion.get("manual"))
        datos["hoja"] = estado_hoja(hoja)

    return jsonify(datos)


def hoja_vigente(hoja):
    """Si la hoja de una visita sigue contando contra su tope.

    Solo deja de contar si el operador la descarto: entonces el invitado
    puede volver a elegir. Si el trabajo ya no aparece en la cola (la
    cola recuerda los ultimos MAX_COLA_VISIBLE), se da por impresa.
    """
    if not hoja:
        return False
    if hoja.get("armando"):
        return True
    with candado_cola:
        for t in cola:
            if t["archivo"] == hoja.get("archivo"):
                return t["estado"] != "descartada"
    return True


def estado_hoja(hoja):
    """Lo que el telefono necesita saber de su hoja, o None."""
    if not hoja_vigente(hoja) or hoja.get("armando"):
        return None
    est = "lista"
    with candado_cola:
        for t in cola:
            if t["archivo"] == hoja["archivo"]:
                est = t["estado"]
                # Recien mandada: la impresora todavia la esta sacando
                if (est == "lista" and time.time() - t.get("lista_en", 0)
                        < SEGUNDOS_IMPRESION):
                    est = "imprimiendo"
                break
    return {"recogida": hoja["recogida"], "n": len(hoja["fotos"]),
            "estado": est}


@app.route("/api/imprimir_hoja/<token>", methods=["POST"])
def api_imprimir_hoja(token):
    """Imprime la hoja de la sesion con las fotos elegidas.

    Seguridad: solo se pueden elegir fotos de ESTA visita (el token es
    secreto y va en la cookie del telefono), sin repetir, hasta el tope,
    y una sola hoja por visita. Al terminar la sesion la visita se borra,
    asi que una sesion nueva empieza sin fotos y no puede imprimir las
    de nadie.
    """
    pedidas = (request.get_json(silent=True) or {}).get("fotos")
    if not isinstance(pedidas, list) or not pedidas:
        return jsonify(ok=False, error="foto"), 400
    pedidas = list(dict.fromkeys(str(f) for f in pedidas))

    hay_destino = (impresion.get("manual")
                   or impresion.get("impresora", "").strip())
    if not (impresion.get("activa") and hay_destino):
        return jsonify(ok=False, error="apagada"), 409
    if impresion.get("hojas", -1) == 0:
        return jsonify(ok=False, error="papel"), 409
    if len(pedidas) > impresion.get("copias_sesion", MAX_FOTOS_HOJA):
        return jsonify(ok=False, error="tope"), 409

    with candado:
        v = visitas.get(token)
        if v is None:
            return jsonify(ok=False, error="sesion"), 409
        if any(f not in v["fotos"] for f in pedidas):
            return jsonify(ok=False, error="foto"), 400
        v["visto"] = time.time()
        hoja = v.get("hoja")

    # hoja_vigente toma el candado de la cola: se llama fuera del otro
    if hoja_vigente(hoja):
        if hoja.get("armando"):
            return jsonify(ok=False, error="armando"), 409
        return jsonify(ok=True, recogida=hoja["recogida"], ya=True)

    with candado:
        v = visitas.get(token)
        if v is None:
            return jsonify(ok=False, error="sesion"), 409
        # Apartar antes de armar: un doble toque no imprime dos hojas
        if v.get("hoja") is not hoja:
            return jsonify(ok=False, error="armando"), 409
        v["hoja"] = {"armando": True}
        if v["recogida"] is None:
            v["recogida"] = siguiente_recogida()
        recogida = v["recogida"]
        marcar_accion(token)

    archivo = f"hoja-{recogida:03d}-{secrets.token_hex(4)}.jpg"
    try:
        componer_hoja(pedidas, FOTOS_DIR / archivo)
    except Exception as e:
        print(f"No se pudo armar la hoja: {e}")
        with candado:
            v = visitas.get(token)
            if v is not None:
                v["hoja"] = None
        return jsonify(ok=False, error="armar"), 500

    with candado:
        v = visitas.get(token)
        if v is not None:
            v["hoja"] = {"archivo": archivo, "recogida": recogida,
                         "fotos": pedidas}

    encolar(archivo, recogida)
    return jsonify(ok=True, recogida=recogida)


@app.route("/api/descartar/<token>", methods=["POST"])
def api_descartar(token):
    """Quita una foto de la galeria de quien se la tomo.

    El archivo NO se borra del disco: el operador conserva todas, por si
    alguien se arrepiente o por si hace falta reimprimir. Lo que se
    quita es el acceso de esa visita y, si todavia estaba esperando
    aprobacion, su lugar en la cola.
    """
    archivo = (request.get_json(silent=True) or {}).get("archivo", "")

    with candado:
        v = visitas.get(token)
        if v is None:
            return jsonify(ok=False, error="sesion"), 409
        if archivo not in v["fotos"]:
            return jsonify(ok=False, error="foto"), 400
        v["fotos"].remove(archivo)
        v["visto"] = time.time()
        marcar_accion(token)
        # Si es la que el espejo esta ensenando en ese momento, fuera
        if estado["foto"] == archivo:
            estado["foto"] = None

    # Una copia ya impresa o en la impresora no se puede deshacer; una
    # que sigue esperando el visto bueno, si.
    with candado_cola:
        for t in cola:
            if t["archivo"] == archivo and t["estado"] == "espera":
                t["estado"] = "descartada"

    return jsonify(ok=True)


@app.route("/api/disparar/<token>", methods=["POST"])
def api_disparar(token):
    """Aqui es donde se agarra el espejo, y solo aqui."""
    with candado:
        # Un token que el espejo no conoce -- se reinicio el servicio, o
        # la visita caduco -- recibe una nueva en el momento en vez de
        # un rechazo. Lo unico que pierde son las fotos viejas.
        token, v = nueva_visita(token)

        fase = estado["fase"]
        if fase == "libre":
            estado["dueno"] = token
        elif token != estado["dueno"]:
            return jsonify(ok=False, error="ocupado"), 409
        elif fase in ("cuenta", "capturando"):
            return jsonify(ok=False, error="ya_va"), 409
        # resultado o espera siendo el dueno: puede disparar otra vez

        estado["fase"] = "cuenta"
        estado["cuenta_fin"] = time.time() + SEGUNDOS_CUENTA
        marcar_accion(token)

    threading.Timer(SEGUNDOS_CUENTA, capturar_ahora, args=(token,)).start()
    return jsonify(ok=True)


def _a_media_foto(token):
    """Si este token tiene una captura en curso, no se le toca nada.

    El aviso de cierre del navegador llega tambien cuando el telefono
    se bloquea, y la gente pica el boton y baja el telefono justo para
    posar: soltar el espejo ahi tiraria la foto que acaban de pedir.
    """
    return (token == estado["dueno"]
            and estado["fase"] in ("cuenta", "capturando"))


@app.route("/api/seguir/<token>", methods=["POST"])
def api_seguir(token):
    """"Sigo aqui": reinicia los quince segundos sin tomar otra foto.

    Lo pica quien vio el aviso y todavia no decide si imprime. Sin
    esto, la unica forma de no perder el espejo seria disparar, y la
    gente acabaria tomando fotos que no quiere para no perder el turno.
    """
    with candado:
        if token != estado["dueno"]:
            return jsonify(ok=False, error="no es tuyo"), 409
        marcar_accion(token)
        v = visitas.get(token)
        if v is not None:
            v["visto"] = time.time()
    return jsonify(ok=True)


@app.route("/api/suelto/<token>", methods=["POST"])
def api_suelto(token):
    """El navegador se va: suelta el espejo, pero NO cierra la sesion.

    Esto es lo que manda el telefono al cerrar la pestana o al
    bloquearse, y por eso no puede borrar nada: la gente se guarda el
    telefono en la bolsa, platica, y lo saca de nuevo para pedir su
    impresion. Cerrarle la sesion ahi seria quitarle sus fotos por
    haber bloqueado la pantalla.
    """
    with candado:
        if token == estado["dueno"] and not _a_media_foto(token):
            soltar_espejo()
    return jsonify(ok=True)


@app.route("/api/terminar/<token>", methods=["POST"])
def api_terminar(token):
    """El boton: cierra la sesion de verdad.

    Suelta el espejo, tira la visita y borra la cookie, asi que el
    telefono queda limpio. Eso importa en una fiesta donde los primos
    comparten un telefono: sin esto, el segundo entraria a la sesion
    del primero por la cookie y veria sus fotos.

    Las fotos en disco no se tocan: el operador las conserva todas.
    """
    with candado:
        if _a_media_foto(token):
            return jsonify(ok=False, error="va_una_foto"), 409
        if token == estado["dueno"]:
            soltar_espejo()
        visitas.pop(token, None)

    r = make_response(jsonify(ok=True))
    r.delete_cookie("visita")
    return r



def pieza_en_pantalla():
    """Lo que la pantalla tiene que pintar ahora, o None.

    Se llama con el candado tomado. El `v` del final obliga al
    navegador a volver a pedir el archivo cuando se reemplaza por otro
    con el mismo nombre.
    """
    show = estado["show"]
    if not show:
        return None
    pieza = bromas.get(show["ranura"], {}).get("piezas", {}).get(show["pieza"])
    if not pieza:
        return None
    return {
        "src": f"/broma/{pieza['archivo']}?v={show['puesta']}",
        "tipo": pieza["tipo"],
    }


@app.route("/broma/<nombre>")
def servir_broma(nombre):
    """Las piezas de las bromas. Publicas: las pide la pantalla."""
    return send_from_directory(DIR_BROMAS, nombre, max_age=0)


@app.route("/fotos/<nombre>")
def servir_foto(nombre):
    """Sirve una foto. Con ?d=1 cuenta como accion del dueno.

    El parametro lo lleva solo el boton de descargar, no las miniaturas
    de la galeria ni la imagen que pinta el espejo: asi "descargar"
    reinicia el reloj y "mirar" no, que es la distincion que mantiene
    el espejo libre.
    """
    tok = request.cookies.get("visita")
    with candado:
        v = visitas.get(tok) if tok else None
        es_de_visita = bool(v and (
            nombre in v["fotos"] or
            (v.get("hoja") and v["hoja"].get("archivo") == nombre)
        ))
        # La pantalla fisica del espejo usa este endpoint en localhost.
        es_del_espejo = (request.remote_addr in ("127.0.0.1", "::1", ip_local())
                          and estado.get("foto") == nombre)
        if request.args.get("d") and es_de_visita and tok:
            marcar_accion(tok)
    if not (autorizado() or es_de_visita or es_del_espejo):
        return jsonify(ok=False, error="sin acceso a esta foto"), 403
    return send_from_directory(FOTOS_DIR, nombre)


# ---------------------------------------------------------------
# Portal cautivo
#
# Al entrar a una red, los telefonos piden una direccion conocida para
# ver si hay internet de verdad. Android espera un 204 vacio, iOS una
# pagina que diga "Success", y Windows un texto fijo. Si reciben eso,
# dan la red por buena; si reciben otra cosa, concluyen que hay un
# portal de por medio y abren el navegador solos.
#
# Esa es toda la magia: aqui se contesta a proposito algo distinto a lo
# que esperan. Sin esto, Android muestra el aviso de "Internet no esta
# disponible" con un boton de Desconectar bien visible, y cada invitado
# tiene que decidir por su cuenta si quedarse. Con esto, el telefono
# dice "Iniciar sesion en la red" y abre la pagina del booth solo.
#
# Para que las peticiones lleguen hasta aqui hace falta ademas que el
# DNS del punto de acceso responda siempre con la IP del espejo; eso se
# configura aparte, en NetworkManager.
# ---------------------------------------------------------------

SONDAS_CAUTIVAS = (
    "/generate_204",            # Android
    "/gen_204",                 # Android
    "/hotspot-detect.html",     # iOS y macOS
    "/library/test/success.html",
    "/connecttest.txt",         # Windows
    "/ncsi.txt",
    "/redirect",
    "/canonical.html",          # NetworkManager y Firefox
    "/success.txt",
    "/chat",                    # algunos Android recientes
)

# Rutas que nunca deben acabar en el portal: si una foto no existe, lo
# correcto es un 404 honesto y no mandar al navegador a dar vueltas.
PREFIJOS_PROPIOS = ("/api/", "/admin", "/fotos/", "/s/", "/static/")


SONDAS_APPLE = ("/hotspot-detect.html", "/library/test/success.html")
EXITO_APPLE = ("<HTML><HEAD><TITLE>Success</TITLE></HEAD>"
               "<BODY>Success</BODY></HTML>")


def al_portal():
    """Manda al booth. Excepcion: el iPhone que ya entro.

    Al iPhone que ya abrio la pagina se le contesta "Success" a su sonda.
    Asi la ventanita del portal cambia "Cancelar" por "Listo" y el
    telefono se queda en la red al cerrarla. Sin esto iOS se salia de la
    red en cuanto se cerraba la ventanita, y no habia forma de abrir las
    fotos en Safari, que es donde si se pueden guardar.
    """
    if request.path in SONDAS_APPLE:
        with candado_red:
            ya_entro = request.remote_addr in _ips_entraron
        if ya_entro:
            r = make_response(EXITO_APPLE)
            r.headers["Content-Type"] = "text/html"
            r.headers["Cache-Control"] = "no-store"
            return r
    return redirect(f"http://{ip_local()}:{PUERTO}/entrar", code=302)


for _ruta in SONDAS_CAUTIVAS:
    app.add_url_rule(_ruta, "sonda_" + _ruta.strip("/").replace(".", "_"),
                     al_portal)


@app.errorhandler(404)
def no_encontrado(e):
    """Con el DNS secuestrado, cualquier direccion del mundo aterriza
    aqui. En vez de un error, se manda al booth."""
    ruta = request.path or "/"
    if any(ruta.startswith(p) for p in PREFIJOS_PROPIOS):
        return jsonify(ok=False, error="no existe"), 404
    return al_portal()


# ---------------------------------------------------------------
# Rutas de administracion
# ---------------------------------------------------------------

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        if request.form.get("pin") == pin_admin:
            resp = make_response(redirect(url_for("admin")))
            return poner_cookie_admin(resp)
        return render_template_string(LOGIN, error=True, acento=evento["acento"])

    if not autorizado():
        return render_template_string(LOGIN, error=False, acento=evento["acento"])

    return render_template_string(
        ADMIN, acento=evento["acento"], direccion=base_url(),
        tipos=TIPOGRAFIAS, partes=PARTES_COLOR,
        claves_color=json.dumps([k for k, _, _ in PARTES_COLOR]),
        evento_json=json.dumps(evento, ensure_ascii=False),
        calibracion_json=json.dumps(calibracion),
        impresion_json=json.dumps(impresion, ensure_ascii=False),
        impresoras_json=json.dumps(impresoras_disponibles()),
        aviso_hojas=AVISO_POCAS_HOJAS, puerto=PUERTO,
    )


@app.route("/admin/evento", methods=["POST"])
def admin_evento():
    if not autorizado():
        return jsonify(ok=False), 403
    datos = request.get_json(silent=True) or {}
    for k in EVENTO_FABRICA:
        if k in datos:
            evento[k] = datos[k]
    if not evento["nombre"].strip():
        evento["nombre"] = EVENTO_FABRICA["nombre"]
    if evento["idioma_espejo"] not in ("bilingue", "es", "en"):
        evento["idioma_espejo"] = "bilingue"
    if evento["lineas"] not in ("ninguna", "arriba", "abajo", "ambas"):
        evento["lineas"] = "abajo"
    evento["centro_visible"] = bool(evento.get("centro_visible"))
    evento["marco_activo"] = bool(evento.get("marco_activo"))
    if evento.get("tipografia") not in TIPOGRAFIAS:
        evento["tipografia"] = "clasica"
    # Un color vacio no es un error: significa que esa parte hereda.
    for k, _, _ in PARTES_COLOR:
        v = str(evento.get(k, "")).strip()
        evento[k] = v if (v.startswith("#") and len(v) == 7) else ""
    for k, respaldo in (("marco_fondo", "#101014"), ("marco_tinta", "")):
        v = str(evento.get(k, "")).strip()
        evento[k] = v if (v.startswith("#") and len(v) == 7) else respaldo
    evento["centro_texto"] = str(evento.get("centro_texto", ""))[:60]
    return jsonify(ok=guardar_evento(), evento=evento)


@app.route("/admin/previa")
def admin_previa():
    if not autorizado():
        return "", 403
    try:
        img = cuadro_previa()
        buf = io.BytesIO()
        img.convert("RGB").save(buf, format="JPEG", quality=70)
        resp = make_response(buf.getvalue())
        resp.headers["Content-Type"] = "image/jpeg"
        resp.headers["Cache-Control"] = "no-store"
        return resp
    except Exception as e:
        return str(e), 500


@app.route("/admin/calibracion", methods=["POST"])
def admin_calibracion():
    if not autorizado():
        return jsonify(ok=False), 403
    datos = request.get_json(silent=True) or {}
    for k in CALIBRACION_FABRICA:
        if k in datos:
            calibracion[k] = datos[k]
    if calibracion.get("resolucion") not in RESOLUCIONES:
        calibracion["resolucion"] = CALIBRACION_FABRICA["resolucion"]
    aplicar_calibracion()
    return jsonify(ok=True, calibracion=calibracion)


@app.route("/admin/preset/<cual>", methods=["POST"])
def admin_preset(cual):
    if not autorizado():
        return jsonify(ok=False), 403
    if cual in PRESETS:
        calibracion.update(PRESETS[cual])
        aplicar_calibracion()
    return jsonify(ok=True, calibracion=calibracion)


@app.route("/admin/guardar", methods=["POST"])
def admin_guardar():
    if not autorizado():
        return jsonify(ok=False), 403
    return jsonify(ok=guardar_calibracion())


@app.route("/admin/restaurar", methods=["POST"])
def admin_restaurar():
    if not autorizado():
        return jsonify(ok=False), 403
    calibracion.update(CALIBRACION_FABRICA)
    aplicar_calibracion()
    return jsonify(ok=True, calibracion=calibracion)


@app.route("/admin/liberar", methods=["POST"])
def admin_liberar():
    if not autorizado():
        return jsonify(ok=False), 403
    with candado:
        soltar_espejo()
    return jsonify(ok=True)


@app.route("/admin/prueba", methods=["POST"])
def admin_prueba():
    if not autorizado():
        return jsonify(ok=False), 403
    nombre = "prueba-" + datetime.now().strftime("%H%M%S") + ".jpg"
    try:
        tomar_foto(FOTOS_DIR / nombre)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500
    return jsonify(ok=True, archivo=nombre)


# ---------------------------------------------------------------
# Rutas de impresion (administracion)
# ---------------------------------------------------------------

@app.route("/admin/cola")
def admin_cola():
    if not autorizado():
        return jsonify(ok=False), 403
    with candado_cola:
        copia = [dict(t) for t in cola]
    return jsonify(cola=copia, impresion=impresion)


@app.route("/admin/cola/<trabajo_id>/imprimir", methods=["POST"])
def admin_cola_imprimir(trabajo_id):
    """Aprueba una foto en espera, reintenta una fallida, o pide otra
    copia de una que ya salio."""
    if not autorizado():
        return jsonify(ok=False), 403
    with candado_cola:
        for t in cola:
            if t["id"] == trabajo_id:
                t["estado"] = "cola"
                t["detalle"] = ""
                return jsonify(ok=True)
    return jsonify(ok=False, error="no esta"), 404


@app.route("/admin/cola/<trabajo_id>/descartar", methods=["POST"])
def admin_cola_descartar(trabajo_id):
    if not autorizado():
        return jsonify(ok=False), 403
    with candado_cola:
        for t in cola:
            if t["id"] == trabajo_id:
                # Lo que ya esta en la impresora no se puede deshacer
                if t["estado"] == "imprimiendo":
                    return jsonify(ok=False, error="ya salio"), 409
                t["estado"] = "descartada"
                return jsonify(ok=True)
    return jsonify(ok=False, error="no esta"), 404


@app.route("/admin/impresion", methods=["POST"])
def admin_impresion():
    if not autorizado():
        return jsonify(ok=False), 403

    datos = request.get_json(silent=True) or {}
    for k in ("activa", "aprobar", "manual"):
        if k in datos:
            impresion[k] = bool(datos[k])
    for k in ("impresora", "opciones"):
        if k in datos:
            impresion[k] = str(datos[k])[:200]
    if isinstance(datos.get("hojas"), int):
        impresion["hojas"] = max(-1, datos["hojas"])
    if isinstance(datos.get("copias_sesion"), int):
        impresion["copias_sesion"] = min(MAX_FOTOS_HOJA,
                                         max(1, datos["copias_sesion"]))

    ok = guardar_impresion()
    return jsonify(ok=ok, impresion=impresion,
                   impresoras=impresoras_disponibles())


@app.route("/admin/impresion/prueba", methods=["POST"])
def admin_impresion_prueba():
    """Manda la foto mas reciente a la impresora, saltandose la cola.

    Sirve para comprobar margenes y color antes de abrir al publico, que
    es justo cuando uno quiere ver una hoja de verdad sin esperar a que
    un invitado pida la suya.
    """
    if not autorizado():
        return jsonify(ok=False), 403

    fotos = sorted(FOTOS_DIR.glob("*.jpg"))
    if not fotos:
        return jsonify(ok=False, error="todavia no hay ninguna foto"), 400

    if impresion.get("manual"):
        # Sin impresora conectada no hay hoja que mandar; se entrega la
        # foto mas reciente para imprimirla a mano y revisar margenes.
        return jsonify(ok=True, manual=True, archivo=fotos[-1].name)

    ok, detalle = enviar_a_impresora({"archivo": fotos[-1].name})
    if ok and impresion.get("hojas", -1) > 0:
        impresion["hojas"] -= 1
        guardar_impresion()
    return jsonify(ok=ok, error=detalle)


def _resumen_bromas():
    with candado:
        show = dict(estado["show"]) if estado["show"] else None
    return {
        "ranuras": [
            {
                "letra": letra,
                "nombre": bromas[letra]["nombre"],
                "tope": bromas[letra]["tope"],
                "piezas": {
                    p: (None if bromas[letra]["piezas"][p] is None else {
                        "tipo": bromas[letra]["piezas"][p]["tipo"],
                        "archivo": bromas[letra]["piezas"][p]["archivo"],
                    })
                    for p in PIEZAS
                },
            }
            for letra in RANURAS
        ],
        "show": show,
    }


@app.route("/admin/marco/previa")
def admin_marco_previa():
    """Ensena como va a quedar la foto, con un cuadro de la camara.

    Sin esto el operador tendria que tomarse una foto de prueba y
    gastar una hoja para saber si el texto cabe.
    """
    if not autorizado():
        return "", 403

    try:
        with candado_camara:
            cuadro = camara.capture_array()
        base = Image.fromarray(cuadro).convert("RGB")
    except Exception:
        # Sin camara disponible, un fondo liso sirve para ver el texto
        base = Image.new("RGB", (1280, 720), (54, 54, 60))

    tmp = FOTOS_DIR / ".previa-marco.jpg"
    base.save(tmp, "JPEG", quality=85)
    try:
        aplicar_marco(tmp)
    except Exception as e:
        return f"no se pudo componer: {e}", 500

    datos = tmp.read_bytes()
    tmp.unlink(missing_ok=True)
    r = make_response(datos)
    r.headers["Content-Type"] = "image/jpeg"
    r.headers["Cache-Control"] = "no-store"
    return r


@app.route("/admin/bromas")
def admin_bromas():
    if not autorizado():
        return jsonify(ok=False), 403
    return jsonify(_resumen_bromas())


@app.route("/admin/bromas/<letra>", methods=["POST"])
def admin_bromas_ajustes(letra):
    """Renombrar la ranura y ponerle (o quitarle) tope."""
    if not autorizado():
        return jsonify(ok=False), 403
    if letra not in RANURAS:
        return jsonify(ok=False, error="esa ranura no existe"), 404

    d = request.get_json(silent=True) or {}
    if "nombre" in d:
        nombre = str(d["nombre"]).strip()[:40]
        bromas[letra]["nombre"] = nombre or f"Broma {letra.upper()}"
    if "tope" in d:
        try:
            bromas[letra]["tope"] = max(0, min(600, int(d["tope"])))
        except (TypeError, ValueError):
            pass

    guardar_bromas()
    return jsonify(ok=True, **_resumen_bromas())


@app.route("/admin/bromas/<letra>/<pieza>/subir", methods=["POST"])
def admin_bromas_subir(letra, pieza):
    """Guarda una pieza.

    Los videos y los GIF animados se guardan tal cual; solo una foto
    fija pasa por PIL, que de paso la encoge y valida que sea una
    imagen de verdad. Pasar un GIF animado por ahi lo dejaria en un
    solo cuadro y la intro no se moveria.
    """
    if not autorizado():
        return jsonify(ok=False), 403
    if letra not in RANURAS or pieza not in PIEZAS:
        return jsonify(ok=False, error="esa ranura no existe"), 404

    f = request.files.get("archivo")
    if f is None:
        return jsonify(ok=False, error="no llego ningun archivo"), 400

    datos = f.read(LIMITE_PIEZA + 1)
    if len(datos) > LIMITE_PIEZA:
        return jsonify(ok=False,
                       error=f"pesa mas de {LIMITE_PIEZA // (1024 * 1024)} MB"), 400
    if not datos:
        return jsonify(ok=False, error="el archivo llego vacio"), 400

    tipo, fmt, ext = que_llego(datos, f.filename or "")
    if tipo is None:
        return jsonify(
            ok=False,
            error="eso no es una imagen ni un video · usa "
                  "gif, png, jpg, mp4 o webm"), 400

    destino = DIR_BROMAS / f"{letra}-{pieza}{ext}"

    if tipo == "video" or ext != ".jpg":
        # Video, o imagen animada: tal cual. Pasar un GIF animado por
        # el normalizador lo dejaria en un solo cuadro.
        destino.write_bytes(datos)
    else:
        try:
            img = Image.open(io.BytesIO(datos)).convert("RGB")
            img.thumbnail((1920, 1920))
            img.save(destino, "JPEG", quality=88)
        except Exception as e:
            return jsonify(ok=False, error=f"no se pudo guardar: {e}"), 400

    # Si antes habia otra pieza con distinta extension, se tira
    for viejo in DIR_BROMAS.glob(f"{letra}-{pieza}.*"):
        if viejo != destino:
            viejo.unlink(missing_ok=True)

    bromas[letra]["piezas"][pieza] = {"archivo": destino.name, "tipo": tipo}
    if not guardar_bromas():
        # El archivo esta en el disco pero el indice no se pudo
        # escribir: al reiniciar la ranura apareceria vacia. Mas vale
        # decirlo ahora que descubrirlo en la fiesta.
        return jsonify(ok=False,
                       error="se subio pero no se pudo guardar el indice · "
                             "revisa el espacio en disco"), 500
    return jsonify(ok=True, tipo=tipo, formato=fmt, **_resumen_bromas())


@app.route("/admin/bromas/<letra>/<pieza>/borrar", methods=["POST"])
def admin_bromas_borrar(letra, pieza):
    if not autorizado():
        return jsonify(ok=False), 403
    if letra not in RANURAS or pieza not in PIEZAS:
        return jsonify(ok=False, error="esa ranura no existe"), 404

    for viejo in DIR_BROMAS.glob(f"{letra}-{pieza}.*"):
        viejo.unlink(missing_ok=True)
    bromas[letra]["piezas"][pieza] = None
    guardar_bromas()

    # Si lo que se borro era justo lo que estaba en pantalla, se quita
    with candado:
        show = estado["show"]
        if show and show["ranura"] == letra and show["pieza"] == pieza:
            estado["show"] = None

    return jsonify(ok=True, **_resumen_bromas())


@app.route("/admin/bromas/<letra>/<pieza>/mostrar", methods=["POST"])
def admin_bromas_mostrar(letra, pieza):
    """Echa una pieza a la pantalla, reemplazando lo que hubiera."""
    if not autorizado():
        return jsonify(ok=False), 403
    if letra not in RANURAS or pieza not in PIEZAS:
        return jsonify(ok=False, error="esa ranura no existe"), 404
    if bromas[letra]["piezas"][pieza] is None:
        return jsonify(ok=False,
                       error=f"primero sube el {pieza} de esta ranura"), 400

    tope = bromas[letra]["tope"]
    ahora = time.time()
    with candado:
        estado["show"] = {
            "ranura": letra, "pieza": pieza, "puesta": int(ahora * 1000),
            "fin": (ahora + tope) if tope else 0,
        }

    return jsonify(ok=True, **_resumen_bromas())


@app.route("/admin/bromas/quitar", methods=["POST"])
def admin_bromas_quitar():
    if not autorizado():
        return jsonify(ok=False), 403
    with candado:
        estado["show"] = None
    return jsonify(ok=True, **_resumen_bromas())


@app.route("/admin/pin", methods=["POST"])
def admin_pin():
    global pin_admin, sesion_admin
    if not autorizado():
        return jsonify(ok=False), 403

    nuevo = str((request.get_json(silent=True) or {}).get("pin", ""))
    if not escribir_pin(nuevo):
        return jsonify(ok=False), 400

    pin_admin = leer_pin()
    sesion_admin = secrets.token_urlsafe(32)  # invalida cookies anteriores
    resp = make_response(jsonify(ok=True))
    return poner_cookie_admin(resp)


# ---------------------------------------------------------------
# Mantenimiento
# ---------------------------------------------------------------

@app.route("/admin/diagnostico")
def admin_diagnostico():
    if not autorizado():
        return jsonify(ok=False), 403
    return jsonify(diagnostico())


@app.route("/admin/apagar", methods=["POST"])
def admin_apagar():
    """Apagado limpio desde el telefono.

    La causa mas comun de que una Pi deje de arrancar es que alguien le
    quito la corriente sin apagarla: la tarjeta se corrompe a medio
    escribir. Un boton a la mano del operador vale mas que cualquier
    advertencia pegada en el chasis.
    """
    if not autorizado():
        return jsonify(ok=False), 403

    try:
        # -n hace que falle de inmediato si sudo fuera a pedir
        # contrasena, en vez de quedarse esperando a nadie.
        r = subprocess.run(["sudo", "-n", "shutdown", "-h", "now"],
                           capture_output=True, text=True, timeout=8)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500

    if r.returncode != 0:
        return jsonify(
            ok=False,
            error="falta el permiso para apagar sin contrasena",
            ayuda=("Corre esto una vez en la Pi:  echo \"$USER ALL=(ALL) "
                   "NOPASSWD: /sbin/shutdown\" | sudo tee "
                   "/etc/sudoers.d/photobooth-apagar")
        ), 500

    return jsonify(ok=True)


@app.route("/admin/fotos/borrar", methods=["POST"])
def admin_borrar_fotos():
    """Vacia la carpeta de fotos y la cola de impresion."""
    if not autorizado():
        return jsonify(ok=False), 403

    borradas = 0
    for f in list(FOTOS_DIR.glob("*.jpg")) + list(ORIGINALES_DIR.glob("*.jpg")):
        try:
            f.unlink()
            borradas += 1
        except Exception:
            pass

    # La cola apunta a archivos que ya no estan; dejarla llena solo
    # serviria para que el operador apruebe fotos fantasma.
    with candado_cola:
        cola.clear()

    with candado:
        soltar_espejo()
        # Las visitas guardan nombres de archivos que acaban de
        # desaparecer: dejarlas serviria para que alguien vea huecos.
        visitas.clear()

    return jsonify(ok=True, borradas=borradas)


# Lo que se lleva y se trae al cambiar de tarjeta. El PIN queda fuera a
# proposito: es lo unico que no conviene que viaje en un archivo que
# alguien puede abrir.
PARTES_CONFIG = ("evento", "calibracion", "impresion")


@app.route("/admin/config/exportar")
def admin_config_exportar():
    if not autorizado():
        return jsonify(ok=False), 403

    bulto = {
        "version": 10,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "evento": evento,
        "calibracion": calibracion,
        "impresion": impresion,
    }
    nombre = "photobooth-" + datetime.now().strftime("%Y%m%d-%H%M") + ".json"
    resp = make_response(json.dumps(bulto, indent=2, ensure_ascii=False))
    resp.headers["Content-Type"] = "application/json; charset=utf-8"
    resp.headers["Content-Disposition"] = f'attachment; filename="{nombre}"'
    return resp


@app.route("/admin/config/importar", methods=["POST"])
def admin_config_importar():
    if not autorizado():
        return jsonify(ok=False), 403

    datos = request.get_json(silent=True)
    if not isinstance(datos, dict) or not any(p in datos for p in PARTES_CONFIG):
        return jsonify(ok=False, error="ese archivo no es una configuracion"), 400

    # Se copian solo las claves conocidas: un archivo editado a mano no
    # deberia poder meter campos que el resto del programa no espera.
    if isinstance(datos.get("evento"), dict):
        for k in EVENTO_FABRICA:
            if k in datos["evento"]:
                evento[k] = datos["evento"][k]
        if not str(evento.get("nombre", "")).strip():
            evento["nombre"] = EVENTO_FABRICA["nombre"]
        guardar_evento()

    if isinstance(datos.get("calibracion"), dict):
        for k in CALIBRACION_FABRICA:
            if k in datos["calibracion"]:
                calibracion[k] = datos["calibracion"][k]
        if calibracion.get("resolucion") not in RESOLUCIONES:
            calibracion["resolucion"] = "media"
        guardar_calibracion()
        aplicar_calibracion()

    if isinstance(datos.get("impresion"), dict):
        for k in IMPRESION_FABRICA:
            if k in datos["impresion"]:
                impresion[k] = datos["impresion"][k]
        guardar_impresion()

    return jsonify(ok=True, evento=evento, calibracion=calibracion,
                   impresion=impresion)


# ---------------------------------------------------------------
# Arranque
# ---------------------------------------------------------------

def servir_en_hilo(puerto):
    """Deja la aplicacion escuchando en un puerto mas, en segundo plano.

    Si no se puede, no se cae nada: el booth sigue funcionando por su
    puerto de siempre y el panel de admin lo reporta. Vale mas un
    espejo que trabaja sin portal cautivo que uno que no arranca.
    """
    try:
        srv = make_server("0.0.0.0", puerto, app, threaded=True)
    except SystemExit:
        # Werkzeug no deja salir el error de bind como excepcion: lo
        # atrapa, imprime el motivo y llama a sys.exit(). Y SystemExit
        # cuelga de BaseException, no de Exception, asi que un
        # "except Exception" lo deja pasar y se lleva el programa
        # entero por delante. Cazarlo aparte es lo que hace que el
        # booth siga arrancando sin el puerto privilegiado.
        return False, f"sin permiso para el puerto {puerto}"
    except Exception as e:
        return False, str(e)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return True, ""


if __name__ == "__main__":
    ok, err = servir_en_hilo(PUERTO_PORTAL)
    portal_activo["ok"] = ok
    portal_activo["error"] = err

    url = base_url()
    print(f"Fotos en:  {FOTOS_DIR}")
    print(f"Espejo:    {url}/")
    print(f"Admin:     {url}/admin")
    print(f"PIN local: {ARCHIVO_PIN} (consultar desde la Pi; no se muestra en el log)")

    if ok:
        print(f"Portal:    puerto {PUERTO_PORTAL} escuchando")
    else:
        print(f"Portal:    sin el puerto {PUERTO_PORTAL} ({err})")
        print("           El booth funciona igual, pero los telefonos no")
        print("           van a abrir la pagina solos al conectarse.")
        print("           Se arregla dandole permiso al servicio:")
        print("             sudo systemctl edit photobooth")
        print("           y agregando, bajo [Service]:")
        print("             AmbientCapabilities=CAP_NET_BIND_SERVICE")

    make_server("0.0.0.0", PUERTO, app, threaded=True).serve_forever()