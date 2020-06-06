function pay_ty (){
	var pay_t = document.getElementById("pay_type").value;
	if (pay_t == "bank"){
		document.getElementById("che_num").disabled=false;
		document.getElementById("bank").value=document.getElementById("pay_type").options[document.getElementById("pay_type").selectedIndex].innerHTML;
		document.getElementById("che_num").required = true;
	}
	if (pay_t == "cash"){
		document.getElementById("che_num").disabled=true;
		document.getElementById("bank").value=document.getElementById("pay_type").options[document.getElementById("pay_type").selectedIndex].innerHTML;
		document.getElementById("che_num").value = "";
		document.getElementById("che_num").required = false;
	}
}
function cancl_invo(submitconfm){
	if (submitconfm == true) {
		document.getElementById('status_s').value="CANCEL";
		document.getElementById('payfrm').submit();
	}
	
}
function rvk_invo(submitconfm){
	if (submitconfm == true) {
		document.getElementById('status_s').value="REVOKE";
		document.getElementById('payfrm').submit();
	}
	
}
function settle_invo(submitconfm){
	if (submitconfm == true) {
		document.getElementById('status_s').value="CLOSE"
			if (parseFloat(document.getElementById("g_total").innerHTML) != parseFloat(document.getElementById("received_amount").value)){
				alert("You haven't recieved the total invoice amount. Invoice will keep as a open invoice.");
			}
			if (document.getElementById("pay_type").value == "bank" && document.getElementById("che_num").value == ""){
				document.getElementById("che_num").focus();
			}
			else{
				document.getElementById('payfrm').submit();
			}
			
		
	}
	
}