<?php
    session_start(); // Must be here to use session info
	// Destroy the variables
	unset($_SESSION['username']);
	unset($_SESSION['logged_in']);
	unset($_SESSION['is_admin']);
	
	// Start snippet from: https://www.php.net/manual/en/function.session-destroy.php
	// Unset all of the session variables.
	$_SESSION = array();

	// If it's desired to kill the session, also delete the session cookie.
	// Note: This will destroy the session, and not just the session data!
	if (ini_get("session.use_cookies")) {
		$params = session_get_cookie_params();
		setcookie(session_name(), '', time() - 42000,
			$params["path"], $params["domain"],
			$params["secure"], $params["httponly"]
		);
	}
	// End snippet
	
	// Destroy the session
    session_destroy();
	// Redirect back to login page
    header("Location: index.html"); 
?>