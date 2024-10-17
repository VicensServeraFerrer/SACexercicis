from practica_2_api import servei
import time

def bucle():
    ids = [0,1,2]
    consens = False

    with servei.test_client() as client:
        while not consens:
            for id in ids:
                resposta_client = client.get(f"/agent/{id}/generar")
                print(f"Decisio de {id}: {resposta_client.get_json()}")
            

            resposta = client.get("/consens")
            consens = resposta.get_json()["consens"]
            print(consens)
            time.sleep(2)

        



if __name__=="__main__":
    bucle()


