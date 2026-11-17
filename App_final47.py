
# MIS TRABAJOS Y CALIFICACIONES - FINAL 102 - GOOGLE SHEET POR APPS SCRIPT WEBHOOK, RECONSTRUIDA DESDE 99, SIN ERROR NAMEERROR - SUBIR 2 PDFs JUNTOS + SIN ERROR FATAL DE FECHAS - SOLO LEYENDITA EN CUADRITO
# Corre con: py -m streamlit run app_final120.py
import streamlit as st
import pandas as pd
# FINAL 96: GOOGLE SHEET COMO BASE DE DATOS - para que no se borre nada y puedas capturar en el celular sin Respaldo
# Como funciona: todo lo que capturas se guarda solo en tu Google Sheet, no en la memoria de Streamlit.
# Si se reinicia la app, si cierras el celular, si se te acaba la pila, al volver a abrir, todo sigue ahi.
# Genera TODO lo que ya tenemos: ficha, historial, desglose final, color VERDE/AMARILLO/ROJO, calificacion, PDF, dias fijos, trimestres.
# Si todavia no configuras el Sheet, la app sigue trabajando como antes con Respaldo, no se traba.
# FINAL 102: GOOGLE SHEET POR APPS SCRIPT WEBHOOK - sin gspread, sin GSheetsConnection, ya queda
# La 101 se comio un pedazo y por eso salia NameError en linea 216. Esta 102 esta reconstruida desde la 99 que si estaba buena.
def _gsheets_conectado():
    try:
        if "gsheets_webhook" in st.secrets:
            return True
        if "connections" in st.secrets and "gsheets_webhook" in st.secrets["connections"]:
            return True
        if "gsheets" in st.secrets and "webhook_url" in st.secrets["gsheets"]:
            return True
        return False
    except:
        return False
def _gsheets_webhook_url():
    try:
        if "gsheets_webhook" in st.secrets:
            _v = st.secrets["gsheets_webhook"]
            return _v if isinstance(_v, str) else (_v.get("url", "") or _v.get("webhook_url", ""))
        if "connections" in st.secrets and "gsheets_webhook" in st.secrets["connections"]:
            _v = st.secrets["connections"]["gsheets_webhook"]
            return _v if isinstance(_v, str) else (_v.get("url", "") or _v.get("webhook_url", ""))
        if "gsheets" in st.secrets:
            return st.secrets["gsheets"].get("webhook_url", "") or st.secrets["gsheets"].get("url", "")
        return ""
    except:
        return ""
