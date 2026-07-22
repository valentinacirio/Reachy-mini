from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose       # per controllare i movimenti della testa di Reachy
import time                                          #libreria per gestire il tempo con time.sleep(n)
import random                                        #libreria per utilizzare la funzione random.shuffle
import msvcrt                                        #libreria per contare i secondi di tempo dopo un evento
from reachy_mini.motion.recorded_move import RecordedMoves #per far ballare reachy

def movimento_positivo(robot): #funzione per far annuire reachy
    robot.goto_target(head=create_head_pose(pitch=-20), duration=0.5) 
    time.sleep(0.5)
    robot.goto_target(head=create_head_pose(pitch=10), duration=0.5)
    time.sleep(0.5)
    robot.goto_target(head=create_head_pose(pitch=-20), duration=0.5)
    time.sleep(0.5)
    robot.goto_target(head=create_head_pose(pitch=0), duration=0.5)

def movimento_negativo(robot): #funzione per far scuotere la testa a reachy
    robot.goto_target(head=create_head_pose(yaw=25, degrees=True), duration=0.5)
    time.sleep(0.5)
    robot.goto_target(head=create_head_pose(yaw=-25, degrees=True), duration=0.5)
    time.sleep(0.5)
    robot.goto_target(head=create_head_pose(yaw=25, degrees=True), duration=0.5)
    time.sleep(0.5)
    robot.goto_target(head=create_head_pose(yaw=0, degrees=True), duration=0.5)

def movimento_dubbioso(robot): #funzione per far inclinare la testa a reachy
    robot.goto_target(head=create_head_pose(roll=-20, degrees=True), duration=0.8)
    time.sleep(2)
    robot.goto_target(head=create_head_pose(roll=0, degrees=True), duration=0.8)

def input_con_attesa(messaggio, nome, timeout=12): #funzione che stampa messaggio di incoraggiamento dopo 10 secondi che attende la risposta
    print(messaggio, end="", flush=True)
    risposta = ""
    inizio = time.time()
    messaggio_mostrato = False
    secondo_messaggio_mostrato = False
    while True:
        if msvcrt.kbhit():
            carattere = msvcrt.getwche()
            if carattere == "\r":
                print()
                # Se l'utente scrive "andiamo avanti" si salta la domanda
                if risposta.lower() == "andiamo avanti":
                    return "andiamo avanti"
                return risposta.lower()
            elif carattere == "\b":
                if risposta:
                    risposta = risposta[:-1]
            else:
                risposta += carattere
        tempo_passato = time.time() - inizio
        # Primo messaggio dopo timeout secondi
        if tempo_passato > timeout and not messaggio_mostrato:
            print(f"\nFai con calma {nome}. Prendi tutto il tempo che desideri, io sono qui ad ascoltarti.")
            messaggio_mostrato = True
        # Secondo messaggio dopo timeout*2 secondi
        if tempo_passato > timeout * 2 and not secondo_messaggio_mostrato:
            print(f"\nSe vuoi puoi scrivere 'andiamo avanti' per passare alla prossima domanda.")
            secondo_messaggio_mostrato = True

def chiedi_conferma(domanda): #funzione per quando non capisce una risposta
    """Chiede una domanda sì/no e ripete finché la risposta non è chiara."""
    SI = ["si", "sì", "va bene", "certo", "certamente", "volentieri", "molto volentieri", "proviamo", "ci provo", "ok", "okay"]
    NO = ["no", "non voglio", "non mi va"]
    while True:
        risposta = input(domanda).lower()
        if risposta in SI:
            return True
        elif risposta in NO:
            return False
        else:
            print("Non ho capito, puoi ripetere?")
            movimento_dubbioso(reachy)

# =====================
# AVVIO
# =====================
print("Avvio di Reachy...")
reachy = ReachyMini()

nome = input("Ciao! Come ti chiami? ")
print(f"Piacere di conoscerti {nome}, io sono Reachy!")

