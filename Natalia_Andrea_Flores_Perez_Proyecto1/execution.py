from proyecto import ObjetoSeguro

# Creando objetos
alicia = ObjetoSeguro("Alicia")
bob = ObjetoSeguro("Bob")

# Utilizacion de los objetos
msj_alicia = "Hola Bob"
print(msj_alicia)
msj_bob = "Hola Alicia"
print(msj_bob)

print("El objeto 1 es: ", alicia.nombre)
print("La llave publica de Alicia es : ", alicia.llave_publica)
# print("Codificar base64 :", alicia.codificar64(msj_alicia))
# print("Decodificar base64 :", alicia.decodificar64(alicia.codificar64(msj_alicia)))
print("El mensaje a cifrar de Alicia es : ", alicia.cifrar_msj(bob.llave_publica, msj_alicia))
print("El mensaje a descifrar de Alicia es : ", alicia.descifrar_msj(alicia.cifrar_msj(bob.llave_publica, msj_alicia)))


print("\n\nEl objeto 2 es: ", bob.nombre)
print("La llave publica de Bob es : ", bob.llave_publica)
# print("Codificar base64 :", bob.codificar64(msj_bob))
# print("Decodificar base64 :", bob.decodificar64(bob.codificar64(msj_bob)))
print("El mensaje a cifrar de Bob es : ", bob.cifrar_msj(alicia.llave_publica, msj_bob))
print("El mensaje a descifrar de Bob es : ", bob.descifrar_msj(bob.cifrar_msj(alicia.llave_publica, msj_bob)))

msj1 = alicia.saludar('Alicia', msj_alicia)
bob.esperar_respuesta(msj1)
rsp = bob.responder(msj_bob)
alicia.esperar_respuesta(rsp)

bob.consultar_msj(1)
alicia.consultar_msj(2)
