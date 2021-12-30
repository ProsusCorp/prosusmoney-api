
import requests
import json


def transferencias():

    rpc_input = {
        "method":"get_transfers",
        "params":{
        }
    }

    url = "http://localhost:16191/json_rpc"
    data = json.dumps(rpc_input)    
    response = requests.post(
         url,
         data
    )

    volcado = (json.dumps(response.json(), indent=4)) 
    print(volcado)
    
    # datos = json.loads(volcado)
    # #print(datos)
    # #print(datos['result']['transfers'])
    # for d in datos['result']['transfers']:
        # respuesta = json.dumps(d, indent=2)
        # #print(respuesta)
        # listado = json.loads(respuesta)
        # print(listado['paymentId'])


# ------------------------------
if __name__ == "__main__":
    transferencias()

