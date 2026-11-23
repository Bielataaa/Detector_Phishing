import re
import unicodedata

# Paraules i expressions sospitoses
urgencia = [
    "urgent",
    "immediatament",
    "ultima oportunitat",
    "sera bloquejat",
    "sera bloquejada",
    "en 24 hores",
    "actua ara",
    "compte suspes",
    "compte suspesa"
]

dades_personals = [
    "contrasenya",
    "verifica el teu compte",
    "verificar el teu compte",
    "dades bancaries",
    "numero de targeta",
    "introdueix les teves dades",
    "credencials"
]

suplantacio = [
    "banc",
    "suport tecnic",
    "administrador",
    "servei de seguretat"
]

escurcadors = [
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "is.gd"
]


# Normalitzar el text
def normalitzar(text):
    text = text.lower()

    text = unicodedata.normalize("NFD", text)

    text = "".join(
        caracter for caracter in text
        if unicodedata.category(caracter) != "Mn"
    )

    return text


# Analitzar el correu electronic
def analitzar_correu(correu):

    text = normalitzar(correu)

    puntuacio = 0
    alertes = []

    # Detectar missatges d'urgencia
    if any(paraula in text for paraula in urgencia):
        puntuacio += 20
        alertes.append("Conté missatges d'urgència")

    # Detectar sol·licituds de dades personals
    if any(paraula in text for paraula in dades_personals):
        puntuacio += 30
        alertes.append("Sol·licita informació personal")

    # Detectar enllaços
    enllacos = re.findall(r"https?://\S+", text)

    if enllacos:
        puntuacio += 15
        alertes.append("Conté un o més enllaços")

    # Detectar escurçadors d'enllaços
    if any(domini in text for domini in escurcadors):
        puntuacio += 25
        alertes.append("Conté un enllaç escurçat")

    # Detectar possibles suplantacions
    if any(paraula in text for paraula in suplantacio):
        puntuacio += 10
        alertes.append("Esmenta una entitat o servei")

    # Limitar la puntuació a 100
    puntuacio = min(puntuacio, 100)

    # Classificar el nivell de risc
    if puntuacio >= 60:
        resultat = "RISC ALT"
    elif puntuacio >= 30:
        resultat = "RISC MITJÀ"
    else:
        resultat = "RISC BAIX"

    return puntuacio, resultat, alertes


# Programa principal
print("================================")
print("     DETECTOR DE PHISHING")
print("================================")

correu = input("\nIntrodueix el correu fictici:\n")

puntuacio, resultat, alertes = analitzar_correu(correu)

print("\n-------- RESULTAT --------")

print("Puntuació de risc:", puntuacio, "/100")
print("Classificació:", resultat)

print("\nIndicadors detectats:")

if alertes:
    for alerta in alertes:
        print("-", alerta)
else:
    print("No s'han trobat indicadors sospitosos.")

print("\nATENCIÓ: un resultat de risc baix")
print("no garanteix que el correu sigui segur.")
