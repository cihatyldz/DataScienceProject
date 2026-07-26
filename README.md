# 🧪 DataScienceProject

Modüler ve genişletilebilir bir makine öğrenmesi pipeline'ı. Veri yükleme, ön işleme ve model eğitimi adımlarını **YAML tabanlı konfigürasyon** ile yönetir; scikit-learn API'siyle tam uyumludur.

---

## 📋 İçindekiler

- [Özellikler](#-özellikler)
- [Proje Yapısı](#-proje-yapısı)
- [Gereksinimler](#-gereksinimler)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
  - [1. Veri Yükleme](#1-veri-yükleme)
  - [2. Konfigürasyon ile Ön İşleme](#2-konfigürasyon-ile-ön-i̇şleme)
  - [3. Model Eğitimi](#3-model-eğitimi)
  - [4. Özel Model Oluşturma](#4-özel-model-oluşturma)
- [Konfigürasyon](#-konfigürasyon)
- [Testler](#-testler)
- [Lisans](#-lisans)

---

## ✨ Özellikler

| Modül | Açıklama |
|---|---|
| **DataLoader** | CSV ve Parquet dosyalarını otomatik algılayarak yükler; tip, yol ve boş dosya doğrulamaları yapar. |
| **DataPreprocessor** | YAML konfigürasyonundan dinamik olarak imputer, scaler ve encoder pipeline'ları oluşturur. |
| **ModelTrainer** | Scikit-learn, XGBoost ve CatBoost gibi farklı kütüphanelerin modellerini tek bir arayüzle eğitir. |
| **Custom Models** | `BaseCustomModel` ve `SklearnCompatibleModel` sınıfları ile özel model tanımlama desteği. |

---

## 📁 Proje Yapısı

```
DataScienceProject/
├── config.yaml                  # Ön işleme konfigürasyonu
├── main.py                      # Uygulama giriş noktası
├── pyproject.toml               # Proje metadata & bağımlılıklar
├── Car_Insurance_Claim.csv      # Örnek veri seti
│
├── src/
│   ├── __init__.py
│   ├── data_loader/
│   │   ├── data_loader.py       # DataLoader sınıfı
│   │   ├── error_messages.py    # Hata mesajları (Enum)
│   │   └── exceptions.py        # Özel exception sınıfları
│   │
│   ├── data_preprocessing/
│   │   ├── data_preprocessor.py # DataPreprocessor sınıfı
│   │   └── load_config.py       # YAML → Pydantic config yükleyici
│   │
│   └── model_training/
│       ├── model_trainer.py     # ModelTrainer sınıfı
│       └── custom_models.py     # BaseCustomModel & SklearnCompatibleModel
│
└── tests/
    ├── conftest.py              # Ortak test fixture'ları
    ├── test_datasets/           # Test veri dosyaları
    ├── data_loader/             # DataLoader testleri
    ├── data_preprocessing/      # DataPreprocessor testleri
    └── model_training/          # ModelTrainer testleri (birim, entegrasyon)
```

---

## 📌 Gereksinimler

- **Python** ≥ 3.12
- Bağımlılıklar:

| Paket | Versiyon |
|---|---|
| numpy | ≥ 2.5.1 |
| pandas | ≥ 3.0.3 |
| pydantic | ≥ 2.13.4 |
| pyyaml | ≥ 6.0.3 |
| scikit-learn | ≥ 1.9.0 |

**Geliştirme bağımlılıkları:** pytest ≥ 9.1.1, ruff ≥ 0.15.22

---

## 🚀 Kurulum

Proje **uv** paket yöneticisi kullanılarak yapılandırılmıştır.

```bash
# Repo'yu klonlayın
git clone https://github.com/<kullanıcı>/DataScienceProject.git
cd DataScienceProject

# Sanal ortam oluşturup bağımlılıkları yükleyin (uv ile)
uv sync

# Alternatif: pip ile kurulum
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -e ".[dev]"
```

---

## 🔧 Kullanım

### 1. Veri Yükleme

`DataLoader` sınıfı CSV ve Parquet formatlarını destekler. Dosya yolu doğrulaması, uzantı kontrolü ve boş dosya denetimi otomatik olarak yapılır.

```python
from src.data_loader import DataLoader

loader = DataLoader()
df = loader.load_data("Car_Insurance_Claim.csv")
print(df.shape)
```

### 2. Konfigürasyon ile Ön İşleme

Ön işleme adımları `config.yaml` dosyasından okunur. Imputer, scaler ve encoder sınıfları dinamik olarak yüklenir.

```python
from src.data_preprocessing import DataPreprocessor, load_config

config = load_config("config.yaml")
preprocessor = DataPreprocessor(config)

X_transformed = preprocessor.fit_transform(df)
```

**Örnek `config.yaml`:**

```yaml
features:
  categorical:
    - city
steps:
  categorical:
    imputer: SimpleImputer
    imputer_kwargs:
      strategy: most_frequent
      fill_value: "unknown"
    encoder: OneHotEncoder
    encoder_kwargs:
      handle_unknown: ignore
      sparse_output: false
  numerical:
    imputer: SimpleImputer
    imputer_kwargs:
      strategy: mean
    scaler: StandardScaler
    scaler_kwargs:
      with_mean: true
      with_std: true
```

### 3. Model Eğitimi

`ModelTrainer`, scikit-learn API'siyle uyumlu herhangi bir modeli sarmalayarak eğitir. `predict`, `predict_proba` ve `feature_importances_` desteği sunar.

```python
from sklearn.ensemble import RandomForestClassifier
from src import ModelTrainer

# Model oluştur ve eğit
model = RandomForestClassifier(n_estimators=100, random_state=42)
trainer = ModelTrainer(model)
trainer.fit(X_train, y_train)

# Tahmin
predictions = trainer.predict(X_test)
probabilities = trainer.predict_proba(X_test)

# Özellik önem dereceleri
importances = trainer.feature_importances_
```

**XGBoost ve CatBoost ile de kullanılabilir:**

```python
from xgboost import XGBClassifier
from catboost import CatBoostClassifier

# XGBoost
trainer = ModelTrainer(XGBClassifier(n_estimators=100, random_state=42))
trainer.fit(X_train, y_train)

# CatBoost
trainer = ModelTrainer(CatBoostClassifier(iterations=100, verbose=False))
trainer.fit(X_train, y_train)
```

### 4. Özel Model Oluşturma

`BaseCustomModel` veya `SklearnCompatibleModel` sınıflarından türeterek kendi modelinizi oluşturabilirsiniz.

```python
from src import BaseCustomModel
import numpy as np

class MyModel(BaseCustomModel):
    def fit(self, X, y, **kwargs):
        self.mean_ = np.mean(y)
        return self

    def predict(self, X):
        return np.full(X.shape[0], self.mean_)

# ModelTrainer ile kullanım
trainer = ModelTrainer(MyModel())
trainer.fit(X_train, y_train)
predictions = trainer.predict(X_test)
```

---

## ⚙️ Konfigürasyon

Ön işleme pipeline'ı tamamen YAML tabanlıdır. Pydantic modelleri ile doğrulanır:

| Model | Açıklama |
|---|---|
| `PreprocessorConfig` | Ana konfigürasyon (features + steps) |
| `FeatureConfig` | `numerical` ve `categorical` özellik listeleri |
| `NumericalStepsConfig` | `imputer`, `scaler` ve ilgili parametreler |
| `CategoricalStepsConfig` | `imputer`, `encoder` ve ilgili parametreler |

Sınıf isimleri (`SimpleImputer`, `StandardScaler`, `OneHotEncoder` vb.) dinamik olarak `sklearn.preprocessing` ve `sklearn.impute` modüllerinden yüklenir. Tam nitelikli isimler de desteklenir (ör. `sklearn.preprocessing.MinMaxScaler`).

---

## 🧪 Testler

Testler **pytest** ile çalıştırılır:

```bash
# Tüm testleri çalıştır
pytest

# Belirli bir modülün testlerini çalıştır
pytest tests/data_loader/
pytest tests/data_preprocessing/
pytest tests/model_training/

# Ayrıntılı çıktı
pytest -v
```

**Test kapsamı:**

- `data_loader/` — Dosya yükleme, uzantı doğrulama, hata senaryoları
- `data_preprocessing/` — Pipeline oluşturma, fit/transform işlemleri
- `model_training/` — Birim testleri, özel model testleri, entegrasyon testleri

---

## 📄 Lisans

Bu proje eğitim amaçlıdır.
