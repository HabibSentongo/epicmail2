let email = document.getElementById("email");

function email_validation(){
    let email_error = document.getElementById("email_error");
    if (/\S+@\S+\.\S+/.test(email.value)){
        email_error.style.display = "none";
        email.setCustomValidity("")
    }
    else {
        email_error.style.display = "block";
        email_error.innerHTML = "Enter correct email";
        email.setCustomValidity("Wrong Email Format.")
    }
}
email.onkeyup = email_validation;
email.onchange = email_validation;

function password_validation() {
    let password_error = document.getElementById("password_error");
    if (/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/.test(password.value)) {
        password_error.style.display = "none";
        password.setCustomValidity("");
    }
    else {
        password_error.style.display = "block";
        password_error.innerHTML = "Password Must have above 7 characters,\
         at least one uppercase letter, lowercase letter and number.";
        password.setCustomValidity("Password is weak.");
    }
}
password.onkeyup = password_validation;
password.onchange = password_validation;

function signin_user() {
    let url = "https://epicmail-sentongo-v2.herokuapp.com/api/v2/auth/signin";
    let new_user = {
        email_address: email.value,
        password: password.value,
    };

    fetch(url, {
        method: "POST",
        headers: {
            "content-type": "application/json",
        },
        body: JSON.stringify(new_user)
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === 404) {
                document.getElementById("page_response").style.display = "block";
                document.getElementById("page_response").innerHTML = data.error;
            }
            else if (data.status === 200) {
                document.getElementById("page_response").style.display = "block";
                document.getElementById("page_response").innerHTML = "Logged in Successfuly";
                window.location.replace("./inbox.html");
            }

        })
}