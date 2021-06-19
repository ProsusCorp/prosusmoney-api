
__author__ = 'www.prosuscorp.com'
__license__ = "MIT"
__maintainer__ = "YerkoBits"


# -----------------------------------------------------------------------
# enviar transacción
'''
[SETUP]
# pip install requests
sudo apt install python-requests
'''
import requests
import json
import binascii
import time

def main():
    # ./prosus-wallet --daemon-port 16181 --rpc-bind-port 16191
    url = "http://localhost:16191/json_rpc"
    # standard json header
    headers = {'content-type': 'application/json'}

    destination_address =  input("ingrese prosus-address del destinatario \n")
	
    # using given mixin
    mixin = 1

    # amount of prosus to send
    total = float(input("ingrese total a transferir \n"))
    amount = float(input("monto cada transacción\n"))
	
    # cryptonote amount format is different then that normally used by people.
    # thus the float amount must be changed to something that cryptonote understands.
    int_amount = int(get_amount(amount))

    # just to make sure that amount->coversion->back gives the same amount as in the initial number.
    assert amount == float(get_money(str(int_amount))), "Amount conversion failed"

    # get some random payment_id
    payment_id = get_payment_id()
	
	# comision (minimo 100000)
    fee = 100000
 
    # simplewallet' procedure/method to call
    rpc_input = {
        "method": "transfer",
        "params": {
				"destinations": 
					[{
					"address": destination_address,
					"amount": int_amount
					}],
				"mixin": mixin,
				"fee": fee,
				"unlock_time": 0,
				"payment_id" : payment_id
				}
   }
	
    # add standard rpc values
    rpc_input.update({"jsonrpc": "2.0", "id": "0"})

#--------------------
    i=1
    while i <= total/amount:
        # execute the rpc request
        response = requests.post(
             url,
             data=json.dumps(rpc_input),
             headers=headers)

        # print the payment_id
        print("#payment_id: ", payment_id)

        # pretty print json output
        print (json.dumps(response.json(), indent=4))

        time.sleep(5)
        i=i+1
#--------------------

def get_amount(amount):
    CRYPTONOTE_DISPLAY_DECIMAL_POINT = 12
    str_amount = str(amount)
    fraction_size = 0

    if '.' in str_amount:
        point_index = str_amount.index('.')
        fraction_size = len(str_amount) - point_index - 1

        while fraction_size < CRYPTONOTE_DISPLAY_DECIMAL_POINT and '0' == str_amount[-1]:
            #print(66)
            str_amount = str_amount[:-1]
            fraction_size = fraction_size - 1

        if CRYPTONOTE_DISPLAY_DECIMAL_POINT < fraction_size:
            return False

        str_amount = str_amount[:point_index] + str_amount[point_index+1:]

    if not str_amount:
        return False

    if fraction_size < CRYPTONOTE_DISPLAY_DECIMAL_POINT:
        str_amount = str_amount + '0'*(CRYPTONOTE_DISPLAY_DECIMAL_POINT - fraction_size)

    return str_amount


def get_money(amount):
    CRYPTONOTE_DISPLAY_DECIMAL_POINT = 12
    s = amount

    if len(s) < CRYPTONOTE_DISPLAY_DECIMAL_POINT + 1:
        # add some trailing zeros, if needed, to have constant width
        s = '0' * (CRYPTONOTE_DISPLAY_DECIMAL_POINT + 1 - len(s)) + s

    idx = len(s) - CRYPTONOTE_DISPLAY_DECIMAL_POINT
    s = s[0:idx] + "." + s[idx:]
    return s

def get_payment_id():
#    payment_id = "50726F73757320436F7270202020202020202020202020202020202020202020"
    payment_id = binascii.hexlify( time.strftime('%c').ljust(32).encode() ).decode('ascii')
    return payment_id


if __name__ == "__main__":
    main()

# -----------------------------------------------------------------------




