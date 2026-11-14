
# MIS TRABAJOS Y CALIFICACIONES - FINAL 55 - SUBIR 2 PDFs JUNTOS + SIN ERROR FATAL DE FECHAS - SOLO LEYENDITA EN CUADRITO
# Corre con: py -m streamlit run app_final55.py
import streamlit as st
import pandas as pd
from datetime import date, timedelta
from io import BytesIO
import re
DOCENTE="Mario Alberto Diaz Becerra"
st.set_page_config(page_title="Mis Trabajos y Calificaciones", layout="centered", initial_sidebar_state="collapsed")
DIAS_ES=["lunes","martes","miércoles","jueves","viernes","sábado","domingo"]
MESES_ES=["","enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
OPCIONES_DIAS=["Lunes","Martes","Miércoles","Jueves","Viernes"]
MAPA_DIA={"Lunes":0,"Martes":1,"Miércoles":2,"Jueves":3,"Viernes":4}
def fecha_bonita(f):
    return f"{DIAS_ES[f.weekday()]} {f.day} de {MESES_ES[f.month]} de {f.year}"
def fecha_corta(f):
    return f"{DIAS_ES[f.weekday()]} {f.day} de {MESES_ES[f.month]}"
# CSS PARA TELEFONO - para que quepa todo y no salga grandote
# En la compu se ve igual. En el telefono: letra mas chica, botones grandes para el dedo, columnas una abajo de otra, tablas con scroll.
st.markdown("""<style>
h1, h2, h3 { color: #FFD400 !important; }
/* Quitar el espacio gigante de los lados en telefono */
.block-container { padding-top: 1rem !important; padding-left: 0.8rem !important; padding-right: 0.8rem !important; max-width: 100% !important; }
/* Botones grandes para el dedo, que quepan */
.stButton > button { width: 100% !important; min-height: 48px !important; font-size: 16px !important; white-space: normal !important; height: auto !important; padding: 10px 12px !important; }
.stDownloadButton > button { width: 100% !important; min-height: 48px !important; font-size: 16px !important; white-space: normal !important; height: auto !important; }
/* Que no haga zoom al picar en los cuadritos en el telefono */
input, select, textarea { font-size: 16px !important; }
/* Tablas con scroll a los lados, no aplastadas */
[data-testid="stDataFrame"], [data-testid="stTable"] { overflow-x: auto !important; }
/* Encabezado: foto + titulo */
.encabezado-wrap { display: flex; justify-content: center; margin: 0; padding: 0; }
.encabezado-box { display: flex; align-items: center; gap: 10px; margin: 0; padding: 0; width: fit-content; max-width: 100%; }
.encabezado-foto img { height: 120px !important; width: auto !important; object-fit: contain; display: block; }
.encabezado-titulo { font-size: clamp(22px, 6vw, 44px); font-weight: 800; color: #FFD400; line-height: 1.05; white-space: normal; }
.encabezado-docente { font-size: clamp(14px, 4vw, 22px); color: white; margin-top: 6px; white-space: normal; }
/* SOLO EN TELEFONO (menos de 768px): todo mas chico y columnas una abajo de otra */
@media (max-width: 768px) {
  .block-container { padding-left: 0.6rem !important; padding-right: 0.6rem !important; }
  h1 { font-size: 26px !important; line-height: 1.15 !important; }
  h2 { font-size: 22px !important; line-height: 1.15 !important; }
  h3 { font-size: 19px !important; line-height: 1.2 !important; }
  p, li, div { font-size: 16px !important; }
  /* Columnas de Streamlit: en telefono una abajo de otra, no aplastadas a los lados */
  [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }
  [data-testid="stHorizontalBlock"] > div { flex: 1 1 100% !important; min-width: 0 !important; max-width: 100% !important; }
  .encabezado-box { flex-wrap: wrap; justify-content: center; text-align: center; }
  .encabezado-foto img { height: 90px !important; }
  .encabezado-titulo, .encabezado-docente { text-align: center; }
}
</style>""", unsafe_allow_html=True)

# ===== FOTO EN CÍRCULO, SIN FONDO, CHIQUITA - NO ABARCA ESPACIO =====
def mostrar_foto_fija(datos_foto, tam=130):
    import base64
    if datos_foto is None:
        return
    try:
        b64 = base64.b64encode(datos_foto).decode()
        html = f"""<div style="text-align:center;"><img src="data:image/png;base64,{b64}" style="height:{tam}px;width:auto;object-fit:contain;background:transparent;display:block;margin:auto;"></div>"""
        st.markdown(html, unsafe_allow_html=True)
    except:
        st.image(datos_foto, width=tam)


def mostrar_encabezado():
    """Encabezado fijo: foto GRANDE pegada al titulo, sin hueco, solo Docente: nombre. Sin Artes, sin escuelas."""
    import base64, os
    try:
        b64 = ""
        if st.session_state.get("foto_docente") is not None:
            b64 = base64.b64encode(st.session_state.foto_docente).decode()
        elif os.path.exists("foto_profe.png"):
            with open("foto_profe.png", "rb") as _f:
                st.session_state.foto_docente = _f.read()
            b64 = base64.b64encode(st.session_state.foto_docente).decode()
        img = f'<img src="data:image/png;base64,{b64}">' if b64 else ""
        # CORREGIDO PARA TELEFONO: antes la foto era 220px fija y el titulo 50px con nowrap, por eso en el telefono no cabia y salia grandote.
        # Ahora usa clases del CSS: en compu grande, en telefono chico y con salto de linea, no aplastado.
        html = f"""
<div class="encabezado-wrap">
  <div class="encabezado-box">
    <div class="encabezado-foto" style="flex:0 0 auto;line-height:0;">{img}</div>
    <div style="flex:0 1 auto;text-align:left;line-height:1.1;">
      <div class="encabezado-titulo">⭐ Mis Trabajos y Calificaciones</div>
      <div class="encabezado-docente">Docente: Mario Alberto Diaz Becerra</div>
    </div>
  </div>
</div>
"""
        st.markdown(html, unsafe_allow_html=True)
    except:
        st.markdown("<h1 style='text-align:center;font-size:44px;'>⭐ Mis Trabajos y Calificaciones</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;font-size:22px;'>Docente: Mario Alberto Diaz Becerra</p>", unsafe_allow_html=True)

# ===== LISTAS EN ARCHIVO listas.json - para no volver a subir los PDFs a cada rato =====
# Antes alumnos y capturas solo vivian en la memoria. Si cerrabas el programa, se borraban y tenias que volver a subir los PDFs.
# Ahora cada que cargas PDFs o guardas una captura, se escribe listas.json en la misma carpeta, y al abrir se lee de ahi.
def _guardar_listas_archivo():
    try:
        import json
        with open("listas.json", "w", encoding="utf-8") as _f:
            json.dump({"alumnos": st.session_state.get("alumnos", []), "registros": st.session_state.get("registros", [])}, _f, ensure_ascii=False, indent=2)
    except:
        pass
def _cargar_listas_archivo():
    try:
        import json, os
        if os.path.exists("listas.json"):
            with open("listas.json", "r", encoding="utf-8") as _f:
                _d = json.load(_f)
            _als = _d.get("alumnos", [])
            # Quitar repetidos: mismo nombre + grupo + escuela = uno solo. Si subiste 2 veces el mismo PDF, se duplicaba.
            _vistos = set(); _limpios = []
            for _a in _als:
                _k = (_a.get("Nombre","").strip().lower(), _a.get("Grupo",""), _a.get("Escuela",""))
                if _k not in _vistos:
                    _vistos.add(_k); _limpios.append(_a)
            return _limpios, _d.get("registros", [])
    except:
        pass
    return [], []
if "alumnos" not in st.session_state: st.session_state.alumnos=[]
if "registros" not in st.session_state: st.session_state.registros=[]
# Al abrir, si no hay nada en memoria pero si hay listas.json, cargarlo
if not st.session_state.alumnos and not st.session_state.registros:
    _al, _rg = _cargar_listas_archivo()
    if _al: st.session_state.alumnos = _al
    if _rg: st.session_state.registros = _rg
if "escuela_activa" not in st.session_state: st.session_state.escuela_activa=None
if "alumno_activo" not in st.session_state: st.session_state.alumno_activo=None
if "trimestre" not in st.session_state: st.session_state.trimestre="Trimestre 2"
if "tri_inicio" not in st.session_state: st.session_state.tri_inicio=date(2026,9,1)
if "tri_fin" not in st.session_state: st.session_state.tri_fin=date(2026,11,30)
if "trimestre_cargado" not in st.session_state: st.session_state.trimestre_cargado=False
if "trimestre_cargado_nombre" not in st.session_state: st.session_state.trimestre_cargado_nombre=""
# ===== DIAS GUARDADOS EN ARCHIVO - para que no se borren al cambiar de grupo, regresar, o cerrar y abrir =====
# Antes los dias solo vivian en la memoria de la pagina (session_state). Si Streamlit recargaba, si cambiabas de grupo y regresabas, o si se reiniciaba el Deploy, se borraban y te los volvia a pedir.
# Ahora cada que le picas a Guardar dias, se escriben en dias_clase.json en la misma carpeta, y al abrir se leen de ahi.
def _cargar_dias_archivo():
    try:
        import json, os
        if os.path.exists("dias_clase.json"):
            with open("dias_clase.json", "r", encoding="utf-8") as _f:
                _d = json.load(_f)
            return _d.get("dias_clase", {}), _d.get("dias_confirmados", {})
    except:
        pass
    return {}, {}
def _guardar_dias_archivo():
    try:
        import json
        with open("dias_clase.json", "w", encoding="utf-8") as _f:
            json.dump({"dias_clase": st.session_state.get("dias_clase", {}), "dias_confirmados": st.session_state.get("dias_confirmados", {})}, _f, ensure_ascii=False, indent=2)
    except:
        pass
if "dias_clase" not in st.session_state: st.session_state.dias_clase={}
if "dias_confirmados" not in st.session_state: st.session_state.dias_confirmados={}
# Al abrir, si no hay nada en memoria pero si hay archivo, cargarlo. Si ya hay en memoria, no pisarlo.
if not st.session_state.dias_clase and not st.session_state.dias_confirmados:
    _dc, _dconf = _cargar_dias_archivo()
    if _dc: st.session_state.dias_clase = _dc
    if _dconf: st.session_state.dias_confirmados = _dconf
if "grupo_sel_actual" not in st.session_state: st.session_state.grupo_sel_actual="-- Elige un grupo --"
if "grupo_confirmado" not in st.session_state: st.session_state.grupo_confirmado=None
if "contador_grupo" not in st.session_state: st.session_state.contador_grupo=0
if "foto_docente" not in st.session_state:
    st.session_state.foto_docente=None
    # Cargar foto fija si ya existe foto_profe.jpg en la misma carpeta (la que mandaste)
    try:
        import os
        if os.path.exists("foto_profe.png"):
            with open("foto_profe.png", "rb") as _ff:
                st.session_state.foto_docente=_ff.read()
    except: pass
if "foto_docente_nombre" not in st.session_state: st.session_state.foto_docente_nombre=""
hoy=date.today()
def _ir_a_portada_limpio():
    # Regresar a la portada de adeveras: sin escuela, sin grupo, sin alumno, y sin widgets viejos.
    # NO borra los dias guardados (dias_clase.json) ni los trimestres (trimestres.json): esos SI quedan guardados.
    st.session_state.escuela_activa = None
    st.session_state.grupo_sel_actual = "-- Elige un grupo --"
    st.session_state.grupo_confirmado = None
    st.session_state.alumno_activo = None
    st.session_state.contador_grupo = st.session_state.get("contador_grupo", 0) + 1
    for _k in list(st.session_state.keys()):
        if str(_k).startswith("sel_grupo_") or str(_k).startswith("multiselect_dias_") or str(_k).startswith("sel_grupo"):
            try: del st.session_state[_k]
            except: pass
    st.rerun()
# ===== TRIMESTRES EN ARCHIVO - para que no se quede con el ultimo cargado =====
# Antes el trimestre solo vivia en la memoria. Si recargabas o cambiabas de pagina, se perdia y se quedaba con el ultimo.
# Ahora cada trimestre que configuras se guarda en trimestres.json, y al abrir, el programa busca SOLO en que trimestre cae HOY y pone ese.
def _cargar_trimestres_archivo():
    try:
        import json, os
        if os.path.exists("trimestres.json"):
            with open("trimestres.json", "r", encoding="utf-8") as _f:
                _d = json.load(_f)
            return _d.get("trimestres", [])
    except:
        pass
    return []
def _guardar_trimestre_archivo(nombre_tri, ini, fin):
    try:
        import json
        _lista = _cargar_trimestres_archivo()
        # Si ya existe ese trimestre, actualizar sus fechas. Si no, agregarlo.
        _encontrado = False
        for _it in _lista:
            if _it.get("nombre") == nombre_tri:
                _it["inicio"] = str(ini); _it["fin"] = str(fin); _encontrado = True
        if not _encontrado:
            _lista.append({"nombre": nombre_tri, "inicio": str(ini), "fin": str(fin)})
        with open("trimestres.json", "w", encoding="utf-8") as _f:
            json.dump({"trimestres": _lista}, _f, ensure_ascii=False, indent=2)
        return _lista
    except:
        return []
def _auto_trimestre_hoy():
    # Buscar en que trimestre cae HOY y poner ese, no el ultimo que cargaste.
    try:
        from datetime import date as _date
        _lista = _cargar_trimestres_archivo()
        for _it in _lista:
            try:
                _ini = _date.fromisoformat(_it["inicio"]); _fin = _date.fromisoformat(_it["fin"])
            except:
                continue
            if _ini <= hoy <= _fin:
                st.session_state.trimestre = _it["nombre"]
                st.session_state.tri_inicio = _ini
                st.session_state.tri_fin = _fin
                st.session_state.trimestre_cargado = True
                st.session_state.trimestre_cargado_nombre = _it["nombre"]
                return True
    except:
        pass
    return False
# Al abrir: si hay trimestres guardados, poner el de HOY automaticamente
_auto_trimestre_hoy()
def calcular_riesgo(faltas, no_trab, no_tarea, indis_n):
    puntos=faltas*2 + no_trab*2 + no_tarea*1 + indis_n*1
    if faltas>=4 or no_trab>=4 or puntos>=10: return "ROJO", "REPROBADO - Hay que hablar con sus papas"
    elif faltas>=2 or no_trab>=2 or puntos>=5: return "AMARILLO", "EN PELIGRO - Se puede recuperar si entrega todo"
    else: return "VERDE", "NORMAL - Sin problema, va bien"
def riesgo_de_alumno(nombre, escuela, grupo):
    regs=[r for r in st.session_state.registros if r["Alumno"]==nombre and r.get("Escuela")==escuela and r.get("Grupo")==grupo]
    faltas=len([r for r in regs if "Falta" in r["Estado"]])
    retardos=len([r for r in regs if "Retardo" in r["Estado"]])
    no_trab=len([r for r in regs if "No entregó" in r["Trabajo"]])
    no_tarea=len([r for r in regs if "No entregó" in r["Tarea"]])
    indis_n=len([r for r in regs if r["Indisciplina"]!="Ninguna"])
    nivel, texto = calcular_riesgo(faltas, no_trab, no_tarea, indis_n)
    return nivel, texto, faltas, retardos, no_trab, no_tarea, indis_n, regs
def trimestre_terminado():
    return hoy > st.session_state.tri_fin
def procesar_un_pdf(datos_pdf, escuela, nombre_archivo, grupo_forzado="Elige el grupo a mano - Auto ya no sirve, mezcla las escuelas"):
    # FINAL 55 REHECHO LIMPIO: NO adivina nada. Escuela y grupo son los que TU elegiste arriba.
    # Si dejas el grupo en Auto, NO carga nada y te dice que elijas el grupo a mano. Asi ya no mezcla UNIDAD con TOMAS.
    import fitz
    if grupo_forzado == "Elige el grupo a mano - Auto ya no sirve, mezcla las escuelas" or not grupo_forzado:
        return 0, {"ERROR_GRUPO": "Elige el grupo a mano arriba, no lo dejes en Auto. Asi no se mezcla."}, ["Elige el grupo a mano."]
    grupo_fijo = grupo_forzado[:2].strip().upper()
    doc = fitz.open(stream=datos_pdf, filetype="pdf")
    total = 0
    por_grupo = {}
    textos_debug = []
    for num_pag, pagina in enumerate(doc):
        texto_pag = pagina.get_text()
        if num_pag < 2:
            textos_debug.append(texto_pag[:1200])
        grupo_actual = grupo_fijo
        lineas = texto_pag.split("\n")
        for linea in lineas:
            linea_original = linea.strip()
            linea = linea_original
            if len(linea) < 5:
                continue
            nombre = None
            m_nom = re.match(r"^[\*\s]*(\d{1,2})[\.\-\s]+([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ ]{5,})$", linea, re.I)
            if m_nom:
                nombre = m_nom.group(2).strip()
            else:
                m2 = re.match(r"^[\*\s]*(\d{1,2})[\.\-\s]+([A-ZÁÉÍÓÚÑ ]{5,}?)(?:\s+[A-Z0-9]{10,}|\s+\d{4,}.*)?$", linea, re.I)
                if m2:
                    nombre = m2.group(2).strip()
                else:
                    if re.match(r"^[A-ZÁÉÍÓÚÑ ]+$", linea) and len(linea.split()) >= 2 and len(linea.split()) <= 6:
                        mayus = linea.upper()
                        if not any(p in mayus for p in ["NOMBRE","LISTA","GRUPO","GRADO","ESCUELA","SECUNDARIA","MATERIA","EVALUACION","CALIFICACION","ASISTENCIA","TURNO","CICLO","PROFESOR","DOCENTE","FIRMA","TOTAL","PROMEDIO","ELECTRONICA","ARTES"]):
                            nombre = linea.strip()
            if not nombre:
                continue
            nombre = re.sub(r"\s+\d+$","",nombre).strip()
            nombre = re.sub(r"\s\d+\s*$","",nombre).strip()
            nombre = re.sub(r"\s+"," ",nombre).strip()
            if len(nombre) < 5:
                continue
            if "NOMBRE" in nombre.upper() or "EVALUACION" in nombre.upper():
                continue
            if len(nombre.split()) < 2:
                continue
            materia = "Artes" if (escuela != "ESCUELA SECUNDARIA ESTATAL # 3046" or grupo_actual == "1B") else "Electrónica"
            existe = any(a["Nombre"].lower()==nombre.lower() and a["Grupo"]==grupo_actual and a["Escuela"]==escuela for a in st.session_state.alumnos)
            if existe:
                continue
            st.session_state.alumnos.append({"Nombre":nombre,"Escuela":escuela,"Grupo":grupo_actual,"Materia":materia})
            por_grupo[grupo_actual] = por_grupo.get(grupo_actual,0)+1
            total += 1
    # Segundo pase para hojas donde numero, nombre y letra vienen en renglones separados
    for pagina in doc:
        texto_pag = pagina.get_text()
        grupo_pag = grupo_fijo
        lineas = [l.strip() for l in texto_pag.split("\n")]
        idx = 0
        while idx < len(lineas):
            linea = lineas[idx]
            if re.match(r"^\d{1,2}$", linea):
                if idx+1 < len(lineas):
                    sig = lineas[idx+1].strip()
                    if re.match(r"^[A-ZÁÉÍÓÚÑ ]+$", sig) and len(sig.split())>=2 and len(sig)>5 and "NOMBRE" not in sig.upper():
                        nombre2 = re.sub(r"\s+"," ",sig).strip()
                        materia2 = "Artes" if (escuela!="ESCUELA SECUNDARIA ESTATAL # 3046" or grupo_pag=="1B") else "Electrónica"
                        existe2 = any(a["Nombre"].lower()==nombre2.lower() and a["Grupo"]==grupo_pag and a["Escuela"]==escuela for a in st.session_state.alumnos)
                        if not existe2:
                            st.session_state.alumnos.append({"Nombre":nombre2,"Escuela":escuela,"Grupo":grupo_pag,"Materia":materia2})
                            por_grupo[grupo_pag] = por_grupo.get(grupo_pag,0)+1
                            total += 1
                        if idx+2 < len(lineas) and re.match(r"^[ABC]$", lineas[idx+2].strip()):
                            idx += 3
                        else:
                            idx += 2
                        continue
            idx += 1
    return total, por_grupo, textos_debug


# ===== PDF MODERNO - MEMBRETE LIMPIO, SIN DESCRIPCION DE EMOJIS, TRIMESTRE SOLO NUMERO =====
def _num_trimestre_pdf():
    # Solo el numero: 1, 2 o 3. No "Trimestre 1" otra vez.
    raw = st.session_state.get("trimestre_cargado_nombre") or st.session_state.get("trimestre") or "1"
    for ch in str(raw):
        if ch.isdigit():
            return ch
    return "1"

def _limpiar_valor_pdf(v):
    # Limpia el texto del PDF: NO describe el emoji. "No entrego - Hoja rota" -> "No entrego el trabajo"
    if v is None: return ""
    s = str(v).strip()
    mapa = {
        "😊 Asistió - Cara feliz": "Asistio",
        "😢 Falta - Cara triste": "Falta",
        "⏰ Retardo - Reloj": "Retardo",
        "📄✅ Entregó - Hoja con palomita": "Entrego el trabajo",
        "📄❌ No entregó - Hoja rota": "No entrego el trabajo",
        "📄❓ No trajo material - Signo de pregunta": "No trajo material",
        "✉️ Entregó - Sobre enviado": "Entrego la tarea",
        "✉️❌ No entregó - Sobre tachado": "No entrego la tarea",
        "😡 No trabajó - Cara enojada": "No trabajo",
        "😊 Asistió": "Asistio",
        "😢 Falta": "Falta",
        "⏰ Retardo": "Retardo",
        "📄✅ Entregó": "Entrego el trabajo",
        "📄❌ No entregó": "No entrego el trabajo",
        "📄❓ No trajo material": "No trajo material",
        "✉️ Entregó": "Entrego la tarea",
        "✉️❌ No entregó": "No entrego la tarea",
        "😡 No trabajó": "No trabajo",
        "😡 No trajo material": "No trajo material",
        "😡 Falta de respeto": "Falta de respeto",
        "No se pidió": "No se pidio",
        "No se pidio": "No se pidio",
        "Ninguna": "Ninguna",
    }
    if s in mapa: return mapa[s]
    # Si viene con emoji + guion, quedarse solo con lo de antes del guion, sin describir el emoji
    if " - " in s:
        s = s.split(" - ")[0]
    # Quitar emojis que queden al inicio
    s = s.encode("ascii", "ignore").decode().strip()
    # Normalizar sin acentos para que el PDF no se rompa con fuentes
    s = s.replace("Entregó", "Entrego").replace("entregó", "entrego").replace("No entregó", "No entrego")
    return s if s else "Sin dato"

def _foto_para_pdf():
    # Regresa un Image de ReportLab con la foto del profe, o None si no hay foto
    try:
        from reportlab.platypus import Image as RLImage
        from reportlab.lib.units import inch
        from io import BytesIO as _Bio
        import os as _os
        datos = None
        if st.session_state.get("foto_docente") is not None:
            datos = st.session_state.foto_docente
        elif _os.path.exists("foto_profe.png"):
            with open("foto_profe.png", "rb") as _f: datos = _f.read()
        elif _os.path.exists("foto_profe.jpg"):
            with open("foto_profe.jpg", "rb") as _f: datos = _f.read()
        if not datos: return None
        # CORREGIDO: antes forzaba width=0.85 x height=1.05 y APLASTABA la foto, salias deforme.
        # Ahora se ESCALA guardando la proporcion: cabe en el cuadrito sin aplastarse.
        # Se mide la foto original y se encoge pareja, no se estira de un lado.
        try:
            from PIL import Image as _PIL
            _pil = _PIL.open(_Bio(datos))
            _w0, _h0 = _pil.size
        except:
            _w0, _h0 = 850, 1050
        _max_w = 0.95*inch
        _max_h = 1.25*inch
        _esc = min(_max_w/_w0, _max_h/_h0)
        img = RLImage(_Bio(datos), width=_w0*_esc, height=_h0*_esc)
        img.hAlign = "CENTER"
        return img
    except:
        return None

def _membrete_pdf(elementos, titulo_doc, subtitulo_doc):
    # MEMBRETE ELEGANTE Y CLARO - acorde al programa (negro / amarillo, limpio)
    # Fondo BLANCO, sin cuadro negro. Foto a la izquierda, titulo grande, linea amarilla abajo.
    # Igual para la lista general y para la ficha del alumno.
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    foto = _foto_para_pdf()
    if foto is None:
        foto_cell = Paragraph("<font size=28>⭐</font>", ParagraphStyle("mf", fontSize=28, alignment=TA_CENTER))
    else:
        foto_cell = foto
    # Titulo del programa: negro elegante, una sola linea
    titulo_st = ParagraphStyle("pdf_titulo", fontSize=19, leading=21, textColor=colors.HexColor("#1B2A41"), fontName="Helvetica-Bold", alignment=TA_LEFT)
    # Titulo del documento (FICHA / CONCENTRADO): dorado oscuro, se lee bien sobre blanco, no amarillo chillante
    sub_st = ParagraphStyle("pdf_sub", fontSize=11, leading=13, textColor=colors.HexColor("#B89600"), fontName="Helvetica-Bold", alignment=TA_LEFT)
    # Docente: gris oscuro, discreto
    docente_st = ParagraphStyle("pdf_doc", fontSize=10, leading=13, textColor=colors.HexColor("#444444"), fontName="Helvetica", alignment=TA_LEFT)
    # Subtitulo (escuela | grupo | trimestre | fecha): gris, chiquito, sin describir emojis
    detalle_st = ParagraphStyle("pdf_det", fontSize=9, leading=11, textColor=colors.HexColor("#666666"), fontName="Helvetica", alignment=TA_LEFT)
    izq = [Paragraph("MIS TRABAJOS Y CALIFICACIONES", titulo_st), Paragraph(titulo_doc, sub_st), Paragraph(f"Docente: {DOCENTE}", docente_st), Paragraph(subtitulo_doc, detalle_st)]
    tabla_textos = Table([[izq[0]], [izq[1]], [izq[2]], [izq[3]]], colWidths=[5.8*inch])
    tabla_textos.setStyle(TableStyle([("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),("TOPPADDING",(0,0),(-1,-1),1),("BOTTOMPADDING",(0,0),(-1,-1),1)]))
    tabla_membrete = Table([[foto_cell, tabla_textos]], colWidths=[1.1*inch, 5.8*inch])
    tabla_membrete.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), colors.white),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
        ("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10),
        # Linea amarilla del programa abajo del membrete, lo unico de color fuerte
        ("LINEBELOW",(0,0),(-1,0), 3, colors.HexColor("#FFD400")),
    ]))
    elementos.append(tabla_membrete)
    elementos.append(Spacer(1, 4))
    # Barra de info: Escuela | Grupo | Trimestre solo numero | Fecha
    info_st = ParagraphStyle("pdf_info", fontSize=9, leading=12, textColor=colors.HexColor("#1B2A41"), alignment=TA_CENTER)
    elementos.append(Paragraph(subtitulo_doc, info_st))
    elementos.append(Spacer(1, 10))

def generar_pdf_ficha_alumno(nombre_al, escuela, grupo):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    buffer=BytesIO()
    doc=SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch, leftMargin=0.6*inch, rightMargin=0.6*inch, title=f"Ficha {nombre_al}", author=DOCENTE)
    styles=getSampleStyleSheet()
    normal=ParagraphStyle("normal", parent=styles["Normal"], fontSize=10, leading=13, textColor=colors.HexColor("#1B2A41"))
    h2=ParagraphStyle("h2", parent=styles["Heading2"], fontSize=13, leading=15, textColor=colors.HexColor("#1B2A41"), fontName="Helvetica-Bold", spaceBefore=14, spaceAfter=6, borderPadding=(0,0,4))
    cell=ParagraphStyle("cell", parent=normal, fontSize=9, leading=11)
    cell_c=ParagraphStyle("cell_c", parent=cell, alignment=TA_CENTER)
    head=ParagraphStyle("head", parent=cell, fontSize=9, leading=11, textColor=colors.white, fontName="Helvetica-Bold", alignment=TA_CENTER)
    nivel, texto, faltas, retardos, no_trab, no_tarea, indis_n, regs_al = riesgo_de_alumno(nombre_al, escuela, grupo)
    num_tri = _num_trimestre_pdf()
    elementos=[]
    _membrete_pdf(elementos, "FICHA PERSONAL DEL ALUMNO", f"{escuela} &nbsp;|&nbsp; Grupo: {grupo} &nbsp;|&nbsp; Trimestre: {num_tri} &nbsp;|&nbsp; Fecha: {fecha_bonita(hoy)}")
    # Nombre del alumno grande, sin recuadro feo
    elementos.append(Paragraph(f"<b>{nombre_al}</b>", ParagraphStyle("nom", parent=normal, fontSize=17, leading=19, alignment=TA_CENTER, textColor=colors.HexColor("#1B2A41"))))
    if st.session_state.trimestre_cargado:
        elementos.append(Paragraph(f"Del {fecha_bonita(st.session_state.tri_inicio)} al {fecha_bonita(st.session_state.tri_fin)}", ParagraphStyle("per", parent=normal, fontSize=9, alignment=TA_CENTER, textColor=colors.HexColor("#64748B"))))
    elementos.append(Spacer(1, 10))
    # Riesgo: pastilla limpia
    color_riesgo = "#0E9F6E" if nivel=="VERDE" else "#F59E0B" if nivel=="AMARILLO" else "#EF4444"
    txt_riesgo = {"VERDE": "VERDE - Normal, va bien", "AMARILLO": "AMARILLO - Hay que estar al pendiente", "ROJO": "ROJO - Necesita apoyo"}.get(nivel, f"{nivel} - {texto}")
    pill = Table([[Paragraph(f"<b>{txt_riesgo}</b>", ParagraphStyle("pill", parent=normal, fontSize=11, alignment=TA_CENTER, textColor=colors.white))]], colWidths=[7.3*inch])
    pill.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1), colors.HexColor(color_riesgo)),("ROUNDEDCORNERS",[6,6,6,6]),("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
    elementos.append(pill)
    elementos.append(Spacer(1, 12))
    # Resumen: encabezado azul marino, texto blanco legible, nada de negro con amarillo
    datos=[[Paragraph("Faltas", head), Paragraph("Retardos", head), Paragraph("No entrego trabajo", head), Paragraph("No entrego tarea", head), Paragraph("Indisciplinas", head), Paragraph("Total capturas", head)],
           [Paragraph(str(faltas), cell_c), Paragraph(str(retardos), cell_c), Paragraph(str(no_trab), cell_c), Paragraph(str(no_tarea), cell_c), Paragraph(str(indis_n), cell_c), Paragraph(str(len(regs_al)), cell_c)]]
    t=Table(datos, colWidths=[0.95*inch,0.95*inch,1.45*inch,1.45*inch,1.15*inch,1.35*inch])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0), colors.HexColor("#1B2A41")),("BACKGROUND",(0,1),(-1,1), colors.HexColor("#F1F5F9")),("GRID",(0,0),(-1,-1),0.5, colors.HexColor("#CBD5E1")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)]))
    elementos.append(t)
    elementos.append(Paragraph("Historial completo", h2))
    if not regs_al:
        elementos.append(Paragraph("Todavia no tiene capturas.", normal))
    else:
        regs_ord=sorted(regs_al, key=lambda x: x.get("Fecha",""))
        filas=[[Paragraph("<b>Fecha</b>", head), Paragraph("<b>Asistencia</b>", head), Paragraph("<b>Trabajo</b>", head), Paragraph("<b>Tarea</b>", head), Paragraph("<b>Indisciplina</b>", head), Paragraph("<b>Anotacion</b>", head)]]
        for r in regs_ord:
            fb=r.get("FechaBonita") or r.get("Fecha","")
            if not r.get("FechaBonita") and r.get("Fecha"):
                try: y,m,d=map(int, r["Fecha"].split("-")); fb=fecha_bonita(date(y,m,d))
                except: fb=r["Fecha"]
            # LIMPIO: solo "No entrego el trabajo", no "Hoja rota"
            filas.append([Paragraph(fb, cell), Paragraph(_limpiar_valor_pdf(r.get("Estado","")), cell_c), Paragraph(_limpiar_valor_pdf(r.get("Trabajo","")), cell_c), Paragraph(_limpiar_valor_pdf(r.get("Tarea","")), cell_c), Paragraph(_limpiar_valor_pdf(r.get("Indisciplina","")), cell_c), Paragraph(r.get("Anotacion","") or "", cell)])
        t2=Table(filas, colWidths=[1.15*inch,1.0*inch,1.25*inch,1.15*inch,1.15*inch,1.6*inch], repeatRows=1)
        estilo=[("BACKGROUND",(0,0),(-1,0), colors.HexColor("#1B2A41")),("GRID",(0,0),(-1,-1),0.5, colors.HexColor("#CBD5E1")),("VALIGN",(0,0),(-1,-1),"TOP"),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6)]
        for i in range(1, len(filas)):
            if i % 2 == 0: estilo.append(("BACKGROUND",(0,i),(-1,i), colors.HexColor("#F8FAFC")))
        t2.setStyle(TableStyle(estilo))
        elementos.append(t2)
    elementos.append(Spacer(1, 30))
    firmas=Table([[Paragraph("___________________________", ParagraphStyle("f", parent=normal, alignment=TA_CENTER)), Paragraph("___________________________", ParagraphStyle("f2", parent=normal, alignment=TA_CENTER))],[Paragraph("Firma del docente", ParagraphStyle("f3", parent=normal, alignment=TA_CENTER, fontSize=9, textColor=colors.HexColor("#64748B"))), Paragraph("Firma del padre / madre", ParagraphStyle("f4", parent=normal, alignment=TA_CENTER, fontSize=9, textColor=colors.HexColor("#64748B")))]], colWidths=[3.65*inch, 3.65*inch])
    firmas.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP")]))
    elementos.append(firmas)
    doc.build(elementos); buffer.seek(0); return buffer

