from hashlib import sha256

def get_hash(formal: str):
    afterstring = formal + 'pAjenG93'
    s256 = sha256(afterstring.encode()).hexdigest()
    string = s256[14] + s256[24] + s256[3] + s256[25] + s256[8] + s256[7]
    return string

id = input('ハイローのユーザーIDを入力')
print(id + ' → ' + get_hash(id))
input('何かキーを入力して終了')