# =====================
# PRIMO GIOCO
# =====================
if chiedi_conferma("Ti andrebbe di aiutarmi in un gioco di parole? "):
    print("Fantastico!")
    time.sleep(1) #time.sleep fa una pausa di (n) secondi
    print("Ti spiego il gioco:")
    time.sleep(1)
    print("Io dirò una parola e tu dovrai dirmi di che categoria si tratta")
    time.sleep(1)
    print("Per esempio: se dico 'banana', puoi rispondere 'frutto'.")
    time.sleep(1)
    print("Se una parola ti sembra troppo difficile puoi dire 'andiamo avanti' per passare alla parola successiva")
    time.sleep(3)
    print("Pronto? Iniziamo!")
    time.sleep(1)

    gioco = { #dizionario parole da far indovinare : [risposte possibili]
        "ukulele": ["strumento musicale"],
        "gatto": ["animale", "un animale", "felino", "un felino"],
        "mango": ["frutto", "un frutto"],
        "tavolo": ["mobile", "un mobile"],
        "colibrì": ["uccello", "un uccello", "un animale", "animale"],
        "automobile": ["mezzo di trasporto", "un mezzo di trasporto", "veicolo", "un veicolo"],
        "cane": ["animale", "un animale"],
        "pizza": ["cibo", "alimento"],
        "aereo": ["mezzo di trasporto", "un mezzo di trasporto", "veicolo", "un veicolo"],
        "scarpa": ["indumento", "un indumento", "calzatura", "una calzatura"]
    }

    indizi = { #dizionario parola : indizio
        "ukulele": "Si usa per fare musica e ha delle corde.",
        "gatto": "Ha i baffi e fa le fusa.",
        "mango": "È giallo, succoso e cresce sugli alberi.",
        "tavolo": "Si trova spesso in cucina o in salotto.",
        "colibrì": "È un animale molto piccolo che vola.",
        "automobile": "Ha quattro ruote.",
        "cane": "È il miglior amico dell'uomo.",
        "pizza": "È un cibo italiano molto famoso.",
        "aereo": "Serve per viaggiare via cielo.",
        "scarpa": "Si indossa ai piedi."
    }

    parole = list(gioco.keys()) #list trasforma in una lista le chiavi del dizionario gioco quindi diventa parole = ["ukulele", "gatto", "mango", ...]
    random.shuffle(parole) #random.shuffle mescola in modo random gli elementi dalla lista parole
    terminato_naturalmente = True

    for i, parola in enumerate(parole): #enumerete restituisce un numero (i) e un elemento (parola) della lista parole
        if i == 1: #quando il ciclo arriva alla seconda parola (in indice 1)...
            print("\nProviamo con una seconda parola!")
            time.sleep(1)
        elif i > 1 and i % 2 == 0: #da dopo la econda parola (indice > 1), ogni due parole (i%2==0) avvia la funzione chiedi_conferma
            if not chiedi_conferma("Mi sto divertendo molto a giocare con te. Vuoi continuare a giocare? "):
                print("Va bene, ci fermiamo qui.")
                time.sleep(2)
                terminato_naturalmente = False
                break

        print("\n--------------------")
        print(f"La parola è: {parola}")
        risposta = input_con_attesa("Di che categoria è questa parola? ", nome, timeout=12) #funzione input_con_attesa ha 3 parametri

        if risposta in ["non so", "non lo so", "non saprei", "non ne sono sicura", "non ne sono sicuro", "non mi ricordo"]:
            print("Ti do un indizio...")
            time.sleep(1)
            print(indizi[parola]) #stampa l'indizio per quella parola
            risposta = input("Riprova: ").lower()

        if risposta == "andiamo avanti":
            print("Ok, passiamo alla prossima parola!")
            time.sleep(1)
            continue
            
        if risposta in ["non voglio continuare", "non voglio più giocare", "basta", "stop"]:
            print("Va bene, possiamo continuare il gioco un'altra volta.")
            terminato_naturalmente = False
            break

        if risposta in gioco[parola]: #se l risposta è nel dizionario gioco, in posizione della parola
            print("Bravo! Risposta corretta!")
            movimento_positivo(reachy)
        else:
            print("Non proprio! Risposte corrette: " + ", ".join(gioco[parola]))
            time.sleep(2)
            print("Non preoccuparti, andrà meglio la prossima volta")
            movimento_negativo(reachy)

        time.sleep(1)
        
    print("\nGioco terminato!")
    time.sleep(2)

