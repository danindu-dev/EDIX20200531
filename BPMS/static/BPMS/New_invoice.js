var count = 1;
var item_list = new Array();
var amount_list = new Array();
var tax_list = new Array();
var tax_name=document.getElementById('tax_name').value
var tax_amount=document.getElementById('tax_amount').value

function additem() {
  var taxdefault="";
  var tax_status="not"
  if (document.getElementById('tax_defaul').value != ""){
	  taxdefault="selected"
	  tax_status="add"
  }
  var tableRef = document.getElementById('invoice_table').getElementsByTagName('tbody')[0];

  var newRow = tableRef.insertRow(tableRef.rows.length);

  var newCell0 = newRow.insertCell(0);
  var newCell1 = newRow.insertCell(1);
  var newCell2 = newRow.insertCell(2);
  
  
  newCell0.id = "no_" + count
  newCell1.id = "item_" + count
  newCell2.id = "amount_" + count
  
  document.getElementById('no_' + count).innerHTML = count;
  
  
  document.getElementById('item_' + count).innerHTML = "<input type='text' class='form-control' id='item_input_" + count + "' oninput='item_input(" + count + ")' >";
  document.getElementById('amount_' + count).innerHTML = "<input type='text' class='form-control' id='amount_input_" + count + "' oninput='amount_input(" + count + ")'><lable for='amount_tax_input_" + count + "'><strong>Tax</strong></lable><select class='form-control' id='amount_tax_input_" + count + "' oninput='tax_cal("+ count +")'> <option value='0'>"+tax_name+" 0%</option> <option value='"+tax_amount+"' "+taxdefault+">"+tax_name+" "+tax_amount+"%</option></select> ";
  document.getElementById('amount_input_' + count).value= "0.00";
  
	item_list[(count-1)]="";
  amount_list[(count-1)]="";
  tax_cal[(count-1)]=tax_status;
  item_input(count);
  amount_input(count);
  tax_cal(count);
  count++;
}

function item_input(item_id) {
	item_list[(item_id-1)]=document.getElementById('item_input_'+item_id).value;
	calc();
  textareaupdate();
}

function amount_input(amount_id) {
	amount_list[(amount_id-1)]=parseFloat(document.getElementById('amount_input_'+amount_id).value).toFixed(2);
 
   setInputFilter(document.getElementById('amount_input_'+amount_id), function(value) {return /^-?\d*[.,]?\d*$/.test(value);}); 
   if (document.getElementById('amount_input_'+amount_id).value == ""){
		document.getElementById('amount_input_'+amount_id).value = 0;
	}
	calc();
   textareaupdate();
}
function tax_cal(tax_id) {
	tax_stat=document.getElementById('amount_tax_input_'+tax_id).value;
	if (tax_stat==tax_amount){
  	tax_list[(tax_id-1)]="add"
  }
  else{
  	tax_list[(tax_id-1)]="not"
  }
  calc();
  textareaupdate()
}

function textareaupdate(){
  for (textupdate="",arraycount = 0, len = item_list.length; arraycount < len; arraycount++) {
  textupdate += item_list[arraycount] + "?";
  document.getElementById('alltext').innerHTML = textupdate;
}

for (numupdate="",arraycount = 0, len = amount_list.length; arraycount < len; arraycount++) {
  numupdate += amount_list[arraycount] + "?";
  document.getElementById('allnum').innerHTML = numupdate;
}

for (taxupdate="",arraycount = 0, len = tax_list.length; arraycount < len; arraycount++) {
  taxupdate += tax_list[arraycount] + "?";
  document.getElementById('alltax').innerHTML = taxupdate;
}

}

function cid1(){
	document.getElementById("cidlong").value=document.getElementById("cidshort").value;
}
function cid2(){
	document.getElementById("cidshort").value=document.getElementById("cidlong").value;
}

// Restricts input for the given textbox to the given inputFilter.

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

function calc(){
	var tax_sum = 0;
	var amount_sum = 0;
	var deduction  = parseFloat(document.getElementById('deduction').value);
	
	
	for (numupdate=0 ,arraycount = 0, len = amount_list.length; arraycount < len; arraycount++) {
		amount_sum += parseFloat(amount_list[arraycount]);
	  if (tax_list[arraycount]=="add"){
		  tax_sum += parseFloat(amount_list[arraycount])*[parseFloat(tax_amount)*0.01];
	  }
	}
	var net_total = amount_sum - deduction
	var g_total = net_total+tax_sum;
	document.getElementById('total').innerHTML = amount_sum.toFixed(2);
	document.getElementById('alltotal').innerHTML = net_total.toFixed(2);
	document.getElementById('tax_sum').innerHTML = tax_sum.toFixed(2);
	document.getElementById('grand_total').innerHTML = g_total.toFixed(2);
	document.getElementById("g_total_to_submit").value = g_total.toFixed(2);
}

function deductionaction(){
	if (document.getElementById('deduction').value == ""){
		document.getElementById('deduction').value = 0;
	}
	var deductioncheck  = parseFloat(document.getElementById('deduction').value);
	
	document.getElementById("deductiontd").innerHTML=(-1*deductioncheck).toFixed(2);
	if (deductioncheck == 0){
		document.getElementById('hdtr1').style.visibility="collapse";
		document.getElementById('hdtr2').style.visibility="collapse";	
	}
	else{
		document.getElementById('hdtr1').style.visibility="visible";
		document.getElementById('hdtr2').style.visibility="visible";
	}
	calc();
}
function submitconfirm(submitconf){
	if (submitconf == true) {
		document.getElementById('invoice_data').submit();
	}	
}

// Install input filters.


  setInputFilter(document.getElementById("deduction"), function(value) {
  return /^-?\d*[.,]?\d*$/.test(value); }); 

function loaditems(){
    var itemstring = document.getElementById('alltext').innerHTML;
    var amountstring = document.getElementById('allnum').innerHTML;
    var taxstring = document.getElementById('alltax').innerHTML;
    var itemlist = itemstring.split("?");
    var item_list_temp = itemlist.filter(Boolean);
    var amountlist = amountstring.split("?");
    var amount_list_temp = amountlist.filter(Boolean);
    var taxlist = taxstring.split("?");
    var tax_list_temp = taxlist.filter(Boolean);

    for (row_count = 1,row_num = item_list_temp.length+1;row_count < row_num; row_count++){
        additem()
        document.getElementById('item_input_'+(row_count)).value=item_list_temp[row_count-1];
        document.getElementById('amount_input_'+(row_count)).value=parseFloat(amount_list_temp[row_count-1]).toFixed(2);
        if (tax_list_temp[row_count-1] == "add"){
            document.getElementById('amount_tax_input_'+(row_count)).value= tax_amount;
        }
        else{
            document.getElementById('amount_tax_input_'+(row_count)).value= 0;
        }
        item_input(row_count);
        amount_input(row_count);
        tax_cal(row_count);
        deductionaction()
    }

    /*for (textupdate="",arraycount = 0, len = item_list.length; arraycount < len; arraycount++) {
      textupdate += item_list[arraycount] + "?";
      document.getElementById('alltext').innerHTML = textupdate;
    }*/
}
