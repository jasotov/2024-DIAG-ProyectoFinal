function password_show_hide(tbPasswordId,ShowEyeId,HideEyeId) {
    var x = document.getElementById(tbPasswordId);
    var show_eye = document.getElementById(ShowEyeId);
    var hide_eye = document.getElementById(HideEyeId);
    hide_eye.classList.remove("d-none");
    if (x.type === "password") {
        x.type = "text";
        show_eye.style.display = "none";
        hide_eye.style.display = "block";
    } else {
        x.type = "password";
        show_eye.style.display = "block";
        hide_eye.style.display = "none";
    }
}

function scrollToBottom(sDivId) {
    scrollableDiv = document.getElementById(sDivId);
    scrollableDiv.scrollTop = scrollableDiv.scrollHeight;
}

function submitMessage(button) {
    msg = document.getElementById("message").value.trim();
    form = document.getElementById("formchat2");
    if (msg != '') {
        button.disabled = true;
        document.getElementById("text").style.display = 'none';
        document.getElementById("spinner").style.display = 'block';
        form.submit();
    }
    else {
        form.className = 'was-validated'; 
    }
}

function showMessageDiv() {
    if (document.getElementById("MsgType1").checked) {
        document.getElementById("FreeMsgDiv").style.display = 'block';
        document.getElementById("QuickMsgDiv").style.display = 'none';
    }
    else {
        document.getElementById("FreeMsgDiv").style.display = 'none';
        document.getElementById("QuickMsgDiv").style.display = 'block';
    }
}

function submitLogin(button) {
    email = document.getElementById("email").value.trim();
    pwd = document.getElementById("password").value.trim();
    form = document.getElementById("login");
    if (email != '' && validateEmail(email) && pwd != '') {
        button.disabled = true;
        document.getElementById("text").style.display = 'none';
        document.getElementById("spinner").style.display = 'block';
        form.submit();
    }
    else {
        form.className = 'was-validated'; 
    }
}

function validateEmail(email){
	var validEmail =  /^\w+([.-_+]?\w+)*@\w+([.-]?\w+)*(\.\w{2,10})+$/;

	if( validEmail.test(email) ){
		return true;
	}else{
		return false;
	}
}