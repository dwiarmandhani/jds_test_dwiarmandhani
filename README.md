# JDS Test Dwiarmandhani

## Deskripsi

Proyek ini adalah aplikasi untuk menganalisis data inflasi dan menyediakan berbagai insight seperti tren inflasi tahunan dan rata-rata inflasi bulanan. Aplikasi ini menggunakan FastAPI sebagai framework backend dan dapat di-host menggunakan Docker.

## Fitur

- **Tren Inflasi Tahunan**: Mendapatkan tren inflasi tahunan berdasarkan provinsi.
- **Rata-rata Inflasi Bulanan**: Mendapatkan rata-rata inflasi bulanan untuk provinsi tertentu.

## Prerequisites

Sebelum memulai, pastikan Anda telah menginstal perangkat lunak berikut:

- Python 3.12 atau lebih baru
- MySQL atau PostgreSQL
- Docker (opsional, untuk containerization)

## Instalasi

### 1. Clone Repository

Clone repository ini ke mesin lokal Anda:

```bash
git clone https://github.com/dwiarmandhani/jds_test_dwiarmandhani.git
cd jds_test_dwiarmandhani
```

### 2. Setup Virtual Environment

Clone repository ini ke mesin lokal Anda:

```bash
python -m venv venv
source venv/bin/activate  # Di Windows, gunakan `venv\Scripts\activate`
```

### 3. Instal Semua Dependensi

Gunakan pip untuk menginstal semua paket yang terdaftar dalam requirements.txt. Jalankan perintah berikut di terminal atau command prompt:

```bash
pip install -r requirements.txt
```

### 4. Buat Database lalu setup

Saya menggunakan mysql di phpmyadmin. buat database bernama chart_dashboard

berikut database url saya di dalam main.py :

```bash
DATABASE_URL = "mysql+pymysql://root:@localhost/chart_dashboard"
```

Jalankan :

```bash
uvicorn main:app --reload
```

\*Note : pertama kali menjalankan bash diatas, akan otomatis membuat database beserta tablenya, namun belum dengan isinya.

Silahkan jalankan :

```bash
python load_data.py
```

Lakukan hal diatas untuk fecth data dari https://opendata.jabarprov.go.id/ dan akan disimpan di dalam database.
Ada 3 data yang saya fecth diantaranya :

1. Data pohon di kecamatan cibeunying kaler
   https://opendata.bandung.go.id/api/bigdata/kecamatan_cibeunying_kaler/jmlh_phn_brdsrkn_klrhn_d_kcmtn_cbnyng_klr_kt_bndng
2. Data Inflasi
   https://data.jabarprov.go.id/api-backend/bigdata/bps/od_20348_inflasi__bulan_prov_2022100_di_indonesia_v3
3. Data pengeluaran per kapita
   https://data.jabarprov.go.id/api-backend/bigdata/bps/od_15049_jml_pengeluaran_per_kapita__prov_di_indonesia_v1

### 5. Jalankan server

Jalankan :

```bash
uvicorn main:app --reload
```

### 6. Dokumentasi API lengkap

```bash
{baseurl}/redoc
http://127.0.0.1:8000/redoc
```
