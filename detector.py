import re
import unicodedata

# Paraules i expressions sospitoses
urgencia = [
    "urgent",
    "immediatament",
    "ultima oportunitat",
    "ultim avis",
    "sera bloquejat",
    "sera bloquejada",
    "sera eliminat",
    "sera eliminada",
    "en 24 hores",
    "en 48 hores",
    "avui mateix",
    "actua ara",
    "paga ara",
    "caduca",
    "retingut",
    "retinguda",
    "compte suspes",
    "compte suspesa"
]

dades_personals = [
    "contrasenya",
    "verifica el teu compte",
    "verifiques el teu compte",
    "verificar el teu compte",
    "confirma les teves dades",
    "actualitza les teves dades",
    "introdueix les teves dades",
    "dades personals",
    "dades bancaries",
    "numero de targeta",
    "codi de seguretat",
    "pin",
    "cvv",
    "dni",
    "credencials"
]

pagaments = [
    "paga",
    "pagar",
    "pagament",
    "transferencia",
    "taxa",
    "despeses d'enviament"
]

premis = [
    "has guanyat",
    "has estat seleccionat",
    "has estat seleccionada",
    "guanyador",
    "guanyadora",
    "premi",
    "sorteig",
    "regal gratuit"
]

suplantacio = [
    "banc",
    "suport tecnic",
    "administrador",
    "servei de seguretat",
    "hisenda",
    "seguretat social",
    "paypal",
    "amazon",
    "netflix",
    "microsoft",
    "apple"
]

escurcadors = [
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "is.gd"
]

paraules_enllac_sospitos = [
    "login",
    "verifica",
    "actualitza",
    "seguretat",
    "pagament",
    "compte"
]

# Frases que tranquil·litzen (ex: "mai et demanarem la contrasenya")
frases_seguretat = [
    "mai et demanarem",
    "mai us demanarem",
    "no et demanarem",
    "no us demanarem",
    "no comparteixis",
    "no compartiu"
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


# Buscar paraules completes (així "banc" no troba "bancaries")
def conte(text, llista):
    return any(
        re.search(r"\b" + re.escape(paraula) + r"\b", text)
        for paraula in llista
    )


# Treure les frases que avisen de NO donar dades
def treure_frases_seguretat(text):
    frases = re.split(r"[.!?\n]+", text)

    frases = [
        frase for frase in frases
        if not any(avis in frase for avis in frases_seguretat)
    ]

    return ". ".join(frases)


# Analitzar el correu electronic
def analitzar_correu(correu):

    text = normalitzar(correu)

    puntuacio = 0
    alertes = []

    # Detectar missatges d'urgencia
    if conte(text, urgencia):
        puntuacio += 20
        alertes.append("Conté missatges d'urgència")

    # Detectar sol·licituds de dades personals
    if conte(treure_frases_seguretat(text), dades_personals):
        puntuacio += 30
        alertes.append("Sol·licita informació personal")

    # Detectar peticions de pagament
    if conte(text, pagaments) or re.search(r"\d+([.,]\d+)?\s?(€|euros?)", text):
        puntuacio += 20
        alertes.append("Demana un pagament o diners")

    # Detectar premis o regals falsos
    if conte(text, premis):
        puntuacio += 20
        alertes.append("Promet un premi o regal")

    # Detectar enllaços
    enllacos = re.findall(r"https?://\S+", text)

    if enllacos:
        puntuacio += 15
        alertes.append("Conté un o més enllaços")

    # Detectar enllaços sense connexió segura
    if any(enllac.startswith("http://") for enllac in enllacos):
        puntuacio += 10
        alertes.append("Conté un enllaç sense connexió segura (http)")

    # Detectar enllaços amb paraules sospitoses
    if any(paraula in enllac for enllac in enllacos for paraula in paraules_enllac_sospitos):
        puntuacio += 15
        alertes.append("Conté un enllaç amb paraules sospitoses")

    # Detectar escurçadors d'enllaços
    if any(re.search(r"(?<![\w.-])" + re.escape(domini) + r"\b", text) for domini in escurcadors):
        puntuacio += 25
        alertes.append("Conté un enllaç escurçat")

    # Detectar possibles suplantacions
    if conte(text, suplantacio):
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
if __name__ == "__main__":
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
