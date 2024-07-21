import requests
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import TreeCountData, ExpenditureData, InflationData

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = "mysql+pymysql://root:@localhost/chart_dashboard"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def fetch_tree_count_data():
    url = "https://opendata.bandung.go.id/api/bigdata/kecamatan_cibeunying_kaler/jmlh_phn_brdsrkn_klrhn_d_kcmtn_cbnyng_klr_kt_bndng"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def fetch_expenditure_data():
    url = "https://data.jabarprov.go.id/api-backend/bigdata/bps/od_15049_jml_pengeluaran_per_kapita__prov_di_indonesia_v1"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def fetch_inflation_data():
    url = "https://data.jabarprov.go.id/api-backend/bigdata/bps/od_20348_inflasi__bulan_prov_2022100_di_indonesia_v3"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def load_data():
    # Fetch data from APIs
    try:
        # Tree Count Data
        tree_count_response = fetch_tree_count_data()
        tree_count_data = tree_count_response.get('data', [])
        if not isinstance(tree_count_data, list):
            logger.error("Unexpected format for Tree Count Data")
            return

        # Expenditure Data
        expenditure_response = fetch_expenditure_data()
        expenditure_data = expenditure_response.get('data', [])
        if not isinstance(expenditure_data, list):
            logger.error("Unexpected format for Expenditure Data")
            return

         # Inflation Data
        inflation_response = fetch_inflation_data()
        inflation_data = inflation_response.get('data', [])
        if not isinstance(inflation_data, list):
            logger.error("Unexpected format for Inflation Data")
            return

    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return

    # Create a session
    db = SessionLocal()
    
    try:
        # Load Tree Count Data
        for item in tree_count_data:
            try:
                data = TreeCountData(
                    id=item.get('id'),
                    kode_provinsi=item.get('kode_provinsi'),
                    nama_provinsi=item.get('nama_provinsi'),
                    bps_kode_kabupaten_kota=item.get('bps_kode_kabupaten_kota'),
                    bps_nama_kabupaten_kota=item.get('bps_nama_kabupaten_kota'),
                    bps_kode_kecamatan=item.get('bps_kode_kecamatan'),
                    bps_nama_kecamatan=item.get('bps_nama_kecamatan'),
                    bps_kode_desa_kelurahan=item.get('bps_kode_desa_kelurahan'),
                    bps_desa_kelurahan=item.get('bps_desa_kelurahan'),
                    kemendagri_kode_kecamatan=item.get('kemendagri_kode_kecamatan'),
                    kemendagri_nama_kecamatan=item.get('kemendagri_nama_kecamatan'),
                    kemendagri_kode_desa_kelurahan=item.get('kemendagri_kode_desa_kelurahan'),
                    kemendagri_nama_desa_kelurahan=item.get('kemendagri_nama_desa_kelurahan'),
                    jenis_pohon=item.get('jenis_pohon'),
                    lokasi_penanaman=item.get('lokasi_penanaman'),
                    jumlah_pohon=item.get('jumlah_pohon'),
                    satuan=item.get('satuan'),
                    tahun=item.get('tahun')
                )
                db.add(data)
            except Exception as e:
                logger.error(f"Error processing TreeCountData item: {item}. Error: {e}")
        db.commit()
        logger.info("Tree Count Data loaded successfully")

        # Load Expenditure Data
        for item in expenditure_data:
            try:
                data = ExpenditureData(
                    id=item.get('id'),
                    jumlah_pengeluaran_per_kapita=item.get('jumlah_pengeluaran_per_kapita'),
                    kode_provinsi=item.get('kode_provinsi'),
                    nama_provinsi=item.get('nama_provinsi'),
                    satuan=item.get('satuan'),
                    tahun=item.get('tahun')
                )
                db.add(data)
            except Exception as e:
                logger.error(f"Error processing ExpenditureData item: {item}. Error: {e}")
        db.commit()
        logger.info("Expenditure Data loaded successfully")

        # Load Inflation Data
        for item in inflation_data:
            try:
                data = InflationData(
                    id=item.get('id'),
                    kode_provinsi=item.get('kode_provinsi'),
                    nama_provinsi=item.get('nama_provinsi'),
                    kode_bulan=item.get('kode_bulan'),
                    nama_bulan=item.get('nama_bulan'),
                    nilai_inflasi=item.get('nilai_inflasi'),
                    satuan=item.get('satuan'),
                    tahun=item.get('tahun')
                )
                db.add(data)
            except Exception as e:
                logger.error(f"Error processing InflationData item: {item}. Error: {e}")
        db.commit()
        logger.info("Inflation Data loaded successfully")
        
    finally:
        db.close()

if __name__ == "__main__":
    load_data()

