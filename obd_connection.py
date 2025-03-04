import obd
import time
from tqdm import tqdm

def conectar_obd(porta, tentativas=5, timeout=1):
    print(f"Tentando conectar na porta {porta}...")
    for i in tqdm(range(tentativas), desc="Conectando", ascii=True):
        connection = obd.OBD(porta, timeout=timeout)
        if connection.is_connected():
            return connection
        print(f"Tentativa {i+1}/{tentativas} - {((i+1)/tentativas)*100:.0f}% concluído")
        time.sleep(0.5)
    return None
