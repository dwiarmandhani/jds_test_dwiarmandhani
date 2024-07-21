from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class InflationData(Base):
    __tablename__ = "inflation_data"

    id = Column(Integer, primary_key=True, index=True)
    kode_provinsi = Column(Integer)
    nama_provinsi = Column(String(255))
    kode_bulan = Column(Integer)
    nama_bulan = Column(String(255))
    nilai_inflasi = Column(Float)
    satuan = Column(String(255))
    tahun = Column(Integer)

class TreeCountData(Base):
    __tablename__ = "tree_count_data"

    id = Column(Integer, primary_key=True, index=True)
    kode_provinsi = Column(Integer)
    nama_provinsi = Column(String(255))
    bps_kode_kabupaten_kota = Column(Integer)
    bps_nama_kabupaten_kota = Column(String(255))
    bps_kode_kecamatan = Column(Integer)
    bps_nama_kecamatan = Column(String(255))
    bps_kode_desa_kelurahan = Column(Integer)
    bps_desa_kelurahan = Column(String(255))
    kemendagri_kode_kecamatan = Column(String(255))
    kemendagri_nama_kecamatan = Column(String(255))
    kemendagri_kode_desa_kelurahan = Column(String(255))
    kemendagri_nama_desa_kelurahan = Column(String(255))
    jenis_pohon = Column(String(255))
    lokasi_penanaman = Column(String(255))
    jumlah_pohon = Column(Integer)
    satuan = Column(String(255))
    tahun = Column(Integer)

class ExpenditureData(Base):
    __tablename__ = "expenditure_data"

    id = Column(Integer, primary_key=True, index=True)
    kode_provinsi = Column(Integer)
    nama_provinsi = Column(String(255))
    jumlah_pengeluaran_per_kapita = Column(Float)
    satuan = Column(String(255))
    tahun = Column(Integer)