else:
    print("Va bene, possiamo giocare un altro giorno.")

# =====================
# SECONDO GIOCO
# =====================
if chiedi_conferma("Ti andrebbe di fare un gioco diverso? "): #è come dire if chiedi_conterma("Ti andrebbe di fare un gioco diverso? ") == True
    print("Fantastico!")
    time.sleep(1)
    print("Ti spiego il gioco:")
    time.sleep(1)
    print("Io ti racconterò una breve storia e tu dopo risponderai ad alcune domande")
    time.sleep(1)
    print("Se una domanda ti sembra troppo difficile puoi dire 'andiamo avanti' per passare alla domanda successiva")
    time.sleep(3)
    print("Pronto? Iniziamo!")
    time.sleep(1)

    print("\n--- STORIA ---")
    time.sleep(1)
    print("Quest'estate Pietro è andato in vacanza in montagna.")
    time.sleep(3)
    print("Ha fatto una bella passeggiata nel bosco e ha raccolto dei mirtilli neri.")
    time.sleep(3)
    print("Nel bosco ha incontrato anche una volpe bianca.")
    time.sleep(3)
    print("Poi si è riposato su una panchina a guardare il sole.")
    time.sleep(2)
    print("FINE DELLA STORIA\n")

    domande = { #dizionario domanda : [risposta]
        "Dove è andato Pietro in vacanza?": ["in montagna", "montagna"],
        "Cosa ha raccolto Pietro nel bosco?": ["mirtilli", "mirtilli neri", "i mirtilli", "dei mirtilli"],
        "Dove si è riposato a guardare il sole?": ["su una panchina", "panchina"],
        "Che animale ha incontrato nel bosco?": ["volpe", "una volpe", "la volpe"],
        "Di che colore era la volpe nel bosco?": ["bianca", "bianco", "era bianca"],
    }

    contatore = 0 #contatore per contare quante domande sono state fatte
    terminato_naturalmente = True

    for domanda, risposta_corretta in domande.items():
        contatore += 1 #ad ogni domanda il contatore aumenta di 1
        print("\n" + domanda)
        risposta = input_con_attesa("Risposta: ", nome, timeout=12).lower() #alla funzione input_con_attesa servono 3 parametri

        if risposta == "andiamo avanti":
            print("Ok, passiamo alla prossima domanda!")
            time.sleep(1)
            continue

        if risposta in ["non voglio continuare", "non voglio più giocare", "basta", "stop"]:
            print("Va bene, possiamo continuare il gioco un'altra volta.")
            terminato_naturalmente = False
            break

        if risposta in ["non so", "non lo so", "non saprei", "non mi ricordo"]:
            print("Nessun problema! Ti dico io la risposta.")
            print("La risposta corretta è: " + ", ".join(risposta_corretta))
            continue

        if risposta in risposta_corretta:
            print("Bravo, sapevo che l'avresti indovinato!")
            movimento_positivo(reachy)
        else:
            print("Non esattamente! Risposte possibili: " + ", ".join(risposta_corretta))
            time.sleep(2)
            print("Non preoccuparti, andrà meglio la prossima volta")
            movimento_negativo(reachy)

        if contatore % 3 == 0: #ogni tre domande chiede se vuole continuare il gioco grazie alla funzione chiedi_conferma
            if not chiedi_conferma("\nMi sto divertendo molto a giocare con te. Vuoi continuare a giocare? "):
                print("Va bene, ci fermiamo qui.")
                terminato_naturalmente = False
                break

    if terminato_naturalmente:
        print("\nGioco terminato, congratulazioni!")

else:
    print("Va bene, possiamo giocare un altro giorno.")

print(f"\nArrivederci {nome}!")
dances = RecordedMoves("pollen-robotics/reachy-mini-dances-library") #reachy fa un ballo finale
move = dances.get("groovy_sway_and_roll")
reachy.play_move(move)