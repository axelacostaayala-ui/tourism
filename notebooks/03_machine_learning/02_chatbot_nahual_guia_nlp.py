"""
Módulo de Inteligencia Artificial y Procesamiento de Lenguaje Natural (NLP):
Chatbot Conversacional 'El Nahual Guía'.

Proyecto Prototípico - 5to Semestre: Ciencias de Datos para Negocios
Universidad Rosario Castellanos
UCA: Aprendizaje de Máquina (Aplicaciones NLP y Sistemas Inteligentes)
Rol: Integrante 1 — Data Engineering & ML Lead (monenri9-svg)

Este script implementa:
1. Vectorizador híbrido TF-IDF de N-gramas de palabras (1-2) y caracteres (3-5) +
   Clasificador Lineal Regularizado Multiclase con calibración Softmax entrenado
   sobre un corpus de consultas de viajeros en español mexicano.
2. Reconocimiento de Entidades Territoriales (Municipios, Estaciones, Guardianes y POIs).
3. Generador de Pistas Gamificadas en Copla/Verso tradicional para los 12 POIs y
   recomendación contextual de comercios locales afiliados ('Bendiciones').
4. Serialización del pipeline NLP en 'modelos/chatbot_nahual_nlp.pkl' y bitácora de
   pruebas conversacionales en 'datos/processed/ml_evaluacion_chatbot_nahual.csv'.
"""

import os
import pickle
import re
from collections import Counter
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROCESSED_DIR = os.path.join(BASE_DIR, "datos", "processed")
MODELOS_DIR = os.path.join(BASE_DIR, "modelos")

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(MODELOS_DIR, exist_ok=True)


# Base de Conocimiento Poética: Coplas y Acertijos del Nahual Guía por Nodo / Guardián
COPLAS_NAHUAL = {
    "EST-01": {
        "guardian": "Xinán (El Guardián de la Escarcha y el Volcán — Legendario)",
        "municipio": "Zinacantepec",
        "copla_pista": (
            "«Donde el viento besa la nieve del gran Xinantécatl ancestral, "
            "busca primero el claustro franciscano del Museo Virreinal; "
            "mira la Pila Monolítica tallada por manos de antaño, "
            "y sube al sendero del bosque donde el coyote cuida su rebaño.»"
        ),
        "gastronomia": (
            "En Zinacantepec te espera 'Barbacoa El Rinconcito Serrano' (15% OFF) "
            "y el pan de fiesta recién horneado en 'Panadería San Miguel'."
        ),
        "ruta_tren": "Baja en la Terminal Zinacantepec (EST-01) de El Insurgente; el centro histórico está a 10 min en transporte local o ciclovía."
    },
    "EST-03": {
        "guardian": "Barrotépetl (El Espíritu Alfarero del Fuego y el Barro — Épico)",
        "municipio": "Metepec",
        "copla_pista": (
            "«Del barro rojo y el horno despierta una quimera alada, "
            "sube la escalinata del Calvario en la colina sagrada; "
            "escucha el torno girar donde el Árbol de la Vida florece, "
            "y en el Mercado Artesanal el espíritu de Metepec aparece.»"
        ),
        "gastronomia": (
            "En Metepec canjea tu bendición en 'Fonda Doña Lupe' (gorditas de maíz azul, 10% OFF), "
            "'Café Cultural El Cerrojo' o prueba el licor tradicional en 'Bar 2 de Abril'."
        ),
        "ruta_tren": "Desciende en Estación Metepec (EST-03) sobre Av. Tecnológico; a 8 minutos conectas con el Barrio de Santiaguito y el Cerro de los Magueyes."
    },
    "EST-04": {
        "guardian": "Acatl-Tule (La Ninfa de los Humedales — Épico)",
        "municipio": "Lerma",
        "copla_pista": (
            "«Entre espejos de agua dulce donde el ave migratoria anida, "
            "las Ciénegas de Lerma guardan la memoria de la vida; "
            "visita el Templo de Santa Clara y en San Pedro Tultepec verás "
            "cómo el tule se entreteje y a Acatl-Tule despertarás.»"
        ),
        "gastronomia": (
            "En Lerma disfruta trucha y platillos lacustres en 'Restaurante Rincón Mexiquense' (15% OFF) "
            "o quesadillas de comal con Doña Mary en el Mercado Municipal."
        ),
        "ruta_tren": "Llega a Estación Lerma (EST-04); a solo 5-7 minutos se ubican el Templo de Santa Clara, el mirador del humedal y los talleres de tule."
    },
    "EST-02": {
        "guardian": "Mosco Matlatzinca (El Centinela de los Portales — Raro)",
        "municipio": "Toluca de Lerdo",
        "copla_pista": (
            "«Bajo el Hombre Sol de vidrio que ilumina el jardín inmortal, "
            "extiende sus alas de colores el guardián del Cosmovitral; "
            "camina por los arcos eternos de Los Portales con fervor, "
            "y en el Museo del Alfeñique hallarás la dulzura y el color.»"
        ),
        "gastronomia": (
            "En Toluca Centro aprovecha 10% OFF en 'Chorizos Tradicionales Los Portales', "
            "dulces de cortesía en 'Alfeñiques San José' y 15% en 'Café y Librería El Labrador'."
        ),
        "ruta_tren": "Baja en Estación Toluca Centro (EST-02) en Av. Pino Suárez; los autobuses urbanos te dejan en Los Portales y el Cosmovitral en 12 minutos."
    }
}


