FLAG_ALIVE    = 1 << 0 
FLAG_SHIELD   = 1 << 1 
FLAG_POISONED = 1 << 2  
FLAG_FLYING   = 1 << 3 
FLAG_INVIS    = 1 << 4 

def add_flag(state:int, flag:int) -> int:
    state |= flag
    return state

def has_flag(state:int,flag:int) ->bool:
    if state & flag:
        return True
    else:
        return False

def remove_flag(state:int,flag:int ) ->int:
    state &= ~flag
    return state


def crack_xor_message(ciphertext:str,known_keyword:str) ->tuple[int,str] | None:

    for key in range(1,256):
        decrypted_text = ""
        for char in ciphertext:
            decrypted_text += chr(ord(char) ^ key)
        if known_keyword in decrypted_text:
            return (key,decrypted_text)

    return None


