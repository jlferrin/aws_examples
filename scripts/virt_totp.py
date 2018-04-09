
import pyotp
import sys


semilla=str(sys.argv[1])

totp = pyotp.TOTP(semilla)
print("Current OTP:", totp.now())

