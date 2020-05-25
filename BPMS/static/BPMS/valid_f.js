
			function check()
			{
				var pass = document.getElementById('pwd_original').value;
				var c_pass = document.getElementById('pwd_retype').value;
				//alert (pass)
				if (pass != c_pass){
					document.getElementById('pwd_conf').className = "form-group is-invalid";
					document.getElementById('pwd_conf').style.color = "#a94442"
					document.getElementById('btns1').disabled = true;
					document.getElementById('btns2').disabled = true;
					document.getElementById('pwd_error').style.visibility = "visible"
				}
				else {
					document.getElementById('pwd_conf').className = "form-group is-valid";
					document.getElementById('pwd_error').style.visibility = "hidden"
					document.getElementById('pwd_conf').style.color = "#777"
					validate_check();
				}
			}
			function validate_check()
			{
				var f1 = document.getElementById('name').value;
				var f2 = document.getElementById('address').value;
				var f3 = document.getElementById('email').value;
				var f4 = document.getElementById('telephone').value;
				var f5 = document.getElementById('contact_person').value;
				var f6 = document.getElementById('con_person_telephone').value;
				var f7 = document.getElementById('username').value;
				var f8 = document.getElementById('Designation').value
				var pass = document.getElementById('pwd_original').value;
				var c_pass = document.getElementById('pwd_retype').value;

				if (pass=="" || c_pass=="" || f1=="" || f2=="" || f3=="" || f4=="" || f5=="" || f6=="" || f7=="" || f8==""){
					document.getElementById('btns1').disabled = true;
					document.getElementById('btns2').disabled = true;
				}
				else {
					document.getElementById('btns1').disabled = false;
					document.getElementById('btns2').disabled = false;
				}
			}
