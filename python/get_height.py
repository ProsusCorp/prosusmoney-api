
import requests
import json


def altura():
    
    rpc_input = {
        "method":"get_height",
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
    # print(datos['result']['height'])


# ------------------------------
if __name__ == "__main__":
    altura()
