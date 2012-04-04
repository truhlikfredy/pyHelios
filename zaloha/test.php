<?php
error_reporting(E_ALL | E_STRICT);

$socket = socket_create(AF_INET, SOCK_DGRAM, SOL_UDP);
socket_bind($socket, '192.168.1.8', 9089);

$from = '';
$port = 0;
while(1) {
socket_recvfrom($socket, $buf, 65536, 0, $from, $port);
$buf=substr($buf,9);
$ar=explode(':',$buf);

//echo "Received $buf from remote address $from and remote port $port" . PHP_EOL;
//var_dump($ar);
//unset($id);
//unset($val);
foreach ($ar as $i) {
    $tmp=explode('=',$i);
//    $id[]=$tmp[0];
    $cislo=$tmp[0];
    settype($cislo,'int');
    $val[$cislo]=$tmp[1];
}
/*
foreach ($val as $k=>$v) {
    echo $k.' '.$v."\n";
}*/
//if (!isset($val[51]) echo $val[51]."\n";
    echo (1+($val[53]*14))."\n";
}
?>
