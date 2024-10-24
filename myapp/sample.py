import random

def generate_otp(length=6):
    
    otp =''.join([str(random.randint(0, 9)) for i in range(length)])
    return otp


print(generate_otp(6))
# print("Your OTP is:", otp)