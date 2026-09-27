from datetime import datetime
from config import MAINTENANCE_START,MAINTENANCE_END,RETRY_DELAYS_MINUTES
def in_window(now=None):
    now=now or datetime.now(); start=datetime.strptime(MAINTENANCE_START,"%H:%M").time(); end=datetime.strptime(MAINTENANCE_END,"%H:%M").time()
    return start<=now.time()<end if start<end else now.time()>=start or now.time()<end
def retry_plan(): return list(RETRY_DELAYS_MINUTES)