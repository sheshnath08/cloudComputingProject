<?php
session_start();
$id = $_SESSION['merchantId'];
?>
<!DOCTYPE html>
<html lang="en">

    <head>

	
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<link rel="stylesheet" media="all" type="text/css" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" />
		<link rel="stylesheet" media="all" type="text/css" href="jquery-ui-timepicker-addon.css" />
		<style type="text/css">
			*{ font-size:12px; font-family:verdana; }
			h1 { font-size:22px; }
			.wrapper { width:900px; margin:0px auto; padding:15px;background-color:#eee; }
			input { width:250px; border: 2px solid #CCC; line-height:20px;height:20px; border-radius:10px; padding:5px; }
		</style>
        <title>Merchant Homepage</title>

		<link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.2.2/css/bootstrap-combined.min.css" rel="stylesheet">
		<link rel="stylesheet" type="text/css" media="screen"
     href="http://tarruda.github.com/bootstrap-datetimepicker/assets/css/bootstrap-datetimepicker.min.css">

	 <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/4.17.37/css/bootstrap-datetimepicker.min.css" />
<script src="http://cdnjs.cloudflare.com/ajax/libs/moment.js/2.5.1/moment.min.js"></script>            
<script src="http://cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/3.0.0/js/bootstrap-datetimepicker.min.js"></script>
		
        <!-- CSS -->
        <link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Roboto:400,100,300,500">
        <link rel="stylesheet" href="assets/bootstrap/css/bootstrap.min.css">
        <link rel="stylesheet" href="assets/font-awesome/css/font-awesome.min.css">
		<link rel="stylesheet" href="assets/css/form-elements.css">
        <link rel="stylesheet" href="assets/css/style.css">
        <script type="text/javascript" src="/bower_components/jquery/jquery.min.js"></script>
        <script type="text/javascript" src="/bower_components/moment/min/moment.min.js"></script>
        <script type="text/javascript" src="/bower_components/bootstrap/dist/js/bootstrap.min.js"></script>
        <script type="text/javascript" src="/bower_components/eonasdan-bootstrap-datetimepicker/build/js/bootstrap-datetimepicker.min.js"></script>
        <link rel="stylesheet" href="/bower_components/bootstrap/dist/css/bootstrap.min.css" />
        <link rel="stylesheet" href="/bower_components/eonasdan-bootstrap-datetimepicker/build/css/bootstrap-datetimepicker.min.css" />
        <link rel="stylesheet" href="/path/to/bootstrap-datetimepicker/build/css/bootstrap-datetimepicker.min.css" />

        <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
        <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
        <!--[if lt IE 9]>
            <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
            <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
        <![endif]-->

        <!-- Favicon and touch icons -->
        <link rel="shortcut icon" href="assets/ico/favicon.png">
        <link rel="apple-touch-icon-precomposed" sizes="144x144" href="assets/ico/apple-touch-icon-144-precomposed.png">
        <link rel="apple-touch-icon-precomposed" sizes="114x114" href="assets/ico/apple-touch-icon-114-precomposed.png">
        <link rel="apple-touch-icon-precomposed" sizes="72x72" href="assets/ico/apple-touch-icon-72-precomposed.png">
        <link rel="apple-touch-icon-precomposed" href="assets/ico/apple-touch-icon-57-precomposed.png">
		<style>
		table, th, td {
			   border: 1px solid black;
   border-collapse: collapse;
}
th, td {
   padding: 5px;
   text-align: center;
}

th{
	font-size: 20px;
  padding: 5px;
  border-bottom-width: 1px;
  border-bottom-style: solid;
  }
 td{
	 font-size: 15px;
	 font-weight: bold;
 }
</style>
        </head>
		

    <body>

        
 <nav class="navbar navbar-inverse">
  <div class="container-fluid">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
    </div>
    <div class="collapse navbar-collapse" id="myNavbar">
      <ul class="nav navbar-nav">
        <li class="active"><a href="#">Welcome</a></li>
      </ul>
      <ul class="nav navbar-nav navbar-right">
        <li><a href="index.html"><span class="glyphicon glyphicon"></span> Sign Out </a></li>
      </ul>
    </div>
  </div>
</nav>
       
        <!-- Top content -->
        <div class="top-content">
        	
            <div class="inner-bg">
                <div class="container">
                	
                    <div class="row">
                        <div class="col-sm-8 col-sm-offset-2 text">
                            <h1></h1>
                            <div class="description">
                            	<p>
	                            	
                            	</p>
                            </div>
                        </div>
                    </div>
                    
                   
	                        	
	                        		<div class="center_div">
	                        			<h3>Current Offers</h3>
	                            		<p></p>
                                    </div>
	                        		
	                            
	                            <div class="form-bottom">
				                   
				                    	<div class="form-group" >
										
				                    		<label class="sr-only" for="form-username">Offer</label>
				                        	<?php 
											$flag=0;
											
											$url = "http://54.173.234.214:5000/api/offers";
                                            $response = file_get_contents($url);
                                            $json = json_decode($response, true);
											$count = 1;
                                            foreach($json['response'] as $item){
												if($item['merchantId'] == $id){
													$flag = 1;
													if($count == 1){
														echo "<table style=\"width:100%\"><tr><th>Description</th><th>Validity</th></tr>";
														$count = 5;
													}
												   echo "<tr><td>".$item['description']."</td>";
	                                               //print "-";
	                                               echo "<td>".$item['Validity']."</td></tr>";
												   //print "\n";
												}
												   }
												   if($flag == 0)
												   {
													   echo "<p style=\"font-size:200%;font-family:verdana;\" >No Offers to Display</p>";
												   }
													echo "</table>";
													//<p align = "center" class="form-username form-control">
                                            ?>
											
                                            
				                        </div>
				                        
				                        
				                    
			                    </div>
		                    
		                
		                	<div class="social-login">
	                        	<h3>Add Offers:</h3>
                                <div class="form-bottom">
				                    <form role="form" action="addoffer.php" method="post" class="registration-form">
				                    	<div class="form-group">
				                    		<label class="sr-only" for="form-offer-name">Offer Description</label>
				                        	<input type="text" name="form-offer-name" placeholder="Offer Description......" class="form-offer-name form-control" id="form-offer-name">
				                        </div>
				                        
				                        <div class="form-group"> 
										<label class="sr-only" for="form-last-name">Valid Till</label>
										<div class="row"> <div class='col-sm-6'> <div class="form-group"> <div class="wrapper">
		
					
			<div class="example-container">
				<div>
					<input type="text" value="" id="basic_example_1" placeholder="Valid Till...."name="basic_example_1" />
				</div>					
			</div>
			
			
	 	</div> </div>
	

    </script>
				                        <button type="submit" class="btn">Add</button>
				                    </form>
			                    </div>
	                        	
	                        </div>
	                        
                        </div>
                       
                   
                    
                </div>
            
            
        </div>

        <!-- Footer -->
        <footer>
        	<div class="container">
        		<div class="row">
        			
        			<div class="col-sm-8 col-sm-offset-2">
        				<div class="footer-border"></div>
        				<p></p>
        			</div>
        			
        		</div>
        	</div>
        </footer>

        <!-- Javascript -->
        <script src="assets/js/jquery-1.11.1.min.js"></script>
        <script src="assets/bootstrap/js/bootstrap.min.js"></script>
        <script src="assets/js/scripts.js"></script>
		<script type="text/javascript" src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
		<script type="text/javascript" src="http://code.jquery.com/ui/1.10.3/jquery-ui.min.js"></script>
		<script type="text/javascript" src="jquery-ui-timepicker-addon.js"></script>
		<script type="text/javascript" src="jquery-ui-sliderAccess.js"></script>
		<script type="text/javascript" src="script.js"></script>
        
        <!--[if lt IE 10]>
            <script src="assets/js/placeholder.js"></script>
        <![endif]-->

    </body>

</html>