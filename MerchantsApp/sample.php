<?php

	$connection = new MongoClient();
	echo "connection to the database successfull!1";
	$db = $connection->mydb;
	echo "mydb selected!!";
	?>