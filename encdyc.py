class TextSecurity:
    """ This class encrypts and decrypts the test using Caesar cipher """
    def __init__(self, shift):
        """ Constructor """
        self.shifter = shift
  
    def _convert(self, text, s):
        """ Return encrypted or decrypted string """
        result=""
        for ch in text:     
            if ch.isupper(): # Deal with uppercase letters
                result += chr((ord(ch) + s - 65) % 26 + 65)
            elif ch.islower(): # Deal with lowercase letters
                result += chr((ord(ch) + s -97) % 26 + 97)
            elif ch.isdigit(): # Deal with digits
                result += chr((ord(ch) + s -48) % 10 + 48)
            else: # Deal with other characters (symbols, etc.)
                result += ch
        return  result
  
    def encrypt(self, text):
        """ Return encrypted string """
        return self._convert(text, self.shifter)
        
    def decrypt(self, text):
        """ Return encrypted string """
        return self._convert(text, -self.shifter) 

# if __name__ == '__main__':
#     cipher = TextSecurity(5)
#     message = "DY20!341"
#     coded = cipher.encrypt(message)
#     print('Secret: ', coded)
#     answer = cipher.decrypt(coded)
#     print('Message:', answer)