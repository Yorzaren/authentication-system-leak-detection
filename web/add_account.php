<?php
session_start();

if ($_SERVER['REQUEST_METHOD'] == 'POST') { // Only run on post request
	// Only accept it from admins
	if ($_SESSION['is_admin'] != true) {
		// Kill script
		//exit("Not Admin");
	}
	
	
	// They are an admin.
	
	// Get the values from the form
	$username = $_POST['new-username'];
	$password = $_POST['password'];
	$confirm_password = $_POST['confirm-password'];
	$type = $_POST['account-type'];
	$admin_username = $_SESSION['username'];
	$admin_password = $_POST['confirm-admin-password-add'];

	// Check if the passwords match.
	if ($password !== $confirm_password) {
		echo('<h2>Account Creation Error:</h2><p>The given user password does not match the confirmation password.</p>');
		//exit(); // Exit early
	}
	
	// Check against password policy 
	$password_passed_policy_check = exec('python policy_check.py --password '.$password); // Returns a string: True or False
	if ($password_passed_policy_check == 'True' || $password_passed_policy_check == True) {
		echo '<p>PASS: The password meets the policy rules.</p>';
	} else {
		echo '<p>FAIL: The password did NOT meet the policy rules.</p>';
		//exit(); // Exit early
	}
	
	// Check the username against the policy.
	$username_passed_policy_check = exec('python policy_check.py --username '.$username);
	if ($username_passed_policy_check == 'True' || $username_passed_policy_check == True) {
		echo '<p>PASS: The username: '.$username.' is free.</p>';
	} else {
		echo '<p>FAIL: The username: '.$username.' is NOT free.</p>';
		//exit(); // Exit early
	}
	
	// Check the type is valid
	if ($type === '1') {
		echo '<p>Passing: Trying to create account as admin user.</p>';
		$system_outcome = exec('python auth_system.py ' . $admin_username . ' ' . $admin_password . ' --add-admin-account ' . ' -t ' . $username . ' -np ' .$password);
		echo $system_outcome;
		
	} elseif ($type === '0') {
		echo '<p>Passing: Trying to create account as normal user.</p>';
		$system_outcome = exec('python auth_system.py '. $admin_username . ' ' . $admin_password);
		echo $system_outcome;
	} else {
		exit('ERROR: Type was not set correctly');
	}

	// Debugging INPUT
	echo "Username input was: " . $username . "<br>";
	echo "Password input was: " . $password . "<br>";
	echo "Confirm password input was: " . $confirm_password . "<br>";
	echo "Type input was: " . $type . "<br>";
	echo "Admin Username input was: " . $admin_username . "<br>";
	echo "Admin Password input was: " . $admin_password . "<br>";

	// Remove things that arent alphanumeric or !@#$%^&*
	// Those characters are allowed by the password policy and username policy.
	// Everything else is NOT allowed.

	// TODO: Might reconsider this.
	// Reasons:
	// It shouldn't be possible for a normal user to submit invalid characters from the client side js.
	// The sanitization exists to help prevent attacks from people bypassing the js check.


	$username = preg_replace( '/([^A-Za-z0-9!@#$%^&*])+/', '', $username);
	$password = preg_replace( '/([^A-Za-z0-9!@#$%^&*])+/', '', $password);

	// Stripper 
	echo "Strip User: " . $username . "<br>";
	echo "Strip Pass: " . $password . "<br>";
	
	
	$output = passthru('python policy_check.py --username '.$username);
	
	if ($output == true || $output == True) {
		echo 'Test was fine';
	} else {
		echo $output;
	}
	echo $output;


	// Redirect the user to a different page
	#header("Location: ./index.html"); // Should point them back to the index.html page which will now display a welcome message.

	// Kill self to prevent execution from continuing forever
	die();
}
?>