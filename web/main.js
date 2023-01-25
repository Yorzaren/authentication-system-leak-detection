window.onload="LoadAbout();";
document.addEventListener("DOMContentLoaded", function(event) {
    if(window.location.hash=="#about") {
		ShowAbout();
	}
});
function ShowAbout() {
	document.getElementById("about-container").style.display="block";
	document.getElementById("login-container").style.display="none";
}
function HideAbout() {
	document.getElementById("about-container").style.display="none";
	document.getElementById("login-container").style.display="block";
}