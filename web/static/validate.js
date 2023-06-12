/* 

CONTAINS_USERNAMEPOLICY
CONTAINS_PASSWORDPOLICY

Must match the policy on the page and the policy checks in the other scripts

*/
var banned_words = ["password"];

function LengthCheck(string, min, max) {
	var str_length = string.length;
	return str_length >= min && str_length <= max;
}
function UppercaseCheck(string, min_number) {
	return string.length - string.replace(/[A-Z]/g, "").length >= min_number;
}
function LowercaseCheck(string, min_number) {
	return string.length - string.replace(/[a-z]/g, "").length >= min_number;
}
function DigitCheck(string, min_number) {
	return string.length - string.replace(/[0-9]/g, "").length >= min_number;
}
function SymbolCheck(string, min_number) {
	return string.length - string.replace(/[!@#$%^&*]/g, "").length >= min_number;
}
function HasForbiddenCharCheck(string) {
	return string.replace(/[A-Za-z0-9!@#$%^&*]/g, "").length > 0; // Replace will return anything not A-Z 0-9 or !@#$%^&* and then we count it
}
function HasBannedWords(string) {
	for(var i = 0; i<banned_words.length; i++) {
		string = string.toLowerCase();
		var banned = banned_words[i].toLowerCase();
		return string.indexOf(banned) >= 0;
	}
	return false;
}
function HasForbiddenUsernameCheck(string) {
	return string.replace(/[A-Za-z0-9]/g, "").length > 0 && string != "";
}
function HasMatchingStrings(string1, string2) {
	return string1 == string2;
}

function UsernameFeedback() {
	var new_username_field = document.getElementById("new-username");

	// Feedback when the users enters a bad character
	if (HasForbiddenUsernameCheck(new_username_field.value)) {
		new_username_field.classList.add('is-invalid');
		document.getElementById('username-rule-no-weird').classList.remove('d-none');
	} else {
		new_username_field.classList.remove('is-invalid');
		document.getElementById('username-rule-no-weird').classList.add('d-none');
	}
	// Check username length
	if (LengthCheck(new_username_field.value, 5, 50)) { document.getElementById('username-rule-length').classList.add('d-none'); } else { document.getElementById('username-rule-length').classList.remove('d-none'); }
	// The previous code shows and hides rules if things are met. If everything is hidden, assume all is good.
	if (document.querySelectorAll("#username-policy li:not(.d-none)").length == 1) { // The requirement on unique can't be checked, its just a note to the user.
		new_username_field.classList.add('is-valid');
		document.getElementById('username-policy').classList.add('d-none');
	} else {
		new_username_field.classList.remove('is-valid');
		document.getElementById('username-policy').classList.remove('d-none');
	}
}

function PasswordPolicyFeedback() {
	var password_field = document.getElementById("password");

	// Hide using d-none (display:none from bootstrap) when condi is met.
	if(LengthCheck(password_field.value, 12, 32)) { document.getElementById('password-rule-length').classList.add('d-none'); } else { document.getElementById('password-rule-length').classList.remove('d-none'); }
	if(UppercaseCheck(password_field.value, 1)) { document.getElementById('password-rule-uppercase').classList.add('d-none'); } else { document.getElementById('password-rule-uppercase').classList.remove('d-none'); }
	if(LowercaseCheck(password_field.value, 1)) { document.getElementById('password-rule-lowercase').classList.add('d-none'); } else { document.getElementById('password-rule-lowercase').classList.remove('d-none'); }
	if(SymbolCheck(password_field.value, 1)) { document.getElementById('password-rule-symbol').classList.add('d-none'); } else { document.getElementById('password-rule-symbol').classList.remove('d-none'); }
	if(DigitCheck(password_field.value, 1)) { document.getElementById('password-rule-digit').classList.add('d-none'); } else { document.getElementById('password-rule-digit').classList.remove('d-none'); }
	
	// Feedback when the users enters a bad character
	if (HasForbiddenCharCheck(password_field.value)) {
		password_field.classList.add('is-invalid');
		document.getElementById('password-rule-no-weird').classList.remove('d-none');
	} else {
		password_field.classList.remove('is-invalid');
		document.getElementById('password-rule-no-weird').classList.add('d-none');
	}
	
	if (HasBannedWords(password_field.value)) {
		password_field.classList.add('is-invalid');
		document.getElementById('password-rule-banned').classList.remove('d-none');
	} else {
		password_field.classList.remove('is-invalid');
		document.getElementById('password-rule-banned').classList.add('d-none');
	}
	
	// The previous code shows and hides rules if things are met. If everything is hidden, assume all is good.
	if (document.querySelectorAll("#password-policy li:not(.d-none)").length == 0) {
		password_field.classList.add('is-valid');
		document.getElementById('password-policy').classList.add('d-none');
	} else {
		password_field.classList.remove('is-valid');
		document.getElementById('password-policy').classList.remove('d-none');
	}
}

function CheckMatchingPasswordsFeedback() {
	var password_field = document.getElementById('password');
	var password_confirm_field = document.getElementById('confirm-password');

	if (HasMatchingStrings(password_field.value, password_confirm_field.value)) {
		password_confirm_field.classList.add('is-valid');
	} else {
		password_confirm_field.classList.remove('is-valid');
	}
}

function CheckDeleteUsernameFeedback() {
	var delete_user_field = document.getElementById('delete-username');
	var confirm_delete_user_field = document.getElementById('confirm-delete-username');

	if (HasMatchingStrings(delete_user_field.value, confirm_delete_user_field.value)) {
		delete_user_field.classList.add('is-valid');
		confirm_delete_user_field.classList.add('is-valid');
	} else {
		delete_user_field.classList.remove('is-valid');
		confirm_delete_user_field.classList.remove('is-valid');
	}
}

function ValidateAddUserForm() {
	var new_username_field = document.getElementById("new-username");

	if (HasForbiddenUsernameCheck(new_username_field.value)) {
		alert("Username contains forbidden characters.");
		return false;
	}
	return ValidateChangePasswordForm();
}

function ValidateDeleteUserForm() {
	var delete_user_field = document.getElementById('delete-username');
	var confirm_delete_user_field = document.getElementById('confirm-delete-username');

	if (HasMatchingStrings(delete_user_field.value, confirm_delete_user_field.value) == false) {
		alert("The given username to delete fields do not match.");
		return false;
	}
	return true;
}

function CheckUnlockUsernameFeedback() {
	var unlock_user_field = document.getElementById('unlock-username');
	var confirm_unlock_user_field = document.getElementById('confirm-unlock-username');

	if (HasMatchingStrings(unlock_user_field.value, confirm_unlock_user_field.value)) {
		unlock_user_field.classList.add('is-valid');
		confirm_unlock_user_field.classList.add('is-valid');
	} else {
		unlock_user_field.classList.remove('is-valid');
		confirm_unlock_user_field.classList.remove('is-valid');
	}
}

function ValidateUnlockUserForm() {
	var unlock_user_field = document.getElementById('unlock-username');
	var confirm_unlock_user_field = document.getElementById('confirm-unlock-username');

	if (HasMatchingStrings(unlock_user_field.value, confirm_unlock_user_field.value) == false) {
		alert("The given username to unlock fields do not match.");
		return false;
	}
	return true;
}

function ValidateChangePasswordForm() {
	var password_field = document.getElementById("password");
	var password_confirm_field = document.getElementById('confirm-password');

	if (HasMatchingStrings(password_field.value, password_confirm_field.value) == false) {
		alert("Passwords don't match.");
		return false;
	}
	if (HasForbiddenCharCheck(password_field.value)) {
		alert("Forbidden characters in password.");
		return false;
	}
	if (HasBannedWords(password_field.value)) {
		alert("Banned word(s) in password.");
		return false;
	}
	if (LengthCheck(password_field.value, 12, 32) == false) {
		alert("Bad password length.");
		return false;
	}
	if (UppercaseCheck(password_field.value, 1) == false) {
		alert("Password does not have enough uppercase letters.");
		return false;
	}
	if (LowercaseCheck(password_field.value, 1) == false) {
		alert("Password does not have enough lowercase letters.");
		return false;
	}
	if (SymbolCheck(password_field.value, 1) == false) {
		alert("Password does not have enough symbols.");
		return false;
	}
	if (DigitCheck(password_field.value, 1) == false) {
		alert("Password does not have enough digits.");
		return false;
	}
	return true;
}