def _cargar_desde_gsheets():
    # FINAL 120: Al abrir la app, leer del Sheet para no perder capturas si se reinicia el celular
    try:
        _url = _gsheets_webhook_url()
        if not _url:
            return False
        import requests
        _r = requests.get(_url, timeout=5)
        if _r.status_code in (200, 302):
            _j = _r.json()
            _regs = _j.get("registros", [])
            if _regs:
                # FINAL 120: Limpiar fecha fea que viene del Sheet como 2026-11-17T06:00:00.000Z
                _DIAS = ["lunes","martes","miércoles","jueves","viernes","sábado","domingo"]
                _MESES = ["","enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
                for _rr in _regs:
                    _f = str(_rr.get("Fecha","") or "").strip()
                    if "T" in _f:
                        _f = _f.split("T")[0]
                    _rr["Fecha"] = _f
                    # Si FechaBonita viene fea o vacia, generarla bonita
                    _fb = str(_rr.get("FechaBonita","") or "").strip()
                    if not _fb or "T" in _fb or _fb == _f or len(_fb) < 5:
                        try:
                            from datetime import date as _date114
                            _y,_m,_d = map(int, _f.split("-"))
                            _dd = _date114(_y,_m,_d)
                            _rr["FechaBonita"] = f"{_DIAS[_dd.weekday()]} {_d} de {_MESES[_m]}"
                        except:
                            _rr["FechaBonita"] = _f
                st.session_state.registros = _regs
                st.session_state._sheet_cargado = True
                return True
        return False
    except:
        return False
def _guardar_en_gsheets():
    try:
        _url = _gsheets_webhook_url()
        if not _url:
            return False, "Falta webhook_url en Secrets - pon el enlace de tu Apps Script"
        import requests
        _regs = list(st.session_state.get("registros", []))
        # FINAL 120: Antes de guardar, leer lo que ya hay en el Sheet y juntarlo con lo nuevo.
        # Si no, cuando guardas a otro alumno, el anterior se borra porque solo manda el nuevo.
        try:
            _r_get = requests.get(_url, timeout=5)
            if _r_get.status_code in (200, 302):
                try:
                    _exist = _r_get.json().get("registros", [])
                except:
                    # FINAL 120: Si el Apps Script es viejo y no regresa JSON con registros, NO sobrescribir el Sheet con solo lo nuevo porque borraria al anterior.
                    return False, "Tu Apps Script es viejo - actualizalo al FINAL 106 para que no borre al anterior. No se guardo para no borrar nada." 
                # FINAL 120: Normalizar Fecha a YYYY-MM-DD aunque venga en 3 formatos: "2026-11-17", "2026-11-17 00:00:00", "17/11/2026" o "martes 17 de noviembre". Si no, se duplica todo.
                def _norm_fecha(_v):
                    _s = str(_v or "").strip()
                    # Si viene como 17/11/2026, voltearlo a 2026-11-17
                    if "/" in _s and len(_s) >= 10:
                        _partes = _s[:10].split("/")
                        if len(_partes) == 3 and len(_partes[2]) == 4:
                            return f"{_partes[2]}-{_partes[1].zfill(2)}-{_partes[0].zfill(2)}"
                    return _s[:10]
                # FINAL 120: SOLO 1 FECHA - usar solo Fecha YYYY-MM-DD para no duplicar. FechaBonita NO se usa para dedup porque venia como "martes 17 de noviembre" y como "2026-11-17" y los contaba como 2.
                # Ademas, forzar FechaBonita desde Fecha para que siempre sea 1 sola.
                _DIAS117 = ["lunes","martes","miércoles","jueves","viernes","sábado","domingo"]
                _MESES117 = ["","enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
                def _fecha_bonita_117(_f):
                    try:
                        from datetime import date as _d117
                        _y,_m,_dd = map(int, _f.split("-"))
                        _dt = _d117(_y,_m,_dd)
                        return f"{_DIAS117[_dt.weekday()]} {_dd} de {_MESES117[_m]}"
                    except:
                        return _f
                _por_clave = {}
                for _r0 in _exist + _regs:
                    _f_norm = _norm_fecha(_r0.get("Fecha",""))
                    # Si Fecha viene como "martes 17 de noviembre" (sin guiones), intentar sacarla de FechaBonita
                    if "-" not in _f_norm and _r0.get("FechaBonita"):
                        _f_norm = _norm_fecha(_r0.get("FechaBonita",""))
                    _r0["Fecha"] = _f_norm
                    _r0["FechaBonita"] = _fecha_bonita_117(_f_norm)
                    _k = (str(_r0.get("Alumno","")).strip().lower(), str(_r0.get("Escuela","")).strip().lower(), str(_r0.get("Grupo","")).strip().lower(), _f_norm)
                    _por_clave[_k] = _r0
                _merged = list(_por_clave.values())
                # Si el usuario borro a proposito, no revivir lo borrado en ESTE guardado, pero limpiar el flag para que el siguiente guardado si junte al anterior
                if st.session_state.get("_sheet_borrado_a_proposito", False):
                    _regs = _regs
                    st.session_state._sheet_borrado_a_proposito = False
                else:
                    _regs = _merged
                    st.session_state.registros = _regs
        except:
            pass
        # FINAL 120: Si registros esta vacio y nunca se cargo del Sheet en esta sesion, NO mandar [] porque borraria el Sheet al reiniciar.
        if not _regs and not st.session_state.get("_sheet_borrado_a_proposito", False) and not st.session_state.get("_sheet_cargado", False) and not st.session_state.get("_hubo_captura_esta_sesion", False):
            return False, "No se mando vacio para no borrar el Sheet al reiniciar - primero carga del Sheet"
        # FINAL 120: Quitar duplicados de lo que se va a mandar, aunque ya vengan duplicados en la sesion. Si no, se duplican todos.
        _seen = set()
        _regs_sin_dup = []
        for _rr in _regs:
            # FINAL 120: Solo 1 fecha - dedup por Fecha YYYY-MM-DD, no por FechaBonita
            _cf2 = str(_rr.get("Fecha","") or "").strip().split("T")[0][:10]
            _k2 = (str(_rr.get("Alumno","")).strip().lower(), str(_rr.get("Escuela","")).strip().lower(), str(_rr.get("Grupo","")).strip().lower(), _cf2)
            if _k2 not in _seen:
                _seen.add(_k2)
                _regs_sin_dup.append(_rr)
        _regs = _regs_sin_dup
        st.session_state.registros = _regs
        _r = requests.post(_url, json={"registros": _regs}, timeout=5)
        if _r.status_code in (200, 302):
            return True, f"Guardado en Google Sheet - {len(_regs)} capturas en Registros"
        return False, f"Apps Script respondio {_r.status_code}: {_r.text[:200]}"
    except Exception as _e_gs:
        return False, f"No se pudo guardar en Google Sheet: {_e_gs}"
from datetime import date, timedelta
from io import BytesIO
import re
DOCENTE="Mario Alberto Diaz Becerra"
st.set_page_config(page_title="Mis Trabajos y Calificaciones", layout="centered", initial_sidebar_state="collapsed")

# FINAL 68: listas ARRIBA, antes de que el programa las use. Asi ya no sale NameError.
LISTAS_FIJAS_UNIDAD = {
"2A": [
"AVILA GONZALEZ ESMERALDA YARITZA",
"CHAPARRO GARFIO MIA MONCERRAT",
"DURAN SAENZ EIMY MARELY",
"ESCOBAR CHAVEZ JULIA MADAHI",
"ESPINOZA CRUZ PEDRO EZEQUIEL CRUZ",
"FABELA CORTEZ YAREL ALONSO",
"FAVELA ESCOBEDO MADELINE ARLETH",
"GAMBOA GONZALEZ ELISA VICTORIA",
"GARCIA PEREZ JOEL EDUARDO",
"HERRERA MANZANARES MARELYN ESTELA",
"HERRERA RAMIREZ IAN SAMIR",
"IBARRA GONZALEZ FERNANDO EMANUEL",
"MEDELLIN PINEDA NICOLAS",
"MENDOZA HOLGUIN JAVIER SAUL",
"MIRANDA RIVERA SEBASTIAN",
"MOLINA LOERA ZULEYMI VICTORIA",
"NEVAREZ URBINA ALISON FERNANDA",
"PALMA IBAÑEZ JAZIEL ALONSO",
"PARRA GONZALEZ JUAN",
"PEREZ RODRIGUEZ OSMARA ALEJANDRA",
"QUINTANA FUENTES MEISY SAMANTHA",
"RAMIREZ ROA IKER SANTIAGO",
"RAMOS ESCARCEGA VALERIA",
"REZA VALENZUELA CIELO IVONNE",
"RUIZ VENZOR LAYLA JOSABETH",
"SALCIDO MENCHACA IVAN CALEB",
"SANCHEZ RAZO FERNANDA ITAI",
"SUAREZ AGUIRRE IKER GAEL",
"TORRES CHAPARRO DANNA VALERIA",
"TORRES RAMOS SARA MARIANNE",
"TRILLO SOLIS IAN PAUL",
"VALDEZ RAMOS SANTIAGO DAMIAN",
"VALDEZ VILLALBA IAN JARED",
"VELOZ ACEVEDO HECTOR ABRAHAM",
"XOLOTL MARTINEZ IHAN KALEHB",
"ZAPATA CRUZ ERICK MATEO"
],
"3A": [
"CARBAJAL VILLAR BRITHANY JAQUELIN",
"CASTILLO GONZALEZ MAHELET SARELY",
"CENTENO FLORES ANGEL GABRIEL",
"CHAPARRO PEREZ GEORGINA",
"CHAVEZ BARRERA LIA AITANA",
"CHAVEZ JR OLIVAS JOSE",
"DOMINGUEZ COVARRUBIAS IVON ARACELY",
"ESPINOZA CORREDOR ANALY HATSUMI",
"FELIX PEREZ OMAR EDUARDO",
"FLORES DE LA CRUZ NICOL ELIZABETH",
"GUERRA MARTINEZ SOFIA SOLEDAD",
"HERNANDEZ MORENO MELANY JULIETT",
"IBARRA GONZALEZ DEREK ALEJANDRO",
"LOZANO DIAZ ERIK APOLONIO",
"LUCERO GONZALEZ DANIEL ELI",
"MENDOZA ENRIQUEZ AMANDA LIZETH",
"NUÑEZ MANCINAS JOEL JERONIMO",
"PERAZA RIVERA EINAR EZEQUIEL",
"PORTILLO RAMOS MARLEN MICHEL",
"SALIDO VALENZUELA JOEL ARIEL",
"VALERIANO MORALES SHELSY YAMILETH"
],
"4A": [
"AVENDAÑO CAMPOS DERECK RENE",
"BIBIANO RODRIGUEZ MELANY ALEXA",
"CANO TORRES YESLI TAMARA",
"CORDOBA GARCIA LARRY YAEL",
"CORRAL TELLEZ MIA JAZMIN",
"DELGADO HERNANDEZ DANIEL ALEJANDRO",
"DIAZ MEZA DILAN LEONARDO",
"DIAZ VILLEZCAS YAEL FERNANDO",
"DOMINGUEZ HERNANDEZ ANDREA",
"DOMINGUEZ ORTEGA NAHOMI MARBELLA",
"ESPINOZA GONZALEZ XIMENA SARAHI",
"ESTEVEZ RAMIREZ HASIEL ISRAEL",
"HERNANDEZ ACEVES JUNIOR ISAAC",
"JAQUEZ PONCE XIMENA ADILENE",
"JAUREGUI VELAZQUEZ GERALDINE CONSUELO",
"JUAREZ MENDOZA JOHANA SOFIA",
"MORENO DANIEL JAZMIN ANAHY",
"MUÑOZ SAPIEN AIDIN SHANTAL",
"OLIVARES LOPEZ JOSHUA ALEJANDRO",
"OLIVAS REY YAZLIN ANDREA",
"PEÑA GONZALEZ RODRIGO",
"REY ESTRADA LIAM SAUL",
"REZA VALENZUELA LUNA YOSELIN",
"RIVERA PADILLA NATALIA NAHOMI",
"ROA RAMOS SARA MICHELLE",
"RODRIGUEZ CORREDOR IKER ADAIR",
"RUBIO VALDEZ IKER AZAEL",
"VEGA ALEMAN ABNER GABRIEL"
],
"4B": [
"ANDAZOLA ROSAS DULCE YARETZI",
"BARFFUSON VILLAGRAN IBRAHIM",
"CARDENAS VELAZQUEZ AARON EDUARDO",
"CHAVEZ OLIVAS ESBEYDI",
"DOMINGUEZ ALCANTAR MIA YAMILETH",
"DOMINGUEZ ALCANTAR RENATA ABIGAIL",
"DOMINGUEZ COVARRUBIAS ABRIL YESENIA",
"FIERRO MORENO SURI VALENTINA",
"GALLEGOS CASTRO JASIEL ALEXIS",
"GARCIA PARRA GABRIEL JACOB",
"GARCIA ZAMARRON HEBER MIGUEL",
"GONZALEZ MONTES ARIANA YAMILETH",
"GRADO AVILA SEBASTIAN",
"HERNANDEZ DE LA TORRE PRISCILA NATALIA",
"HERRERA RAMIREZ ANGEL SEBASTIAN",
"MACIAS MORENO REBECA VICTORIA",
"MEDINA LOPEZ DRAKE SANTIAGO",
"MONGE ESCARCEGA ALONDRA ESTEFANIA",
"PAYAN PIZARRO ARIANA MARELY",
"PEREYRA TAPIA EIMI VICTORIA",
"PORTILLO FLORES PAUL ISAIR",
"QUIROZ PORTILLO CARLOS ALBERTO",
"RAMIREZ ROA AILEN ALEJANDRA",
"REYES LOPEZ THIAGO ISMAEL",
"ROSAS LOPEZ RICARDO ELIAN",
"SALAZAR GONZALEZ MELANNIE AYTHANA",
"SIDAS OLIVAS VICTORIA LILIANA",
"TORRES RAMOS EDDY SEBASTIAN",
"VIOLETA DEL ANGEL JESUS ABRAHAM"
],
"5A": [
"AGUIRRE VEGA AIMEE FERNANDA",
"ALARCON ALVIDREZ ELIAN OBED",
"ALMAZAN SOSA ARLETH ELIZABETH",
"ARMENDARIZ RODRIGUEZ BYRON CALEB",
"AVILA VILLEZCAS EILEEN YUSEL",
"BALTAZAR SOLANO NATHAN LIAM",
"BARRIOS CISNEROS AYLIN DAYANA",
"BECERRIL CAMARILLO SCARLETT ADRIANA",
"BUSTILLOS VELAZQUEZ DARIEL DAVID",
"CAZARES CHAVEZ SAID ALEJANDRO",
"DE AVILA FLORES MARIO DANIEL",
"DOMINGUEZ ORTEGA FREDY ALEXIS",
"ESPINOZA GARCIA ADAM ALBERTO",
"FLORES POLITO ZAYRA VICTORIA",
"GOMEZ ALBINEDA YARETZI ARIANA",
"GONZALEZ OLIVAS ELIAN ALEJANDRO",
"GRANADOS MURILLO BRYANA LIZETH",
"GUEVARA VELASCO GABRIELA CAMILA",
"HERNANDEZ GONZALEZ IKER DANIEL",
"HERNANDEZ RAMIREZ ANGELA YAMILETH",
"LOPEZ ORTEGA VICTOR ALONSO",
"MEDINA BIBIANO DANNA FERNANDA",
"RIVERA GARCIA ANEL FERNANDA",
"RUIZ ANGULO ADILENE MELANIE",
"SAENZ RIVERA IVANNA SAMAI",
"SANCHEZ GONZALEZ YATZIRI VICTORIA",
"SANCHEZ GONZALEZ YURITZI ROMINA",
"SILVA PEREZ AXEL JOEL",
"SMITH LOYA RAMON ALEXIS"
],
"5B": [
"ARENIVAS SANCHEZ ROBERTO ANTONIO",
"BAILON VILLARREAL AXEL JULIAN",
"CARAVEO MENDOZA REICHEL ALEJANDRA",
"CHACON SINALOA AXEL LEONARDO",
"CORDOBA GARCIA ASHLEY NAOMI",
"ESPINOZA DURAN DANIEL ALEJANDRO",
"FRANCO LORIA VALERIA VANESSA",
"GARCIA MARQUEZ LUIS ANGEL",
"GARCIA TREVIZO ALISON MAILEN",
"GONZALEZ LOZOYA ALEXA DAYANA",
"JUAREZ ESPARZA REGINA GABRIELA",
"LARA PERAZA JONATHAN EFREN",
"MANINI FRANCO DANNA ISABELLE",
"MENDOZA FLORES JOSE MAURICIO",
"MORALES PANTALEON ARACELI",
"NAVARRO SUBIAS DANNA SOFIA",
"OLIVAS PIÑON ESTEBAN",
"PAREDES ROMERO ELIAN SAID",
"PEREYRA TAPIA EVAN JAVIER",
"PONCE DE LEON PRIETO OSIRIS RAMON",
"RAMIREZ TRINIDAD SIDNEY JAEN",
"RESENDIZ JUAREZ AYLEEN SOFIA",
"RIVAS DOMINGUEZ BLANCA MARBELLA",
"RIVERA PADILLA AZUL AITANA",
"RODRIGUEZ RODRIGUEZ LUISA IVANNA",
"RODRIGUEZ VALENZUELA GERSON SANTIAGO",
"SINALOA GONZALEZ DELIA MALENY",
"VARGAS GUTIERREZ ASHLEY NICOLE",
"WALKER GENESIS ALEXA"
]
}
LISTAS_FIJAS_SECUNDARIA = {
"1B": [
"AGUIRRE IBARRA ZOE VICTORIA",
"AGUIRRE RAMOS CESAR OMAR",
"ALMARAZ PAREDES ISAIAS",
"CASTRUITA DE LA CRUZ ANGEL ALBERTO",
"CHAPARRO LERMA GENESIS SARAI",
"CONTRERAS GARCIA DANIELA ARIKO",
"COSS TALAMANTES CARLOS DAMIAN",
"DE SANTIAGO AGUILERA SAID ADRIAN",
"DURAN VILLALBA DILANY AMERICA",
"ENRIQUEZ ROMERO LAURA SOFIA",
"GONZALEZ VILLA NATHAN LEHINAD",
"ISLAS SAENZ GENESIS ANDREA",
"LEDEZMA CARRILLO DANNA YAMILETH",
"LOPEZ JAVIER XIMENA VALERIA",
"MARQUEZ ANCHONDO ANGELICA ALEXA",
"MARTINEZ BAYRRUZ MANUEL ALEJANDRO",
"MARTINEZ FERNANDEZ ELISA",
"MENDOZA SILVAS LEIA SOPHIA",
"NUÑEZ LARA FATIMA VIANEY",
"PEREZ GARCIA IKER SANTIAGO",
"PINEDA CHAVEZ ANGEL SAID",
"RAMIREZ DOMINGUEZ ALESSANDRA GUADALUPE",
"ROBLES LOZANO AARON ALEXANDER",
"RODRIGUEZ MONTIEL ALAN GERARDO",
"SALINAS DURAN JOSELYN ITZAYANA",
"SANCHEZ AGUILAR DIANA FERNANDA",
"TREVIZO ACOSTA MARLEY CELESTE",
"VILLALOBOS MORALES XIMENA",
"YAÑEZ DELGADO DERIAN ALEXIS"
],
"3C": [
"ACOSTA ALANIS CARLOS SAID",
"BOLAÑOS ROBLEDO LEONARDO DANIEL",
"CARDENAS FLORES BRAYAN JESUS",
"CASTRUITA DE LA CRUZ AXEL RENE",
"ESCARCEGA ROMAN LUIS ANGEL",
"ESPITIA CLETO HUGO",
"GARCIA LOPEZ ANGEL TADEO",
"MUÑOZ BALLESTEROS IVAN PAOLO",
"PEREZ RONQUILLO KATHERINE SOFIA",
"QUINTANA MARTHA ANGEL ADRIAN",
"RENTERIA TENA ANGEL SANTIAGO",
"ROMERO PORTILLO BRANDON TADEO",
"ROSALES MASCORRO SANTIAGO"
]
}
# ===== FINAL 80: TOMAS GAMEROS ADENTRO DEL CODIGO - leido de LISTAS_DE_LOS_GRUPOS.pdf que mandaste =====
# 1-A 28 + 2-A 28 + 3-A 26 + 4-A 18 + 5-A 18 + 5-B 18 + 6-A 26 = 162 alumnos. Ya no hay que subir su PDF nunca mas.
LISTAS_FIJAS_TOMAS = {
"1A": [
"AGUIRRE OCHOA JESUS FERNANDO",
"ALARCON SOLIS EIDAN ASAHEL",
"BUSTILLOS MORALES ARLETTE ZAHORY",
"CARRILLO GONZALEZ MARCOS JOSE",
"CORCHADO MORENO DAILYN REGINA",
"FLORES GRANADOS MARIBEL",
"GONZALEZ RIOS DILAN",
"HERMOSILLO RIVERO EMILIANO ALEJANDRO",
"HIDALGO CASTILLO JUAN ADRIAN",
"LOYA CANO JESUS ANTONIO",
"MANRIQUEZ DUARTE MELINA",
"MANRIQUEZ DUARTE MELISA",
"MARES SANCHEZ FERNANDO OMAR",
"MATA MENDOZA LUIS ANGEL",
"MEDRANO VILLA LUISA DANIELA",
"MELENDEZ TABURA EDNA REGINA",
"MILLAN VILLALBA ISAAC",
"MIRANDA FRANCO AARON",
"MORALES LOPEZ NATALIA JIMENA",
"NORIEGA FLORES MATIAS",
"PEREZ DEL TORO EMILY SAMANTHA",
"RAMIREZ HIDALGO NOAH PAULETH",
"ROSALES NUÑEZ RENATA VICTORIA",
"RUBIO HINOJOSA ISMAEL",
"RUBIO RAMIREZ ELEAZAR",
"VALAZQUEZ GONZALEZ MAYLIN JOHANA",
"VILLALOBOS ESPARZA REGINA",
"YAÑEZ RAMOS EMMANUEL ALI",
],
"2A": [
"AGUILAR CASTILLO LUIS FERNANDO",
"AGUILAR RODRIGUEZ MARLENE ISABELLA",
"AL KUBAISI NAVA HAYDER KHALID FALAH",
"ARZATE MUÑOZ ENOC ISAY",
"ARZATE MUÑOZ SERGIO ISAIAS",
"CASTILLO JAQUEZ AMERICA DALILA",
"CHAVEZ CARREON AIRAM VALENTINA",
"DELGADO HERNANDEZ CARLOS DANIEL",
"FRANCO VIOLETA MARIO ALEXIS",
"GALLEGOS MOLINA ADAMARIS",
"GOMEZ RUBIO MARIA FERNANDA",
"HERNANDEZ LOZANO AARON ENRIQUE",
"HERNANDEZ LOZANO JULIAN ALONSO",
"HERRERA ESTRADA MANUEL HUMBERTO",
"HOLGUIN VASQUEZ CAMILA ABIGAIL",
"LAREZ SOTO SOFIA VICTORIA",
"LECHUGA LEYVA MATEO",
"LERMA KATAJIRI DAYAMI ANDREA",
"LOPEZ CRUZ SOFIA MABEL",
"MAGALLANES DUARTE PAULETTE NOEMY",
"MELENDEZ CARRILLO TADEO",
"MELENDEZ HOLGUIN DYLAN VIDAL",
"MOLINAR CARDENAS ALAN HUMBERTO",
"MONTES ALDACO ABRAHAM ELIAN",
"NUÑEZ JIMENEZ DAVID SEBASTIAN",
"ORTEGA CARLOS DAMIAN",
"ORTEGA BACA ANDREA",
"TORRES AGUERO DAYLIN NAHOMY",
],
"3A": [
"ALDERETE FIERRO IRVING MANUEL",
"ALVAREZ TARIN ARIEL ALEXANDER",
"ARANDA MARTINEZ ELINA",
"ARMENDARIZ LUJAN SARA ILIANA",
"BURROLA ARMENDARIZ ISABELLA",
"FLORES VEGA CORALINE ALEJANDRA",
"FRANCO ROMERO ARIAN",
"GALLEGOS RIVAS MAURICIO",
"GONZALEZ EMILIO HUMBERTO",
"GONZALEZ CANO HEISOL DANIELA",
"GUERRERO MENDEZ JESUS AARON",
"HERNANDEZ DE LA CRUZ ELIETH SAMARA",
"HERNANDEZ ESPINOZA JUAN SAID",
"LEDEZMA TERRAZAS RAMON",
"MEDINA REYES KAROL ALBERTO",
"MEDRANO VILLA DANIELA AMAIRANY",
"MELENDEZ CARRILLO JR ENRIQUE",
"MELENDEZ TABURA ROGELIO ALBERTO",
"MENDOZA PRIMO KARLA VALERIA",
"MOLINAR CUEVAS MARIA RENATA",
"RAMIREZ CALVILLO JONATHAN DANIEL",
"RICO ARZABALA TADEO LEONEL",
"RUBIO MARQUEZ EMMA GERALDINE",
"SILVA CERA ABRIL ELENA",
"TAPIA SANCHEZ DOMINIC",
"VILLEGAS LOZANO JAZMIN LUCIA",
],
"4A": [
"AGUILAR GONZALEZ BENJAMIN ISAAC",
"ARMENDARIZ FIERRO AARON GERARDO",
"BALDERRAMA ZUBIA IRIS ANDREA",
"BEJAR MACIAS OSCAR MANUEL",
"CARRASCO DELGADO MATEO",
"CHAVIRA BEJARANO EMILY",
"CHAVIRA GONZALEZ LUIS EMILIO",
"DEL HIERRO RODRIGUEZ VICTORIA",
"FIERRO VALENZUELA JOSE RAYMUNDO",
"FLORES CORRAL LIA MARIANA",
"GALLEGOS RIVAS KARLA MICHELL",
"GONZALEZ ORTEGA ALISON GERALDINE",
"GONZALEZ VAZQUEZ KARINA",
"MANRIQUEZ DUARTE ELIAR RAFAEL",
"NAJERA MUÑIZ JORGE LUIS",
"PACHECO VICENCIO CALEB EDUARDO",
"RODRIGUEZ DOMINGUEZ RENATA",
"SOTO OLIVAS RENATA",
],
"5A": [
"ARMENDARIZ NIÑO PAULINA",
"CHAVEZ CALDERON CAMILA",
"ESTRADA RAMIREZ ROBERTA",
"FIGUEROA RODRIGUEZ CARIME IVANA",
"GALLEGOS KEIRY PAOLA",
"GONZALEZ RIOS KEVIN JESUS",
"HIDALGO MURGUIA NYAH PATRICIA",
"LEAL RODRIGUEZ DANTE ANDRE",
"LOPEZ MOLINA BRISA JAZMIN",
"MARTINEZ RUBIO ALEC",
"NAJERA JAQUEZ VALENTINA",
"OLIVAS ELIAS",
"ORTEGA LUIS RAUL",
"RAMOS DOMINGUEZ RENE",
"RIVERO RAMIREZ ERICK ISAAC",
"ROMERO DOMINGUEZ MATEO",
"RUBIO MORALES LUCIANA",
"VALDEZ VILLALOBOS HELEN ANAHY",
],
"5B": [
"ALVIDREZ AGUILAR CESAR ISAAC",
"BELTRAN GALLEGOS AMAIRANY RENATA",
"ESTRADA SAMEER ADRIAN",
"FLORES JOSELIN SCARLETT",
"FLORES CORRAL DEMIAN IRAM",
"HERNANDEZ RODRIGUEZ MAXIMILIANO",
"JAQUEZ CARRILLO CESAR EMILIO",
"MARQUEZ GONZALEZ EDGAR MATEO",
"MEDINA QUEZADA AXEL AARON",
"MOLINAR CARDENAS PAULINA YULISSA",
"NUÑEZ GARDEA LUISA YANELI",
"OCON GONZALEZ JAZIEL ALONSO",
"ORTEGA LOZANO KARLA ISABELLA",
"RAMOS PACHECO OSMAR TADEO",
"RODRIGUEZ ROBERTO",
"RUBIO HINOJOSA LUIS ANGEL",
"TARIN CASTILLO AYLI",
"VILLALOBOS ESPARZA MIA",
],
"6A": [
"AL KUBAISI NAVA ALHASSAN ALI",
"AVILA SAUCEDO DANIELA ROSARIO",
"BALDERRAMA GONZALEZ DYLAN",
"CENICEROS BANDA ZADQUIEL",
"CHAVIRA BEJARANO ISABELLA",
"DELGADO DERMA DEMETRIO",
"FIERRO OLIVAS ANGEL SEBASTIAN",
"GANDARA VENZOR DAEL ALEJANDRO",
"GARCIA VARGAS ANAHI",
"GOMEZ SERRANO KENDRA GISELLE",
"GUERRERO VALENCIA RAUL ISAIAS",
"HERNANDEZ MARTINEZ ALEXA",
"LAZALDE CARMONA DANIA YAMILETH",
"LOPEZ CRUZ SERGIO IRAM",
"MENDIAS MENDOZA LYA JARETH",
"MOLINAR CUEVAS MARIO",
"MUÑOZ GONZALEZ PAUL GERARDO",
"PONCE RUEDA ALISON ARIADNE",
"RABAGO MERINO ALEXA MARILE",
"RIVAS OLAVE KENDRA NICOLE",
"SOSA TORRES MARIA TERESA",
"TERAN SANCHEZ MARCO ELI",
"VELASCO RAMIREZ VICTOR GAEL",
"VELAZQUEZ GONZALEZ ALEXA JOKEBED",
"VENEGAS MOLINA MIGUEL ANGEL",
"VILLALOBOS SAENZ EMIR GERARDO",
],
}
ESCUELA_TOMAS_NOMBRE = "TOMAS GAMEROS # 2131"
ESCUELA_UNIDAD_NOMBRE = "UNIDAD PROLETARIA # 2294"
ESCUELA_SECUNDARIA_NOMBRE = "ESCUELA SECUNDARIA ESTATAL # 3046"

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
.block-container { padding-top: 3.5rem !important; padding-left: 0.8rem !important; padding-right: 0.8rem !important; max-width: 100% !important; }
/* Botones grandes para el dedo, que quepan */
.stButton > button { width: 100% !important; min-height: 48px !important; font-size: 16px !important; white-space: normal !important; height: auto !important; padding: 10px 12px !important; }
.stDownloadButton > button { width: 100% !important; min-height: 48px !important; font-size: 16px !important; white-space: normal !important; height: auto !important; }
/* Que no haga zoom al picar en los cuadritos en el telefono */
input, select, textarea { font-size: 16px !important; }
/* Tablas con scroll a los lados, no aplastadas */
[data-testid="stDataFrame"], [data-testid="stTable"] { overflow-x: auto !important; }
/* Encabezado: foto + titulo */
/* ARREGLO CORTE VISUAL STUDIO: nada se sale a los lados, todo se parte y cabe */
* { box-sizing: border-box !important; }
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] { overflow-x: hidden !important; max-width: 100vw !important; }
.encabezado-wrap { display: flex; justify-content: center; margin: 0; padding: 20px 0 10px 0 !important; width: 100% !important; overflow: visible !important; }
.encabezado-box { display: flex; align-items: center; gap: 10px; margin: 0; padding: 0; width: 100% !important; max-width: 720px !important; flex-wrap: wrap !important; justify-content: center !important; text-align: center !important; }
.encabezado-foto { flex: 0 0 auto !important; max-width: 100% !important; }
.encabezado-foto img { height: 90px !important; max-width: 100% !important; width: auto !important; object-fit: contain; display: block; margin: auto; }
.encabezado-titulo { font-size: clamp(20px, 5vw, 36px) !important; font-weight: 800; color: #FFD400; line-height: 1.25 !important; white-space: normal !important; word-break: break-word !important; overflow-wrap: anywhere !important; max-width: 100% !important; }
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

/* ===== 4 MODOS EN 1 SOLO CODIGO - FINAL 57 ===== */
/* CELULAR: hasta 600px - letra chica, 1 columna, botones grandes para el dedo */
@media (max-width: 600px) {
  .encabezado-foto img { height: 70px !important; }
  .encabezado-titulo { font-size: 22px !important; }
  .stButton > button { min-height: 52px !important; font-size: 17px !important; }
  [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }
  [data-testid="stHorizontalBlock"] > div { flex: 1 1 100% !important; }
}
/* TABLET: 601 a 1024px - mediano, 2 columnas */
@media (min-width: 601px) and (max-width: 1024px) {
  .block-container { max-width: 900px !important; }
  .encabezado-foto img { height: 110px !important; }
  .encabezado-titulo { font-size: 32px !important; }
  .stButton > button { font-size: 17px !important; min-height: 50px !important; }
}
/* LAPTOP: 1025 a 1920px - normal, como siempre */
@media (min-width: 1025px) and (max-width: 1920px) {
  .block-container { max-width: 1100px !important; }
  .encabezado-foto img { height: 130px !important; }
  .encabezado-titulo { font-size: 38px !important; }
}
/* ANTI-EMPALME CELULAR FINAL 62: botones que no se cortan, se parten en 2 renglones */
@media (max-width: 600px) {
  .stButton > button, .stDownloadButton > button { white-space: normal !important; overflow-wrap: anywhere !important; text-overflow: clip !important; height: auto !important; min-height: 52px !important; line-height: 1.2 !important; }
  [data-testid="stVerticalBlock"] { overflow-x: hidden !important; }
}
/* ANTI-EMPALME CELULAR FINAL 61: nada se encima, todo una abajo de otra, con aire */
@media (max-width: 600px) {
  [data-testid="stHorizontalBlock"] { flex-direction: column !important; gap: 12px !important; }
  [data-testid="stHorizontalBlock"] > div { width: 100% !important; max-width: 100% !important; min-width: 0 !important; }
  .stButton > button, .stDownloadButton > button { margin-bottom: 8px !important; }
  [data-testid="stVerticalBlock"] > div { overflow: visible !important; }
  h1, h2, h3 { overflow-wrap: anywhere !important; }
}
/* TV / PANTALLA GRANDE: mas de 1921px - todo gigante para que se vea de lejos */
@media (min-width: 1921px) {
  .block-container { max-width: 1600px !important; }
  .encabezado-foto img { height: 180px !important; }
  .encabezado-titulo { font-size: 56px !important; }
  .encabezado-docente { font-size: 32px !important; }
  h1 { font-size: 48px !important; } h2 { font-size: 40px !important; } h3 { font-size: 32px !important; }
  p, li, div, .stButton > button { font-size: 24px !important; }
  .stButton > button { min-height: 70px !important; padding: 18px !important; }
  input, select, textarea { font-size: 22px !important; }
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
    <div style="flex:1 1 220px;min-width:0;text-align:center;line-height:1.1;">
      <div class="encabezado-titulo">⭐ Mis Trabajos y Calificaciones</div>
      <div class="encabezado-docente">Docente: Mario Alberto Diaz Becerra</div>
    </div>
  </div>
</div>
"""
        st.markdown(html, unsafe_allow_html=True)
    except:
        st.markdown("<h1 style='text-align:center;font-size:clamp(22px,6vw,36px);word-break:break-word;'>⭐ Mis Trabajos y Calificaciones</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;font-size:clamp(14px,4vw,20px);word-break:break-word;'>Docente: Mario Alberto Diaz Becerra</p>", unsafe_allow_html=True)

# ===== FINAL 79: YA NO SE USA NINGUN JSON DE LA NUBE =====
# Los archivos listas.json, trimestres.json y dias_clase.json YA NO SE RESPETAN porque Streamlit Cloud los BORRA cada vez que se reinicia o subes una version nueva.
# Por eso desaparecieron tus listas y tus trimestres: no es que el programa no los leyera, es que la nube ya los habia borrado antes de abrir.
# A partir de ahora: TODO vive ADENTRO DEL CODIGO (UNIDAD 172, SECUNDARIA 42, los 3 trimestres, los dias por defecto) + en la memoria mientras usas la app.
# Lo UNICO que si se guarda de verdad es el RESPALDO que TU descargas con el boton "Descargar Respaldo" y que TU vuelves a subir con "Restaurar Respaldo" cuando subas una version nueva.
# Ya no se escribe ni se lee ningun .json de la nube.
def _guardar_listas_archivo():
    # FINAL 120: Ya NO manda sola al Sheet cada que abres algo, porque eso duplicaba sin que te metieras al alumno.
    # Solo se manda cuando le das a Guardar, a Borrar este dia, o a Probar.
    return
def _cargar_listas_archivo():
    # FINAL 79: ya no se lee listas.json de la nube, porque la nube lo borra. Se regresa vacio y las listas fijas de abajo (UNIDAD + SECUNDARIA) son las que cargan.
    return [], []
if "alumnos" not in st.session_state: st.session_state.alumnos=[]
if "registros" not in st.session_state: st.session_state.registros=[]
if "registros" in st.session_state and not st.session_state.registros and not st.session_state.get("_sheet_cargado", False):
    _cargar_desde_gsheets()
# Al abrir, si no hay nada en memoria pero si hay listas.json, cargarlo
if not st.session_state.alumnos and not st.session_state.registros:
    _al, _rg = _cargar_listas_archivo()
    if _al: st.session_state.alumnos = _al
    if _rg: st.session_state.registros = _rg
# FINAL 77: SE QUITO TODO LO DEL LINK ?escuela=&grupo=&alumno= . Eso era lo que te trababa el celular.
# Ya no se guarda ni se lee nada del link. La navegacion es solo con botones, asi no se cicla ni se inhabilita nada.
# Si te sales a WhatsApp y regresas, vuelves al inicio y le picas de nuevo a tu escuela y grupo. Es 2 clics, pero nunca se traba.
# FINAL 67: cargar listas fijas leidas de tus PDFs si todavia no estan. No duplica, no borra capturas.
for _esc_fija, _listas_fija in [(ESCUELA_TOMAS_NOMBRE, LISTAS_FIJAS_TOMAS), (ESCUELA_UNIDAD_NOMBRE, LISTAS_FIJAS_UNIDAD), (ESCUELA_SECUNDARIA_NOMBRE, LISTAS_FIJAS_SECUNDARIA)]:
    for _g_fija, _nombres_fija in _listas_fija.items():
        for _n_fija in _nombres_fija:
            _ex = any(a.get("Nombre","").lower()==_n_fija.lower() and a.get("Grupo")==_g_fija and a.get("Escuela")==_esc_fija for a in st.session_state.alumnos)
            if not _ex:
                _mat_fija = "Artes" if (_esc_fija==ESCUELA_SECUNDARIA_NOMBRE and _g_fija=="1B") else ("Electrónica" if _esc_fija==ESCUELA_SECUNDARIA_NOMBRE else "Primaria")
                st.session_state.alumnos.append({"Nombre": _n_fija, "Escuela": _esc_fija, "Grupo": _g_fija, "Materia": _mat_fija})

# FINAL 77: tambien se quito el segundo bloque que escribia en el link a cada rato. Ese era el que hacia que el celular se recargara solo y se inhabilitaran los botones.
if "escuela_activa" not in st.session_state: st.session_state.escuela_activa=None
if "alumno_activo" not in st.session_state: st.session_state.alumno_activo=None
if "trimestre" not in st.session_state: st.session_state.trimestre="Trimestre 2"
if "tri_inicio" not in st.session_state: st.session_state.tri_inicio=date(2026,11,16)
if "tri_fin" not in st.session_state: st.session_state.tri_fin=date(2027,3,6)
if "trimestre_cargado" not in st.session_state: st.session_state.trimestre_cargado=False
if "trimestre_cargado_nombre" not in st.session_state: st.session_state.trimestre_cargado_nombre=""
# ===== DIAS GUARDADOS EN ARCHIVO - para que no se borren al cambiar de grupo, regresar, o cerrar y abrir =====
# Antes los dias solo vivian en la memoria de la pagina (session_state). Si Streamlit recargaba, si cambiabas de grupo y regresabas, o si se reiniciaba el Deploy, se borraban y te los volvia a pedir.
# Ahora cada que le picas a Guardar dias, se escriben en dias_clase.json en la misma carpeta, y al abrir se leen de ahi.
def _cargar_dias_archivo():
    # FINAL 79: ya no se lee dias_clase.json de la nube. Los dias viven en memoria + en tu Respaldo.
    return {}, {}
def _guardar_dias_archivo():
    # FINAL 79: ya no se escribe dias_clase.json.
    return
if "dias_clase" not in st.session_state: st.session_state.dias_clase={}
if "dias_confirmados" not in st.session_state: st.session_state.dias_confirmados={}
# ===== FINAL 82: DIAS FIJOS DE PRIMARIAS ADENTRO DEL CODIGO - ya no hay que ponerlos =====
# Te los paso el profe el 16 nov 2026. Primarias NO cambian en todo el ciclo, por eso van adentro.
# Lunes=0, Martes=1, Miercoles=2, Jueves=3, Viernes=4
# TOMAS: 1A Lunes, 2A Miercoles, 3A Miercoles, 4A Lunes, 5A Miercoles, 5B Lunes, 6A Lunes
# UNIDAD: 2A Martes, 3A Martes, 4A Martes, 4B Jueves, 5A Jueves, 5B Jueves
# SECUNDARIA NO VA AQUI: ahi si te cambian horario cada mes, por eso esos dias SI los sigues cambiando tu.
DIAS_FIJOS_PRIMARIAS = {
    "TOMAS GAMEROS # 2131|1A": [0],
    "TOMAS GAMEROS # 2131|2A": [2],
    "TOMAS GAMEROS # 2131|3A": [2],
    "TOMAS GAMEROS # 2131|4A": [0],
    "TOMAS GAMEROS # 2131|5A": [2],
    "TOMAS GAMEROS # 2131|5B": [0],
    "TOMAS GAMEROS # 2131|6A": [0],
    "UNIDAD PROLETARIA # 2294|2A": [1],
    "UNIDAD PROLETARIA # 2294|3A": [1],
    "UNIDAD PROLETARIA # 2294|4A": [1],
    "UNIDAD PROLETARIA # 2294|4B": [3],
    "UNIDAD PROLETARIA # 2294|5A": [3],
    "UNIDAD PROLETARIA # 2294|5B": [3],
}
# Al abrir, poner los dias fijos de primarias y marcarlos como confirmados. Si ya tenias otros dias en primarias, estos los corrigen solos.
# Secundaria NO se toca, esos los sigues poniendo tu cada mes.
for _llave_fija, _dias_fijos in DIAS_FIJOS_PRIMARIAS.items():
    st.session_state.dias_clase[_llave_fija] = list(_dias_fijos)
    st.session_state.dias_confirmados[_llave_fija] = True
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
# FINAL 78: trimestres POR DEFECTO adentro del codigo. Si la nube borra trimestres.json al reiniciarse, ya no se queda en blanco.
# FINAL 81: TRIMESTRES CORREGIDOS por el profe el 16 nov 2026 - ya no son los de antes
# Trimestre 1: 31 ago al 14 nov 2026 / Trimestre 2: 16 nov al 6 mar 2027 / Trimestre 3: 8 mar al 4 jul 2027
# Hoy 16 nov 2026 ya cae en Trimestre 2, por eso al abrir debe decir Trimestre 2 solo.
TRIMESTRES_POR_DEFECTO = [
    {"nombre": "Trimestre 1", "inicio": "2026-08-31", "fin": "2026-11-14"},
    {"nombre": "Trimestre 2", "inicio": "2026-11-16", "fin": "2027-03-06"},
    {"nombre": "Trimestre 3", "inicio": "2027-03-08", "fin": "2027-07-04"},
]
def _cargar_trimestres_archivo():
    # FINAL 79: ya no se lee trimestres.json. Siempre se usan los 3 de adentro del codigo, por eso ya no se pierde ninguno.
    return list(TRIMESTRES_POR_DEFECTO)
def _guardar_trimestre_archivo(nombre_tri, ini, fin):
    # FINAL 79: ya no se escribe trimestres.json (la nube lo borra). Se actualiza solo en memoria y en los defaults de arriba.
    try:
        _lista = _cargar_trimestres_archivo()
        _encontrado = False
        for _it in _lista:
            if _it.get("nombre") == nombre_tri:
                _it["inicio"] = str(ini); _it["fin"] = str(fin); _encontrado = True
        if not _encontrado:
            _lista.append({"nombre": nombre_tri, "inicio": str(ini), "fin": str(fin)})
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
# ===== FINAL 72: PUNTUACION Y PESOS - TODO SUMA A LA CALIFICACION FINAL =====
PESOS_FINAL = {"Asistencia": 5, "Trabajos": 30, "Tareas": 5, "Conducta": 10, "Practicas": 25, "Proyecto": 25}
# FINAL 83: PESOS POR ESCUELA - Primaria se queda tal cual, Secundaria cambia
# Primaria (TOMAS + UNIDAD): Asistencia 5%, Trabajos 30%, Tareas 5%, Conducta 10%, Practicas 25%, Proyecto 25% = 100%
# Secundaria: Asistencia 0% (se le quita), Examen 10%, Trabajos 20%, Tareas 10%, Conducta 10%, Practicas 25%, Proyecto 25% = 100%
PESOS_PRIMARIA = {"Asistencia": 5, "Trabajos": 30, "Tareas": 5, "Conducta": 10, "Practicas": 25, "Proyecto": 25}
PESOS_SECUNDARIA = {"Asistencia": 0, "Examen": 10, "Trabajos": 20, "Tareas": 10, "Conducta": 10, "Practicas": 25, "Proyecto": 25}
# Fecha del examen solo secundaria - se guarda en session_state, se configura por grupo
if "fecha_examen_sec" not in st.session_state: st.session_state.fecha_examen_sec = {}
if "examen_configurado" not in st.session_state: st.session_state.examen_configurado = {}
# FINAL 92: METAS DEL TRIMESTRE - cuantos vas a calificar, para que el programa sepa la base
if "metas_trimestre" not in st.session_state: st.session_state.metas_trimestre = {}
# FINAL 86: PUNTOS MAS PAREJOS Y EQUITATIVOS - corregido como pidio el profe
# Trabajos: a destiempo pero bien ya no baja a 6, ahora es 8. A medias 6. A destiempo e incompleto 1.
PUNTOS_ASISTENCIA = {"😊 Asistió": 10, "⏰ Retardo": 8, "😢 Falta": 0}
PUNTOS_TRABAJO = {"Entrega en tiempo y forma, como se pidió": 10, "Entrega a destiempo": 8, "Entrega trabajo a medias": 6, "Hizo el trabajo solo por hacerlo": 3, "Entrega a destiempo e incompleto": 1, "Actividad no realizada": 0, "No cuenta con material": 0, "No se pidió": None, "📄✅ Entregó": 10, "📄❌ No entregó": 0, "Sin material de trabajo": 0}
PUNTOS_TAREA = {"✉️ Entregó": 10, "✉️❌ No entregó": 0, "No se pidió": None}
# FINAL 88: CONDUCTA COMO ESTABA, PERO CON RESTA - empieza en 10 y le quita lo que hizo mal
# Ninguna = 10 (no le quita nada)
# Conversación en clase quita 1 -> 9
# No siguió instrucciones quita 1 -> 9
# Se levantó sin autorización quita 3 -> 7
# Uso de dispositivos quita 6 -> 4
# Genera distracción quita 8 -> 2
# Falta de respeto quita 10 -> 0
# FINAL 89: CONDUCTA SON DECIMAS - por orden de gravedad, como lo dijo el profe
# Ninguna 0, Conversación 1, No siguió 1, Se levantó 3, Dispositivos 6, Distracción 8, Falta respeto 10
# 1 decima = 0.1 puntos. Si ofende, le quita 10 decimas = 1.0 punto. Así hasta que se quede sin ese 10%.
PUNTOS_CONDUCTA_DECIMAS = {"Ninguna": 0, "Conversación durante la clase": 1, "Falta de respeto a compañero o docente": 10, "Se levantó de su lugar sin autorización": 3, "No siguió las instrucciones": 1, "Uso de dispositivos electrónicos en clase": 6, "Genera distracción en sus compañeros": 8, "Trabajos": 3, "Sin material de trabajo": 3, "Actividad no realizada": 3}
PUNTOS_CONDUCTA = {"Ninguna": 10, "Conversación durante la clase": 9, "Falta de respeto a compañero o docente": 0, "Se levantó de su lugar sin autorización": 7, "No siguió las instrucciones": 9, "Uso de dispositivos electrónicos en clase": 4, "Genera distracción en sus compañeros": 2, "Trabajos": 6, "Sin material de trabajo": 6, "Actividad no realizada": 6}
PUNTOS_PRACTICA = {"Entrega práctica en tiempo y forma": 10, "Entrega práctica a destiempo": 8, "Entrega práctica a destiempo e incompleta": 5, "Entrega práctica a destiempo haciendo lo que quiso": 3, "No entrega práctica": 0, "No se pidió": None}
PUNTOS_PROYECTO = {"Entrega proyecto en tiempo y forma": 10, "Entrega a destiempo": 8, "Entrega a destiempo e incompleto": 5, "Entrega a destiempo y haciendo lo que quiso": 3, "No entrega proyecto": 0, "Todavía no se pide": None, "No se pidió": None}
LISTA_CONDUCTAS = ["Ninguna","Conversación durante la clase","Falta de respeto a compañero o docente","Se levantó de su lugar sin autorización","No siguió las instrucciones","Uso de dispositivos electrónicos en clase","Genera distracción en sus compañeros","Trabajos"]
LISTA_TRABAJOS = ["Entrega en tiempo y forma, como se pidió","Entrega a destiempo","Entrega trabajo a medias","Hizo el trabajo solo por hacerlo","Entrega a destiempo e incompleto","Actividad no realizada","No cuenta con material","No se pidió"]
LISTA_PRACTICAS = ["No se pidió","Entrega práctica en tiempo y forma","Entrega práctica a destiempo","Entrega práctica a destiempo e incompleta","Entrega práctica a destiempo haciendo lo que quiso","No entrega práctica"]
LISTA_PROYECTOS = ["Todavía no se pide","Entrega proyecto en tiempo y forma","Entrega a destiempo","Entrega a destiempo e incompleto","Entrega a destiempo y haciendo lo que quiso","No entrega proyecto"]
def _puntos(mapa, valor):
    if valor is None: return None
    v = str(valor).strip()
    if v in mapa: return mapa[v]
    return None
def calcular_calificacion_final(nombre, escuela, grupo):
    regs = [r for r in st.session_state.registros if r.get("Alumno")==nombre and r.get("Escuela")==escuela and r.get("Grupo")==grupo]
    _tri = st.session_state.get("trimestre_cargado_nombre")
    if _tri:
        regs = [r for r in regs if r.get("Trimestre")==_tri]
    if not regs: return None
    _metas_g = st.session_state.get("metas_trimestre", {}).get(f"{escuela}|{grupo}", {})
    def _prom(mapa, campo, meta_key=None):
        # FINAL 120: Solo contar lo que SI se evaluo ese dia. Si ese dia no se puso Practica/Proyecto/Tarea, no cuenta, no baja la calificacion.
        # Valores que significan "no se evaluo ese dia" no son 0, son None.
        _NO_EVALUADO = {"", None, "Sin práctica", "Sin practica", "Sin proyecto", "Sin tarea", "Sin trabajo", "No aplica", "No se evaluó", "No se evaluo", "Ninguno", "Ninguna", "Sin examen", "Sin asistencia", "-"}
        pts = []
        for r in regs:
            _v = r.get(campo)
            if str(_v).strip() in _NO_EVALUADO or _v in _NO_EVALUADO:
                continue
            _p = _puntos(mapa, _v)
            if _p is not None:
                pts.append(_p)
        if not pts and not _metas_g.get(meta_key):
            return None, 0
        if not pts:
            return 0.0, 0
        _meta = _metas_g.get(meta_key) if meta_key else None
        if _meta and isinstance(_meta, (int, float)) and _meta > 0:
            _faltan = max(0, int(_meta) - len(pts))
            _suma = sum(pts) + 0 * _faltan
            return _suma / int(_meta), len(pts)
        return sum(pts)/len(pts), len(pts)
    prom_asis, n_asis = _prom(PUNTOS_ASISTENCIA, "Estado", None)
    prom_trab, n_trab = _prom(PUNTOS_TRABAJO, "Trabajo", "Trabajos")
    prom_tar, n_tar = _prom(PUNTOS_TAREA, "Tarea", "Tareas")
    # FINAL 88: CONDUCTA RESTA, BUENA CONDUCTA SUMA +1
    # Conducta (lo malo) SOLO RESTA: Ninguna=10, si se porta mal baja a 8 o 6, falta de respeto=0
    # Conducta Positiva (Felicitaciones / Excelente) AHORA VIVE ADENTRO DE CONDUCTA, ya no es decimas aparte:
    #   Felicitacion = 8, Excelente desempeno = 10, Excelente + Felicitacion = 10, Ninguno = no cuenta
    # Por dia: si no hay felicitación, queda su conducta normal. Si sí hay, se promedia: (Conducta + Positiva)/2
    # Ejemplo: Conversó (8) + Felicitación (8) = 8.0. No siguió instrucciones (6) + Excelente (10) = 8.0
    # Si tiene Falta de respeto (0), la positiva NO lo salva, se queda en 0. Así sí le perjudica.
    # Así la Conducta al final solo da su 10% completo si SIEMPRE se portó bien o tuvo excelente.
    # FINAL 88: BUENA CONDUCTA suma +1 cada vez, para juntar el 10% faltante
    # Felicitaciones +1, Buen trabajo +1, Ayuda a sus compañeros +1, Excelente desempeño +1, Atento +1
    # Si siempre tuvo indisciplina y nunca tuvo buena conducta, se queda en 0% en ese apartado y su calificación baja.
    # Se suma al puntaje de conducta de ese día, máximo 10. Si tiene Falta de respeto (0), la buena NO lo salva.
    # FINAL 89: BUENA CONDUCTA da 1 decima cada una = +0.1. Si tuvo buena, genera ese 10%. Si no, se queda en 0%.
    PUNTOS_POSITIVA = {"Ninguno": 0, "Ninguna": 0, "": 0, "Felicitaciones": 1, "Buen trabajo": 1, "Ayuda a sus compañeros": 1, "Excelente desempeño": 1, "Atento": 1, "Excelente desempeño en la actividad": 1, "Felicitación por buen trabajo": 1, "Felicitación por ayuda a compañeros": 1, "Excelente desempeño + Felicitación": 1}
    regs_ordenados = sorted(regs, key=lambda x: x.get("Fecha",""))
    _conteo_reinc_acum = {}
    _n_reincidencia = 0
    pts_cond=[]
    _n_excelente = 0
    _n_felicitacion = 0
    # FINAL 89: Conducta = 10 - (decimas quitadas - decimas ganadas) / 10
    _decimas_quitadas = 0
    _decimas_ganadas = 0
    for r in regs_ordenados:
        _ind = r.get("Indisciplina")
        _dec = PUNTOS_CONDUCTA_DECIMAS.get(str(_ind).strip(), 0) if _ind else 0
        _re = r.get("Reincidencia")
        if _re and str(_re).strip()!="" and str(_re).strip()!="Ninguna":
            _n_reincidencia += 1
            _conteo_reinc_acum[_re] = _conteo_reinc_acum.get(_re, 0) + 1
            if _conteo_reinc_acum[_re] >= 2:
                _dec += 1
        _decimas_quitadas += _dec
        _exc = r.get("Excelente")
        _p_pos = PUNTOS_POSITIVA.get(str(_exc).strip(), 0) if _exc else 0
        if _p_pos:
            _n_excelente += 1
            if "Felicitación" in str(_exc) or "Felicitaciones" in str(_exc): _n_felicitacion += 1
        _decimas_ganadas += _p_pos
        pts_cond.append(1)
    # FINAL 91: CONDICIONANTE DEL PROFE - Si no alcanza decimas positivas y arroja negativas, en ese apartado tiene 0%
    # Neta = ganadas - quitadas. Ejemplo: +5 - 15 = -10 decimas -> NO se le resta -1.0 extra, se le pone 0% en Conducta.
    # O sea, pierde todo ese 10% de Conducta, pero no le quitamos mas alla de ese 10%.
    # Si la neta es positiva, esa es su conducta: neta decimas = puntos en Conducta (max 10). Ej: +5 = 5.0, +10 = 10.0
    _net_decimas_conducta = _decimas_ganadas - _decimas_quitadas
    # FINAL 120: Reincidencia baja 0.2 aparte de la conducta. Ej: 1 reincidencia = -0.2, 2 reincidencias = -0.4
    # Conducta se queda igual, solo se agrega esto.
    _decimas_extras = -0.2 * float(_n_reincidencia)
    # FINAL 120: Aviso si tiene 3 reincidencias seguidas de la misma indisciplina - para mandar reporte al profe y al director/a
    _alerta_reporte = False
    _reincidencia_aviso = ""
    _racha = []
    for _r_av in regs_ordenados:
        _re_av = str(_r_av.get("Reincidencia","") or "").strip()
        if _re_av and _re_av != "Ninguna":
            if _racha and _racha[-1] == _re_av:
                _racha.append(_re_av)
            else:
                _racha = [_re_av]
            if len(_racha) >= 3:
                _alerta_reporte = True
                _reincidencia_aviso = _re_av
                break
        else:
            _racha = []
    if pts_cond:
        # FINAL 120: Conducta = 10 - quitadas + ganadas, no solo neta. Si no se porto mal y tiene 1 felicitacion, es 10, no 1.
        # Ejemplo: 0 quitadas + 1 ganada = 10. 1 quitada + 0 ganadas = 9. 10 quitadas = 0.
        prom_cond = max(0.0, min(10.0, 10.0 - float(_decimas_quitadas) + float(_decimas_ganadas)))
        _aporte_conducta = 0.0
    else:
        prom_cond = None
        _net_decimas_conducta = 0
        _aporte_conducta = 0.0
    n_cond = len(pts_cond)
    prom_prac, n_prac = _prom(PUNTOS_PRACTICA, "Practica", "Practicas")
    prom_proy, n_proy = _prom(PUNTOS_PROYECTO, "Proyecto", "Proyecto")
    # FINAL 83: Examen solo secundaria - calificacion del 5 al 10 que se captura en la ficha, se promedia
    _es_sec = (escuela == ESCUELA_SECUNDARIA_NOMBRE)
    _pesos = PESOS_SECUNDARIA if _es_sec else PESOS_PRIMARIA
    # Examen: buscar registros con campo Examen (numero 5-10). Si no hay, no cuenta.
    _pts_ex = []
    for _r in regs:
        _ex = _r.get("Examen")
        if _ex is not None and str(_ex) != "" and str(_ex) != "Sin examen":
            try: _pts_ex.append(float(_ex))
            except: pass
    _meta_ex = _metas_g.get("Examen") if _metas_g else None
    if _pts_ex:
        prom_ex = sum(_pts_ex) / int(_meta_ex) if (_meta_ex and _meta_ex > 0) else sum(_pts_ex)/len(_pts_ex)
    else:
        prom_ex = 0.0 if (_meta_ex and _meta_ex > 0) else None
    n_ex = len(_pts_ex)
    # FINAL 91: Conducta SI entra con su peso 10, pero si la neta es negativa vale 0%. Asi pierde ese 10% completo, no mas.
    if _es_sec:
        detalle = {"Asistencia": (prom_asis, n_asis, 0), "Examen": (prom_ex, n_ex, 10), "Trabajos": (prom_trab, n_trab, 20), "Tareas": (prom_tar, n_tar, 10), "Conducta": (prom_cond, n_cond, 10), "Practicas": (prom_prac, n_prac, 25), "Proyecto": (prom_proy, n_proy, 25)}
    else:
        detalle = {"Asistencia": (prom_asis, n_asis, 5), "Trabajos": (prom_trab, n_trab, 30), "Tareas": (prom_tar, n_tar, 5), "Conducta": (prom_cond, n_cond, 10), "Practicas": (prom_prac, n_prac, 25), "Proyecto": (prom_proy, n_proy, 25)}
    total_peso=0; total_pts=0
    for k,(prom,n,peso) in detalle.items():
        if prom is not None:
            total_peso+=peso; total_pts+=(prom/10)*peso
    if total_peso==0: return None
    cal_base = total_pts/total_peso*10
    # FINAL 91: Conducta ya va adentro del ponderado con peso 10 y valor 0% si la neta es negativa. No se suma aparte.
    cal = max(0.0, min(10.0, cal_base + _decimas_extras))
    es_final = (prom_prac is not None and prom_proy is not None)
    return {"cal": cal, "cal_base": cal_base, "decimas": _decimas_extras, "n_reincidencia": _n_reincidencia, "alerta_reporte": _alerta_reporte, "reincidencia_aviso": _reincidencia_aviso, "n_excelente": _n_excelente, "detalle": detalle, "total_peso": total_peso, "es_final": es_final, "n_regs": len(regs), "net_decimas_conducta": _net_decimas_conducta, "aporte_conducta": _aporte_conducta, "decimas_quitadas": _decimas_quitadas, "decimas_ganadas": _decimas_ganadas}

def calcular_riesgo(faltas, no_trab, no_tarea, indis_n):
    puntos=faltas*2 + no_trab*2 + no_tarea*1 + indis_n*1
    # FINAL 94: Textos cortos, sin repetir lo de la calificacion - el promedio ya lo dice
    if faltas>=4 or no_trab>=4 or puntos>=10: return "ROJO", "ROJO"
    elif faltas>=2 or no_trab>=2 or puntos>=5: return "AMARILLO", "AMARILLO"
    else: return "VERDE", "VERDE"
def riesgo_de_alumno(nombre, escuela, grupo):
    regs=[r for r in st.session_state.registros if r["Alumno"]==nombre and r.get("Escuela")==escuela and r.get("Grupo")==grupo]
    faltas=len([r for r in regs if "Falta" in r["Estado"]])
    retardos=len([r for r in regs if "Retardo" in r["Estado"]])
    no_trab=len([r for r in regs if "No entregó" in r["Trabajo"]])
    no_tarea=len([r for r in regs if "No entregó" in r["Tarea"]])
    indis_n=len([r for r in regs if r["Indisciplina"]!="Ninguna"])
    nivel, texto = calcular_riesgo(faltas, no_trab, no_tarea, indis_n)
    # FINAL 93: NIVEL POR CALIFICACION FINAL - como lo pidio el profe
    # Verde 8 a 10, Amarillo 6 a 7.9, Rojo menos de 6. Si ya esta en rojo por faltas, se queda en rojo.
    # Si su calificacion es menor de 6, aunque no tenga tantas faltas, se va a rojo directo porque va reprobando.
    try:
        _calc_riesgo = calcular_calificacion_final(nombre, escuela, grupo)
        if _calc_riesgo:
            _cal_r = _calc_riesgo["cal"]
            if _cal_r < 6.0:
                nivel, texto = "ROJO", "ROJO"
            elif _cal_r < 8.0 and nivel == "VERDE":
                nivel, texto = "AMARILLO", "AMARILLO"
            elif _cal_r >= 8.0 and nivel == "AMARILLO":
                # Si tiene calificacion alta pero tiene faltas, se queda en amarillo por las faltas, no baja a verde
                pass
    except:
        pass
    return nivel, texto, faltas, retardos, no_trab, no_tarea, indis_n, regs
def trimestre_terminado():
    return hoy > st.session_state.tri_fin

# ===== LISTAS FIJAS LEIDAS DE TUS PDFs - FINAL 67 =====

def procesar_un_pdf(datos_pdf, escuela, nombre_archivo, grupo_forzado="Auto - que el programa detecte solo (recomendado)"):
    # FINAL 102 - GOOGLE SHEET POR APPS SCRIPT WEBHOOK, RECONSTRUIDA DESDE 99, SIN ERROR NAMEERROR REHECHO LIMPIO: NO adivina nada. Escuela y grupo son los que TU elegiste arriba.
    # Si dejas el grupo en Auto, NO carga nada y te dice que elijas el grupo a mano. Asi ya no mezcla UNIDAD con TOMAS.
    import fitz
    # FINAL 66: AUTO SI SIRVE, como antes. Auto = detectar el grupo por pagina, leyendo lo que dice el PDF (1A, 2A, 1B, 3C, etc).
    # Solo es error si no viene nada. Auto ya no es error.
    es_auto = (grupo_forzado in ("Auto - que el programa detecte solo (recomendado)", "Auto - que el programa detecte solo (recomendado)", "Auto", None, "")) or (isinstance(grupo_forzado, str) and grupo_forzado.strip()=="")
    es_mixto = isinstance(grupo_forzado, str) and grupo_forzado.startswith("MIXTO_")
    if not grupo_forzado and not es_auto:
        return 0, {"ERROR_GRUPO": "El programa detecta el grupo solo. Si sale mal, elige el grupo a mano."}, ["Elige el grupo a mano."]
    if es_auto:
        grupo_fijo = None
        grupos_mixto = []
    elif es_mixto:
        # MIXTO_1B_3C -> grupos = ["1B","3C"]
        _partes = grupo_forzado.replace("MIXTO_","").split("_")
        grupos_mixto = _partes
        grupo_fijo = grupos_mixto[0]
    else:
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
        if es_auto:
            # Detectar grupo de ESTA pagina, como antes: buscar "GRUPO 2A", "GRUPO: 2A", "1 - A", "1A", "2A", etc. en las primeras lineas.
            _txt = texto_pag.upper()
            _det = None
            # Buscar "GRUPO 1A", "GRUPO: 1A", "GRUPO 1 - A", etc.
            _m = re.search(r"GRUPO\s*[:\-]?\s*([1-6])\s*[-\s]*([A-C])", _txt)
            if not _m:
                _m = re.search(r"(?:GRADO/GRUPO|GRUPO/SECCI[OÓ]N|GRUPO)\s*[:\-]?\s*([1-6])\s*-\s*([A-C])", _txt)
            if not _m:
                for _linea_head in texto_pag.split("\n")[:12]:
                    _mh = re.match(r"\s*([1-6])\s*-\s*([A-C])\s*$", _linea_head.strip())
                    if _mh:
                        _m = _mh; break
            if _m:
                _det = _m.group(1) + _m.group(2)
            else:
                # Buscar "1A", "2A", "1B", "3C" solito en el encabezado (primeras 15 lineas)
                _head = "\n".join(texto_pag.split("\n")[:15]).upper()
                for _g in ["1A","2A","3A","4A","5A","5B","6A","1B","3B","3C","1C","2B","2C"]:
                    if re.search(r"(?<![A-Z0-9])" + _g + r"(?![A-Z0-9])", _head):
                        _det = _g; break
            if _det:
                grupo_actual = _det
                grupo_fijo = _det  # Para las paginas que no traen grupo, usar el ultimo que si traia
            elif grupo_fijo:
                grupo_actual = grupo_fijo
            else:
                grupo_actual = "SIN_GRUPO"
                # Si no detecto grupo en esta pagina, saltarla (no cargarla en un solo grupo a lo menso)
                continue
        if es_mixto:
            # Buscar en la pagina cual grupo dice: "1B", "3C", "3A", "3B". El que aparezca mas, ese es el grupo de esa pagina.
            _txt_up = texto_pag.upper()
            _mejor = grupo_fijo; _mejor_n = 0
            for _g in grupos_mixto:
                _n = _txt_up.count(_g)
                if _n > _mejor_n:
                    _mejor_n = _n; _mejor = _g
            grupo_actual = _mejor
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
        grupo_pag = grupo_fijo if grupo_fijo else "SIN_GRUPO"
        if es_auto:
            # En el segundo pase, usar el grupo que ya se detecto en el primer pase para esta pagina, si no, buscarlo otra vez
            _txt2 = texto_pag.upper()
            _m2 = re.search(r"GRUPO\s*[:\-]?\s*([1-6])\s*[-\s]*([A-C])", _txt2)
            if _m2:
                grupo_pag = _m2.group(1) + _m2.group(2)
            elif grupo_fijo:
                grupo_pag = grupo_fijo
            else:
                continue
        if es_mixto:
            _txt_up2 = texto_pag.upper(); _mejor2 = grupo_fijo; _mejor_n2 = 0
            for _g in grupos_mixto:
                _n2 = _txt_up2.count(_g)
                if _n2 > _mejor_n2:
                    _mejor_n2 = _n2; _mejor2 = _g
            grupo_pag = _mejor2
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
        "Sin material de trabajo": "Sin material de trabajo",
        "✉️ Entregó - Sobre enviado": "Entrego la tarea",
        "✉️❌ No entregó - Sobre tachado": "No entrego la tarea",
        "Actividad no realizada": "Actividad no realizada",
        "😊 Asistió": "Asistio",
        "😢 Falta": "Falta",
        "⏰ Retardo": "Retardo",
        "📄✅ Entregó": "Entrego el trabajo",
        "📄❌ No entregó": "No entrego el trabajo",
        "Sin material de trabajo": "No trajo material",
        "✉️ Entregó": "Entrego la tarea",
        "✉️❌ No entregó": "No entrego la tarea",
        "Actividad no realizada": "Actividad no realizada",
        "Sin material de trabajo": "Sin material de trabajo",
        "Falta de respeto a compañero o docente": "Falta de respeto a compañero o docente",
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
    txt_riesgo = {"VERDE": "VERDE", "AMARILLO": "AMARILLO", "ROJO": "ROJO"}.get(nivel, f"{nivel}")
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
    # FINAL 95: PDF FICHA - Durante trimestre SOLO Historial, al final SOLO Desglose final
    _es_final_pdf = trimestre_terminado()
    _calc_pdf = calcular_calificacion_final(nombre_al, escuela, grupo)
    if _es_final_pdf and _calc_pdf:
        elementos.append(Paragraph("Calificación final del trimestre - por apartado", h2))
        _es_sec_pdf = (escuela == ESCUELA_SECUNDARIA_NOMBRE)
        if _es_sec_pdf:
            elementos.append(Paragraph("Secundaria: Asistencia 0% (no cuenta) | Examen 10% | Trabajos 20% | Tareas 10% | Conducta 10% | Prácticas 25% | Proyecto 25%", ParagraphStyle("notap", parent=normal, fontSize=8.5, textColor=colors.HexColor("#64748B"))))
        else:
            elementos.append(Paragraph("Primaria: Asistencia 5% | Trabajos 30% | Tareas 5% | Conducta 10% | Prácticas 25% | Proyecto 25%", ParagraphStyle("notap2", parent=normal, fontSize=8.5, textColor=colors.HexColor("#64748B"))))
        _filas_cal = [[Paragraph("<b>Apartado</b>", head), Paragraph("<b>Promedio</b>", head), Paragraph("<b>Peso</b>", head), Paragraph("<b>Aporte</b>", head)]]
        for _k, (_prom, _n, _peso) in _calc_pdf["detalle"].items():
            if _prom is None:
                _prom_txt = "Sin capturas"
                _aporte_txt = "0.00"
            else:
                _prom_txt = f"{_prom:.1f} / 10"
                _aporte_txt = f"{(_prom/10)*_peso:.2f} de {_peso}"
            _filas_cal.append([Paragraph(_k, cell), Paragraph(_prom_txt, cell_c), Paragraph(f"{_peso}%", cell_c), Paragraph(_aporte_txt, cell_c)])
        _tcal = Table(_filas_cal, colWidths=[2.2*inch, 1.5*inch, 1.0*inch, 2.6*inch], repeatRows=1)
        _est_cal = [("BACKGROUND",(0,0),(-1,0), colors.HexColor("#1B2A41")),("GRID",(0,0),(-1,-1),0.5, colors.HexColor("#CBD5E1")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]
        for _ii in range(1, len(_filas_cal)):
            if _ii % 2 == 0: _est_cal.append(("BACKGROUND",(0,_ii),(-1,_ii), colors.HexColor("#F8FAFC")))
        _tcal.setStyle(TableStyle(_est_cal))
        elementos.append(_tcal)
        elementos.append(Spacer(1, 8))
        elementos.append(Paragraph(f"<b>CALIFICACIÓN FINAL: {_calc_pdf['cal']:.1f} / 10</b>", ParagraphStyle("calfin", parent=normal, fontSize=14, leading=16, alignment=TA_CENTER, textColor=colors.HexColor("#1B2A41"))))
        if _calc_pdf.get("decimas", 0) > 0:
            elementos.append(Paragraph(f"Base: {_calc_pdf.get('cal_base', _calc_pdf['cal']):.1f} + Décimas por excelente desempeño: {_calc_pdf['decimas']:.1f}", ParagraphStyle("caldet", parent=normal, fontSize=9, alignment=TA_CENTER, textColor=colors.HexColor("#64748B"))))
        elementos.append(Spacer(1, 6))
    elif not _es_final_pdf:
        pass
    else:
        elementos.append(Paragraph("Calificación final del trimestre: Todavía no tiene capturas.", h2))
    if not _es_final_pdf:
        elementos.append(Paragraph("Historial completo", h2))
    if _es_final_pdf:
        pass
    elif not regs_al:
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
    # FINAL 84: LISTA DEL GRUPO YA TRAE CALIFICACION FINAL - es la misma que sale en la ficha, para darsela a los maestros
    filas=[[Paragraph("<b>#</b>", head), Paragraph("<b>Alumno</b>", head_l), Paragraph("<b>Riesgo</b>", head), Paragraph("<b>Faltas</b>", head), Paragraph("<b>Sin trabajo</b>", head), Paragraph("<b>Sin tarea</b>", head), Paragraph("<b>Calif. Final</b>", head), Paragraph("<b>Capturas</b>", head)]]
    for idx, al in enumerate(alumnos_grupo):
        nivel, texto, faltas, retardos, no_trab, no_tarea, indis_n, regs = riesgo_de_alumno(al["Nombre"], escuela, grupo)
        # Pastilla de riesgo con texto legible
        color_r = "#0E9F6E" if nivel=="VERDE" else "#F59E0B" if nivel=="AMARILLO" else "#EF4444"
        riesgo_txt = f'<font color="{color_r}"><b>{nivel}</b></font>'
        _calc_g = calcular_calificacion_final(al["Nombre"], escuela, grupo)
        _cal_txt = f"{_calc_g['cal']:.1f}" if _calc_g else "Sin calif."
        filas.append([Paragraph(str(idx+1), cell_c), Paragraph(al["Nombre"], cell), Paragraph(riesgo_txt, cell_c), Paragraph(str(faltas), cell_c), Paragraph(str(no_trab), cell_c), Paragraph(str(no_tarea), cell_c), Paragraph(f"<b>{_cal_txt}</b>", cell_c), Paragraph(str(len(regs)), cell_c)])
    t2=Table(filas, colWidths=[0.35*inch,2.45*inch,0.75*inch,0.55*inch,0.85*inch,0.75*inch,0.85*inch,0.75*inch], repeatRows=1)
    estilo=[("BACKGROUND",(0,0),(-1,0), colors.HexColor("#1B2A41")),("GRID",(0,0),(-1,-1),0.5, colors.HexColor("#CBD5E1")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6)]
    for i in range(1, len(filas)):
        if i % 2 == 0: estilo.append(("BACKGROUND",(0,i),(-1,i), colors.HexColor("#F8FAFC")))
    t2.setStyle(TableStyle(estilo))
    elementos.append(t2)
    # FINAL 85: DESGLOSE POR APARTADO EN LA LISTA GENERAL - para que los maestros vean de donde sale la calificacion
    # Una tabla por alumno? No, una sola tabla grande: Alumno | cada apartado (promedio 0-10) | Calif Final
    # Primaria: Asis, Trab, Tarea, Cond, Prac, Proy | Secundaria: Asis 0%, Examen, Trab, Tarea, Cond, Prac, Proy
    elementos.append(Paragraph("Desglose por apartado - Todos los alumnos", h2))
    _es_sec_lista = (escuela == ESCUELA_SECUNDARIA_NOMBRE)
    if _es_sec_lista:
        elementos.append(Paragraph("Secundaria: Asistencia 0% (no cuenta) | Examen 10% | Trabajos 20% | Tareas 10% | Conducta 10% | Prácticas 25% | Proyecto 25%", ParagraphStyle("notag", parent=normal, fontSize=8.5, textColor=colors.HexColor("#64748B"))))
        _hdr_des = [Paragraph("<b>#</b>", head), Paragraph("<b>Alumno</b>", head_l), Paragraph("<b>Asis.</b>", head), Paragraph("<b>Examen</b>", head), Paragraph("<b>Trab.</b>", head), Paragraph("<b>Tarea</b>", head), Paragraph("<b>Cond.</b>", head), Paragraph("<b>Prác.</b>", head), Paragraph("<b>Proy.</b>", head), Paragraph("<b>Final</b>", head)]
        _filas_des = [_hdr_des]
        for _idx2, _al2 in enumerate(alumnos_grupo):
            _c2 = calcular_calificacion_final(_al2["Nombre"], escuela, grupo)
            def _pv(_d, _k):
                if not _c2: return "-"
                _v = _c2["detalle"].get(_k, (None,0,0))[0]
                return f"{_v:.1f}" if _v is not None else "-"
            _fin2 = f"{_c2['cal']:.1f}" if _c2 else "Sin calif."
            _filas_des.append([Paragraph(str(_idx2+1), cell_c), Paragraph(_al2["Nombre"], cell), Paragraph(_pv(None,"Asistencia"), cell_c), Paragraph(_pv(None,"Examen"), cell_c), Paragraph(_pv(None,"Trabajos"), cell_c), Paragraph(_pv(None,"Tareas"), cell_c), Paragraph(_pv(None,"Conducta"), cell_c), Paragraph(_pv(None,"Practicas"), cell_c), Paragraph(_pv(None,"Proyecto"), cell_c), Paragraph(f"<b>{_fin2}</b>", cell_c)])
        _t_des = Table(_filas_des, colWidths=[0.30*inch,2.10*inch,0.55*inch,0.65*inch,0.55*inch,0.55*inch,0.55*inch,0.55*inch,0.55*inch,0.60*inch], repeatRows=1)
    else:
        elementos.append(Paragraph("Primaria: Asistencia 5% | Trabajos 30% | Tareas 5% | Conducta 10% | Prácticas 25% | Proyecto 25%", ParagraphStyle("notag2", parent=normal, fontSize=8.5, textColor=colors.HexColor("#64748B"))))
        _hdr_des = [Paragraph("<b>#</b>", head), Paragraph("<b>Alumno</b>", head_l), Paragraph("<b>Asis.</b>", head), Paragraph("<b>Trab.</b>", head), Paragraph("<b>Tarea</b>", head), Paragraph("<b>Cond.</b>", head), Paragraph("<b>Prác.</b>", head), Paragraph("<b>Proy.</b>", head), Paragraph("<b>Final</b>", head)]
        _filas_des = [_hdr_des]
        for _idx2, _al2 in enumerate(alumnos_grupo):
            _c2 = calcular_calificacion_final(_al2["Nombre"], escuela, grupo)
            def _pv2(_k):
                if not _c2: return "-"
                _v = _c2["detalle"].get(_k, (None,0,0))[0]
                return f"{_v:.1f}" if _v is not None else "-"
            _fin2 = f"{_c2['cal']:.1f}" if _c2 else "Sin calif."
            _filas_des.append([Paragraph(str(_idx2+1), cell_c), Paragraph(_al2["Nombre"], cell), Paragraph(_pv2("Asistencia"), cell_c), Paragraph(_pv2("Trabajos"), cell_c), Paragraph(_pv2("Tareas"), cell_c), Paragraph(_pv2("Conducta"), cell_c), Paragraph(_pv2("Practicas"), cell_c), Paragraph(_pv2("Proyecto"), cell_c), Paragraph(f"<b>{_fin2}</b>", cell_c)])
        _t_des = Table(_filas_des, colWidths=[0.30*inch,2.40*inch,0.60*inch,0.60*inch,0.60*inch,0.60*inch,0.60*inch,0.60*inch,0.65*inch], repeatRows=1)
    _est_des = [("BACKGROUND",(0,0),(-1,0), colors.HexColor("#1B2A41")),("GRID",(0,0),(-1,-1),0.5, colors.HexColor("#CBD5E1")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4)]
    for _ii in range(1, len(_filas_des)):
        if _ii % 2 == 0: _est_des.append(("BACKGROUND",(0,_ii),(-1,_ii), colors.HexColor("#F8FAFC")))
    _t_des.setStyle(TableStyle(_est_des))
    elementos.append(_t_des)
    elementos.append(Paragraph("Cada número es el promedio de ese apartado del 0 al 10. Al final, la calificación final ya con sus porcentajes aplicados.", ParagraphStyle("notades", parent=normal, fontSize=8.5, textColor=colors.HexColor("#64748B"))))
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
            _todo = {"alumnos": st.session_state.get("alumnos", []), "registros": st.session_state.get("registros", []), "dias_clase": st.session_state.get("dias_clase", {}), "dias_confirmados": st.session_state.get("dias_confirmados", {}), "fecha_examen_sec": {k: str(v) for k,v in st.session_state.get("fecha_examen_sec", {}).items()}, "examen_configurado": st.session_state.get("examen_configurado", {}), "metas_trimestre": st.session_state.get("metas_trimestre", {})}
            # FINAL 79: trimestres de la memoria + defaults, no del archivo (la nube lo borra)
            _todo["trimestres"] = {"trimestres": _cargar_trimestres_archivo()}
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
                if "fecha_examen_sec" in _d:
                    from datetime import date as _dfe
                    _fe = {}
                    for _k,_v in _d["fecha_examen_sec"].items():
                        try: _fe[_k] = _dfe.fromisoformat(str(_v))
                        except: pass
                    st.session_state.fecha_examen_sec = _fe
                if "examen_configurado" in _d: st.session_state.examen_configurado = _d["examen_configurado"]
                if "trimestres" in _d:
                    # FINAL 79: ya no se escribe trimestres.json. Los trimestres del respaldo se quedan en memoria al restaurar.
                    pass
                _guardar_listas_archivo(); _guardar_dias_archivo()
                st.success("✅ Restaurado. Ya quedaron igual telefono y compu.")
                st.rerun()
            except Exception as _e:
                st.error(f"No se pudo restaurar: {_e}")
    # FINAL 75: si no ves alumnos, es porque la nube se reinicio al subir la nueva version y borro listas.json. UNIDAD y SECUNDARIA estan adentro del codigo y regresan solas. TOMAS tambien, ya esta adentro del codigo desde la Final 80.
    _total_al = len(st.session_state.get("alumnos", []))
    st.info(f"👥 Ahorita tienes {_total_al} alumnos cargados en total. TOMAS debe tener 162, UNIDAD 172 y SECUNDARIA 42 = 376 en total. Si te sale 0, no se borraron, solo se reinició la nube al subir la versión nueva. Pícale a Recuperar.")
    if st.button("🔄 Recuperar listas de TOMAS, UNIDAD y SECUNDARIA - Si no ves alumnos, pícale aquí", use_container_width=True):
        _agregados = 0
        for _esc_fija, _listas_fija in [(ESCUELA_TOMAS_NOMBRE, LISTAS_FIJAS_TOMAS), (ESCUELA_UNIDAD_NOMBRE, LISTAS_FIJAS_UNIDAD), (ESCUELA_SECUNDARIA_NOMBRE, LISTAS_FIJAS_SECUNDARIA)]:
            for _g_fija, _nombres_fija in _listas_fija.items():
                for _n_fija in _nombres_fija:
                    _ex = any(a.get("Nombre","").lower()==_n_fija.lower() and a.get("Grupo")==_g_fija and a.get("Escuela")==_esc_fija for a in st.session_state.alumnos)
                    if not _ex:
                        _mat_fija = "Artes" if (_esc_fija==ESCUELA_SECUNDARIA_NOMBRE and _g_fija=="1B") else ("Electrónica" if _esc_fija==ESCUELA_SECUNDARIA_NOMBRE else "Primaria")
                        st.session_state.alumnos.append({"Nombre": _n_fija, "Escuela": _esc_fija, "Grupo": _g_fija, "Materia": _mat_fija}); _agregados += 1
        _guardar_listas_archivo(); st.success(f"✅ Recuperados {_agregados} alumnos de TOMAS, UNIDAD y SECUNDARIA. Ya deben salir otra vez."); st.rerun()
    st.write("✅ TOMAS ya está adentro del código. Ya no tienes que subir su PDF nunca más. Si no te sale TOMAS, pícale a Recuperar de arriba.")
    st.subheader("Elige una escuela para entrar:")
    st.write("")
    if st.button("🏫 Tomas Gameros # 2131  •  Primaria  •  Artes", use_container_width=True):
        st.session_state.escuela_activa="TOMAS GAMEROS # 2131"; st.session_state.grupo_sel_actual="-- Elige un grupo --"; st.session_state.grupo_confirmado=None; st.session_state.alumno_activo=None; st.rerun()
    st.write("")
    if st.button("🏫 Unidad Proletaria # 2294  •  Primaria  •  Artes", use_container_width=True):
        st.session_state.escuela_activa="UNIDAD PROLETARIA # 2294"; st.session_state.grupo_sel_actual="-- Elige un grupo --"; st.session_state.grupo_confirmado=None; st.session_state.alumno_activo=None; st.rerun()
    st.write("")
    if st.button("🏫 Escuela Secundaria Estatal # 3046  •  Secundaria  •  1B Artes / 3C Electrónica", use_container_width=True):
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
# FINAL 63 ARREGLO NameError grupo_sel: si estas en la FICHA, tambien definir grupo_sel aunque no se muestre configurar.
# Antes al esconder configurar, grupo_sel no existia y la ficha se caia en la linea 1082.
if st.session_state.get("alumno_activo") is not None:
    grupo_sel = st.session_state.get("grupo_confirmado") or _grupo_pre
    alumnos_esc = _alumnos_esc_pre
    _llave_ficha = f"{escuela}|{grupo_sel}"
    dias_clase_grupo = st.session_state.dias_clase.get(_llave_ficha, [0])
    nombres_dias_grupo = [DIAS_ES[d] for d in dias_clase_grupo]
    llave_dias = _llave_ficha
# ===== ENCABEZADO FIJO ADENTRO - MISMO QUE EN PORTADA =====
mostrar_encabezado()
if not modo_lista and st.session_state.get("alumno_activo") is None:  # FINAL 62: si estas en la ficha, NO mostrar configurar. Solo ficha.
    # FINAL 78: sin aviso de trimestre en cada pantalla, solo en portada.
    st.header(f"🏫 {escuela}")
    _n_esta = len([a for a in st.session_state.alumnos if a.get("Escuela")==escuela])
    _n_otras = len([a for a in st.session_state.alumnos if a.get("Escuela")!=escuela])
    # FINAL 78: sin leyendas de conteo, para que la lista salga luego luego.
    _n_esta = len([a for a in st.session_state.alumnos if a.get("Escuela")==escuela])
    _n_otras = len([a for a in st.session_state.alumnos if a.get("Escuela")!=escuela])

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
    # ===== UPLOAD FINAL 102 - GOOGLE SHEET POR APPS SCRIPT WEBHOOK, RECONSTRUIDA DESDE 99, SIN ERROR NAMEERROR - TU LE DICES DE QUE GRUPO ES CADA PDF =====
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
            st.success(f"🔒 Estás cargando en: **{escuela}**. Todo lo que subas aquí se va a {escuela}, no a otra escuela. Ya no se puede cambiar aquí, para que no se mezcle.")
            escuela_pdf = escuela  # FINAL 60: la escuela es SIEMPRE la de la pagina. Asi UNIDAD ya no agarra lo de TOMAS.
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
                        opcion=st.selectbox(f"¿De qué grupo es este archivo {f.name}?", ["Auto - que el programa detecte solo (recomendado)", "1B - Artes", "3A - Electrónica", "3B - Electrónica", "3C - Electrónica", "3A y 3B juntos - Electrónica", "1B y 3C juntos - Secundaria"], key=f"grupo_pdf_{idx_f}_36")
                    else:
                        opcion=st.selectbox(f"¿De qué grupo es este archivo {f.name}?", ["Auto - que el programa detecte solo (recomendado)", "1A", "2A", "3A", "4A", "5A", "5B", "6A", "1B", "3B"], key=f"grupo_pdf_{idx_f}_36")
                    grupos_por_archivo[f.name]=opcion
                    if opcion=="3A y 3B juntos - Electrónica":
                        st.info("ℹ️ Este PDF trae 3A y 3B juntos. El programa va a intentar separarlos por las páginas.")
                st.write("")
                if st.button("✅ Cargar todos los alumnos de estos PDFs", use_container_width=True):
                    total_general=0; por_grupo_total={}
                    for f in archivos_pdf:
                        opcion_elegida=grupos_por_archivo.get(f.name, "Auto - que el programa detecte solo (recomendado)")
                        try:
                            # Si eligió "3A y 3B juntos", primero intentar como Auto (que detecta por página), si sale 0, intentar como 3A
                            if opcion_elegida in ("3A y 3B juntos - Electrónica", "1B y 3C juntos - Secundaria"):
                                _mixto = "MIXTO_1B_3C" if opcion_elegida=="1B y 3C juntos - Secundaria" else "MIXTO_3A_3B"
                                total_uno, por_grupo_uno, debug = procesar_un_pdf(f.getvalue(), escuela_pdf, f.name, _mixto)
                                if total_uno==0:
                                    # Si no detectó nada, probar forzando 3A y luego 3B por separado no funciona, así que mostrar diagnóstico
                                    st.warning(f"⚠️ En {f.name} no detecté grupo en automático. Abajo te muestro lo que sí leyó para que veamos cómo viene.")
                            else:
                                # Convertir "3A - Electrónica" -> "3A", "1B - Artes" -> "1B"
                                grupo_forzado = opcion_elegida[:2] if opcion_elegida!="Auto - que el programa detecte solo (recomendado)" else opcion_elegida
                                total_uno, por_grupo_uno, debug = procesar_un_pdf(f.getvalue(), escuela_pdf, f.name, grupo_forzado)
                            if "ERROR_GRUPO" in por_grupo_uno:
                                st.error(f"❌ {f.name}: {por_grupo_uno['ERROR_GRUPO']}")
                            elif "ERROR_ESCUELA" in por_grupo_uno:
                                st.error(f"❌ {f.name}: {por_grupo_uno['ERROR_ESCUELA']} No se cargó nada, para no mezclar escuelas.")
                            total_general+=total_uno
                            for g,c in por_grupo_uno.items():
                                if isinstance(c, (int, float)):
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
        # ARREGLO ERROR escuela_pdf is not defined: en este bloque (cuando la escuela esta en blanco) no existia esa variable
        escuela_pdf = escuela
        st.write("")
        if archivos_pdf:
            st.write(f"Archivos que elegiste: **{len(archivos_pdf)}**")
            # Por cada archivo, un selector de grupo - ESTO ES LO QUE ARREGLA LO DE 3A
            grupos_por_archivo={}
            for idx_f, f in enumerate(archivos_pdf):
                st.write(f"---")
                st.write(f"**Archivo {idx_f+1}: {f.name}**")
                if escuela=="ESCUELA SECUNDARIA ESTATAL # 3046":
                    opcion=st.selectbox(f"¿De qué grupo es este archivo {f.name}?", ["Auto - que el programa detecte solo (recomendado)", "1B - Artes", "3A - Electrónica", "3B - Electrónica", "3C - Electrónica", "3A y 3B juntos - Electrónica", "1B y 3C juntos - Secundaria"], key=f"grupo_pdf_{idx_f}_36")
                else:
                    opcion=st.selectbox(f"¿De qué grupo es este archivo {f.name}?", ["Auto - que el programa detecte solo (recomendado)", "1A", "2A", "3A", "4A", "5A", "5B", "6A", "1B", "3B"], key=f"grupo_pdf_{idx_f}_36")
                grupos_por_archivo[f.name]=opcion
                if opcion=="3A y 3B juntos - Electrónica":
                    st.info("ℹ️ Este PDF trae 3A y 3B juntos. El programa va a intentar separarlos por las páginas.")
            st.write("")
            if st.button("✅ Cargar todos los alumnos de estos PDFs", use_container_width=True):
                total_general=0; por_grupo_total={}
                for f in archivos_pdf:
                    opcion_elegida=grupos_por_archivo.get(f.name, "Auto - que el programa detecte solo (recomendado)")
                    try:
                        # Si eligió "3A y 3B juntos", primero intentar como Auto (que detecta por página), si sale 0, intentar como 3A
                        if opcion_elegida in ("3A y 3B juntos - Electrónica", "1B y 3C juntos - Secundaria"):
                            _mixto = "MIXTO_1B_3C" if opcion_elegida=="1B y 3C juntos - Secundaria" else "MIXTO_3A_3B"
                            total_uno, por_grupo_uno, debug = procesar_un_pdf(f.getvalue(), escuela_pdf, f.name, _mixto)
                            if total_uno==0:
                                # Si no detectó nada, probar forzando 3A y luego 3B por separado no funciona, así que mostrar diagnóstico
                                st.warning(f"⚠️ En {f.name} no detecté grupo en automático. Abajo te muestro lo que sí leyó para que veamos cómo viene.")
                        else:
                            # Convertir "3A - Electrónica" -> "3A", "1B - Artes" -> "1B"
                            grupo_forzado = opcion_elegida[:2] if opcion_elegida!="Auto - que el programa detecte solo (recomendado)" else opcion_elegida
                            total_uno, por_grupo_uno, debug = procesar_un_pdf(f.getvalue(), escuela_pdf, f.name, grupo_forzado)
                        # FINAL 64 ARREGLO int+str: si no elegiste grupo, por_grupo_uno trae ERROR_GRUPO con texto, no numeros. No sumar, solo avisar.
                        if "ERROR_GRUPO" in por_grupo_uno:
                            st.error(f"❌ {f.name}: {por_grupo_uno['ERROR_GRUPO']} - Elige arriba el grupo, por ejemplo 2A, y vuelve a picarle a Cargar.")
                            continue
                        total_general+=total_uno
                        for g,c in por_grupo_uno.items():
                            # Solo sumar si c es numero, por si viene texto
                            if isinstance(c, (int, float)):
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
    # BOTON NUEVO FINAL 102 - GOOGLE SHEET POR APPS SCRIPT WEBHOOK, RECONSTRUIDA DESDE 99, SIN ERROR NAMEERROR: Eliminar la escuela YA cargada (no solo el PDF antes de cargarlo)
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
    # FINAL 92: CONFIGURAR CUANTOS VAS A CALIFICAR ESTE TRIMESTRE
    _llave_metas = f"{escuela}|{grupo_sel}"
    _metas_actuales = st.session_state.get("metas_trimestre", {}).get(_llave_metas, {})
    with st.expander("📊 ¿Cuántos vas a calificar este trimestre? (para que el programa sepa la base)", expanded=False):
        st.write("Pon cuántos trabajos, tareas, prácticas, proyectos y exámenes vas a calificar en este trimestre en este grupo. Lo que falte por capturar va a contar como 0. Si lo dejas en 0, el programa sigue sacando promedio solo de lo que ya capturaste.")
        _c1, _c2 = st.columns(2)
        with _c1:
            _m_trab = st.number_input("Trabajos a calificar", min_value=0, max_value=50, step=1, value=int(_metas_actuales.get("Trabajos", 0)), key=f"meta_trab_{grupo_sel}_92")
            _m_tar = st.number_input("Tareas a calificar", min_value=0, max_value=50, step=1, value=int(_metas_actuales.get("Tareas", 0)), key=f"meta_tar_{grupo_sel}_92")
            _m_prac = st.number_input("Prácticas a calificar", min_value=0, max_value=50, step=1, value=int(_metas_actuales.get("Practicas", 0)), key=f"meta_prac_{grupo_sel}_92")
        with _c2:
            _m_proy = st.number_input("Proyectos a calificar", min_value=0, max_value=10, step=1, value=int(_metas_actuales.get("Proyecto", 0)), key=f"meta_proy_{grupo_sel}_92")
            _m_ex = st.number_input("Exámenes a calificar (solo secundaria)", min_value=0, max_value=10, step=1, value=int(_metas_actuales.get("Examen", 0)), key=f"meta_ex_{grupo_sel}_92")
        if st.button("✅ Guardar cuántos voy a calificar", key=f"btn_meta_{grupo_sel}_92"):
            st.session_state.metas_trimestre[_llave_metas] = {"Trabajos": int(_m_trab), "Tareas": int(_m_tar), "Practicas": int(_m_prac), "Proyecto": int(_m_proy), "Examen": int(_m_ex)}
            st.success(f"✅ Guardado: Trabajos {_m_trab}, Tareas {_m_tar}, Prácticas {_m_prac}, Proyecto {_m_proy}, Examen {_m_ex}. Lo que falte cuenta como 0.")
            st.rerun()
        if _metas_actuales:
            st.info(f"Actual: Trabajos {_metas_actuales.get('Trabajos',0)}, Tareas {_metas_actuales.get('Tareas',0)}, Prácticas {_metas_actuales.get('Practicas',0)}, Proyecto {_metas_actuales.get('Proyecto',0)}, Examen {_metas_actuales.get('Examen',0)}")
if st.session_state.alumno_activo is not None:
    nombre_al=st.session_state.alumno_activo
    # --- FINAL 78: FICHA LIMPIA, EN ESTE ORDEN Y SIN LEYENDAS ---
    # 1. Nombre del alumno + Regresar (arriba, siempre visible)
    # 2. Dia de captura
    # 3. Apartados para capturar + Guardar
    # 4. Estatus verde / amarillo / rojo
    # 5. Generar PDF (solo cuando le picas, antes se generaba solo y trababa la pagina)
    # Ya NO se genera el PDF solo al abrir la ficha. Eso era lo que hacia que todo se pusiera lento y no te dejara volver atras.
    if st.button("⬅️ Regresar a la lista de "+grupo_sel, key="btn_regresar_lista_ficha_78"):
        st.session_state.alumno_activo=None; st.rerun()
    st.subheader(f"{nombre_al}")
    st.write(f"{escuela}  •  Grupo {grupo_sel}")
    st.divider()
    # 2. Dia de captura - ARRIBA, no al final
    if not st.session_state.trimestre_cargado:
        fecha_por_defecto = hoy
    elif hoy < st.session_state.tri_inicio:
        fecha_por_defecto = st.session_state.tri_inicio
    elif hoy > st.session_state.tri_fin:
        fecha_por_defecto = st.session_state.tri_fin
    else:
        fecha_por_defecto = hoy
    fecha_captura=st.date_input("📅 Día de captura", value=fecha_por_defecto, key=f"fecha_cap_{nombre_al}_78")
    puede_capturar = True
    if st.session_state.trimestre_cargado and (fecha_captura < st.session_state.tri_inicio or fecha_captura > st.session_state.tri_fin):
        puede_capturar = False
        st.write(f"Esta fecha no está dentro de {st.session_state.trimestre_cargado_nombre}.")
    # 3. Apartados para capturar
    st.subheader("Captura del día")
    # FINAL 83: EXAMEN SOLO SECUNDARIA - se habilita solo cuando configuras la fecha del examen
    _es_sec_ficha = (escuela == ESCUELA_SECUNDARIA_NOMBRE)
    _llave_examen = f"{escuela}|{grupo_sel}"
    _fecha_examen_guardada = st.session_state.get("fecha_examen_sec", {}).get(_llave_examen)
    _examen_habilitado = bool(_es_sec_ficha and _fecha_examen_guardada)
    # Configurar fecha del examen - SOLO SECUNDARIA, arriba de la captura
    if _es_sec_ficha:
        with st.expander("📝 Examen - Configurar fecha del examen (solo secundaria)", expanded=False):
            st.write("Pon la fecha del examen y pícale a Guardar fecha. Hasta que no pongas fecha, el campo de calificación del examen sale bloqueado.")
            _fecha_ex_temp = st.date_input("📅 Fecha del examen", value=_fecha_examen_guardada if _fecha_examen_guardada else hoy, key=f"fecha_examen_{grupo_sel}_83")
            if st.button("✅ Guardar fecha del examen", key=f"btn_fecha_examen_{grupo_sel}_83"):
                st.session_state.fecha_examen_sec[_llave_examen] = _fecha_ex_temp
                st.session_state.examen_configurado[_llave_examen] = True
                st.success(f"✅ Fecha del examen guardada: {fecha_bonita(_fecha_ex_temp)}. Ya puedes poner la calificación del examen.")
                st.rerun()
            if _fecha_examen_guardada:
                st.success(f"✅ Examen programado: {fecha_bonita(_fecha_examen_guardada)}")
            else:
                st.warning("⚠️ Todavía no has configurado la fecha del examen. El examen está bloqueado.")
    col1,col2=st.columns(2)
    with col1:
        if _es_sec_ficha:
            asistencia=st.selectbox("Asistencia - 0% (en secundaria no cuenta)", ["😊 Asistió","⏰ Retardo","😢 Falta"], key="f_asis78")
            trabajo=st.selectbox("Trabajo - 20%", LISTA_TRABAJOS, key="f_trab78")
            practica=st.selectbox("Prácticas / Trabajos especiales - 25%", LISTA_PRACTICAS, key="f_prac78")
        else:
            asistencia=st.selectbox("Asistencia - 5%", ["😊 Asistió","⏰ Retardo","😢 Falta"], key="f_asis78")
            trabajo=st.selectbox("Trabajo - 30%", LISTA_TRABAJOS, key="f_trab78")
            practica=st.selectbox("Prácticas / Trabajos especiales - 25%", LISTA_PRACTICAS, key="f_prac78")
    with col2:
        if _es_sec_ficha:
            tarea=st.selectbox("Tarea - 10%", ["No se pidió","✉️ Entregó","✉️❌ No entregó"], key="f_tar78")
            indis=st.selectbox("Conducta en clase - 10%", LISTA_CONDUCTAS, key="f_ind78")
            proyecto=st.selectbox("Proyecto final - 25%", LISTA_PROYECTOS, key="f_proy78")
        else:
            tarea=st.selectbox("Tarea - 5%", ["No se pidió","✉️ Entregó","✉️❌ No entregó"], key="f_tar78")
            indis=st.selectbox("Conducta en clase - 10%", LISTA_CONDUCTAS, key="f_ind78")
            proyecto=st.selectbox("Proyecto final - 25%", LISTA_PROYECTOS, key="f_proy78")
    # Campo Examen - SOLO SECUNDARIA, solo si hay fecha configurada, del 5 al 10
    examen_val = None
    if _es_sec_ficha:
        if _examen_habilitado:
            examen_val = st.number_input(f"📝 Examen - 10% (Fecha: {fecha_bonita(_fecha_examen_guardada)}) - Calificación del 5 al 10", min_value=5.0, max_value=10.0, step=0.1, value=10.0, key="f_examen83")
            st.write("Pon la calificación que sacó en el examen, del 5 al 10.")
        else:
            st.info("📝 Examen - 10% - BLOQUEADO. Primero configura la fecha del examen arriba para habilitarlo.")
            examen_val = None
    reincidencia=st.selectbox("Reincidencia", LISTA_CONDUCTAS, key="f_reinc78")
    excelente=st.selectbox("Buena conducta - suma +1 ese día", ["Ninguno","Felicitaciones","Buen trabajo","Ayuda a sus compañeros","Excelente desempeño","Atento"], key="f_excel78")
    anotacion=st.text_area("Anotaciones del día", key="f_anot78", placeholder="Ej: Conversó durante la actividad...")
    # FINAL 98: NO DEJAR CAPTURAR CON FECHA FUTURA NI SI NO ES DIA DE CLASE
    # Si hoy es lunes 16, no puede capturar como martes 17, aunque cambie la fecha en el calendario
    # La fecha de captura no puede ser mayor que hoy, y tiene que ser dia de clase de ese grupo
    _es_fecha_futura = fecha_captura > hoy
    if _es_fecha_futura:
        st.error(f"⛔ No puedes capturar como {fecha_bonita(fecha_captura)} porque hoy es {fecha_bonita(hoy)}. No puedes capturar un dia que todavia no llega.")
        st.info("Pon la fecha de hoy para capturar.")
    # FINAL 97: NO DEJAR CAPTURAR SI NO ES DIA DE CLASE - CORREGIDO: el grupo viene como "2-A" con guion y DIAS_FIJOS es "2A" sin guion, por eso no lo encontraba y dejaba pasar
    _grupo_norm_ficha = grupo_sel.replace("-", "").replace(" ", "").upper()
    _llave_dias_ficha = f"{escuela}|{grupo_sel}"
    _llave_dias_ficha_norm = f"{escuela}|{_grupo_norm_ficha}"
    _dias_clase_ficha = st.session_state.get("dias_clase", {}).get(_llave_dias_ficha, [])
    if not _dias_clase_ficha:
        _dias_clase_ficha = st.session_state.get("dias_clase", {}).get(_llave_dias_ficha_norm, [])
    if not _dias_clase_ficha:
        # Buscar en DIAS_FIJOS directamente, sin guion
        for _k_f, _v_f in DIAS_FIJOS_PRIMARIAS.items():
            if _k_f.split("|")[0] == escuela and _k_f.split("|")[1].replace("-", "").upper() == _grupo_norm_ficha:
                _dias_clase_ficha = list(_v_f)
                break
    _dia_captura = fecha_captura.weekday()
    _es_dia_clase = (_dia_captura in _dias_clase_ficha) if _dias_clase_ficha else True
    if not _es_dia_clase:
        st.error(f"⛔ Hoy es {DIAS_ES[_dia_captura]} y a este grupo le das clase los: {', '.join([DIAS_ES[d] for d in _dias_clase_ficha])}. No puedes capturar hoy.")
        st.info("Si necesitas capturar otro dia, cambia los dias de clase del grupo primero.")
    if puede_capturar:
        if st.button("💾 Guardar captura", key="btn_guardar_cap_78"):
            if _es_fecha_futura:
                st.error("⛔ No se guardó: no puedes capturar una fecha futura.")
                st.stop()
            if not _es_dia_clase:
                st.error("⛔ No se guardó: no es día de clase de este grupo.")
                st.stop()
            ya_existe=any(r["Alumno"]==nombre_al and r.get("Escuela")==escuela and r.get("Grupo")==grupo_sel and r.get("Trimestre")==st.session_state.trimestre_cargado_nombre and r.get("Fecha")==str(fecha_captura) and r.get("Estado")==asistencia for r in st.session_state.registros)
            ya_hay_ese_dia=any(r["Alumno"]==nombre_al and r.get("Escuela")==escuela and r.get("Grupo")==grupo_sel and r.get("Trimestre")==st.session_state.trimestre_cargado_nombre and r.get("Fecha")==str(fecha_captura) for r in st.session_state.registros)
            if ya_existe or ya_hay_ese_dia:
                st.write("Ya tienes una captura ese día. No la guardé otra vez.")
            else:
                st.session_state.registros.append({"Alumno":nombre_al,"Escuela":escuela,"Grupo":grupo_sel,"Trimestre":st.session_state.trimestre_cargado_nombre,"Fecha":str(fecha_captura),"FechaBonita":fecha_bonita(fecha_captura),"Estado":asistencia,"Trabajo":trabajo,"Tarea":tarea,"Indisciplina":indis,"Practica":practica,"Proyecto":proyecto,"Reincidencia":reincidencia,"Excelente":excelente,"Anotacion":anotacion,"Examen":examen_val,"FechaExamen":str(_fecha_examen_guardada) if _fecha_examen_guardada else ""})
                _guardar_listas_archivo()
                _ok_gs, _msg_gs = _guardar_en_gsheets()
                if _ok_gs:
                    st.success(f"Guardado - {fecha_bonita(fecha_captura)} - {_msg_gs}")
                else:
                    st.warning(f"Guardado en la app, pero {_msg_gs}. Revisa tu Google Sheet.")
                st.rerun()
    else:
        st.write("No se puede guardar fuera del trimestre.")
    st.divider()
    # 4. Estatus verde / amarillo / rojo + calificación
    nivel, texto_riesgo, faltas, retardos, no_trab, no_tarea, indis_n, regs_al = riesgo_de_alumno(nombre_al, escuela, grupo_sel)
    # FINAL 94: Solo el color, sin repetir lo de la calificacion - el promedio ya lo dice abajo
    if nivel=="VERDE":
        st.success(f"🟢 VERDE")
    elif nivel=="AMARILLO":
        st.warning(f"🟡 AMARILLO")
    else:
        st.error(f"🔴 ROJO")
    _calc = calcular_calificacion_final(nombre_al, escuela, grupo_sel)
    if _calc:
        st.subheader(f"Calificación: {_calc['cal']:.1f} / 10")
        if _calc.get("decimas", 0) > 0:
            st.write(f"Base: {_calc.get('cal_base', _calc['cal']):.1f} + Décimas: {_calc['decimas']:.1f} = Total: {_calc['cal']:.1f}")
    else:
        st.write("Todavía no tiene capturas.")
    st.divider()
    # 5. Generar PDF - SOLO cuando le picas, no antes
    # FINAL 102: Solo UN boton Probar - el 98 duplicado se quito
    if st.button("🔍 Probar conexión con Google Sheet", key="btn_probar_gs_102"):
        _ok_t, _msg_t = _guardar_en_gsheets()
        if _ok_t:
            st.success(f"✅ Sí está conectado: {_msg_t}")
        else:
            st.error(f"❌ No está conectado: {_msg_t}")
    if st.button("📄 Generar PDF de esta ficha", key="btn_pdf_ficha_78", use_container_width=True):
        try:
            pdf_ficha=generar_pdf_ficha_alumno(nombre_al, escuela, grupo_sel)
            st.download_button(label="⬇️ Descargar PDF", data=pdf_ficha, file_name=f"Ficha_{nombre_al.replace(' ','_')}_{grupo_sel}.pdf", mime="application/pdf", use_container_width=True, key="dl_pdf_ficha_78")
        except Exception as e:
            st.error(f"No se pudo generar el PDF: {e}")
    if st.button("🗑️ Eliminar a este alumno", key="btn_eliminar_alumno_78"):
        for i,a in enumerate(st.session_state.alumnos):
            if a["Nombre"]==nombre_al and a["Escuela"]==escuela and a["Grupo"]==grupo_sel:
                del st.session_state.alumnos[i]; _guardar_listas_archivo(); break
        st.session_state.alumno_activo=None; st.rerun()
    with st.expander("📋 Historial"):
        if not regs_al:
            st.write("Todavía no tiene capturas.")
        else:
            for idx_r, r in enumerate(sorted(regs_al, key=lambda x: x.get("Fecha",""))):
                # FINAL 120: Si FechaBonita viene fea como 2026-11-17T06:00:00.000Z, mostrar solo 2026-11-17
                _fb_m = str(r.get("FechaBonita") or r.get("Fecha",""))
                fecha_mostrar = _fb_m.split("T")[0] if "T" in _fb_m else _fb_m
                st.write(f"**{fecha_mostrar}** - {r.get('Trimestre','')} - {r['Estado']} - Trabajo: {r['Trabajo']} - Tarea: {r['Tarea']} - Conducta: {r['Indisciplina']}")
                if r.get("Anotacion"):
                    st.write(f"{r['Anotacion']}")
                if st.button(f"🗑️ Borrar este día - {fecha_mostrar}", key=f"borrar_dia_78_{idx_r}_{r.get('Fecha','')}"):
                    for i, rr in enumerate(st.session_state.registros):
                        if rr["Alumno"]==nombre_al and rr.get("Escuela")==escuela and rr.get("Grupo")==grupo_sel and rr.get("Fecha")==r.get("Fecha"):
                            st.session_state._sheet_borrado_a_proposito = True; del st.session_state.registros[i]; _guardar_listas_archivo(); _guardar_en_gsheets(); break
                    st.rerun()
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
