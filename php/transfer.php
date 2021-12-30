<?php
require_once 'classes/jsonRPCClient.php';
	$jsonrpc_server = 'http://127.0.0.1:16191/json_rpc';
  // $jsonrpc_server = 'http://usuario:contrasena@127.0.0.1:16191/json_rpc';
	$jsonRPCclient_instancia = new jsonRPCClient($jsonrpc_server);

$getheight = $jsonRPCclient_instancia -> get_height();
$altura = $getheight['height'];
	echo "bloque <br>";
	echo $altura ."<br>";
	echo "<br>";


//$monto = 1 *1e12;
$monto = 1;
$billetera = "Prosus38FZ6VGSptmp5RBrgiMYvaRexx9T5Bz8D3PKwGQ1aGue55mSW8iheFvLAPuDDWWBnDJZN2Q1a8PZGKbWhCAogPfYxoYLE4f";
$identificador= "343d6cab4ec4715b4d7d8a078582d88d11a69c3f14aa1cc205467fc11fa22f6b";

$destinatario    = array(
		"amount" => $monto,
		"address" => $billetera
);
$datospago       = array(
		"destinations" => $destinatario,
		"payment_id" => $identificador,
		"fee" => 100000, //unidades atómicas
		"mixin" => 1, 
		"unlock_time" => 0
);
$transferencia  = $jsonRPCclient_instancia -> transfer($datospago);
if (array_key_exists("tx_hash", $transferencia))
	{
	echo "tx_hash <br>";
	echo $transferencia['tx_hash'] ;	
	echo "<br>";
	}
	
	
?>
