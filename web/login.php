<?php
session_start();

if ($_SERVER['REQUEST_METHOD'] == 'POST') { // Only run on post request
	// Get the username and password from the form
	$username = $_POST['username'];
	$password = $_POST['password'];



	// input
	echo "Username input was: " . $username . "<br>";
	echo "Password input was: " . $password . "<br>";

	// Remove things that arent alphanumeric or !@#$%^&*
	// Those characters are allowed by the password policy and username policy.
	// Everything else is NOT allowed.
	
	$username = preg_replace( '/([^A-Za-z0-9!@#$%^&*])+/', '', $username);
	$password = preg_replace( '/([^A-Za-z0-9!@#$%^&*])+/', '', $password);

	// Stripper 
	echo "Strip User: " . $username . "<br>";
	echo "Strip Pass: " . $password . "<br>";
	
	
	$output = passthru('python test2.py');
	echo $output;

	// Set session info for later
	if (true) {
		$_SESSION['logged_in'] = true;
		$_SESSION['is_admin'] = true;
		$_SESSION['username'] = $username;
	}
	// Redirect the user to a different page
	#header("Location: ./index.html"); // Should point them back to the index.html page which will now display a welcome message.

	// Kill self to prevent execution from continuing forever
	die();
}
?>