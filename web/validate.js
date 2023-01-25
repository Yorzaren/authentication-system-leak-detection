/* 

CONTAINS_PASSWORDPOLICY

Must match the policy on the page and the policy checks in the other scripts

*/


function LengthCheck(min, max) {
	var pw = document.getElementById("password").value.length;
	return pw >= min && pw <= max
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

function PasswordsMatch() {
	return document.getElementById("password").value == document.getElementById("confirm-password").value
}
function DeleteUsernameMatch() {
	return document.getElementById("delete-username").value == document.getElementById("confirm-delete-username").value
}

function PasswordPolicyFeedback() {
	// Short hand if statement: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Conditional_Operator
	// Hide using d-none (display:none from bootstrap) when condi is met.
	(LengthCheck(12, 32)) ? document.getElementById('password-rule-length').classList.add('d-none') : document.getElementById('password-rule-length').classList.remove('d-none');
	(UppercaseCheck(1)) ? document.getElementById('password-rule-uppercase').classList.add('d-none') : document.getElementById('password-rule-uppercase').classList.remove('d-none');
	(LowercaseCheck(1)) ? document.getElementById('password-rule-lowercase').classList.add('d-none') : document.getElementById('password-rule-lowercase').classList.remove('d-none');
	(SymbolCheck(1)) ? document.getElementById('password-rule-symbol').classList.add('d-none') : document.getElementById('password-rule-symbol').classList.remove('d-none');
	(DigitCheck(1)) ? document.getElementById('password-rule-digit').classList.add('d-none') : document.getElementById('password-rule-digit').classList.remove('d-none');
	
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
	if (PasswordsMatch() == false) {
		alert("Passwords don't match.");
		return false;
	}
	if (HasForbiddenCharCheck()) {
		alert("Forbidden characters in password.");
		return false;
	}
	if (LengthCheck(12, 32) == false) {
		alert("Bad password length.")
		return false;
	}
	if (UppercaseCheck(1) == false) {
		alert("Password does not have enough uppercase letters.");
		return false;
	}
	if (LowercaseCheck(1) == false) {
		alert("Password does not have enough lowercase letters.")
		return false;
	}
	if (SymbolCheck(1) == false) {
		alert("Password does not have enough symbols.")
		return false;
	}
	if (DigitCheck(1) == false) {
		alert("Password does not have enough digits.")
		return false;
	}
}

function ValidateDeleteUserForm() {
	if (DeleteUsernameMatch() == false) {
		alert("The given username to delete fields do not match.")
		return false;
	}
}