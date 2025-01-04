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