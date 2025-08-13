from datetime import datetime
from pydantic import BaseModel

class TimeRange(BaseModel):
    start_time: datetime
    end_time: datetime 
    
