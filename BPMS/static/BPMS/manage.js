function item_update(submitconfm){
	if (submitconfm == true) {
		document.getElementById('todo').value="update";
		document.getElementById('itemfrm').submit();
	}
}
function item_add(submitconfm){
	if (submitconfm == true) {
		document.getElementById('todo').value="add";
		document.getElementById('itemfrm').submit();
	}
}
function item_delete(submitconfm){
	if (submitconfm == true) {
		document.getElementById('todo').value="delete";
		document.getElementById('itemfrm').submit();
	}
}