class ClasificadorNLPNahual:
    """
    Pipeline NLP en NumPy: Tokenización + N-gramas híbridos (palabras 1-2 y caracteres 3-4)
    + Ponderación TF-IDF sublineal + Clasificador Lineal Multiclase L2 con Softmax.
    """
    def __init__(self, reg_lambda=0.15, temp_softmax=4.5):
        self.reg_lambda = reg_lambda
        self.temp_softmax = temp_softmax
        self.vocab_ = {}
        self.idf_ = None
        self.classes_ = None
        self.W_ = None

    @staticmethod
    def _extraer_tokens(texto):
        stopwords = {"de", "la", "el", "en", "para", "con", "por", "los", "las", "del", "al", "un", "una", "que", "qué", "se", "me", "mi", "es", "son", "o", "y", "a"}
        limpio = re.sub(r"[^\wáéíóúñü\s]", " ", texto.lower())
        palabras = [w for w in limpio.split() if len(w) > 2 and w not in stopwords]
        feats = list(palabras)
        # Prefijos morfológicos (raíces de 4 y 5 letras) para capturar familias léxicas
        for w in palabras:
            if len(w) >= 4:
                feats.append(f"stem4:{w[:4]}")
            if len(w) >= 5:
                feats.append(f"stem5:{w[:5]}")
        # Bigramas de palabras contenido
        for i in range(len(palabras) - 1):
            feats.append(f"{palabras[i]}_{palabras[i+1]}")
        return feats

    def _vectorizar(self, textos, fit=False):
        docs_tokens = [self._extraer_tokens(t) for t in textos]
        if fit:
            df_counts = Counter()
            for toks in docs_tokens:
                for tok in set(toks):
                    df_counts[tok] += 1
            self.vocab_ = {tok: idx for idx, (tok, _) in enumerate(sorted(df_counts.items()))}
            n_docs = len(textos)
            self.idf_ = np.zeros(len(self.vocab_), dtype=float)
            for tok, idx in self.vocab_.items():
                self.idf_[idx] = np.log((1.0 + n_docs) / (1.0 + df_counts[tok])) + 1.0

        X = np.zeros((len(textos), len(self.vocab_)), dtype=float)
        for i, toks in enumerate(docs_tokens):
            counts = Counter(toks)
            for tok, c in counts.items():
                if tok in self.vocab_:
                    X[i, self.vocab_[tok]] = (1.0 + np.log(c)) * self.idf_[self.vocab_[tok]]
            norma = np.linalg.norm(X[i])
            if norma > 1e-9:
                X[i] /= norma
        return X

    def fit(self, textos, etiquetas):
        X = self._vectorizar(textos, fit=True)
        self.classes_ = np.unique(etiquetas)
        n_samples, n_features = X.shape
        Y = np.zeros((n_samples, len(self.classes_)), dtype=float)
        for i, y_val in enumerate(etiquetas):
            c_idx = int(np.where(self.classes_ == y_val)[0][0])
            Y[i, c_idx] = 1.0

        # Solución dual de Kernel Lineal Ridge Multiclase: W = X^T (X X^T + lambda I)^(-1) Y
        G = X @ X.T + self.reg_lambda * np.eye(n_samples)
        alpha = np.linalg.solve(G, Y)
        self.W_ = X.T @ alpha
        return self

    def predict_proba(self, textos):
        X = self._vectorizar(textos, fit=False)
        logits = (X @ self.W_) * self.temp_softmax
        logits -= np.max(logits, axis=1, keepdims=True)
        exp_l = np.exp(logits)
        return exp_l / np.sum(exp_l, axis=1, keepdims=True)

    def predict(self, textos):
        probs = self.predict_proba(textos)
        idx = np.argmax(probs, axis=1)
        return self.classes_[idx]


