import secrets
from django.conf import settings
from django.core import signing
from django.utils import timezone
def generate_hex_code(): return secrets.token_hex(3).upper()
def build_unique_code(ambulance_id,date=None):
 date=date or timezone.localdate(); return f"NEMSAS/JSEMSAS/{ambulance_id}/{date:%Y-%m-%d}/{generate_hex_code()}"
def build_etc_code(facility_code,date=None):
 date=date or timezone.localdate(); return f"NEMSAS/JSEMSAS/ETC/{facility_code}/{date:%Y-%m-%d}/{generate_hex_code()}"
def build_qr_token(claim_type,object_id,expires_minutes=43200): return signing.dumps({"type":claim_type,"id":str(object_id),"iat":int(timezone.now().timestamp())},key=settings.QR_SIGNING_KEY,salt="jsemsas.qr",compress=True)
def verify_qr_token(token,max_age=2592000): return signing.loads(token,key=settings.QR_SIGNING_KEY,salt="jsemsas.qr",max_age=max_age)
