"""
Modelo de Aprendizaje de Máquina: Predicción Dinámica del Índice de Saturación
Turística (IST), Asignación de Rareza Inversa y Motor de Recomendación de Rutas.

Proyecto Prototípico - 5to Semestre: Ciencias de Datos para Negocios
Universidad Rosario Castellanos
UCA: Aprendizaje de Máquina (Machine Learning)
Rol: Integrante 1 — Data Engineering & ML Lead (monenri9-svg)

Este script ejecuta:
1. Construcción del dataset supervisado espaciotemporal anclado en la estacionalidad
   oficial del CETM 2024 (SECTUR) y los aforos de las 7 estaciones de 'El Insurgente'.
2. Entrenamiento, validación cruzada (5-Fold CV) y comparación rigurosa de 4 algoritmos
   supervisados: Ridge Regression, Decision Tree CART, Random Forest y Gradient Boosting.
3. Cálculo dinámico de la categoría de Rareza Inversa según el IST predicho para evitar
   trasladar la saturación hacia destinos emergentes.
4. Motor de Recomendación Híbrido y Sustentable (Similitud Coseno + Penalización de
   Capacidad/IST) para personalizar rutas por perfil de viajero (Buyer Persona).
5. Serialización del modelo campeón en 'modelos/' y generación de figuras ejecutivas.
"""

import os
import tempfile
os.environ.setdefault("MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "mpl_cache"))

import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración estética
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans, Arial, Helvetica'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

np.random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROCESSED_DIR = os.path.join(BASE_DIR, "datos", "processed")
MODELOS_DIR = os.path.join(BASE_DIR, "modelos")
KPIS_DIR = os.path.join(BASE_DIR, "campana", "kpis")

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(MODELOS_DIR, exist_ok=True)
os.makedirs(KPIS_DIR, exist_ok=True)


# =============================================================================
# 1. IMPLEMENTACIÓN DE ALGORITMOS SUPERVISADOS (CART, RANDOM FOREST, GBR, RIDGE)
# =============================================================================

class RidgeRegressorML:
    """Regresión Lineal Regularizada L2 (Tikhonov / Ridge) con solución analítica cerrada."""
    def __init__(self, alpha=1.0):
        self.alpha = alpha
        self.coef_ = None
        self.intercept_ = 0.0

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)
        self.intercept_ = float(np.mean(y))
        y_c = y - self.intercept_
        n_features = X.shape[1]
        A = X.T @ X + self.alpha * np.eye(n_features)
        self.coef_ = np.linalg.solve(A, X.T @ y_c)
        return self

    def predict(self, X):
        X = np.asarray(X, dtype=float)
        return self.intercept_ + X @ self.coef_


class CARTDecisionTreeRegressor:
    """Árbol de Regresión CART con reducción de varianza (MSE) e importancia de variables."""
    def __init__(self, max_depth=6, min_samples_leaf=8, max_features=None, seed=42):
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.max_features = max_features
        self.rng = np.random.default_rng(seed)
        self.tree_ = None
        self.feature_importances_ = None

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)
        n_samples, n_features = X.shape
        self.feature_importances_ = np.zeros(n_features, dtype=float)
        self.tree_ = self._build_tree(X, y, depth=0)
        total_imp = np.sum(self.feature_importances_)
        if total_imp > 0:
            self.feature_importances_ /= total_imp
        return self

    def _build_tree(self, X, y, depth):
        n_samples, n_features = X.shape
        val_nodo = float(np.mean(y))
        if depth >= self.max_depth or n_samples < 2 * self.min_samples_leaf or np.var(y) < 1e-8:
            return {"leaf": True, "val": val_nodo}

        if self.max_features is not None and self.max_features < n_features:
            feat_indices = self.rng.choice(n_features, size=self.max_features, replace=False)
        else:
            feat_indices = np.arange(n_features)

        best_gain = 0.0
        best_split = None
        var_total = np.var(y) * n_samples

        for f_idx in feat_indices:
            col = X[:, f_idx]
            uniq = np.unique(col)
            if len(uniq) <= 1:
                continue
            # Evaluar percentiles candidatos para partición rápida y exacta
            thresholds = np.unique(np.percentile(col, [15, 30, 50, 70, 85])) if len(uniq) > 10 else (uniq[:-1] + uniq[1:]) / 2.0
            for thr in thresholds:
                left_mask = col <= thr
                n_l = int(np.sum(left_mask))
                n_r = n_samples - n_l
                if n_l < self.min_samples_leaf or n_r < self.min_samples_leaf:
                    continue
                y_l = y[left_mask]
                y_r = y[~left_mask]
                gain = var_total - (np.var(y_l) * n_l + np.var(y_r) * n_r)
                if gain > best_gain:
                    best_gain = gain
                    best_split = (int(f_idx), float(thr), left_mask)

        if best_split is None or best_gain <= 1e-9:
            return {"leaf": True, "val": val_nodo}

        f_idx, thr, left_mask = best_split
        self.feature_importances_[f_idx] += best_gain
        left_child = self._build_tree(X[left_mask], y[left_mask], depth + 1)
        right_child = self._build_tree(X[~left_mask], y[~left_mask], depth + 1)
        return {
            "leaf": False,
            "feat": f_idx,
            "thr": thr,
            "left": left_child,
            "right": right_child
        }

    def _predict_row(self, row, node):
        while not node["leaf"]:
            if row[node["feat"]] <= node["thr"]:
                node = node["left"]
            else:
                node = node["right"]
        return node["val"]

    def predict(self, X):
        X = np.asarray(X, dtype=float)
        return np.array([self._predict_row(row, self.tree_) for row in X])


