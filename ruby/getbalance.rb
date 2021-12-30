require 'faraday'
require 'json'

    rpc_input = {
        "method":"getbalance",
        "params":{
        }
    }
    url = "http://localhost:16191/json_rpc"
    data = JSON.dump(rpc_input)
    response = Faraday.post(
         url,
         data
    )

volcado = JSON.parse(response.body)
puts volcado.dig('result', 'available_balance')/(10.0**12) 
