# Natalia Andrea Flores Perez
# 03/12/21

import io
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import base64

#Creacion de la clase
class ObjetoSeguro:
    '''Descrip: Creación de un objeto seguro, se recibe el nombre
    en formato String.'''
    #Definicion de los atributos del objeto
    def __init__(self, nombre): #Constructor
        #Atributos que se reciben
        self.nombre = nombre
        self.llave_publica, self.__private_key = self.__gen_llaves()
        
    #Metodos del objeto
    def __gen_llaves(self):
        '''Descrip:Genera la llave privada y la llave pública.''' 
        # Generar pareja de llaves RSA de 2048 bits de longitud
        keyPair = RSA.generate(2048)
        
        # Passphrase para encriptar la llave privada
        secret_code = "12345"
        
        # Exportamos la llave privada
        __private_key = keyPair.export_key(passphrase=secret_code)
        
        # Obtenemos la llave pública
        public_key = keyPair.publickey().export_key()
        
        return public_key, __private_key
    
    def saludar(self, name, msj):
        '''Descrip: Comienza la comunicación.''' 
        cifrado = self.cifrar_msj(self.llave_publica, msj)
        f'{name} mensaje: {cifrado}'
        return cifrado
    
    def responder(self, msj):
        '''Descrip:Genera la respuesta al mensaje.'''
        if self.esperar_respuesta(msj) != 0:
            respuesta = self.esperar_respuesta(msj) + "MensajeRespuesta"
            return print(respuesta)
    
    def llave_publica(self):
        '''Obtener la llave pública del objeto seguro.''' 
        return self.public_key
    
    
    def cifrar_msj(self, pub_key, msj):
        '''Descrip:Cifrar un mensaje con la llave pública
        del destinatario, el retorno es el mensaje cifrado.'''
        # Cargamos la llave pública (instancia de clase RSA)
        print("-----------------------------------------------------")
        print(type(msj))
        keyPair = RSA.importKey(pub_key)
        
        # Instancia del cifrador asimétrico
        cipher_rsa = PKCS1_OAEP.new(keyPair)
        
        # Generamos una llave para el cifrado simétrico
        aes_key = get_random_bytes(16)
        
        # Encriptamos la llave del cifrado simétrico con la llave pública RSA
        enc_aes_key = cipher_rsa.encrypt(aes_key)
        
        # Encriptamos los datos mediante cifrado simétrico (AES)
        cipher_aes = AES.new(aes_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(self.codificar64(msj))
        
        # Concatenamos la llave simétrica cifrada a los datos cifrados con ella
        enc_data = b"".join((enc_aes_key, cipher_aes.nonce, tag, ciphertext))
        print("Enc data")
        print(type(enc_data))
        return enc_data
    
    def descifrar_msj(self, msj):
        '''Descrip: Descifrar un mensaje cifrado, el retorno 
        es el mensaje en texto plano codificado en base64.''' 
        msj = str(msj)
        data_file = io.BytesIO(self.cifrar_msj(self.llave_publica,msj))
        
        # Cargamos la llave privada (instancia de clase RSA)
        keyPair = RSA.importKey(self.__private_key,  passphrase="12345")
        
        # Instancia del cifrador asimétrico
        cipher_rsa = PKCS1_OAEP.new(keyPair)
        
        # Separamos las distintas partes del msj cifrado
        enc_aes_key, nonce, tag, ciphertext =\
            (data_file.read(c) for c in (keyPair.size_in_bytes(), 16, 16, -1))
        
        # Desencriptamos la clave AES mediante la llave privada RSA
        aes_key = cipher_rsa.decrypt(enc_aes_key)
        
        # Desencriptamos los datos en si con la clave AES
        cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        print(type(data))
        print(type(self.decodificar64(data)))
        return self.decodificar64(data)
    
    def codificar64(self, msj):
        '''Descrip:Codificar un mensaje en texto plano en base64,
        el retorno es el mensaje en texto plano codificado en base64.''' 
        # Msj UTF-8 a encriptar
        # Trabajamos con bytes, codifcamos el msj.
        bin_data = msj.encode("utf-8")
        text_64_encode = base64.b64encode(bin_data)
        return text_64_encode
        
    
    def decodificar64(self, msj):
        '''Descrip:Decodificar un mensaje en base64 un mensaje en 
        texto plano, el retorno es el mensaje en texto plano''' 
        # Decodificamos el msj
        text_64_decode = base64.b64decode(msj)
        cadena = text_64_decode.decode("utf-8")
        return cadena
    
    def almacenar_msj(self, msj):
        '''Descrip:Almacenar un mensaje en texto plano en un archivo
        de texto y se le asigna un ID '''
        almacenar = {
            'ID': self.identificador+1,
            'Nombre': self.nombre,
            'Mensaje': msj
            }
        f = open ('RegistroMsj_<'+self.nombre+'>.txt','w')
        f.write(almacenar)
        f.close()
        return f'ID:<{self.identificador}>'
    
    def consultar_msj(self, identificador):
        '''Descrip:Consultar un mensaje del registro en el archivo de
        texto con el ID asignado.''' 
        f = open ('RegistroMsj_<'+self.nombre+'>.txt','r')
        if self.identificador in f:
            mensaje = f.read()
            #print(mensaje)
            f.close()
            return print(mensaje)
        
    def esperar_respuesta(self, msj):
        '''Descrip:Esperar una respuesta cifrada con llave pública que
        se desencadena hacer un saludo a otro objeto.''' 
        descifrado = self.descifrar_msj(msj)
        decodificacion = self.decodificar64(descifrado)
        return self.almacenar_msj(decodificacion)