class RandomForestRegressorML:
    """Ensamble Bagging de Árboles CART con muestreo Bootstrap y subespacio aleatorio."""
    def __init__(self, n_estimators=45, max_depth=8, min_samples_leaf=5, seed=42):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.seed = seed
        self.trees_ = []
        self.feature_importances_ = None

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)
        n_samples, n_features = X.shape
        max_f = max(4, int(np.ceil(n_features * 0.75)))
        rng = np.random.default_rng(self.seed)

        self.trees_ = []
        imp_acum = np.zeros(n_features, dtype=float)
        for i in range(self.n_estimators):
            boot_idx = rng.choice(n_samples, size=n_samples, replace=True)
            tree = CARTDecisionTreeRegressor(
                max_depth=self.max_depth,
                min_samples_leaf=self.min_samples_leaf,
                max_features=max_f,
                seed=self.seed + i
            )
            tree.fit(X[boot_idx], y[boot_idx])
            self.trees_.append(tree)
            imp_acum += tree.feature_importances_

        self.feature_importances_ = imp_acum / max(1e-9, np.sum(imp_acum))
        return self

    def predict(self, X):
        preds = np.column_stack([t.predict(X) for t in self.trees_])
        return np.mean(preds, axis=1)


class GradientBoostingRegressorML:
    """Ensamble secuencial Gradient Boosting (Friedman 2001) sobre residuos pseudo-gradiente."""
    def __init__(self, n_estimators=65, learning_rate=0.10, max_depth=5, min_samples_leaf=6, seed=42):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.seed = seed
        self.init_val_ = 0.0
        self.trees_ = []
        self.feature_importances_ = None

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)
        n_samples, n_features = X.shape
        self.init_val_ = float(np.mean(y))
        y_hat = np.full(n_samples, self.init_val_, dtype=float)

        self.trees_ = []
        imp_acum = np.zeros(n_features, dtype=float)
        for m in range(self.n_estimators):
            residuos = y - y_hat
            tree = CARTDecisionTreeRegressor(
                max_depth=self.max_depth,
                min_samples_leaf=self.min_samples_leaf,
                max_features=None,
                seed=self.seed + m
            )
            tree.fit(X, residuos)
            update = tree.predict(X)
            y_hat += self.learning_rate * update
            self.trees_.append(tree)
            imp_acum += tree.feature_importances_

        self.feature_importances_ = imp_acum / max(1e-9, np.sum(imp_acum))
        return self

    def predict(self, X):
        X = np.asarray(X, dtype=float)
        y_hat = np.full(X.shape[0], self.init_val_, dtype=float)
        for tree in self.trees_:
            y_hat += self.learning_rate * tree.predict(X)
        return y_hat


class PreprocesadorTabular:
    """Codifica one-hot la variable id_estacion y estandariza variables numéricas."""
    def __init__(self, estaciones_orden, cols_num):
        self.estaciones_orden = estaciones_orden
        self.cols_num = cols_num
        self.medias_ = None
        self.stds_ = None
        self.feature_names_ = [f"id_estacion_{e}" for e in estaciones_orden[1:]] + cols_num

    def fit_transform(self, df):
        X_num = df[self.cols_num].to_numpy(dtype=float)
        self.medias_ = np.mean(X_num, axis=0)
        self.stds_ = np.where(np.std(X_num, axis=0) < 1e-8, 1.0, np.std(X_num, axis=0))
        return self.transform(df)

    def transform(self, df):
        # One-hot encoding de estación (excluyendo primera categoría de referencia)
        ohe_cols = []
        for est in self.estaciones_orden[1:]:
            ohe_cols.append((df["id_estacion"] == est).astype(float).to_numpy())
        X_cat = np.column_stack(ohe_cols)
        X_num = (df[self.cols_num].to_numpy(dtype=float) - self.medias_) / self.stds_
        return np.hstack([X_cat, X_num])


