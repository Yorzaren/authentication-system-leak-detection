/* 

CONTAINS_USERNAMEPOLICY
CONTAINS_PASSWORDPOLICY

Must match the policy on the page and the policy checks in the other scripts

*/


function LengthCheck(target_id, min, max) {
	var pw = document.getElementById(target_id).value.length;
	return pw >= min && pw <= max;
}
function UppercaseCheck(min_number) {
	var pw = document.getElementById("password").value;
	return pw.length - pw.replace(/[A-Z]/g, '').length >= min_number;
}
function LowercaseCheck(min_number) {
	var pw = document.getElementById("password").value;
	return pw.length - pw.replace(/[a-z]/g, '').length >= min_number;
}
function DigitCheck(min_number) {
	var pw = document.getElementById("password").value;
	return pw.length - pw.replace(/[0-9]/g, '').length >= min_number;
}
function SymbolCheck(min_number) {
	var pw = document.getElementById("password").value;
	return pw.length - pw.replace(/[!@#$%^&*]/g, '').length >= min_number;
}
function HasForbiddenCharCheck() {
	var pw = document.getElementById("password").value;
	return pw.replace(/[A-Za-z0-9!@#$%^&*]/g, '').length > 0;
}
function HasForbiddenUsernameCheck() {
	var user = document.getElementById("new-username").value;
	return user.replace(/[A-Za-z0-9]/g, '').length > 0 && user != "";
}

function PasswordsMatch() {
	return document.getElementById("password").value == document.getElementById("confirm-password").value;
}
function DeleteUsernameMatch() {
	return document.getElementById("delete-username").value == document.getElementById("confirm-delete-username").value;
}

function UsernameFeedback() {
	// Feedback when the users enters a bad character
	if (HasForbiddenUsernameCheck()) {
		document.getElementById('new-username').classList.add('is-invalid');
		document.getElementById('username-rule-no-weird').classList.remove('d-none');
	} else {
		document.getElementById('new-username').classList.remove('is-invalid');
		document.getElementById('username-rule-no-weird').classList.add('d-none');
	}
	// Check username length
	if (LengthCheck("new-username", 5, 50)) { document.getElementById('username-rule-length').classList.add('d-none'); } else { document.getElementById('username-rule-length').classList.remove('d-none'); }
	// The previous code shows and hides rules if things are met. If everything is hidden, assume all is good.
	if (document.querySelectorAll("#username-policy li:not(.d-none)").length == 1) { // The requirement on unique can't be checked, its just a note to the user.
		document.getElementById('new-username').classList.add('is-valid');
		document.getElementById('username-policy').classList.add('d-none');
	} else {
		document.getElementById('new-username').classList.remove('is-valid');
		document.getElementById('username-policy').classList.remove('d-none');
	}
}

function PasswordPolicyFeedback() {
	// Hide using d-none (display:none from bootstrap) when condi is met.
	if(LengthCheck("password", 12, 32)) { document.getElementById('password-rule-length').classList.add('d-none'); } else { document.getElementById('password-rule-length').classList.remove('d-none'); }
	if(UppercaseCheck(1)) { document.getElementById('password-rule-uppercase').classList.add('d-none'); } else { document.getElementById('password-rule-uppercase').classList.remove('d-none'); }
	if(LowercaseCheck(1)) { document.getElementById('password-rule-lowercase').classList.add('d-none'); } else { document.getElementById('password-rule-lowercase').classList.remove('d-none'); }
	if(SymbolCheck(1)) { document.getElementById('password-rule-symbol').classList.add('d-none'); } else { document.getElementById('password-rule-symbol').classList.remove('d-none'); }
	if(DigitCheck(1)) { document.getElementById('password-rule-digit').classList.add('d-none'); } else { document.getElementById('password-rule-digit').classList.remove('d-none'); }
	
	// Feedback when the users enters a bad character
	if (HasForbiddenCharCheck()) {
		document.getElementById('password').classList.add('is-invalid');
		document.getElementById('password-rule-no-weird').classList.remove('d-none');
	} else {
		document.getElementById('password').classList.remove('is-invalid');
		document.getElementById('password-rule-no-weird').classList.add('d-none');
	}
	
	// The previous code shows and hides rules if things are met. If everything is hidden, assume all is good.
	if (document.querySelectorAll("#password-policy li:not(.d-none)").length == 0) {
		document.getElementById('password').classList.add('is-valid');
		document.getElementById('password-policy').classList.add('d-none');
	} else {
		document.getElementById('password').classList.remove('is-valid');
		document.getElementById('password-policy').classList.remove('d-none');
	}
}

function CheckMatchingPasswordsFeedback() {
	if (PasswordsMatch()) {
		document.getElementById('confirm-password').classList.add('is-valid');
	} else {
		document.getElementById('confirm-password').classList.remove('is-valid');
	}
}

function CheckDeleteUsernameFeedback() {
	if (DeleteUsernameMatch()) {
		document.getElementById('delete-username').classList.add('is-valid');
		document.getElementById('confirm-delete-username').classList.add('is-valid');
	} else {
		document.getElementById('delete-username').classList.remove('is-valid');
		document.getElementById('confirm-delete-username').classList.remove('is-valid');
	}
}

function ValidateAddUserForm() {
	if (HasForbiddenUsernameCheck()) {
		alert("Username contains forbidden characters.");
	}
	ValidateChangePasswordForm();
}

function ValidateDeleteUserForm() {
	if (DeleteUsernameMatch() == false) {
		alert("The given username to delete fields do not match.");
		return false;
	}
}

function ValidateChangePasswordForm() {
	if (PasswordsMatch() == false) {
		alert("Passwords don't match.");
		return false;
	}
	if (HasForbiddenCharCheck()) {
		alert("Forbidden characters in password.");
		return false;
	}
	if (LengthCheck(12, 32) == false) {
		alert("Bad password length.");
		return false;
	}
	if (UppercaseCheck(1) == false) {
		alert("Password does not have enough uppercase letters.");
		return false;
	}
	if (LowercaseCheck(1) == false) {
		alert("Password does not have enough lowercase letters.");
		return false;
	}
	if (SymbolCheck(1) == false) {
		alert("Password does not have enough symbols.");
		return false;
	}
	if (DigitCheck(1) == false) {
		alert("Password does not have enough digits.");
		return false;
	}
}