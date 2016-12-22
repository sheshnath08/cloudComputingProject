<?php
session_start();
if ( isset( $_POST['signin'] ) ) {
	$password = $_POST['form-password'];
	$id = $_POST['form-username'];
	$_SESSION["merchantId"] = $id;
	//585430c8780548477e4de385
	// Connecting to the server
	$opts = array('http'=>array('header' => "User-Agent:GoogleChrome/1.0\r\n"));
	$context = stream_context_create($opts);
	$header = file_get_contents('http://54.173.234.214:5000/api/merchants/login/merchantId='.$id,false,$context);
	echo $header;
	$obj = json_decode($header, true);
	$dbpassword = $obj['password'];
	//echo "\n db password is".$dbpassword;
	if($dbpassword == $password){
		
	header('Location: homepage.php');
	}
	else
	{
		header('Location: index.html');
		echo "wrong login credentials";
	}
 }
?>