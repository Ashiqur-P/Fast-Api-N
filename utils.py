from passlib.context import CryptContext

# পাসওয়ার্ড সিকিউরিটি কনফিগারেশন
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """প্লেইন পাসওয়ার্ডকে হ্যাশ করার ফাংশন"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """হ্যাশ পাসওয়ার্ড ভেরিফাই করার ফাংশন (যা আপনার ফাইলে মিসিং ছিল)"""
    return pwd_context.verify(plain_password, hashed_password)