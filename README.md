# Szakdolgozat – Gépitanulás alkalmazása az orvosi sugárterápiában

## Célkitűzés

Ez a projekt célul tűzte ki, hogy klasszikus gépi tanulási módszereket alkalmazzon nem-kissejtes tüdőrákos (NSCLC) betegek túlélési idejének predikciójára. A munka során két különböző megközelítést vetünk össze:

- **Random Survival Forest (RSF)** – nemparaméteres túlélési modell, amely képes kezelni cenzorált adatokat és nemlineáris kapcsolatokat.
- **Cox regressziós modell** – a túlélésidő-analízis hagyományos statisztikai módszere.

A klinikai adatokat alapos előfeldolgozás után tápláljuk be a modellekbe, majd azok prediktív teljesítményét **Harrell-féle C-index** és **Kaplan–Meier görbék** segítségével értékeljük.

A projekt része egy automatizált pipeline, amely tartalmazza:
- az adatok betöltését és tisztítását,
- normalizálást, hiánykezelést,
- modellépítést (RSF, Cox),
- értékelést és ábrakészítést.

Az eredmények célja annak bemutatása, hogy milyen mértékben alkalmazhatók gépi tanulási módszerek az onkológiai predikciós problémákban.

## Adatforrás

Az adatok a TCIA (The Cancer Imaging Archive) [NSCLC-Radiomics](https://wiki.cancerimagingarchive.net/display/Public/NSCLC-Radiomics) adatbázisból származnak, amely a következőket tartalmazza:

- DICOM formátumú CT képek
- Klinikai adatok `.csv` fájlban (túlélési idő, nem, TNM stádium, stb.)

> **Megjegyzés**: Az adatok nem kerülnek feltöltésre ebbe a repóba. Lokálisan kell elhelyezni őket a mappában.

## Szkriptek leírása

| Fájlnév                     | Leírás |
|----------------------------|--------|
| `load_clinical_data.py`    | Klinikai adatok betöltése CSV fájlból. |
| `prepare_clinical_data.py` | Tisztítás, előfeldolgozás, normalizálás. |
| `join_csvs.py`             | CSV fájlok összefűzése, összevonása. |
| `normalize.py`             | Klinikai változók normalizálása. |
| `hianykezelo.py`           | Hiányzó adatok kezelése (pl. imputálás). |
| `5fold_rsf.py`             | 5-szörös keresztvalidáció Random Survival Forest-tel. |
| `rsf.py`                   | RSF modell egyszeri futtatása (nem cross-validation). |
| `cox.py`                   | Cox regressziós modell betanítása. |
| `cox_forestplot.py`        | Cox modell eredményeinek forest plot ábrázolása. |
| `cox_risk.py`              | Cox modell kockázati arányainak kiszámítása. |
| `c-index.py`               | Modellek kiértékelése Harrell-féle C-index-szel. |
| `osszehasonlitas.py`       | RSF és Cox modellek teljesítményének összehasonlítása. |
| `kaplan_meier_gender.py`   | Kaplan–Meier görbék nemek szerint. |
| `kaplan_meier_stage.py`    | Kaplan–Meier görbék stádium szerint. |
| `select_for_cox.py`        | Változók kiválasztása Cox modellhez. |
| `run_all.py`               | Teljes pipeline indítása, szkriptek futtatása sorrendben. |
| `check.py`                 | Általános adatellenőrzés. |
| `check_mask.py`            | DICOM maszk fájlok ellenőrzése. |
| `dicom_to_nifti.py`        | DICOM → NIfTI konvertálás. |
| `delete_all.py`            | Tesztcélú fájltörlő szkript (óvatosan használandó). |
| `params.yaml`              | Modell és adatfeldolgozás konfigurációs paraméterei. |


## Használat

1. A függőségek telepítése:
   ```bash
   pip install -r requirements.txt
   ```

2. A szkriptek futtatása:
   ```bash
   python rfs.py
   ```

## Modell

A projekt két különböző túlélési modellezési módszert alkalmaz:

### 1. Random Survival Forest (RSF)
Nemparaméteres ensemble modell, amely képes a cenzorált adatokkal való munkára. Kétféleképpen kerül alkalmazásra:
- **`rsf.py`**: Egyszeri tanítás és predikció.
- **`5fold_rsf.py`**: 5-szörös keresztvalidáció a robusztus teljesítményértékeléshez.

### 2. Cox regressziós modell
A klasszikus statisztikai megközelítés, amely a túlélési idő log-hazard arányainak lineáris kapcsolatát feltételezi.
- **`cox.py`**: A modell tanítása.
- **`select_for_cox.py`**: Jellemzők kiválasztása a modell számára.
- **`cox_risk.py`**: Kockázati értékek becslése.
- **`cox_forestplot.py`**: Vizuális megjelenítés (forest plot).

### Kiértékelés és összehasonlítás
- **`c-index.py`**: A prediktív teljesítmény kvantitatív értékelése Harrell-féle C-index segítségével.
- **`kaplan_meier_gender.py`**, **`kaplan_meier_stage.py`**: Kaplan–Meier görbék nem és stádium szerint.
- **`osszehasonlitas.py`**: A Cox és RSF modellek teljesítményének közvetlen összehasonlítása.

- **Metrikák és ábrák**: a generált ábrák/adatok nem kerülnek feltöltésre. A szakdolgozat szövegében kerülnek bemutatásra.

## Szerző

**Wágner Katrin**  
BSc szakdolgozat – Pázmány Péter Katolikus Egyetem  
2025