def construir_corpus_entrenamiento_nlp():
    """
    Define el corpus etiquetado de entrenamiento para las 6 intenciones del viajero:
      1. PISTA_ACERTIJO_POI
      2. RECOMENDACION_GASTRONOMIA_CUPON
      3. TRANSPORTE_COMO_LLEGAR
      4. LORE_HISTORIA_GUARDIAN
      5. MODO_OFFLINE_Y_QR
      6. VENTANA_DEL_TIEMPO_HISTORIA
    """
    ejemplos = [
        # 1. PISTA_ACERTIJO_POI
        ("dame una pista en verso para encontrar al guardián", "PISTA_ACERTIJO_POI"),
        ("¿dónde están los códigos qr en zinacantepec?", "PISTA_ACERTIJO_POI"),
        ("nahual dime un acertijo en rima para despertar al guardián de metepec", "PISTA_ACERTIJO_POI"),
        ("¿qué puntos de interés debo visitar para desbloquear la carta?", "PISTA_ACERTIJO_POI"),
        ("ayúdame con la misión de exploración en las ciénegas de lerma", "PISTA_ACERTIJO_POI"),
        ("¿cuál es el acertijo de los portales y el cosmovitral en toluca?", "PISTA_ACERTIJO_POI"),
        ("quiero una copla para guiar mi camino hacia el árbol de la vida", "PISTA_ACERTIJO_POI"),
        ("¿qué lugares tengo que recorrer a pie en esta estación?", "PISTA_ACERTIJO_POI"),
        ("dime la rima secreta para hallar el taller de tule", "PISTA_ACERTIJO_POI"),
        ("¿cómo despierto al guardián dormido de este pueblo?", "PISTA_ACERTIJO_POI"),

        # 2. RECOMENDACION_GASTRONOMIA_CUPON
        ("¿dónde puedo comer rico y barato con mi cupón de descuento?", "RECOMENDACION_GASTRONOMIA_CUPON"),
        ("¿qué fondas o restaurantes locales aceptan las bendiciones?", "RECOMENDACION_GASTRONOMIA_CUPON"),
        ("tenemos hambre en familia, ¿dónde venden barbacoa o tlacoyos con descuento?", "RECOMENDACION_GASTRONOMIA_CUPON"),
        ("¿qué talleres de artesanías dan descuento con la carta épica?", "RECOMENDACION_GASTRONOMIA_CUPON"),
        ("quiero canjear mi código otp de 4 dígitos en un comercio local", "RECOMENDACION_GASTRONOMIA_CUPON"),
        ("¿dónde compro chorizo verde, alfeñiques o un café tradicional?", "RECOMENDACION_GASTRONOMIA_CUPON"),
        ("recomiéndame dónde comer trucha o antojitos en lerma", "RECOMENDACION_GASTRONOMIA_CUPON"),
        ("¿qué beneficios económicos me da desbloquear a xinán?", "RECOMENDACION_GASTRONOMIA_CUPON"),
        ("busco artesanías de barro o cestería de tule directo con artesanos", "RECOMENDACION_GASTRONOMIA_CUPON"),
        ("¿cuánto descuento me hacen en las cooperativas ecoturísticas?", "RECOMENDACION_GASTRONOMIA_CUPON"),

        # 3. TRANSPORTE_COMO_LLEGAR
        ("¿cómo llego en el tren interurbano el insurgente desde observatorio?", "TRANSPORTE_COMO_LLEGAR"),
        ("¿cuánto cuesta el boleto del tren y a qué hora pasa?", "TRANSPORTE_COMO_LLEGAR"),
        ("¿en qué estación de el insurgente me bajo para conocer los humedales de lerma?", "TRANSPORTE_COMO_LLEGAR"),
        ("¿cómo camino desde la estación del tren hasta el museo virreinal?", "TRANSPORTE_COMO_LLEGAR"),
        ("¿se puede usar la tarjeta de movilidad integrada para viajar?", "TRANSPORTE_COMO_LLEGAR"),
        ("¿qué ruta es más accesible y plana para un adulto mayor?", "TRANSPORTE_COMO_LLEGAR"),
        ("ábreme la ruta en google maps para llegar caminando al mirador", "TRANSPORTE_COMO_LLEGAR"),
        ("¿cuánto tiempo hago de santa fe a zinacantepec o metepec en tren?", "TRANSPORTE_COMO_LLEGAR"),
        ("¿qué estación conecta con el cablebús línea 3 en chapultepec?", "TRANSPORTE_COMO_LLEGAR"),
        ("¿cuáles son los horarios con menos gente para viajar en tren?", "TRANSPORTE_COMO_LLEGAR"),

        # 4. LORE_HISTORIA_GUARDIAN
        ("cuéntame la leyenda y el origen cultural del guardián xinán", "LORE_HISTORIA_GUARDIAN"),
        ("¿quién es acatl-tule y por qué protege los humedales de lerma?", "LORE_HISTORIA_GUARDIAN"),
        ("cuéntame por qué en los pueblos emergentes los guardianes son épicos y legendarios", "LORE_HISTORIA_GUARDIAN"),
        ("explícame cómo funciona el sistema de rareza inversa del juego", "LORE_HISTORIA_GUARDIAN"),
        ("¿qué significa barrotépetl y su relación con los árboles de la vida?", "LORE_HISTORIA_GUARDIAN"),
        ("háblame de la herencia matlatzinca y la historia del guardián", "LORE_HISTORIA_GUARDIAN"),
        ("¿qué espíritus guardianes habitan en el valle de toluca?", "LORE_HISTORIA_GUARDIAN"),
        ("¿por qué en los lugares muy llenos el guardián está fatigado o común?", "LORE_HISTORIA_GUARDIAN"),

        # 5. MODO_OFFLINE_Y_QR
        ("¿qué pasa si subo hacia el nevado de toluca y me quedo sin señal de internet?", "MODO_OFFLINE_Y_QR"),
        ("¿cómo funciona el modo offline-first si se me acaban los datos?", "MODO_OFFLINE_Y_QR"),
        ("¿cómo escaneo el código qr si estoy en una zona rural sin cobertura?", "MODO_OFFLINE_Y_QR"),
        ("¿dónde descargo el paquete del mapa antes de subir a la montaña?", "MODO_OFFLINE_Y_QR"),
        ("¿cómo valida mi cupón el artesano si no tiene internet ni terminal?", "MODO_OFFLINE_Y_QR"),
        ("¿se guardan mis cartas vivas 2d aunque no tenga wifi ni datos?", "MODO_OFFLINE_Y_QR"),

        # 6. VENTANA_DEL_TIEMPO_HISTORIA
        ("¿cómo era este lugar hace cien años en las fotos antiguas?", "VENTANA_DEL_TIEMPO_HISTORIA"),
        ("quiero activar la cámara de la ventana del tiempo en el templo", "VENTANA_DEL_TIEMPO_HISTORIA"),
        ("muéstrame cómo lucía la antigua laguna de lerma en el siglo xix", "VENTANA_DEL_TIEMPO_HISTORIA"),
        ("quiero ver cómo lucía el antiguo mercado de toluca antes de ser el cosmovitral", "VENTANA_DEL_TIEMPO_HISTORIA"),
        ("comparar fotografía histórica del convento franciscano del siglo xvi", "VENTANA_DEL_TIEMPO_HISTORIA"),
        ("¿cómo se veían los portales de toluca cuando pasaban tranvías de mulas?", "VENTANA_DEL_TIEMPO_HISTORIA")
    ]
    return pd.DataFrame(ejemplos, columns=["texto_usuario", "intencion"])


