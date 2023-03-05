<?php
session_start();

if ($_SERVER['REQUEST_METHOD'] == 'POST') { // Only run on post request
    // Get the username and password from the form
	$username = $_POST['username'];
	$password = $_POST['password'];



    // input
    echo "Username input was: " . $_POST['username'] . "<br>";
    echo "Password input was: " . $_POST['password'] . "<br>";

    $output = passthru('python test2.py');
    echo $output;

	// Set session info for later
    if (true) {
        $_SESSION['logged_in'] = true;
        $_SESSION['username'] = $username;
    }
    // Redirect the user to a different page
    #header("Location: ./index.html"); // Should point them back to the index.html page which will now display a welcome message.

    // Kill self to prevent execution from continuing forever
    die();
}
?>