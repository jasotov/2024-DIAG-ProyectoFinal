$("input[type=password]").keyup(function(){
    var ucase = new RegExp("[A-Z]+");
	var lcase = new RegExp("[a-z]+");
	var num = new RegExp("[0-9]+");
    var bOk1 = true;
    var bOk2 = true;

	if ($("#password1").val() != "") {
	
		if($("#password1").val().length >= 8){
			$("#8char").removeClass("bi-exclamation-circle");
			$("#8char").addClass("bi-check-circle");
			$("#8char").css("color","#00A41E");
		}else{
			$("#8char").removeClass("bi-check-circle");
			$("#8char").addClass("bi-exclamation-circle");
			$("#8char").css("color","#FF0004");
			bOk1 = false;
		}
		
		if(ucase.test($("#password1").val())){
			$("#ucase").removeClass("bi-exclamation-circle");
			$("#ucase").addClass("bi-check-circle");
			$("#ucase").css("color","#00A41E");
		}else{
			$("#ucase").removeClass("bi-check-circle");
			$("#ucase").addClass("bi-exclamation-circle");
			$("#ucase").css("color","#FF0004");
			bOk1 = false;
		}
		
		if(lcase.test($("#password1").val())){
			$("#lcase").removeClass("bi-exclamation-circle");
			$("#lcase").addClass("bi-check-circle");
			$("#lcase").css("color","#00A41E");
		}else{
			$("#lcase").removeClass("bi-check-circle");
			$("#lcase").addClass("bi-exclamation-circle");
			$("#lcase").css("color","#FF0004");
			bOk1 = false;
		}
		
		if(num.test($("#password1").val())){
			$("#num").removeClass("bi-exclamation-circle");
			$("#num").addClass("bi-check-circle");
			$("#num").css("color","#00A41E");
		}else{
			$("#num").removeClass("bi-check-circle");
			$("#num").addClass("bi-exclamation-circle");
			$("#num").css("color","#FF0004");
			bOk1 = false;
		}

		if (bOk1) {
			$("#password1").removeClass("is-invalid");
			$("#password1").addClass("is-valid");
		} else {
			$("#password1").removeClass("is-valid");
			$("#password1").addClass("is-invalid");
		}

	} else {
		$("#8char").removeClass("bi-exclamation-circle");
		$("#ucase").removeClass("bi-exclamation-circle");
		$("#lcase").removeClass("bi-exclamation-circle");
		$("#num").removeClass("bi-exclamation-circle");
		bOk1 = false;
	}
	
	if ($("#password1").val() != "" || $("#password2").val() != "") {
		if($("#password1").val() == $("#password2").val()){
			$("#pwmatch").removeClass("bi-exclamation-circle");
			$("#pwmatch").addClass("bi-check-circle");
			$("#pwmatch").css("color","#00A41E");
		}else{
			$("#pwmatch").removeClass("bi-check-circle");
			$("#pwmatch").addClass("bi-exclamation-circle");
			$("#pwmatch").css("color","#FF0004");
			bOk2 = false;
		}
	} else {
		$("#pwmatch").removeClass("bi-exclamation-circle");
		bOk2 = false;
	}

    if (bOk1 && bOk2) {
        $("#passwordsok").val('ok');
    }
    else {
        $("#passwordsok").val('');
    }
});
