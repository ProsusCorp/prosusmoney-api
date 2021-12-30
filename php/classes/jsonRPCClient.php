<?php

class jsonRPCClient {
       
        /**
         * Debug state
         *
         * @var boolean
         */
        private $debug = true;
       
        /**
         * The server URL
         *
         * @var string
         */
        private $url;
        /**
         * The request id
         *
         * @var integer
         */
        private $id;
        /**
         * If true, notifications are performed instead of requests
         *
         * @var boolean
         */
        private $notification = false;
       
        /**
         * Takes the connection parameters
         *
         * @param string $url
         * @param boolean $debug
         */
        public function __construct($url,$debug = false) {
                // server URL
                $this->url = $url;
                // proxy
                empty($proxy) ? $this->proxy = '' : $this->proxy = $proxy;
                // debug state
                empty($debug) ? $this->debug = false : $this->debug = true;
                // message id
                $this->id = 1;
        }
       
        /**
         * Sets the notification state of the object. In this state, notifications are performed, instead of requests.
         *
         * @param boolean $notification
         */
        public function setRPCNotification($notification) {
                empty($notification) ?
                                                        $this->notification = false
                                                        :
                                                        $this->notification = true;
        }
       
        /**
         * Performs a jsonRCP request and gets the results as an array
         *
         * @param string $method
         * @param array $params
         * @return array
         */
        public function __call($method,$params) {
               
                // check
                if (!is_scalar($method)) {
                        throw new Exception('Method name has no scalar value');
                }
               
                // check
                if (is_array($params)) {
                        // no keys
                        $params = array_values($params);
                } else {
                        throw new Exception('Params must be given as array');
                }
               
                // sets notification or request task
                if ($this->notification) {
                        $currentId = NULL;
                } else {
                        $currentId = $this->id;
                }
               
                $request = array('jsonrpc' => '2.0',
                                                'method' => $method,
                                                'params' => $params
                                                );

                if($method == "send_transaction" OR $method == "get_transaction" OR $method == "transfer"){
                $request = str_replace(array('[', ']'), '', htmlspecialchars(json_encode($request), ENT_NOQUOTES));
                $this->debug && $this->debug.='***** Request *****'."\n".$request."\n".'***** End Of request *****'."\n\n";

                if(preg_match("/\"destinations\":{/i",$request)){
                        $request = str_replace("\"destinations\":{", "\"destinations\":[{", $request);
                        $request = str_replace("},\"payment"  ,"}],\"payment", $request);
                }

                }else{
                        $request = json_encode($request,JSON_FORCE_OBJECT);
                }

              // performs the HTTP POST
                $ch = curl_init($this->url);
                curl_setopt($ch,CURLOPT_RETURNTRANSFER, true);
                curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-type: application/json'));
                curl_setopt($ch, CURLOPT_POST, true);
                curl_setopt($ch, CURLOPT_POSTFIELDS, $request);
                $response = json_decode(curl_exec($ch),true);
                curl_close($ch);
                //print_r($response); //debug

                // debug output
                if ($this->debug) {
                        echo nl2br($debug);
                }
               
                // final checks and return
                if (!$this->notification) {
                       

                        if (!is_array($response)) {
                             echo "Can't connect to wallet. Please try again later.";
                             exit();
                         }

                        if (array_key_exists("error",$response)) {
                                return $response['error']['message'];
                        }
                       
                        return $response['result'];
                       
                } else {
                        return true;
                }
        }
}
?>
