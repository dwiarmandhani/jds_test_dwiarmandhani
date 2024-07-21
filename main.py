from fastapi import FastAPI, Depends, HTTPException, Header, Query
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Base, TreeCountData, ExpenditureData, InflationData
from pydantic import BaseModel
from typing import List

DATABASE_URL = "mysql+pymysql://root:@localhost/chart_dashboard"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI()

class TreeCountDataSchema(BaseModel):
    kode_provinsi: int
    nama_provinsi: str
    bps_kode_kabupaten_kota: int
    bps_nama_kabupaten_kota: str
    bps_kode_kecamatan: int
    bps_nama_kecamatan: str
    bps_kode_desa_kelurahan: int
    bps_desa_kelurahan: str
    kemendagri_kode_kecamatan: str
    kemendagri_nama_kecamatan: str
    kemendagri_kode_desa_kelurahan: str
    kemendagri_nama_desa_kelurahan: str
    jenis_pohon: str
    lokasi_penanaman: str
    jumlah_pohon: int
    satuan: str
    tahun: int

class ExpenditureDataSchema(BaseModel):
    jumlah_pengeluaran_per_kapita: float
    kode_provinsi: int
    nama_provinsi: str
    satuan: str
    tahun: int

class InflationDataSchema(BaseModel):
    kode_provinsi: int
    nama_provinsi: str
    kode_bulan: int
    nama_bulan: str
    nilai_inflasi: float
    satuan: str
    tahun: int

class ExpenditureTrendSchema(BaseModel):
    tahun: int
    nama_provinsi: str
    jumlah_pengeluaran_per_kapita: float

class TreeCountByLocationSchema(BaseModel):
    lokasi_penanaman: str
    jumlah_pohon: int

class ExpenditureExtremesSchema(BaseModel):
    nama_provinsi: str
    pengeluaran_tertinggi: float
    pengeluaran_terendah: float


class YearlyInflationTrendSchema(BaseModel):
    tahun: int
    nilai_inflasi: float
    nama_provinsi: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_token(x_token: str = Header(...)):
    if x_token != "qwerTyUiOp564321xYZ":  
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

@app.get("/tree_count_data", response_model=list[TreeCountDataSchema])
def get_tree_count_data(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(TreeCountData).offset(skip).limit(limit).all()

@app.get("/expenditure_data", response_model=list[ExpenditureDataSchema])
def get_expenditure_data(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(ExpenditureData).offset(skip).limit(limit).all()

@app.get("/inflation_data", response_model=list[InflationDataSchema])
def get_inflation_data(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(InflationData).offset(skip).limit(limit).all()

@app.get("/tree_count_data/{id}", response_model=TreeCountDataSchema)
def get_tree_count_data_by_id(id: int, db: Session = Depends(get_db)):
    data = db.query(TreeCountData).filter(TreeCountData.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data

@app.get("/expenditure_data/{id}", response_model=ExpenditureDataSchema)
def get_expenditure_data_by_id(id: int, db: Session = Depends(get_db)):
    data = db.query(ExpenditureData).filter(ExpenditureData.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data

@app.get("/inflation_data/{id}", response_model=InflationDataSchema)
def get_inflation_data_by_id(id: int, db: Session = Depends(get_db)):
    data = db.query(InflationData).filter(InflationData.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data

@app.get("/insights/expenditure_trend_by_province", response_model=List[ExpenditureTrendSchema])
def get_expenditure_trend_by_province(nama_provinsi: str, db: Session = Depends(get_db)):
    results = db.query(
        ExpenditureData.tahun,
        ExpenditureData.nama_provinsi,
        func.avg(ExpenditureData.jumlah_pengeluaran_per_kapita).label("jumlah_pengeluaran_per_kapita")
    ).filter(ExpenditureData.nama_provinsi == nama_provinsi).group_by(ExpenditureData.tahun, ExpenditureData.nama_provinsi).all()
    return results

@app.get("/insights/tree_count_by_location", response_model=List[TreeCountByLocationSchema])
def get_tree_count_by_location(db: Session = Depends(get_db), x_token: str = Depends(verify_token)):
    results = db.query(
        TreeCountData.lokasi_penanaman,
        func.sum(TreeCountData.jumlah_pohon).label("jumlah_pohon")
    ).group_by(TreeCountData.lokasi_penanaman).all()
    return results

@app.get("/insights/expenditure_extremes_by_province", response_model=List[ExpenditureExtremesSchema])
def get_expenditure_extremes_by_province(db: Session = Depends(get_db), x_token: str = Depends(verify_token)):
    subquery_high = db.query(
        ExpenditureData.nama_provinsi,
        func.max(ExpenditureData.jumlah_pengeluaran_per_kapita).label("pengeluaran_tertinggi")
    ).group_by(ExpenditureData.nama_provinsi).subquery()

    subquery_low = db.query(
        ExpenditureData.nama_provinsi,
        func.min(ExpenditureData.jumlah_pengeluaran_per_kapita).label("pengeluaran_terendah")
    ).group_by(ExpenditureData.nama_provinsi).subquery()

    results = db.query(
        subquery_high.c.nama_provinsi,
        subquery_high.c.pengeluaran_tertinggi,
        subquery_low.c.pengeluaran_terendah
    ).join(subquery_low, subquery_high.c.nama_provinsi == subquery_low.c.nama_provinsi).all()

    return results



@app.get("/insights/yearly_inflation_trend", response_model=List[YearlyInflationTrendSchema])
def get_yearly_inflation_trend(
    kode_provinsi: int,
    db: Session = Depends(get_db),
    x_token: str = Depends(verify_token)
):
    results = db.query(
        InflationData.tahun,
        func.avg(InflationData.nilai_inflasi).label("nilai_inflasi"),
        InflationData.nama_provinsi
    ).filter(
        InflationData.kode_provinsi == kode_provinsi
    ).group_by(
        InflationData.tahun,
        InflationData.nama_provinsi
    ).order_by(
        InflationData.tahun
    ).all()

    # Format results to match the schema
    formatted_results = [
        {
            "tahun": result.tahun,
            "nilai_inflasi": float(result.nilai_inflasi),
            "nama_provinsi": result.nama_provinsi
        } 
        for result in results
    ]

    return formatted_results