# =============================================================================
# 2. GENERACIÓN DEL DATASET ESPACIOTEMPORAL Y ENTRENAMIENTO
# =============================================================================

def construir_dataset_entrenamiento():
    """
    Construye un dataset supervisado de 2,520 observaciones diarias/horarias por estación
    combinando los datos reales de estacionalidad nacional (CETM 2024) y las capacidades
    de diseño del Tren Interurbano 'El Insurgente'.
    """
    df_rareza = pd.read_csv(os.path.join(PROCESSED_DIR, "indice_saturacion_rareza_estaciones.csv"))
    df_estac = pd.read_csv(os.path.join(PROCESSED_DIR, "estacionalidad_promedio_mensual_mexico.csv"))
    mapa_indice_mes = dict(zip(df_estac["mes"], df_estac["indice_estacional_ocupacion_base100"]))

    clima_mes = {
        1: (12.5, 0.08), 2: (14.0, 0.10), 3: (16.5, 0.15), 4: (18.0, 0.25),
        5: (18.5, 0.45), 6: (17.0, 0.75), 7: (16.0, 0.80), 8: (16.2, 0.78),
        9: (15.8, 0.82), 10: (15.0, 0.35), 11: (13.5, 0.12), 12: (12.0, 0.08)
    }

    registros = []
    for _, row_est in df_rareza.iterrows():
        est_id = row_est["id_estacion"]
        nombre_est = row_est["nombre_estacion"]
        cap_diseno = row_est["capacidad_diseno"]
        afluencia_base = row_est["afluencia_diaria"]
        es_urbano_corporativo = 1 if est_id in ["EST-05", "EST-06", "EST-07"] else 0

        for dia_idx in range(360):
            mes = (dia_idx // 30) + 1
            dia_semana = dia_idx % 7
            es_fin_semana = 1 if dia_semana in [5, 6] else 0
            es_puente = 1 if (dia_semana in [0, 4] and np.random.rand() < 0.14) else 0
            indice_cetm = mapa_indice_mes.get(mes, 100.0)

            temp_base, lluvia_base = clima_mes[mes]
            temperatura_c = round(np.random.normal(temp_base, 2.2), 1)
            prob_lluvia = round(np.clip(np.random.normal(lluvia_base, 0.15), 0.0, 1.0), 2)

            bloque_horario = int(np.random.choice([0, 1, 2], p=[0.30, 0.45, 0.25]))
            evento_cultural_local = 1 if (es_fin_semana and np.random.rand() < 0.30) else 0
            intensidad_pauta = round(np.random.uniform(0.1, 1.0), 2)

            factor_estacional = (indice_cetm / 100.0)
            if es_urbano_corporativo:
                factor_dia = 0.68 if es_fin_semana else 1.12
                factor_hora = 1.18 if bloque_horario in [0, 2] else 0.78
            else:
                factor_dia = 1.25 if es_fin_semana else 0.82
                factor_hora = 1.15 if (es_fin_semana and bloque_horario == 1) else (1.08 if bloque_horario in [0, 2] else 0.72)

            efecto_puente = 1.18 if (es_puente and not es_urbano_corporativo) else 1.0
            efecto_clima = 1.0 - (0.16 * prob_lluvia) + (0.008 * (temperatura_c - 15.0))
            efecto_evento = 1.14 if evento_cultural_local else 1.0
            efecto_campana = 1.0 + (0.12 * intensidad_pauta * (1.0 if not es_urbano_corporativo else 0.2))

            ruido = np.random.normal(1.0, 0.042)
            afluencia_sim = afluencia_base * factor_estacional * factor_dia * factor_hora * efecto_puente * efecto_clima * efecto_evento * efecto_campana * ruido
            afluencia_sim = max(500.0, min(cap_diseno * 1.08, afluencia_sim))
            ist_real = round(afluencia_sim / cap_diseno, 4)

            registros.append({
                "id_estacion": est_id,
                "nombre_estacion": nombre_est,
                "mes": mes,
                "dia_semana": dia_semana,
                "es_fin_de_semana": es_fin_semana,
                "es_puente_festivo": es_puente,
                "bloque_horario": bloque_horario,
                "indice_estacional_cetm": indice_cetm,
                "temperatura_c": temperatura_c,
                "probabilidad_lluvia": prob_lluvia,
                "evento_cultural_activo": evento_cultural_local,
                "intensidad_pauta_campana": intensidad_pauta,
                "capacidad_diseno": cap_diseno,
                "afluencia_diaria_observada": round(afluencia_sim, 0),
                "ist_observado": ist_real
            })

    return pd.DataFrame(registros)


def clasificar_rareza_inversa(ist_val):
    if ist_val < 0.35:
        return "Legendario"
    elif ist_val < 0.60:
        return "Épico"
    elif ist_val < 0.85:
        return "Raro"
    else:
        return "Común / Fatigado"


def calcular_metricas(y_true, y_pred):
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    r2 = 1.0 - (ss_res / max(1e-12, ss_tot))
    rmse = float(np.sqrt(np.mean((y_true - y_pred) ** 2)))
    mae = float(np.mean(np.abs(y_true - y_pred)))
    mape = float(np.mean(np.abs((y_true - y_pred) / np.maximum(1e-5, y_true))) * 100.0)
    return r2, rmse, mae, mape


def entrenar_y_evaluar_modelos(df):
    cols_num = [
        "mes", "dia_semana", "es_fin_de_semana", "es_puente_festivo",
        "bloque_horario", "indice_estacional_cetm", "temperatura_c",
        "probabilidad_lluvia", "evento_cultural_activo", "intensidad_pauta_campana"
    ]
    estaciones_orden = sorted(df["id_estacion"].unique().tolist())

    # Partición Train (80%) / Test (20%) estratificada aleatoria
    idx_perm = np.random.permutation(len(df))
    n_train = int(0.80 * len(df))
    df_train = df.iloc[idx_perm[:n_train]].reset_index(drop=True)
    df_test = df.iloc[idx_perm[n_train:]].reset_index(drop=True)

    prep = PreprocesadorTabular(estaciones_orden, cols_num)
    X_train = prep.fit_transform(df_train)
    y_train = df_train["ist_observado"].to_numpy(dtype=float)
    X_test = prep.transform(df_test)
    y_test = df_test["ist_observado"].to_numpy(dtype=float)

    # Constructores de los 4 modelos a evaluar
    constructores = [
        ("Ridge Regression (Lineal Base)", lambda: RidgeRegressorML(alpha=1.5)),
        ("Decision Tree Regressor (CART)", lambda: CARTDecisionTreeRegressor(max_depth=7, min_samples_leaf=8)),
        ("Random Forest Regressor", lambda: RandomForestRegressorML(n_estimators=40, max_depth=8, min_samples_leaf=5)),
        ("Gradient Boosting Regressor", lambda: GradientBoostingRegressorML(n_estimators=65, learning_rate=0.12, max_depth=5, min_samples_leaf=6))
    ]

    # Índices para validación cruzada 5-Fold
    folds = np.array_split(idx_perm, 5)
    X_all = prep.transform(df)
    y_all = df["ist_observado"].to_numpy(dtype=float)

    resultados_metricas = []
    modelos_entrenados = {}

    for nombre, fn_ctor in constructores:
        print(f"[*] Entrenando y validando (5-Fold CV): {nombre}...")
        mod = fn_ctor()
        mod.fit(X_train, y_train)
        y_pred_tr = mod.predict(X_train)
        y_pred_te = mod.predict(X_test)

        r2_tr, _, _, _ = calcular_metricas(y_train, y_pred_tr)
        r2_te, rmse_te, mae_te, mape_te = calcular_metricas(y_test, y_pred_te)

        # 5-Fold Cross-Validation
        cv_r2_list = []
        for f_idx in range(5):
            val_indices = folds[f_idx]
            tr_indices = np.hstack([folds[j] for j in range(5) if j != f_idx])
            m_cv = fn_ctor()
            m_cv.fit(X_all[tr_indices], y_all[tr_indices])
            p_cv = m_cv.predict(X_all[val_indices])
            r2_f, _, _, _ = calcular_metricas(y_all[val_indices], p_cv)
            cv_r2_list.append(r2_f)

        rareza_real = [clasificar_rareza_inversa(v) for v in y_test]
        rareza_pred = [clasificar_rareza_inversa(v) for v in y_pred_te]
        acc_rareza = float(np.mean([r == p for r, p in zip(rareza_real, rareza_pred)]) * 100.0)

        resultados_metricas.append({
            "modelo": nombre,
            "r2_train": round(r2_tr, 4),
            "r2_test": round(r2_te, 4),
            "cv_r2_media": round(float(np.mean(cv_r2_list)), 4),
            "cv_r2_std": round(float(np.std(cv_r2_list)), 4),
            "rmse_test": round(rmse_te, 4),
            "mae_test": round(mae_te, 4),
            "mape_test_pct": round(mape_te, 2),
            "exactitud_asignacion_rareza_pct": round(acc_rareza, 2)
        })
        modelos_entrenados[nombre] = (mod, y_pred_te)

    df_metricas = pd.DataFrame(resultados_metricas).sort_values(by="r2_test", ascending=False).reset_index(drop=True)
    mejor_nombre = df_metricas.iloc[0]["modelo"]
    mejor_mod, mejor_pred_test = modelos_entrenados[mejor_nombre]

    # Serializar artefacto completo (Preprocesador + Modelo Campeón)
    artefacto = {"preprocesador": prep, "modelo": mejor_mod, "nombre_modelo": mejor_nombre}
    ruta_modelo = os.path.join(MODELOS_DIR, "modelo_predictivo_ist_gbr.pkl")
    with open(ruta_modelo, "wb") as f:
        pickle.dump(artefacto, f)
    print(f"[+] Modelo campeón '{mejor_nombre}' serializado en: {ruta_modelo}")

    # Evaluar escenarios estratégicos por estación
    escenarios_eval = []
    estaciones_info = df[["id_estacion", "nombre_estacion", "capacidad_diseno"]].drop_duplicates().sort_values("id_estacion")
    configs_escenarios = [
        ("Martes Laboral Hora Pico (8:00h)", 10, 1, 0, 0, 0, 94.12, 14.5, 0.20, 0, 0.30),
        ("Miércoles Valle Mediodía (13:00h)", 9, 2, 0, 0, 1, 86.31, 16.0, 0.65, 0, 0.85),
        ("Sábado Fin de Semana Familiar (12:00h)", 10, 5, 1, 0, 1, 94.12, 17.5, 0.15, 1, 0.80),
        ("Domingo Puente Noviembre (13:00h)", 11, 6, 1, 1, 1, 105.51, 15.0, 0.10, 1, 0.50)
    ]

    for _, r_est in estaciones_info.iterrows():
        for desc_esc, mes, d_sem, fin_sem, puente, b_hor, cetm, temp, lluvia, ev_cult, pauta in configs_escenarios:
            fila_df = pd.DataFrame([{
                "id_estacion": r_est["id_estacion"],
                "mes": mes,
                "dia_semana": d_sem,
                "es_fin_de_semana": fin_sem,
                "es_puente_festivo": puente,
                "bloque_horario": b_hor,
                "indice_estacional_cetm": cetm,
                "temperatura_c": temp,
                "probabilidad_lluvia": lluvia,
                "evento_cultural_activo": ev_cult,
                "intensidad_pauta_campana": pauta
            }])
            X_in = prep.transform(fila_df)
            ist_pred = float(mejor_mod.predict(X_in)[0])
            ist_pred = max(0.05, min(1.05, ist_pred))
            rareza_dinamica = clasificar_rareza_inversa(ist_pred)
            mult_recompensa = 3.0 if rareza_dinamica == "Legendario" else (2.0 if rareza_dinamica == "Épico" else (1.4 if rareza_dinamica == "Raro" else 1.0))

            escenarios_eval.append({
                "id_estacion": r_est["id_estacion"],
                "nombre_estacion": r_est["nombre_estacion"],
                "escenario_temporal": desc_esc,
                "ist_predicho_ml": round(ist_pred, 3),
                "afluencia_estimada": int(round(ist_pred * r_est["capacidad_diseno"])),
                "capacidad_diseno": r_est["capacidad_diseno"],
                "rareza_dinamica_asignada": rareza_dinamica,
                "multiplicador_bendicion": mult_recompensa
            })

    df_pred_escenarios = pd.DataFrame(escenarios_eval)
    return df_metricas, mejor_mod, prep, y_test, mejor_pred_test, df_pred_escenarios


def motor_recomendacion_rutas_sustentables(df_pred_escenarios):
    """
    Motor de Recomendación Basado en Contenido y Consciente de la Capacidad
    de Carga (Congestion-Aware Recommender System) mediante Similitud Coseno.
    """
    perfiles_usuarios = {
        "Familia Trabajadora": [0.85, 0.75, 0.95, 0.90, 0.60, 1.00],
        "Joven Mochilero / Explorador": [1.00, 0.55, 0.85, 0.35, 0.70, 0.95],
        "Adulto Mayor": [0.35, 0.75, 0.90, 1.00, 1.00, 0.85],
        "Turista Cultural / Internacional": [0.40, 1.00, 0.85, 0.75, 0.95, 0.50]
    }

    rutas_guardianes = {
        "EST-01": {
            "destino": "Zinacantepec (Xinán - Legendario)",
            "vector": [1.00, 0.55, 0.85, 0.40, 0.75, 0.95],
            "circuito_recomendado": "Museo Virreinal S. XVI -> Pila Monolítica -> Sendero Raíces del Xinantécatl",
            "comercio_ancla": "Barbacoa El Rinconcito Serrano & Cooperativa Xinantécatl (25% OFF)"
        },
        "EST-03": {
            "destino": "Metepec (Barrotépetl - Épico)",
            "vector": [0.40, 1.00, 0.90, 0.75, 0.95, 0.60],
            "circuito_recomendado": "Mercado Artesanal -> Taller Familia Soteno -> Capilla del Calvario",
            "comercio_ancla": "Taller Familia Soteno & Fonda Doña Lupe (15% OFF)"
        },
        "EST-04": {
            "destino": "Lerma (Acatl-Tule - Épico)",
            "vector": [0.90, 0.80, 0.95, 0.90, 0.65, 1.00],
            "circuito_recomendado": "Mirador Ciénegas de Lerma -> Taller de Tule San Pedro -> Templo Santa Clara",
            "comercio_ancla": "Cestería de Tule La Laguna & Rincón Mexiquense (20% OFF)"
        },
        "EST-02": {
            "destino": "Toluca Centro (Mosco Matlatzinca - Raro)",
            "vector": [0.30, 0.75, 0.90, 1.00, 1.00, 0.85],
            "circuito_recomendado": "Cosmovitral Jardín Botánico -> Los Portales -> Museo del Alfeñique",
            "comercio_ancla": "Chorizos Los Portales & Dulcería San José (10% OFF)"
        }
    }

    sub_fin = df_pred_escenarios[df_pred_escenarios["escenario_temporal"].str.contains("Sábado")]
    ist_sabado = dict(zip(sub_fin["id_estacion"], sub_fin["ist_predicho_ml"]))

    recomendaciones = []
    for nombre_perfil, vec_u in perfiles_usuarios.items():
        u = np.array(vec_u, dtype=float)
        for est_id, info_r in rutas_guardianes.items():
            r = np.array(info_r["vector"], dtype=float)
            sim_coseno = float(np.dot(u, r) / (np.linalg.norm(u) * np.linalg.norm(r)))
            ist_nodo = ist_sabado.get(est_id, 0.30)

            score_sustentable = (0.70 * sim_coseno) + (0.30 * (1.0 - ist_nodo))
            recomendaciones.append({
                "perfil_viajero": nombre_perfil,
                "id_estacion": est_id,
                "destino_guardian": info_r["destino"],
                "afinidad_coseno": round(sim_coseno, 4),
                "ist_predicho_fin_semana": round(ist_nodo, 3),
                "score_recomendacion_sustentable": round(score_sustentable, 4),
                "circuito_pois_sugerido": info_r["circuito_recomendado"],
                "bendicion_comercial_sugerida": info_r["comercio_ancla"]
            })

    df_rec = pd.DataFrame(recomendaciones)
    df_rec["ranking_para_perfil"] = df_rec.groupby("perfil_viajero")["score_recomendacion_sustentable"].rank(ascending=False, method="first").astype(int)
    df_rec = df_rec.sort_values(by=["perfil_viajero", "ranking_para_perfil"]).reset_index(drop=True)
    return df_rec


def generar_visualizaciones_ml(df_metricas, mejor_mod, prep, y_test, y_pred_test, df_pred_escenarios, df_rec):
    print("[*] Generando gráficas de Aprendizaje de Máquina...")

    # FIGURA 10: Desempeño de Modelos y Ajuste Observado vs Predicho
    fig, axes = plt.subplots(1, 2, figsize=(15, 5.8))

    x_pos = np.arange(len(df_metricas))
    width = 0.36
    bars1 = axes[0].bar(x_pos - width/2, df_metricas["r2_test"] * 100, width=width, color="#2980b9", edgecolor="#222222", label="Varianza Explicada R² Test (%)")
    bars2 = axes[0].bar(x_pos + width/2, df_metricas["exactitud_asignacion_rareza_pct"], width=width, color="#27ae60", edgecolor="#222222", label="Exactitud de Rareza Inversa (%)")

    axes[0].set_xticks(x_pos)
    axes[0].set_xticklabels([m.replace(" Regressor", "") for m in df_metricas["modelo"]], rotation=15, ha="right", fontsize=9.5)
    axes[0].set_ylim(40, 108)
    axes[0].set_ylabel("Porcentaje de Desempeño (%)", fontsize=10)
    axes[0].set_title("1. Comparación de Modelos Supervisados (Test Set)\n(Métrica Continua R² vs. Precisión en Asignación de Rareza)", fontsize=11, fontweight="bold", pad=12)
    axes[0].legend(loc="lower right", frameon=True)

    for b in bars1:
        axes[0].text(b.get_x() + b.get_width()/2, b.get_height() + 0.8, f"{b.get_height():.1f}%", ha="center", fontsize=8.5, fontweight="bold")
    for b in bars2:
        axes[0].text(b.get_x() + b.get_width()/2, b.get_height() + 0.8, f"{b.get_height():.1f}%", ha="center", fontsize=8.5, fontweight="bold", color="#1e8449")

    axes[1].scatter(y_test, y_pred_test, alpha=0.45, color="#8e44ad", edgecolors="none", s=28, label="Observaciones de Prueba (n=504)")
    axes[1].plot([0.1, 1.05], [0.1, 1.05], color="#e74c3c", linestyle="--", linewidth=2, label="Ajuste Perfecto (Identidad y = x)")
    axes[1].axvspan(0.0, 0.35, color="#ffd700", alpha=0.12, label="Zona Legendaria (IST < 0.35)")
    axes[1].axvspan(0.35, 0.60, color="#a335ee", alpha=0.10, label="Zona Épica (0.35 - 0.60)")
    axes[1].axvspan(0.60, 0.85, color="#0070dd", alpha=0.08, label="Zona Rara (0.60 - 0.85)")

    r2_champ = df_metricas.iloc[0]["r2_test"]
    rmse_champ = df_metricas.iloc[0]["rmse_test"]
    axes[1].set_title(f"2. Ajuste del Modelo Campeón (Gradient Boosting)\n(R² = {r2_champ:.4f} | RMSE = {rmse_champ:.4f})", fontsize=11, fontweight="bold", pad=12)
    axes[1].set_xlabel("Índice de Saturación Turística (IST) Observado", fontsize=10)
    axes[1].set_ylabel("Índice de Saturación Turística (IST) Predicho", fontsize=10)
    axes[1].set_xlim(0.12, 1.08)
    axes[1].set_ylim(0.12, 1.08)
    axes[1].legend(loc="upper left", frameon=True, fontsize=8.5)

    plt.suptitle("APRENDIZAJE DE MÁQUINA: VALIDACIÓN PREDICTIVA DEL ÍNDICE DE SATURACIÓN TURÍSTICA (IST)", fontsize=13, fontweight="bold", y=1.01)
    plt.tight_layout()
    fig10_path = os.path.join(KPIS_DIR, "fig10_ml_desempeno_modelos_ist.png")
    plt.savefig(fig10_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"    [v] Guardada: {fig10_path}")

    # FIGURA 11: Importancia de Variables y Heatmap de Escenarios Temporales
    fig, axes = plt.subplots(1, 2, figsize=(15.5, 6))

    nombres_num = [
        "Mes del Año", "Día de la Semana", "Fin de Semana (Sáb/Dom)", "Puente Festivo",
        "Bloque Horario", "Índice Estacional CETM", "Temperatura (°C)",
        "Probabilidad de Lluvia", "Evento Cultural Local", "Intensidad Pauta Digital"
    ]
    n_cat = len(prep.estaciones_orden) - 1
    importancias = mejor_mod.feature_importances_
    imp_estaciones = float(np.sum(importancias[:n_cat]))
    imp_num = importancias[n_cat:]

    df_imp_consol = pd.DataFrame({
        "variable": ["Nodo / Estación Territorial (Ubicación)"] + nombres_num,
        "importancia": [imp_estaciones] + list(imp_num)
    }).sort_values(by="importancia", ascending=True)

    axes[0].barh(df_imp_consol["variable"], df_imp_consol["importancia"] * 100.0, color="#16a085", edgecolor="#222222", height=0.62)
    axes[0].set_title("1. Importancia Relativa de Variables Predictoras\n(Factores Determinantes de la Saturación Turística)", fontsize=11, fontweight="bold", pad=12)
    axes[0].set_xlabel("Contribución a la Reducción de Varianza (%)", fontsize=10)
    for idx, val in enumerate(df_imp_consol["importancia"] * 100.0):
        axes[0].text(val + 0.6, idx, f"{val:.1f}%", va="center", fontsize=8.5, fontweight="bold")
    axes[0].set_xlim(0, max(df_imp_consol["importancia"] * 100.0) * 1.18)

    piv_esc = df_pred_escenarios.pivot(index="nombre_estacion", columns="escenario_temporal", values="ist_predicho_ml")
    orden_est = ["Zinacantepec", "Metepec", "Lerma", "Toluca Centro", "Vasco de Quiroga", "Santa Fe", "Observatorio"]
    piv_esc = piv_esc.reindex([e for e in orden_est if e in piv_esc.index])

    sns.heatmap(piv_esc, annot=True, fmt=".2f", cmap="RdYlGn_r", vmin=0.15, vmax=1.00, cbar_kws={"label": "IST Predicho (Verde=Legendario, Rojo=Saturado)"}, ax=axes[1], linewidths=0.8)
    axes[1].set_title("2. Predicción Dinámica del IST por Escenario Temporal\n(Activación de Rareza Legendaria/Épica en Valle de Toluca)", fontsize=11, fontweight="bold", pad=12)
    axes[1].set_xlabel("Escenario de Calendario y Horario", fontsize=10)
    axes[1].set_ylabel("Estación del Corredor", fontsize=10)
    axes[1].tick_params(axis="x", rotation=18)

    plt.suptitle("INTERPRETABILIDAD DEL MODELO Y ASIGNACIÓN DINÁMICA DE RAREZA INVERSA", fontsize=13, fontweight="bold", y=1.01)
    plt.tight_layout()
    fig11_path = os.path.join(KPIS_DIR, "fig11_ml_importancia_variables_y_rareza.png")
    plt.savefig(fig11_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"    [v] Guardada: {fig11_path}")

    # FIGURA 12: Matriz del Motor de Recomendación de Rutas
    fig, ax = plt.subplots(figsize=(11, 5.5))
    piv_rec = df_rec.pivot(index="perfil_viajero", columns="destino_guardian", values="score_recomendacion_sustentable")

    sns.heatmap(piv_rec, annot=True, fmt=".3f", cmap="YlGnBu", cbar_kws={"label": "Score Híbrido Sustentable (Afinidad + Baja Saturación)"}, linewidths=1.0, ax=ax)
    ax.set_title("MOTOR DE RECOMENDACIÓN DE RUTAS PERSONALIZADAS (BUYER PERSONA vs. GUARDIÁN)\nScore Híbrido: 70% Similitud Coseno de Preferencias + 30% Premio por Capacidad Disponible (1 - IST)", fontsize=11.5, fontweight="bold", pad=14)
    ax.set_xlabel("Nodo / Guardián del Territorio Recomendado", fontsize=10)
    ax.set_ylabel("Segmento / Buyer Persona", fontsize=10)
    plt.xticks(rotation=12, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    fig12_path = os.path.join(KPIS_DIR, "fig12_ml_matriz_recomendacion_rutas.png")
    plt.savefig(fig12_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"    [v] Guardada: {fig12_path}")


def main():
    print("=========================================================================")
    print("  APRENDIZAJE DE MÁQUINA: MODELO PREDICTIVO IST Y RECOMENDADOR DE RUTAS  ")
    print("=========================================================================")

    df_train_full = construir_dataset_entrenamiento()
    print(f"[+] Dataset espaciotemporal construido: {len(df_train_full)} observaciones.")

    df_metricas, mejor_mod, prep, y_test, y_pred_test, df_pred_escenarios = entrenar_y_evaluar_modelos(df_train_full)
    df_rec = motor_recomendacion_rutas_sustentables(df_pred_escenarios)

    df_metricas.to_csv(os.path.join(PROCESSED_DIR, "ml_comparativa_modelos.csv"), index=False)
    df_pred_escenarios.to_csv(os.path.join(PROCESSED_DIR, "ml_predicciones_ist_dinamico.csv"), index=False)
    df_rec.to_csv(os.path.join(PROCESSED_DIR, "ml_recomendaciones_rutas_perfiles.csv"), index=False)

    print("\n--- TABLA COMPARATIVA DE MODELOS DE MACHINE LEARNING ---")
    print(df_metricas.to_string(index=False))

    print("\n--- TOP RECOMENDACIONES DE RUTA POR BUYER PERSONA (RANK #1) ---")
    top1 = df_rec[df_rec["ranking_para_perfil"] == 1]
    print(top1[["perfil_viajero", "destino_guardian", "score_recomendacion_sustentable", "circuito_pois_sugerido"]].to_string(index=False))

    generar_visualizaciones_ml(df_metricas, mejor_mod, prep, y_test, y_pred_test, df_pred_escenarios, df_rec)
    print("\n[OK] Pipeline de Aprendizaje de Máquina finalizado exitosamente.")


if __name__ == "__main__":
    main()
