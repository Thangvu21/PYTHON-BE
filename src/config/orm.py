# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from src.db.model import Base
# from src.config.conf import Configuration

# config = Configuration()

# engine = create_engine(config.db_url)
# SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# def check_connection():
#     try:
#         # sử dụng context manager, đảm bảo tài nguyên được giải phóng đúng cách, kể cả khi có lỗi xảy ra.
#         with engine.connect() as conn:
#             print("Kết nôi SQLALchemy thành công")
#     except Exception as e:
#         print(f"kết nối thất bại {e}")
    

# check_connection()