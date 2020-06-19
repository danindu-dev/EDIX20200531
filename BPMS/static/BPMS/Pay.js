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
function ckeck_rcd(){
    setInputFilter(document.getElementById('received_amount'), function(value) {return /^-?\d*[.,]?\d*$/.test(value); });
    if ((parseFloat(document.getElementById("g_total").innerHTML) < parseFloat(document.getElementById("received_amount").value))){
        document.getElementById("received_amount").value = document.getElementById("g_total").innerHTML;
    }
}
function settle_invo(submitconfm){
	if (submitconfm == true) {
		document.getElementById('status_s').value="CLOSE"
			if ((parseFloat(document.getElementById("g_total").innerHTML) != parseFloat(document.getElementById("received_amount").value)) && (parseFloat(document.getElementById("received_amount").value) != 0)){
				alert("You haven't recieved the total invoice amount. Invoice will keep as a open invoice.");
			}
			if (document.getElementById("pay_type").value == "bank" && document.getElementById("che_num").value == ""){
				document.getElementById("che_num").focus();
			}

			if (parseFloat(document.getElementById("received_amount").value ) != 0){
			    document.getElementById('payfrm').submit();
			}
			else{
				alert("Received amount cannot be 0.00");
			}
			
		
	}
	
}



function setInputFilter(textbox, inputFilter) {
  ["input", "keydown", "keyup", "mousedown", "mouseup", "select", "contextmenu", "drop"].forEach(function(event) {
    textbox.addEventListener(event, function() {
      if (inputFilter(this.value)) {
        this.oldValue = this.value;
        this.oldSelectionStart = this.selectionStart;
        this.oldSelectionEnd = this.selectionEnd;
      } else if (this.hasOwnProperty("oldValue")) {
        this.value = this.oldValue;
        this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
      } else {
        this.value = "";
      }
    });
  });
}




