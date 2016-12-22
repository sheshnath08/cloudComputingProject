<?php
session_start();
$merchantId = $_SESSION["merchantId"];
$offer = $_POST['form-offer-name'];
$timeinput = $_POST['basic_example_1'];
$validity = explode(" ", $timeinput);
$date = explode("/",$validity[0]);
$dateformat = $date[2]."-".$date[0]."-".$date[1];

$time = explode(":",$validity[1]);

$timeformat = $time[0].":".$time[1].":00";
$validityformat = $dateformat." ".$timeformat;

$obj = new stdClass();
$obj->merchantId = $merchantId;
$obj->description = $offer;
$obj->validity = $validityformat;
$data_string = json_encode($obj); 
echo $data_string;

$ch = curl_init("http://54.173.234.214:5000/api/offers");                                                                      
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");                                                                     
curl_setopt($ch, CURLOPT_POSTFIELDS, $data_string);                                                                  
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);                                                                      
curl_setopt($ch, CURLOPT_HTTPHEADER, array(                                                                          
    'Content-Type: application/json',                                                                                
    'Content-Length: ' . strlen($data_string))                                                                       
);                           
$result = curl_exec($ch);?>                               
<html><script>alert("offer successfully added!!");</script></html>
<?php
header('Location: homepage.php');
//echo $result;

?>