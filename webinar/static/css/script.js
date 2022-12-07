
var attempt = 3; // Variable to count number of attempts.
// Below function Executes on click of login button.
function validate(){
var username = document.getElementById("user").value;
var password = document.getElementById("cont").value;

if ( username == "feria" && password == "12"){
    alert ("Usuario autenticado!");
    window.location = "{% url 'iniciointerno' %}"; // Redirecting to other page.
    return false;
    }
    else if ( username == "trans" && password == "1"){
        alert ("Usuario autenticado!");
        window.location = "{% url 'iniciotransportista' %}"; // Redirecting to other page.
        return false;
        }
        else if ( username == "pro" && password == "2"){
            alert ("Usuario autenticado!");
            window.location = "{% url 'inicioproveedor' %}"; // Redirecting to other page.
            return false;
            }else{
    
    }
}



function confirmar(){
if (confirm('Estas seguro que quieres pujar ese monto?')) {
    // Save it!
    <a href="ListadoSubastasIng.html">Subastas</a>;
  } else {
    // Do nothing!
    console.log('Thing was not saved to the database.');
  }
}