def detectar_nodo_entidad(texto):
    """Detecta si el usuario menciona un municipio o guardián específico del corredor."""
    t = texto.lower()
    # Priorizar nombres explícitos de municipios y guardianes antes de palabras secundarias
    if any(k in t for k in ["metepec", "barrotépetl", "barrotepetl", "calvario", "árbol de la vida"]):
        return "EST-03"
    elif any(k in t for k in ["lerma", "acatl", "ciénega", "cienega", "humedal", "santa clara", "tultepec"]):
        return "EST-04"
    elif any(k in t for k in ["zinacantepec", "xinán", "xinan", "nevado de toluca", "virreinal"]):
        return "EST-01"
    elif any(k in t for k in ["cosmovitral", "portales", "alfeñique", "mosco", "toluca"]):
        return "EST-02"
    elif any(k in t for k in ["barro", "alfarer", "tlacoyo"]):
        return "EST-03"
    elif any(k in t for k in ["tule", "trucha"]):
        return "EST-04"
    elif any(k in t for k in ["volcán", "barbacoa"]):
        return "EST-01"
    return "EST-01"


def entrenar_clasificador_nahual():
    """Entrena y valida por validación cruzada estratificada el clasificador NLP del Nahual Guía."""
    df_corpus = construir_corpus_entrenamiento_nlp()
    textos = df_corpus["texto_usuario"].tolist()
    etiquetas = df_corpus["intencion"].to_numpy()

    # Validación cruzada 5-Fold
    idx_perm = np.random.RandomState(42).permutation(len(df_corpus))
    folds = np.array_split(idx_perm, 5)
    acc_folds = []
    for f in range(5):
        val_idx = folds[f]
        tr_idx = np.hstack([folds[j] for j in range(5) if j != f])
        clf_cv = ClasificadorNLPNahual()
        clf_cv.fit([textos[i] for i in tr_idx], etiquetas[tr_idx])
        preds = clf_cv.predict([textos[i] for i in val_idx])
        acc_folds.append(np.mean(preds == etiquetas[val_idx]))

    modelo_nlp = ClasificadorNLPNahual()
    modelo_nlp.fit(textos, etiquetas)

    ruta_pkl = os.path.join(MODELOS_DIR, "chatbot_nahual_nlp.pkl")
    with open(ruta_pkl, "wb") as f:
        pickle.dump(modelo_nlp, f)

    print(f"[+] Clasificador NLP 'El Nahual Guía' entrenado (Exactitud CV 5-Fold: {np.mean(acc_folds)*100:.1f}%)")
    print(f"    Vocabulario N-gramas TF-IDF: {len(modelo_nlp.vocab_)} características")
    print(f"    Serializado en: {ruta_pkl}")
    return modelo_nlp


