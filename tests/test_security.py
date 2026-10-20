from app.core.security import hash_password, verify_password

def test_password_hash_round_trip():
    password = "Example-Password-123!"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("Wrong-Password-123!", hashed)
