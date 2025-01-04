//A basic message
function sweetAlert(sText) {
	Swal.fire(
		{
			text: sText,
			showClass: { popup: 'animate__animated animate__fadeInUp animate__faster' },
			hideClass: { popup: 'animate__animated animate__fadeOutDown animate__faster' }
		}
	);
}
function sweetAlert2(sTitle, sText, sIcon) {
	Swal.fire(
		{
			title: sTitle,
			html: sText,
			icon: sIcon,
			customClass: {
				popup: 'my-swal'
			},
			showClass: { popup: 'animate__animated animate__fadeInUp animate__faster' },
			hideClass: { popup: 'animate__animated animate__fadeOutDown animate__faster' }
		}
	);
}

function sweetAlertRedirect(sTitle, sText, sIcon, sURL) {
	Swal.fire(
		{
			title: sTitle,
			text: sText,
			icon: sIcon,
			showClass: { popup: 'animate__animated animate__fadeInUp animate__faster' },
			hideClass: { popup: 'animate__animated animate__fadeOutDown animate__faster' }
		}
	).then(function () {
		window.location = sURL;
	});
}

function sweetConfirm(sTitle, sText, sIcon, sConfirmButtonText, sSuccessMsg, sElementId) {
	Swal.fire({
		title: sTitle,
		html: sText,
		icon: sIcon,
		showCancelButton: true,
		confirmButtonText: sConfirmButtonText,
		cancelButtonText: 'Cancelar',
		showClass: { popup: 'animate__animated animate__fadeInUp animate__faster' },
		hideClass: { popup: 'animate__animated animate__fadeOutDown animate__faster' }
	}).then(function (result) {
		if (result.value) {
			//setTimeout(function () {
			//	Swal.fire(sTitle, sSuccessMsg, "success");
			//},3000);
			document.getElementById(sElementId).click();
		}
	});

}