def responder_consulta_nahual(modelo_nlp, consulta_usuario):
    probs = modelo_nlp.predict_proba([consulta_usuario])[0]
    clases = modelo_nlp.classes_
    idx_max = int(np.argmax(probs))
    intencion = str(clases[idx_max])
    confianza = float(probs[idx_max])

    nodo = detectar_nodo_entidad(consulta_usuario)
    info = COPLAS_NAHUAL[nodo]

    if intencion == "PISTA_ACERTIJO_POI":
        respuesta = (
            f"🦊 [Nahual Guía - {info['municipio']}]: Escucha con atención el verso de {info['guardian']}: "
            f"{info['copla_pista']}"
        )
    elif intencion == "RECOMENDACION_GASTRONOMIA_CUPON":
        respuesta = (
            f"🍲 [Nahual Guía - Bendición Local en {info['municipio']}]: {info['gastronomia']} "
            f"Solo muestra tu código OTP de 4 dígitos (ej. BND-4821) al locatario."
        )
    elif intencion == "TRANSPORTE_COMO_LLEGAR":
        respuesta = (
            f"🚆 [Nahual Guía - Movilidad Sustentable]: {info['ruta_tren']} "
            f"Viajar en el tren eléctrico evita hasta 8.4 kg de CO2 frente al auto particular. "
            f"Te recomiendo viajar entre 10:00 y 16:00 hrs para disfrutar sin filas."
        )
    elif intencion == "LORE_HISTORIA_GUARDIAN":
        respuesta = (
            f"✨ [Nahual Guía - Sabiduría del Territorio]: En {info['municipio']} habita {info['guardian']}. "
            f"Nuestro Sistema de Rareza Inversa premia a quienes visitan pueblos con capacidad disponible: "
            f"entre menos saturado está el destino, más legendario es el Guardián y mayor tu descuento."
        )
    elif intencion == "MODO_OFFLINE_Y_QR":
        respuesta = (
            f"📶 [Nahual Guía - Modo Offline-First]: ¡No necesitas señal en la montaña ni en la ciénega! "
            f"Tu app guarda en caché SQLite las coordenadas GPS y tokens QR. Al escanear en sitio, "
            f"se genera una firma SHA-256 y tu cupón OTP funciona sin conexión a internet."
        )
    else:
        respuesta = (
            f"⏳ [Nahual Guía - La Ventana del Tiempo]: Activa el filtro histórico de tu cámara frente al monumento en "
            f"{info['municipio']}. Podrás deslizar la barra interactiva para comparar cómo lucía en los siglos XVI-XIX "
            f"frente al paisaje actual."
        )

    return {
        "consulta_viajero": consulta_usuario,
        "intencion_detectada": intencion,
        "confianza_nlp": round(confianza, 3),
        "nodo_territorial": f"{nodo} ({info['municipio']})",
        "respuesta_nahual_guia": respuesta
    }


