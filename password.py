from passlib.hash import pbkdf2_sha256
hash = pbkdf2_sha256.hash("BwzQp%_-ZS92$JLkDxLkVvhRxL%Hm%JaZE-c!S9-")
#print(hash)
print(pbkdf2_sha256.verify("BwzQp%_-ZS92$JLkDxLkVvhRxL%Hm%JaZE-c!S9-", hash))