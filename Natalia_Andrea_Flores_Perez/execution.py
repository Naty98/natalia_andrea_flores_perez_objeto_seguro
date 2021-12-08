from proyecto import ObjetoSeguro

#Creando objetos    
alicia = ObjetoSeguro("Alicia")
bob = ObjetoSeguro("Bob")

#Utilizacion de los objetos
print("El objeto 1 es: ", alicia.nombre)
print("La llave publica de Alicia es : ", alicia.llave_publica)
msj_alicia = "Hola Bob"
print(msj_alicia)
#print("La llave privada de Alicia es : ", alicia.__private_key)
print("Codificar base64 :", alicia.codificar64(msj_alicia))
print("Decodificar base64 :", alicia.decodificar64(alicia.codificar64(msj_alicia)))
print("El mensaje a cifrar de Alicia es : ", alicia.cifrar_msj(bob.llave_publica, msj_alicia))
print("El mensaje a descifrar de Alicia es : ", alicia.descifrar_msj(alicia.cifrar_msj(bob.llave_publica, msj_alicia)))


print("\n\nEl objeto 2 es: ",bob.nombre)
print("La llave publica de Bob es : ", bob.llave_publica)
msj_bob = "Hola Alicia"
print(msj_bob)
#print("La llave privada de Bob es : ", bob.__private_key)
print("Codificar base64 :", bob.codificar64(msj_bob))
print("Decodificar base64 :", bob.decodificar64(bob.codificar64(msj_bob)))
print("El mensaje a cifrar de Bob es : ", bob.cifrar_msj(alicia.llave_publica, msj_bob))
print("El mensaje a descifrar de Alicia es : ", bob.descifrar_msj(bob.cifrar_msj(alicia.llave_publica, msj_bob)))