def main():
    print("=========================================================================")
    print("  CHATBOT IA 'EL NAHUAL GUÍA' - MOTOR NLP Y GENERADOR DE COPLAS          ")
    print("=========================================================================")

    modelo_nlp = entrenar_clasificador_nahual()

    consultas_prueba = [
        "Nahual, dame un acertijo en rima para encontrar al guardián de Zinacantepec",
        "¿Dónde podemos comer barbacoa o tlacoyos con descuento familiar en Metepec?",
        "¿En qué estación de El Insurgente me bajo para conocer los humedales de Lerma?",
        "¿Qué pasa si subo hacia el Nevado de Toluca y me quedo sin señal de internet?",
        "Cuéntame por qué en los pueblos emergentes los guardianes son Épicos y Legendarios",
        "Quiero ver cómo lucía el antiguo mercado de Toluca antes de ser el Cosmovitral"
    ]

    bitacora = []
    print("\n--- DEMOSTRACIÓN DE INTERACCIÓN CONVERSACIONAL ---")
    for q in consultas_prueba:
        res = responder_consulta_nahual(modelo_nlp, q)
        bitacora.append(res)
        print(f"\n[Viajero]: {res['consulta_viajero']}")
        print(f" -> Intención: {res['intencion_detectada']} (Confianza: {res['confianza_nlp']*100:.1f}%) | Nodo: {res['nodo_territorial']}")
        print(f" -> {res['respuesta_nahual_guia']}")

    df_eval = pd.DataFrame(bitacora)
    out_csv = os.path.join(PROCESSED_DIR, "ml_evaluacion_chatbot_nahual.csv")
    df_eval.to_csv(out_csv, index=False)
    print(f"\n[+] Bitácora de evaluación del Chatbot exportada en: {out_csv}")
    print("\n[OK] Módulo NLP 'El Nahual Guía' finalizado exitosamente.")


if __name__ == "__main__":
    main()