def generar_pdf_general_grupo(escuela, grupo, alumnos_grupo, dias_clase_grupo):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    buffer=BytesIO()
    doc=SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch, leftMargin=0.6*inch, rightMargin=0.6*inch, title=f"Concentrado {grupo}", author=DOCENTE)
    styles=getSampleStyleSheet()
    normal=ParagraphStyle("normal", parent=styles["Normal"], fontSize=10, leading=13, textColor=colors.HexColor("#1B2A41"))
    h2=ParagraphStyle("h2", parent=styles["Heading2"], fontSize=13, leading=15, textColor=colors.HexColor("#1B2A41"), fontName="Helvetica-Bold", spaceBefore=14, spaceAfter=6)
    small=ParagraphStyle("small", parent=styles["Normal"], fontSize=8.5, leading=10.5, textColor=colors.HexColor("#1B2A41"))
    cell=ParagraphStyle("cell", parent=normal, fontSize=9, leading=11)
    cell_c=ParagraphStyle("cell_c", parent=cell, alignment=TA_CENTER)
    head=ParagraphStyle("head", parent=cell, fontSize=9, leading=11, textColor=colors.white, fontName="Helvetica-Bold", alignment=TA_CENTER)
    head_l=ParagraphStyle("head_l", parent=head, alignment=TA_LEFT)
    num_tri = _num_trimestre_pdf()
    dias_txt = ", ".join([DIAS_ES[d] for d in dias_clase_grupo]) if dias_clase_grupo else ""
    elementos=[]
    _membrete_pdf(elementos, f"CONCENTRADO GENERAL DEL GRUPO {grupo}", f"{escuela} &nbsp;|&nbsp; Grupo: {grupo} &nbsp;|&nbsp; Trimestre: {num_tri} &nbsp;|&nbsp; Fecha: {fecha_bonita(hoy)} &nbsp;|&nbsp; Dias: {dias_txt}")
    if st.session_state.trimestre_cargado:
        elementos.append(Paragraph(f"Del {fecha_bonita(st.session_state.tri_inicio)} al {fecha_bonita(st.session_state.tri_fin)}", ParagraphStyle("per", parent=normal, fontSize=9, alignment=TA_CENTER, textColor=colors.HexColor("#64748B"))))
        elementos.append(Spacer(1, 8))
    amarillos=[]; rojos=[]; verdes=[]; total_faltas=0; total_no_trab=0
    for al in alumnos_grupo:
        nivel, texto, faltas, retardos, no_trab, no_tarea, indis_n, regs = riesgo_de_alumno(al["Nombre"], escuela, grupo)
        total_faltas+=faltas; total_no_trab+=no_trab
        if nivel=="AMARILLO": amarillos.append(al["Nombre"])
        elif nivel=="ROJO": rojos.append(al["Nombre"])
        else: verdes.append(al["Nombre"])
    # Resumen: encabezado azul marino legible, NO negro con amarillo
    datos=[[Paragraph("Total alumnos", head), Paragraph("En verde", head), Paragraph("En amarillo", head), Paragraph("En rojo", head), Paragraph("Total faltas", head), Paragraph("Total sin trabajo", head)],
           [Paragraph(str(len(alumnos_grupo)), cell_c), Paragraph(str(len(verdes)), cell_c), Paragraph(str(len(amarillos)), cell_c), Paragraph(str(len(rojos)), cell_c), Paragraph(str(total_faltas), cell_c), Paragraph(str(total_no_trab), cell_c)]]
    t=Table(datos, colWidths=[1.05*inch,0.95*inch,1.25*inch,0.95*inch,1.05*inch,1.45*inch])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0), colors.HexColor("#1B2A41")),("BACKGROUND",(0,1),(-1,1), colors.HexColor("#F1F5F9")),("GRID",(0,0),(-1,-1),0.5, colors.HexColor("#CBD5E1")),("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)]))
    elementos.append(t)
    elementos.append(Paragraph("Lista general - Todos los alumnos", h2))
    # Encabezados CLAROS: Alumno, Riesgo, Faltas, Sin trabajo, Sin tarea, Capturas - nada en negro
    filas=[[Paragraph("<b>#</b>", head), Paragraph("<b>Alumno</b>", head_l), Paragraph("<b>Riesgo</b>", head), Paragraph("<b>Faltas</b>", head), Paragraph("<b>Sin trabajo</b>", head), Paragraph("<b>Sin tarea</b>", head), Paragraph("<b>Capturas</b>", head)]]
    for idx, al in enumerate(alumnos_grupo):
        nivel, texto, faltas, retardos, no_trab, no_tarea, indis_n, regs = riesgo_de_alumno(al["Nombre"], escuela, grupo)
        # Pastilla de riesgo con texto legible
        color_r = "#0E9F6E" if nivel=="VERDE" else "#F59E0B" if nivel=="AMARILLO" else "#EF4444"
        riesgo_txt = f'<font color="{color_r}"><b>{nivel}</b></font>'
        filas.append([Paragraph(str(idx+1), cell_c), Paragraph(al["Nombre"], cell), Paragraph(riesgo_txt, cell_c), Paragraph(str(faltas), cell_c), Paragraph(str(no_trab), cell_c), Paragraph(str(no_tarea), cell_c), Paragraph(str(len(regs)), cell_c)])
    t2=Table(filas, colWidths=[0.35*inch,2.85*inch,0.85*inch,0.65*inch,0.95*inch,0.85*inch,0.8*inch], repeatRows=1)
    estilo=[("BACKGROUND",(0,0),(-1,0), colors.HexColor("#1B2A41")),("GRID",(0,0),(-1,-1),0.5, colors.HexColor("#CBD5E1")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6)]
    for i in range(1, len(filas)):
        if i % 2 == 0: estilo.append(("BACKGROUND",(0,i),(-1,i), colors.HexColor("#F8FAFC")))
    t2.setStyle(TableStyle(estilo))
    elementos.append(t2)
    elementos.append(Paragraph("Concentrado AMARILLO", h2))
    if not amarillos: elementos.append(Paragraph("No hay alumnos en amarillo.", normal))
    else:
        for i,n in enumerate(amarillos): elementos.append(Paragraph(f"{i+1}. {n}", normal))
    elementos.append(Paragraph("Concentrado ROJO", h2))
    if not rojos: elementos.append(Paragraph("No hay alumnos en rojo.", normal))
    else:
        for i,n in enumerate(rojos): elementos.append(Paragraph(f"{i+1}. {n}", normal))
    elementos.append(Spacer(1, 24))
    elementos.append(Paragraph("___________________________", ParagraphStyle("f", parent=normal, alignment=TA_CENTER)))
    elementos.append(Paragraph("Firma del docente", ParagraphStyle("f2", parent=normal, alignment=TA_CENTER, fontSize=9, textColor=colors.HexColor("#64748B"))))
    doc.build(elementos); buffer.seek(0); return buffer

# PORTADA
if st.session_state.escuela_activa is None:
    # ===== ENCABEZADO FIJO - YA SALE SOLA LA FOTO, NO HAY QUE SUBIRLA =====
    # Foto a la izquierda, cuerpo completo sin círculo para que no te corte la cabeza
    # Título grande a lo largo en un solo renglón al centro, y abajo nombre + grupos
    mostrar_encabezado()
    st.divider()
    with st.expander("⚙️ Configurar trimestre - Pícale aquí para cambiarlo", expanded=False):
        st.subheader("📅 1. Calendario - Primero tienes que CARGAR el trimestre")
        c1,c2,c3=st.columns(3)
        with c1: tri_sel_temp=st.selectbox("¿Qué trimestre es?", ["Trimestre 1","Trimestre 2","Trimestre 3"], index=["Trimestre 1","Trimestre 2","Trimestre 3"].index(st.session_state.trimestre), key="tri_sel_portada18")
        with c2: tri_ini_temp=st.date_input("¿Desde cuándo inicia?", value=st.session_state.tri_inicio, key="tri_ini_portada18")
        with c3: tri_fin_temp=st.date_input("¿Cuándo termina?", value=st.session_state.tri_fin, key="tri_fin_portada18")
        st.write("")
        if st.button("📅 CARGAR ESTE TRIMESTRE", use_container_width=True):
            # Si pones 14 nov al 8 mar, el 8 mar es del año que sigue (2027), no del mismo año
            # Si no, quedaría fin (8 mar 2026) antes que inicio (14 nov 2026) y por eso se tronaba
            fin_corregido = tri_fin_temp
            if fin_corregido < tri_ini_temp:
                try:
                    fin_corregido = fin_corregido.replace(year=fin_corregido.year+1)
                except: pass
                st.info(f"ℹ️ Como tu trimestre cruza de año, lo guardé como del {fecha_bonita(tri_ini_temp)} al {fecha_bonita(fin_corregido)}. Del 14 de noviembre al 8 de marzo del año que sigue.")
            st.session_state.trimestre=tri_sel_temp; st.session_state.tri_inicio=tri_ini_temp; st.session_state.tri_fin=fin_corregido
            st.session_state.trimestre_cargado=True; st.session_state.trimestre_cargado_nombre=tri_sel_temp; _guardar_trimestre_archivo(tri_sel_temp, tri_ini_temp, fin_corregido); st.session_state.ultimo_tri_guardado=f"{tri_sel_temp} - Del {fecha_bonita(tri_ini_temp)} al {fecha_bonita(fin_corregido)}"; st.rerun()
        st.write("")
        if st.session_state.get("ultimo_tri_guardado"): st.success(f"✅ GUARDADO: {st.session_state.ultimo_tri_guardado}")
        # LISTA DE LOS 3: para que veas que SI se guardaron los otros dos, no solo el de hoy
        _todos_tri = _cargar_trimestres_archivo()
        if _todos_tri:
            st.write("**Trimestres que ya tienes guardados:**")
            for _it in _todos_tri:
                try:
                    from datetime import date as _d2
                    _ini2 = _d2.fromisoformat(_it["inicio"]); _fin2 = _d2.fromisoformat(_it["fin"])
                    _es_hoy = " ← **ESTE ES EL DE HOY, con este capturas**" if _ini2 <= hoy <= _fin2 else ""
                    st.write(f"- **{_it['nombre']}**: del {fecha_bonita(_ini2)} al {fecha_bonita(_fin2)}{_es_hoy}")
                except:
                    st.write(f"- **{_it['nombre']}**")
            st.write("Para guardar otro: elige arriba qué trimestre es, pon sus fechas, y pícale a **CARGAR ESTE TRIMESTRE**. Se agrega a la lista, no borra los otros.")
        if st.session_state.trimestre_cargado:
            if trimestre_terminado(): st.info(f"ℹ️ Este trimestre ya terminó el {fecha_bonita(st.session_state.tri_fin)}. Carga el siguiente cuando quieras.")
            else: st.success(f"✅ TRIMESTRE CARGADO: {st.session_state.trimestre_cargado_nombre} - Del {fecha_bonita(st.session_state.tri_inicio)} al {fecha_bonita(st.session_state.tri_fin)}")
        else: st.warning("⚠️ Todavía NO has cargado ningún trimestre.")
        st.divider()
    # ===== RESPALDO - para que telefono y compu vean lo mismo en la nube =====
    # En la nube, listas.json vive en el servidor. Telefono y compu abren LA MISMA url, por eso ven lo mismo.
    # Si algun dia la nube se reinicia, con este respaldo lo restauras.
    with st.expander("💾 Respaldo - Descargar / Subir tus listas (para la nube)", expanded=False):
        st.write("**En el telefono:** despues de capturar, picale a **Descargar respaldo** y guardalo. **En la compu:** picale a **Subir respaldo** y eliges ese archivo. Asi quedan igual.")
        st.write("")
        try:
            import json as _json, os as _os
            _todo = {"alumnos": st.session_state.get("alumnos", []), "registros": st.session_state.get("registros", []), "dias_clase": st.session_state.get("dias_clase", {}), "dias_confirmados": st.session_state.get("dias_confirmados", {})}
            # Trimestres del archivo
            try:
                with open("trimestres.json", "r", encoding="utf-8") as _f: _todo["trimestres"] = _json.load(_f)
            except: _todo["trimestres"] = {"trimestres": []}
            _bytes = _json.dumps(_todo, ensure_ascii=False, indent=2).encode("utf-8")
            st.download_button("⬇️ Descargar respaldo de TODO (listas + dias + trimestres)", data=_bytes, file_name="respaldo_control_escolar.json", mime="application/json", use_container_width=True)
        except Exception as _e:
            st.write(f"No se pudo preparar el respaldo: {_e}")
        st.write("")
        _sub = st.file_uploader("⬆️ Subir respaldo para restaurar todo", type=["json"], key="subir_respaldo_47")
        if _sub is not None:
            try:
                import json as _json2
                _d = _json2.loads(_sub.getvalue().decode("utf-8"))
                if "alumnos" in _d: st.session_state.alumnos = _d["alumnos"]
                if "registros" in _d: st.session_state.registros = _d["registros"]
                if "dias_clase" in _d: st.session_state.dias_clase = _d["dias_clase"]
                if "dias_confirmados" in _d: st.session_state.dias_confirmados = _d["dias_confirmados"]
                if "trimestres" in _d:
                    with open("trimestres.json", "w", encoding="utf-8") as _f: _json2.dump(_d["trimestres"], _f, ensure_ascii=False, indent=2)
                _guardar_listas_archivo(); _guardar_dias_archivo()
                st.success("✅ Restaurado. Ya quedaron igual telefono y compu.")
                st.rerun()
            except Exception as _e:
                st.error(f"No se pudo restaurar: {_e}")
    st.subheader("Elige una escuela para entrar:")
    st.write("")
    if st.button("🏫 Tomas Gameros # 2131  •  Primaria  •  Artes", use_container_width=True):
        st.session_state.escuela_activa="TOMAS GAMEROS # 2131"; st.session_state.grupo_sel_actual="-- Elige un grupo --"; st.session_state.grupo_confirmado=None; st.session_state.alumno_activo=None; st.rerun()
    st.write("")
    if st.button("🏫 Unidad Proletaria # 2294  •  Primaria  •  Artes", use_container_width=True):
        st.session_state.escuela_activa="UNIDAD PROLETARIA # 2294"; st.session_state.grupo_sel_actual="-- Elige un grupo --"; st.session_state.grupo_confirmado=None; st.session_state.alumno_activo=None; st.rerun()
    st.write("")
    if st.button("🏫 Escuela Secundaria Estatal # 3046  •  Secundaria  •  1B Artes / 3A y 3B Electrónica", use_container_width=True):
        st.session_state.escuela_activa="ESCUELA SECUNDARIA ESTATAL # 3046"; st.session_state.grupo_sel_actual="-- Elige un grupo --"; st.session_state.grupo_confirmado=None; st.session_state.alumno_activo=None; st.rerun()
    st.stop()

escuela=st.session_state.escuela_activa

# ===== MODO LIMPIO: si ya esta todo cargado, esconder configuracion =====
# Si ya elegiste grupo y ya elegiste dias, ya no necesitas ver PDFs, ni elegir grupo, ni elegir dias.
# Solo se muestra el titulo de la pagina en la que estas + la lista del grupo.
_alumnos_esc_pre = [a for a in st.session_state.alumnos if a["Escuela"]==escuela]
_grupos_pre = sorted(set(a["Grupo"] for a in _alumnos_esc_pre))
_grupo_pre = st.session_state.get("grupo_confirmado") or "-- Elige un grupo --"
# CORREGIDO: antes modo_lista usaba grupo_sel_actual, que es lo que el selector pone solito al elegir.
# Por eso en cuanto elegias 3C, como ya tenia dias guardados, te aventaba a la lista sin dejarte picar a Portada.
# Ahora solo entra a la lista si TU le picaste a Entrar o a Guardar dias (grupo_confirmado), no solo por elegir en el selector.
_llave_dias_pre = f"{escuela}|{_grupo_pre}"
_dias_pre = st.session_state.dias_clase.get(_llave_dias_pre, [])
# Hay dias reales si la llave existe (aunque sea [0] = sin dia, lo consideramos configurado solo si ya se guardo algo distinto al default vacio)
_tiene_dias = bool(st.session_state.get("dias_confirmados", {}).get(_llave_dias_pre, False))  # Solo si TU le picaste a Guardar dias. Antes cualquier llave [0] falsa lo activaba y te metia al grupo sin dejarte cambiar.
modo_lista = (_grupo_pre != "-- Elige un grupo --" and _grupo_pre in _grupos_pre and _tiene_dias and st.session_state.get("alumno_activo") is None)
if modo_lista:
    # Variables que la lista de abajo necesita, aunque nos saltemos la configuracion
    grupo_sel = _grupo_pre
    alumnos_esc = _alumnos_esc_pre
    dias_clase_grupo = _dias_pre if _dias_pre else [0]
    nombres_dias_grupo = [DIAS_ES[d] for d in dias_clase_grupo]
    llave_dias = _llave_dias_pre
# ===== ENCABEZADO FIJO ADENTRO - MISMO QUE EN PORTADA =====
mostrar_encabezado()
if not modo_lista:
    if st.session_state.trimestre_cargado and not trimestre_terminado(): st.success(f"✅ {st.session_state.trimestre_cargado_nombre} CARGADO - Del {fecha_bonita(st.session_state.tri_inicio)} al {fecha_bonita(st.session_state.tri_fin)} - Hoy: {fecha_bonita(hoy)}")
    elif st.session_state.trimestre_cargado and trimestre_terminado(): st.info(f"ℹ️ {st.session_state.trimestre_cargado_nombre} ya terminó el {fecha_bonita(st.session_state.tri_fin)}. Carga el siguiente cuando quieras.")
    else: st.warning("⚠️ No has cargado trimestre. Regresa a la portada y pícale a CARGAR ESTE TRIMESTRE.")
    st.header(f"🏫 {escuela}")
    st.write("")
    if st.button("⬅️ Regresar a la portada"):
        _ir_a_portada_limpio()
    st.write("")
    with st.expander("📅 Cambiar / Cargar otro trimestre"):
        st.write("Pon las fechas nuevas y pícale a Cargar.")
        st.write("")
        c1,c2,c3=st.columns(3)
        with c1: tri_sel2=st.selectbox("¿Qué trimestre es?", ["Trimestre 1","Trimestre 2","Trimestre 3"], index=["Trimestre 1","Trimestre 2","Trimestre 3"].index(st.session_state.trimestre), key="tri_sel_esc18")
        with c2: tri_ini2=st.date_input("¿Desde cuándo inicia?", value=st.session_state.tri_inicio, key="tri_ini_esc18")
        with c3: tri_fin2=st.date_input("¿Cuándo termina?", value=st.session_state.tri_fin, key="tri_fin_esc18")
        st.write("")
        if st.button("📅 CARGAR ESTE TRIMESTRE"):
            fin2 = tri_fin2
            if fin2 < tri_ini2:
                try: fin2 = fin2.replace(year=fin2.year+1)
                except: pass
                st.info(f"ℹ️ Como cruza de año, lo guardé hasta el {fecha_bonita(fin2)} del año que sigue.")
            st.session_state.trimestre=tri_sel2; st.session_state.tri_inicio=tri_ini2; st.session_state.tri_fin=fin2
            st.session_state.trimestre_cargado=True; st.session_state.trimestre_cargado_nombre=tri_sel2; _guardar_trimestre_archivo(tri_sel2, tri_ini2, fin2); st.session_state.ultimo_tri_guardado=f"{tri_sel2} - Del {fecha_bonita(tri_ini2)} al {fecha_bonita(fin2)}"; st.rerun()
        st.write("")
        if st.session_state.get("ultimo_tri_guardado"): st.success(f"✅ GUARDADO: {st.session_state.ultimo_tri_guardado}")
        _todos2 = _cargar_trimestres_archivo()
        if _todos2:
            st.write("**Trimestres guardados:**")
            for _it in _todos2:
                try:
                    from datetime import date as _d3
                    _a = _d3.fromisoformat(_it["inicio"]); _b = _d3.fromisoformat(_it["fin"])
                    _eh = " ← **ESTE ES EL DE HOY**" if _a <= hoy <= _b else ""
                    st.write(f"- **{_it['nombre']}**: del {fecha_bonita(_a)} al {fecha_bonita(_b)}{_eh}")
                except: st.write(f"- **{_it['nombre']}**")
    st.divider()
    # ===== UPLOAD FINAL 55 - TU LE DICES DE QUE GRUPO ES CADA PDF =====
    if _alumnos_esc_pre:
        with st.expander("📄 Cargar / cambiar PDFs - Ya tienes alumnos cargados, pícale aquí solo si quieres cambiarlos", expanded=False):
            st.subheader("📄 1. Cargar los PDFs de ESTA escuela")
            if escuela=="ESCUELA SECUNDARIA ESTATAL # 3046":
                st.write("En secundaria son **2 archivos**: uno de **1B Artes** y otro de **3A y 3B Electrónica**.")
                st.write("**AHORA TU LE DICES DE QUE GRUPO ES CADA PDF**, para que no tenga que adivinarlo y no te salga 0 alumnos.")
                st.write("Si el PDF de Electrónica trae 3A y 3B juntos, elige '3A y 3B juntos'. Si trae solo 3A, elige '3A'.")
            else:
                st.write(f"Aquí subes el PDF de **{escuela}**.")
            st.write("")
            st.warning(f"⚠️ Estás cargando en: **{escuela}**. Si este PDF es de OTRA escuela, cámbiala aquí, si no te la mete en la equivocada.")
            escuela_pdf = st.selectbox("¿De qué escuela es este PDF? Tú lo eliges, ya no adivina", ["TOMAS GAMEROS # 2131", "UNIDAD PROLETARIA # 2294", "ESCUELA SECUNDARIA ESTATAL # 3046"], index=["TOMAS GAMEROS # 2131", "UNIDAD PROLETARIA # 2294", "ESCUELA SECUNDARIA ESTATAL # 3046"].index(escuela) if escuela in ["TOMAS GAMEROS # 2131", "UNIDAD PROLETARIA # 2294", "ESCUELA SECUNDARIA ESTATAL # 3046"] else 0, key=f"escuela_pdf_{escuela}_51")
            # Contador para poder dejar el Upload en blanco cuando le picas a Quitar
            if f"contador_upload_{escuela}" not in st.session_state:
                st.session_state[f"contador_upload_{escuela}"] = 0
            if f"pdfs_quitados_{escuela}" not in st.session_state:
                st.session_state[f"pdfs_quitados_{escuela}"] = []
            archivos_pdf=st.file_uploader("Sube aquí tus PDFs - Puedes subir 1 o 2 juntos", type=["pdf"], accept_multiple_files=True, key=f"pdfs_{escuela}_{st.session_state[f'contador_upload_{escuela}']}")
            st.write("")
            if archivos_pdf:
                # Quitar los que ya quitaste antes
                archivos_pdf = [f for f in archivos_pdf if f.name not in st.session_state[f"pdfs_quitados_{escuela}"]]
                st.write(f"Archivos que elegiste: **{len(archivos_pdf)}**")
                # BOTON PARA DEJAR TODO EN BLANCO
                if st.button("🗑️ Quitar todos los PDFs y dejar en blanco", key=f"btn_quitar_todos_{escuela}_53"):
                    st.session_state[f"pdfs_quitados_{escuela}"] = []
                    st.session_state[f"contador_upload_{escuela}"] = st.session_state[f"contador_upload_{escuela}"] + 1
                    st.rerun()
                # BOTON POR CADA ARCHIVO PARA ELIMINARLO EN ESE MOMENTO
                for _f_q in list(archivos_pdf):
                    col_q1, col_q2 = st.columns([3, 1])
                    with col_q1:
                        st.write(f"📄 {_f_q.name}")
                    with col_q2:
                        if st.button(f"🗑️ Quitar este PDF y dejar en blanco", key=f"btn_quitar_{escuela}_{_f_q.name}_53"):
                            # Quitar DE VERDAD: borrar de quitados y cambiar la llave del Upload para que quede en blanco
                            st.session_state[f"pdfs_quitados_{escuela}"] = [_n for _n in st.session_state.get(f"pdfs_quitados_{escuela}", [])]
                            st.session_state[f"pdfs_quitados_{escuela}"].append(_f_q.name)
                            # Si ya quitaste todos los que habia, cambiar la llave para que el Upload quede vacio
                            _total_subidos = len([_x for _x in archivos_pdf if True])
                            # Guardar cuantos faltan: si quitaste el ultimo, cambiar llave
                            st.session_state[f"contador_upload_{escuela}"] = st.session_state.get(f"contador_upload_{escuela}", 0) + 1
                            st.rerun()
                # Por cada archivo, un selector de grupo - ESTO ES LO QUE ARREGLA LO DE 3A
                grupos_por_archivo={}
                for idx_f, f in enumerate(archivos_pdf):
                    st.write(f"---")
                    st.write(f"**Archivo {idx_f+1}: {f.name}**")
                    if escuela=="ESCUELA SECUNDARIA ESTATAL # 3046":
                        opcion=st.selectbox(f"¿De qué grupo es este archivo {f.name}?", ["Elige el grupo a mano - Auto ya no sirve, mezcla las escuelas", "1B - Artes", "3A - Electrónica", "3B - Electrónica", "3C - Electrónica", "3A y 3B juntos - Electrónica"], key=f"grupo_pdf_{idx_f}_36")
                    else:
                        opcion=st.selectbox(f"¿De qué grupo es este archivo {f.name}?", ["Elige el grupo a mano - Auto ya no sirve, mezcla las escuelas", "1A", "2A", "3A", "4A", "5A", "5B", "6A", "1B", "3B"], key=f"grupo_pdf_{idx_f}_36")
                    grupos_por_archivo[f.name]=opcion
                    if opcion=="3A y 3B juntos - Electrónica":
                        st.info("ℹ️ Este PDF trae 3A y 3B juntos. El programa va a intentar separarlos por las páginas.")
                st.write("")
                if st.button("✅ Cargar todos los alumnos de estos PDFs", use_container_width=True):
                    total_general=0; por_grupo_total={}
                    for f in archivos_pdf:
                        opcion_elegida=grupos_por_archivo.get(f.name, "Elige el grupo a mano - Auto ya no sirve, mezcla las escuelas")
                        try:
                            # Si eligió "3A y 3B juntos", primero intentar como Auto (que detecta por página), si sale 0, intentar como 3A
                            if opcion_elegida=="3A y 3B juntos - Electrónica":
                                total_uno, por_grupo_uno, debug = procesar_un_pdf(f.getvalue(), escuela_pdf, f.name, "Elige el grupo a mano - Auto ya no sirve, mezcla las escuelas")
                                if total_uno==0:
                                    # Si no detectó nada, probar forzando 3A y luego 3B por separado no funciona, así que mostrar diagnóstico
                                    st.warning(f"⚠️ En {f.name} no detecté grupo en automático. Abajo te muestro lo que sí leyó para que veamos cómo viene.")
                            else:
                                # Convertir "3A - Electrónica" -> "3A", "1B - Artes" -> "1B"
                                grupo_forzado = opcion_elegida[:2] if opcion_elegida!="Elige el grupo a mano - Auto ya no sirve, mezcla las escuelas" else opcion_elegida
                                total_uno, por_grupo_uno, debug = procesar_un_pdf(f.getvalue(), escuela_pdf, f.name, grupo_forzado)
                            if "ERROR_GRUPO" in por_grupo_uno:
                                st.error(f"❌ {f.name}: {por_grupo_uno['ERROR_GRUPO']}")
                            elif "ERROR_ESCUELA" in por_grupo_uno:
                                st.error(f"❌ {f.name}: {por_grupo_uno['ERROR_ESCUELA']} No se cargó nada, para no mezclar escuelas.")
                            total_general+=total_uno
                            for g,c in por_grupo_uno.items():
                                por_grupo_total[g]=por_grupo_total.get(g,0)+c
                            if total_uno==0:
                                _ya = len([a for a in st.session_state.alumnos if a["Escuela"]==escuela])
                                if _ya>0:
                                    st.warning(f"⚠️ {f.name}: se agregaron 0 NUEVOS porque esos alumnos YA estaban cargados. Tienes {_ya} alumnos en {escuela}. No es error, no los duplica.")
                                else:
                                    st.error(f"❌ {f.name}: se agregaron 0 alumnos - No entendí este PDF. Fíjate que sea el PDF de {escuela} y que sea lista de alumnos, no el concentrado ni la ficha. Abajo pícale a 'Ver qué sí leyó' para ver qué leyó.")
                                with st.expander(f"🔍 Ver qué sí leyó el programa de {f.name} - Pícale aquí"):
                                    st.write("Esto es lo que el programa sí pudo leer de las primeras 2 páginas.")
                                    if debug:
                                        for i, txt in enumerate(debug):
                                            st.write(f"--- Página {i+1} ---")
                                            st.write(txt if txt.strip() else "(Página en blanco)")
                                    else:
                                        st.write("(No leyó nada)")
                            else:
                                st.success(f"✔️ {f.name}: se agregaron {total_uno} alumnos - {por_grupo_uno}")
                        except Exception as e:
                            st.error(f"Error en {f.name}: {e}")
                    if total_general==0:
                        st.info("ℹ️ No se agregaron alumnos nuevos. Puede ser que ya estaban cargados antes, si ya los habías cargado, no los duplica. Si es la primera vez y sale 0, elige arriba el grupo a mano y vuelve a picarle a Cargar.")
                    else:
                        st.success(f"¡LISTO! En total se agregaron {total_general} alumnos nuevos de {escuela}. Por grupo: {por_grupo_total}")
                        _guardar_listas_archivo()
                        st.rerun()
            else:
                st.info("Todavía no has elegido ningún PDF. Pícale a Browse files arriba.")
    else:
        st.subheader("📄 1. Cargar los PDFs de ESTA escuela")
        if escuela=="ESCUELA SECUNDARIA ESTATAL # 3046":
            st.write("En secundaria son **2 archivos**: uno de **1B Artes** y otro de **3A y 3B Electrónica**.")
            st.write("**AHORA TU LE DICES DE QUE GRUPO ES CADA PDF**, para que no tenga que adivinarlo y no te salga 0 alumnos.")
            st.write("Si el PDF de Electrónica trae 3A y 3B juntos, elige '3A y 3B juntos'. Si trae solo 3A, elige '3A'.")
        else:
            st.write(f"Aquí subes el PDF de **{escuela}**.")
        st.write("")
        archivos_pdf=st.file_uploader("Sube aquí tus PDFs - Puedes subir 1 o 2 juntos", type=["pdf"], accept_multiple_files=True, key=f"pdfs_{escuela}_36")
        st.write("")
        if archivos_pdf:
            st.write(f"Archivos que elegiste: **{len(archivos_pdf)}**")
            # Por cada archivo, un selector de grupo - ESTO ES LO QUE ARREGLA LO DE 3A
            grupos_por_archivo={}
            for idx_f, f in enumerate(archivos_pdf):
                st.write(f"---")
                st.write(f"**Archivo {idx_f+1}: {f.name}**")
                if escuela=="ESCUELA SECUNDARIA ESTATAL # 3046":
                    opcion=st.selectbox(f"¿De qué grupo es este archivo {f.name}?", ["Elige el grupo a mano - Auto ya no sirve, mezcla las escuelas", "1B - Artes", "3A - Electrónica", "3B - Electrónica", "3C - Electrónica", "3A y 3B juntos - Electrónica"], key=f"grupo_pdf_{idx_f}_36")
                else:
                    opcion=st.selectbox(f"¿De qué grupo es este archivo {f.name}?", ["Elige el grupo a mano - Auto ya no sirve, mezcla las escuelas", "1A", "2A", "3A", "4A", "5A", "5B", "6A", "1B", "3B"], key=f"grupo_pdf_{idx_f}_36")
                grupos_por_archivo[f.name]=opcion
                if opcion=="3A y 3B juntos - Electrónica":
                    st.info("ℹ️ Este PDF trae 3A y 3B juntos. El programa va a intentar separarlos por las páginas.")
            st.write("")
            if st.button("✅ Cargar todos los alumnos de estos PDFs", use_container_width=True):
                total_general=0; por_grupo_total={}
                for f in archivos_pdf:
                    opcion_elegida=grupos_por_archivo.get(f.name, "Elige el grupo a mano - Auto ya no sirve, mezcla las escuelas")
                    try:
                        # Si eligió "3A y 3B juntos", primero intentar como Auto (que detecta por página), si sale 0, intentar como 3A
                        if opcion_elegida=="3A y 3B juntos - Electrónica":
                            total_uno, por_grupo_uno, debug = procesar_un_pdf(f.getvalue(), escuela_pdf, f.name, "Elige el grupo a mano - Auto ya no sirve, mezcla las escuelas")
                            if total_uno==0:
                                # Si no detectó nada, probar forzando 3A y luego 3B por separado no funciona, así que mostrar diagnóstico
                                st.warning(f"⚠️ En {f.name} no detecté grupo en automático. Abajo te muestro lo que sí leyó para que veamos cómo viene.")
                        else:
                            # Convertir "3A - Electrónica" -> "3A", "1B - Artes" -> "1B"
                            grupo_forzado = opcion_elegida[:2] if opcion_elegida!="Elige el grupo a mano - Auto ya no sirve, mezcla las escuelas" else opcion_elegida
                            total_uno, por_grupo_uno, debug = procesar_un_pdf(f.getvalue(), escuela_pdf, f.name, grupo_forzado)
                        total_general+=total_uno
                        for g,c in por_grupo_uno.items():
                            por_grupo_total[g]=por_grupo_total.get(g,0)+c
                        if total_uno==0:
                            st.error(f"❌ {f.name}: se agregaron 0 alumnos - {por_grupo_uno}")
                            with st.expander(f"🔍 Ver qué sí leyó el programa de {f.name} - Pícale aquí"):
                                st.write("Esto es lo que el programa sí pudo leer de las primeras 2 páginas.")
                                if debug:
                                    for i, txt in enumerate(debug):
                                        st.write(f"--- Página {i+1} ---")
                                        st.write(txt if txt.strip() else "(Página en blanco)")
                                else:
                                    st.write("(No leyó nada)")
                        else:
                            st.success(f"✔️ {f.name}: se agregaron {total_uno} alumnos - {por_grupo_uno}")
                    except Exception as e:
                        st.error(f"Error en {f.name}: {e}")
                if total_general==0:
                    st.info("ℹ️ No se agregaron alumnos nuevos. Puede ser que ya estaban cargados antes, si ya los habías cargado, no los duplica. Si es la primera vez y sale 0, elige arriba el grupo a mano y vuelve a picarle a Cargar.")
                else:
                    st.success(f"¡LISTO! En total se agregaron {total_general} alumnos nuevos de {escuela}. Por grupo: {por_grupo_total}")
                    _guardar_listas_archivo()
                    st.rerun()
        else:
            st.info("Todavía no has elegido ningún PDF. Pícale a Browse files arriba.")
    st.divider()
    alumnos_esc=[a for a in st.session_state.alumnos if a["Escuela"]==escuela]
    if not alumnos_esc:
        st.info(f"Todavía no tienes alumnos en {escuela}. Sube los PDFs arriba.")
        st.stop()
    # Boton para arreglar el 2A: 64 alumnos (duplicados por subir 2 veces el mismo PDF)
    if st.button(f"🧹 Limpiar alumnos repetidos de {escuela}", key=f"btn_limpiar_dup_{escuela}_49"):
        _antes = len(st.session_state.alumnos)
        _vistos2 = set(); _limp2 = []
        for _a in st.session_state.alumnos:
            _k2 = (_a.get("Nombre","").strip().lower(), _a.get("Grupo",""), _a.get("Escuela",""))
            if _k2 not in _vistos2:
                _vistos2.add(_k2); _limp2.append(_a)
        st.session_state.alumnos = _limp2
        _guardar_listas_archivo()
        st.success(f"✅ Listo. Antes: {_antes} alumnos en total. Ahora: {len(_limp2)}. Se quitaron {_antes-len(_limp2)} repetidos.")
        st.rerun()
    # BOTON NUEVO FINAL 55: Eliminar la escuela YA cargada (no solo el PDF antes de cargarlo)
    # Antes solo se podia borrar grupo por grupo. Ahora se borra TODA la escuela de una vez y queda en blanco para volver a subirla bien.
    if st.button(f"🗑️ Eliminar TODA la lista ya cargada de {escuela} y dejar en blanco", key=f"btn_eliminar_escuela_{escuela}_54"):
        _antes_a = len(st.session_state.alumnos)
        _antes_r = len(st.session_state.registros)
        # Borrar alumnos de esa escuela
        st.session_state.alumnos = [a for a in st.session_state.alumnos if a.get("Escuela") != escuela]
        # Borrar registros/capturas de esa escuela (si el registro tiene Escuela)
        st.session_state.registros = [r for r in st.session_state.registros if r.get("Escuela") != escuela]
        # Limpiar tambien los PDFs que estaban en espera de esa escuela
        st.session_state[f"archivos_elegidos_{escuela}"] = []
        st.session_state[f"pdfs_quitados_{escuela}"] = []
        st.session_state[f"contador_upload_{escuela}"] = st.session_state.get(f"contador_upload_{escuela}", 0) + 1
        _guardar_listas_archivo()
        st.success(f"✅ Listo. Se borraron {_antes_a - len(st.session_state.alumnos)} alumnos y {_antes_r - len(st.session_state.registros)} capturas de {escuela}. Ya quedo en blanco, puedes subir otra vez su PDF bien.")
        st.rerun()
    st.subheader(f"📋 2. Elige el grupo de {escuela}")
    grupos_disponibles=sorted(set(a["Grupo"] for a in alumnos_esc))
    opciones_grupo=["-- Elige un grupo --"]+grupos_disponibles
    if st.session_state.grupo_sel_actual not in opciones_grupo:
        st.session_state.grupo_sel_actual="-- Elige un grupo --"
    # Si ya hay un grupo confirmado Y estamos viendo su ficha, no volver a pedir grupo: usar ese grupo y saltar al resto
    if st.session_state.get("alumno_activo") is not None and st.session_state.get("grupo_confirmado") in grupos_disponibles:
        grupo_sel = st.session_state.grupo_confirmado
        st.session_state.grupo_sel_actual = grupo_sel
        llave_dias = f"{escuela}|{grupo_sel}"
        # Dias ya guardados de ese grupo, para la ficha
        _dg = st.session_state.dias_clase.get(llave_dias, [])
        dias_clase_grupo = _dg if _dg else [0]
        nombres_dias_grupo = [DIAS_ES[d] for d in dias_clase_grupo]
    else:
        grupo_elegido=st.selectbox("¿A qué grupo quieres entrar?", opciones_grupo, index=opciones_grupo.index(st.session_state.grupo_sel_actual) if st.session_state.grupo_sel_actual in opciones_grupo else 0, key=f"sel_grupo_{st.session_state.contador_grupo}_36")
        # OJO: elegir en el selector NO te mete. Solo guarda lo que elegiste en pantalla.
        # Antes aqui se ponia grupo_sel_actual = grupo_elegido y como ya tenia dias, te aventaba a la lista sin dejarte picar a Portada.
        st.session_state.grupo_sel_actual=grupo_elegido
        if grupo_elegido=="-- Elige un grupo --":
            for g in grupos_disponibles:
                cnt=len([a for a in alumnos_esc if a["Grupo"]==g])
                st.write(f"- **{g}**: {cnt} alumnos")
            st.stop()
        grupo_sel = grupo_elegido
        llave_dias=f"{escuela}|{grupo_sel}"
        # Si este grupo YA tiene dias guardados, NO saltar a dias ni a lista solo: mostrar boton Entrar
        if st.session_state.get("dias_confirmados", {}).get(llave_dias, False):
            _dn = [DIAS_ES[d] for d in st.session_state.dias_clase.get(llave_dias, [])]
            st.success(f"✅ {grupo_sel} ya tiene días guardados: **{', '.join(_dn)}**")
            st.write("Si quieres entrar a su lista, pícale a **Entrar**. Si quieres irte a la portada, pícale a **Regresar a la portada** arriba, ya no te va a aventar a la lista solo.")
            if st.button(f"➡️ Entrar a la lista de {grupo_sel}", use_container_width=True):
                st.session_state.grupo_confirmado = grupo_sel
                st.rerun()
            st.stop()
        # Si NO tiene dias, abajo sale el selector de dias (no se hace st.stop aqui)
    # Solo si NO estamos en ficha y NO tenemos dias confirmados, llega aqui al selector de dias de abajo
    st.divider()
    st.subheader(f"📅 ¿Qué días le das clase a {grupo_sel}?")
    st.write("Elige los días y pícale a **Guardar días**. Hasta que TÚ le piques, no se guarda nada, para que no te meta al grupo antes.")
    # Si ya había días confirmados antes, esos son el default. Si no, empezar en blanco, NO en lunes falso.
    if st.session_state.get("dias_confirmados", {}).get(llave_dias, False):
        dias_guardados_numeros=st.session_state.dias_clase.get(llave_dias, [])
    else:
        dias_guardados_numeros=[]
    dias_guardados_nombres=[OPCIONES_DIAS[d] for d in dias_guardados_numeros if d < len(OPCIONES_DIAS)]
    dias_elegidos_nombres=st.multiselect(f"Elige los días de clase de {grupo_sel}", OPCIONES_DIAS, default=dias_guardados_nombres, key=f"multiselect_dias_{escuela}_{grupo_sel}_38")
    dias_elegidos_numeros=[MAPA_DIA[n] for n in dias_elegidos_nombres]
    if st.button(f"✅ Guardar días de {grupo_sel}", use_container_width=True):
        if not dias_elegidos_numeros:
            st.warning("⚠️ Elige al menos un día antes de guardar.")
            dias_clase_grupo = dias_guardados_numeros
            nombres_dias_grupo = [DIAS_ES[d] for d in dias_clase_grupo]
        else:
            st.session_state.dias_clase[llave_dias]=dias_elegidos_numeros
            st.session_state.dias_confirmados[llave_dias]=True
            st.session_state.grupo_confirmado=grupo_sel
            _guardar_dias_archivo()  # Guardar en dias_clase.json para que no se borre al cambiar de grupo
            dias_clase_grupo=dias_elegidos_numeros
            nombres_dias_grupo=[DIAS_ES[d] for d in dias_clase_grupo]
            st.success(f"✅ Guardado: A **{grupo_sel}** le das clase los: **{', '.join(nombres_dias_grupo)}**")
            st.rerun()
    else:
        # Mientras no guardas, usar lo que elegiste en pantalla para que no se truene, pero SIN marcarlo como confirmado
        dias_clase_grupo = dias_elegidos_numeros if dias_elegidos_numeros else dias_guardados_numeros
        nombres_dias_grupo=[DIAS_ES[d] for d in dias_clase_grupo] if dias_clase_grupo else ["Sin días todavía"]
        if dias_clase_grupo:
            st.info(f"Vas a guardar: **{', '.join(nombres_dias_grupo)}** - Pícale a **Guardar días** para entrar a la lista.")
if st.session_state.alumno_activo is not None:
    nombre_al=st.session_state.alumno_activo
    st.divider()
    st.subheader(f"📁 Ficha Personal - {nombre_al}")
    st.write(f"**Escuela:** {escuela}  •  **Grupo:** {grupo_sel}  •  **Días de clase:** {', '.join(nombres_dias_grupo)}")
    if st.session_state.trimestre_cargado: st.write(f"**Trimestre cargado:** {st.session_state.trimestre_cargado_nombre} del {fecha_bonita(st.session_state.tri_inicio)} al {fecha_bonita(st.session_state.tri_fin)}")
    st.write("")
    if st.button("⬅️ Regresar a la lista de "+grupo_sel):
        st.session_state.alumno_activo=None; st.rerun()
    st.write("")
    nivel, texto_riesgo, faltas, retardos, no_trab, no_tarea, indis_n, regs_al = riesgo_de_alumno(nombre_al, escuela, grupo_sel)
    if nivel=="VERDE": st.success(f"🟢 NORMAL - {texto_riesgo}")
    elif nivel=="AMARILLO": st.warning(f"🟡 EN PELIGRO - {texto_riesgo}")
    else: st.error(f"🔴 REPROBADO - {texto_riesgo}")
    st.write(f"**Factor de riesgo:**  😢 Faltas: {faltas}  •  📄❌ No entregó trabajo: {no_trab}  •  ✉️❌ No entregó tarea: {no_tarea}  •  😡 Indisciplinas: {indis_n}")
    st.divider()
    st.subheader("📄 Exportar esta ficha a PDF")
    try:
        pdf_ficha=generar_pdf_ficha_alumno(nombre_al, escuela, grupo_sel)
        st.download_button(label=f"📄 Generar PDF de la ficha de {nombre_al}", data=pdf_ficha, file_name=f"Ficha_{nombre_al.replace(' ','_')}_{grupo_sel}_{st.session_state.trimestre_cargado_nombre or 'Trimestre'}.pdf", mime="application/pdf", use_container_width=True)
    except Exception as e:
        st.error(f"No se pudo generar el PDF: {e}. Instala con: py -m pip install reportlab")
    st.divider()
    st.subheader("✏️ Llenar captura - Con el día que es")
    # PARA ESO SE CARGA EL TRIMESTRE: el programa ya sabe cuando empieza y termina y no deja capturar fuera
    # NUNCA error fatal, solo leyendita en cuadrito azul (st.info)
    puede_capturar = True
    motivo_bloqueo = ""
    if not st.session_state.trimestre_cargado:
        puede_capturar = False
        motivo_bloqueo = "Todavía no has cargado el trimestre. Regresa a la portada, pon desde cuándo hasta cuándo es, y pícale a CARGAR ESTE TRIMESTRE. Para eso se carga el trimestre, para que el programa sepa cuándo sí puedes capturar."
    elif hoy < st.session_state.tri_inicio:
        puede_capturar = False
        motivo_bloqueo = f"Tu trimestre {st.session_state.trimestre_cargado_nombre} todavía no empieza. Empieza el {fecha_bonita(st.session_state.tri_inicio)} y hoy es {fecha_bonita(hoy)}. Mañana que ya sea {fecha_bonita(st.session_state.tri_inicio)} ya vas a poder capturar. Por eso cargaste el trimestre, para que no te deje capturar antes de que empiece."
    elif hoy > st.session_state.tri_fin:
        puede_capturar = False
        motivo_bloqueo = f"Tu trimestre {st.session_state.trimestre_cargado_nombre} ya se acabó el {fecha_bonita(st.session_state.tri_fin)} y hoy es {fecha_bonita(hoy)}. Ya no se puede capturar de ese trimestre. Carga el siguiente trimestre en la portada para que ya puedas capturar otra vez. Por eso cargaste el trimestre, para que no te deje capturar después de que se acabó."
    else:
        st.info(f"ℹ️ Hoy es {fecha_bonita(hoy)} - Estás dentro del {st.session_state.trimestre_cargado_nombre} que va del {fecha_bonita(st.session_state.tri_inicio)} al {fecha_bonita(st.session_state.tri_fin)}. Sí puedes capturar.")
    if not puede_capturar:
        st.info(f"ℹ️ {motivo_bloqueo}")
        st.write("")
        st.write("Abajo te dejo ver el historial, pero no te dejo guardar captura nueva hasta que estés dentro del trimestre que cargaste.")
    if True:
        # Fecha por defecto SIEMPRE dentro del trimestre cargado, para que nunca se truene
        # Si hoy está dentro, usa hoy. Si hoy está antes, usa el inicio. Si hoy está después, usa el fin.
        if not st.session_state.trimestre_cargado:
            fecha_por_defecto = hoy
        elif hoy < st.session_state.tri_inicio:
            fecha_por_defecto = st.session_state.tri_inicio
        elif hoy > st.session_state.tri_fin:
            fecha_por_defecto = st.session_state.tri_fin
        else:
            fecha_por_defecto = hoy
        # SIN min_value ni max_value para que nunca salga el error fatal StreamlitValueBelowMinError
        fecha_captura=st.date_input("📅 ¿De qué día es esta captura?", value=fecha_por_defecto, key=f"fecha_cap_{nombre_al}_36")
        st.write(f"Vas a guardar la captura del **{fecha_bonita(fecha_captura)}**")
        if st.session_state.trimestre_cargado and (fecha_captura < st.session_state.tri_inicio or fecha_captura > st.session_state.tri_fin):
            st.info(f"ℹ️ Esa fecha no está dentro del trimestre que cargaste ({st.session_state.trimestre_cargado_nombre} del {fecha_bonita(st.session_state.tri_inicio)} al {fecha_bonita(st.session_state.tri_fin)}). Por eso no te voy a dejar guardarla, para que no se revuelva con otro trimestre.")
            puede_capturar = False
        if fecha_captura.weekday() not in dias_clase_grupo:
            st.info(f"ℹ️ Ojo: El {fecha_bonita(fecha_captura)} es {DIAS_ES[fecha_captura.weekday()]} y a {grupo_sel} le das clase los {', '.join(nombres_dias_grupo)}.")
        col1,col2=st.columns(2)
        with col1:
            asistencia=st.selectbox("😊 Asistencia", ["😊 Asistió","😢 Falta","⏰ Retardo"], key="f_asis21")
            trabajo=st.selectbox("📄 Trabajo", ["📄✅ Entregó","📄❌ No entregó","📄❓ No trajo material","No se pidió"], key="f_trab21")
        with col2:
            tarea=st.selectbox("✉️ Tarea", ["✉️ Entregó","✉️❌ No entregó","No se pidió"], key="f_tar21")
            indis=st.selectbox("😡 Indisciplina", ["Ninguna","😡 No trabajó","😡 No trajo material","😡 Falta de respeto"], key="f_ind21")
        anotacion=st.text_area("📝 Anotaciones del día", key="f_anot21", placeholder="Ej: No trabajó, se paró mucho...")
        st.write("")
        colg1,colg2=st.columns(2)
        with colg1:
            if puede_capturar:
                if st.button(f"💾 Guardar captura - {fecha_corta(fecha_captura)}"):
                    ya_existe=any(r["Alumno"]==nombre_al and r.get("Escuela")==escuela and r.get("Grupo")==grupo_sel and r.get("Trimestre")==st.session_state.trimestre_cargado_nombre and r.get("Fecha")==str(fecha_captura) and r.get("Estado")==asistencia and r.get("Trabajo")==trabajo and r.get("Tarea")==tarea and r.get("Indisciplina")==indis and r.get("Anotacion")==anotacion for r in st.session_state.registros)
                    ya_hay_ese_dia=any(r["Alumno"]==nombre_al and r.get("Escuela")==escuela and r.get("Grupo")==grupo_sel and r.get("Trimestre")==st.session_state.trimestre_cargado_nombre and r.get("Fecha")==str(fecha_captura) for r in st.session_state.registros)
                    if ya_existe: st.info(f"ℹ️ Ya guardaste esto mismo el {fecha_bonita(fecha_captura)}. No lo guardé otra vez para que no se duplique.")
                    elif ya_hay_ese_dia: st.info(f"ℹ️ Ya tienes una captura el {fecha_bonita(fecha_captura)} para {nombre_al}. No la guardé para que no se duplique.")
                    else:
                        st.session_state.registros.append({"Alumno":nombre_al,"Escuela":escuela,"Grupo":grupo_sel,"Trimestre":st.session_state.trimestre_cargado_nombre,"Fecha":str(fecha_captura),"FechaBonita":fecha_bonita(fecha_captura),"Estado":asistencia,"Trabajo":trabajo,"Tarea":tarea,"Indisciplina":indis,"Anotacion":anotacion})
                        _guardar_listas_archivo()  # Guardar captura en listas.json para no perderla
                        st.success(f"✅ Guardado para {nombre_al} - Captura del **{fecha_bonita(fecha_captura)}** - {st.session_state.trimestre_cargado_nombre}"); st.rerun()
            else:
                st.info("ℹ️ No se puede guardar captura ahorita porque estás fuera del trimestre que cargaste. Cambia la fecha a una dentro del trimestre, o carga el trimestre que sí es.")
        with colg2:
            if st.button(f"🗑️ Eliminar a {nombre_al}"):
                for i,a in enumerate(st.session_state.alumnos):
                    if a["Nombre"]==nombre_al and a["Escuela"]==escuela and a["Grupo"]==grupo_sel:
                        del st.session_state.alumnos[i]; _guardar_listas_archivo(); break
                st.session_state.alumno_activo=None; st.success(f"Se eliminó {nombre_al}"); st.rerun()
    st.divider()
    st.subheader("📋 Historial - Con el día que se guardó")
    if not regs_al: st.write("Todavía no tiene capturas.")
    else:
        regs_ordenados=sorted(regs_al, key=lambda x: x.get("Fecha",""))
        for idx_r, r in enumerate(regs_ordenados):
            fecha_mostrar=r.get("FechaBonita") or r.get("Fecha","")
            if not r.get("FechaBonita") and r.get("Fecha"):
                try: y,m,d=map(int, r["Fecha"].split("-")); fecha_mostrar=fecha_bonita(date(y,m,d))
                except: fecha_mostrar=r["Fecha"]
            st.write(f"**📅 Captura del {fecha_mostrar}** - {r.get('Trimestre','')} - {r['Estado']} - {r['Trabajo']} - {r['Tarea']} - {r['Indisciplina']}")
            if r["Anotacion"]: st.write(f"📝 {r['Anotacion']}")
            st.write("")
            if st.button(f"🗑️ Borrar este día - {fecha_mostrar}", key=f"borrar_dia_{escuela}_{grupo_sel}_{nombre_al}_{idx_r}_{r.get('Fecha','')}_36"):
                for i, rr in enumerate(st.session_state.registros):
                    if rr["Alumno"]==nombre_al and rr.get("Escuela")==escuela and rr.get("Grupo")==grupo_sel and rr.get("Fecha")==r.get("Fecha") and rr.get("Estado")==r.get("Estado") and rr.get("Trabajo")==r.get("Trabajo"):
                        del st.session_state.registros[i]; _guardar_listas_archivo(); break
                st.success(f"Se borró solo la captura del {fecha_mostrar}."); st.rerun()
            st.write("---")
    st.stop()
st.divider()
st.header(f"📋 Lista de {grupo_sel} - {escuela}")
alumnos_grupo=[a for a in alumnos_esc if a["Grupo"]==grupo_sel]
st.write(f"Total en {grupo_sel}: **{len(alumnos_grupo)} alumnos**  •  Le das clase los: {', '.join(nombres_dias_grupo)}")
st.write("")
if st.button("⬅️ Regresar a la portada (inicio)", key="btn_portada_desde_lista_42"):
    _ir_a_portada_limpio()
if st.button(f"📅 Cambiar días de clase de {grupo_sel} - Ahora: {', '.join(nombres_dias_grupo)}", key="btn_cambiar_dias_38"):
    # Quitar la confirmación para que vuelva a salir el selector de días y lo puedas cambiar
    try:
        st.session_state.dias_confirmados[llave_dias]=False
        _guardar_dias_archivo()
    except: pass
    st.rerun()
if st.button("⬅️ Regresar a elegir otro grupo", key="btn_regresar_grupo35"):
    # Antes solo cambiaba la variable, pero Streamlit se quedaba con el grupo viejo guardado en el selector (key sel_grupo18).
    # Por eso no regresaba. Ahora borramos el selector viejo y cambiamos su llave para que nazca en blanco.
    st.session_state.grupo_sel_actual="-- Elige un grupo --"; st.session_state.grupo_confirmado=None; st.session_state.alumno_activo=None
    st.session_state.contador_grupo = st.session_state.get("contador_grupo", 0) + 1
    # Borrar todas las llaves viejas del selector Y del multiselect de dias, para que no regrese al grupo anterior ni a sus dias
    for _k in list(st.session_state.keys()):
        if str(_k).startswith("sel_grupo_") or str(_k).startswith("multiselect_dias_"):
            try: del st.session_state[_k]
            except: pass
    st.rerun()
st.write("")
st.divider()
for idx, al in enumerate(alumnos_grupo):
    nombre=al["Nombre"]
    regs=[r for r in st.session_state.registros if r["Alumno"]==nombre and r.get("Escuela")==escuela and r.get("Grupo")==grupo_sel]
    col_n, col_f, col_b = st.columns([4,1,2])
    with col_n: st.write(f"**{idx+1}. {nombre}**")
    with col_f: st.write(f"Capturas: {len(regs)}")
    with col_b:
        if st.button(f"➡️ Abrir ficha de {nombre}", key=f"abrir_{escuela}_{grupo_sel}_{idx}_36"):
            st.session_state.alumno_activo=nombre; st.rerun()
st.divider()
st.subheader(f"📊 Concentrado - Grupo {grupo_sel}")
amarillos=[]; rojos=[]
for al in alumnos_grupo:
    nivel, texto, faltas, retardos, no_trab, no_tarea, indis_n, regs = riesgo_de_alumno(al["Nombre"], escuela, grupo_sel)
    if nivel=="AMARILLO": amarillos.append((al["Nombre"], faltas, no_trab, no_tarea))
    elif nivel=="ROJO": rojos.append((al["Nombre"], faltas, no_trab, no_tarea))
st.warning(f"🟡 CONCENTRADO AMARILLO - {len(amarillos)} alumnos en peligro en {grupo_sel}")
with st.expander(f"🟡 Ver lista de los {len(amarillos)} alumnos en AMARILLO"):
    if not amarillos: st.write("No hay ningún alumno en amarillo.")
    else:
        for j, (nom, f, nt, nta) in enumerate(amarillos):
            c1,c2,c3=st.columns([4,2,2])
            with c1: st.write(f"**{j+1}. {nom}**")
            with c2: st.write(f"😢 Faltas: {f}  •  📄❌ Sin trabajo: {nt}")
            with c3:
                if st.button(f"➡️ Ir a su ficha - {nom}", key=f"amarillo_{escuela}_{grupo_sel}_{j}_36"):
                    st.session_state.alumno_activo=nom; st.rerun()
st.error(f"🔴 CONCENTRADO ROJO - {len(rojos)} alumnos reprobados en {grupo_sel}")
with st.expander(f"🔴 Ver lista de los {len(rojos)} alumnos en ROJO"):
    if not rojos: st.write("No hay ningún alumno en rojo.")
    else:
        for j, (nom, f, nt, nta) in enumerate(rojos):
            c1,c2,c3=st.columns([4,2,2])
            with c1: st.write(f"**{j+1}. {nom}**")
            with c2: st.write(f"😢 Faltas: {f}  •  📄❌ Sin trabajo: {nt}")
            with c3:
                if st.button(f"➡️ Ir a su ficha - {nom}", key=f"rojo_{escuela}_{grupo_sel}_{j}_36"):
                    st.session_state.alumno_activo=nom; st.rerun()
st.divider()
st.subheader("📄 Generar PDF General del Grupo")
try:
    pdf_grupo=generar_pdf_general_grupo(escuela, grupo_sel, alumnos_grupo, dias_clase_grupo)
    st.download_button(label=f"📄 Generar PDF General del Grupo {grupo_sel}", data=pdf_grupo, file_name=f"Concentrado_General_{grupo_sel}_{escuela.replace(' ','_')}_{st.session_state.trimestre_cargado_nombre or 'Trimestre'}.pdf", mime="application/pdf", use_container_width=True)
except Exception as e:
    st.error(f"No se pudo generar el PDF del grupo: {e}. Instala con: py -m pip install reportlab")
st.divider()
if st.button(f"🗑️ Eliminar todo el grupo {grupo_sel}"):
    st.session_state.alumnos=[a for a in st.session_state.alumnos if not (a["Escuela"]==escuela and a["Grupo"]==grupo_sel)]; _guardar_listas_archivo()
    st.session_state.grupo_sel_actual="-- Elige un grupo --"; st.success(f"Se eliminó el grupo {grupo_sel}"); st.rerun()
