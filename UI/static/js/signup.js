let email = document.getElementById("email_address");
let first_name = document.getElementById("first_name");
let last_name = document.getElementById("last_name");
let password = document.getElementById("password");
let confirm_password = document.getElementById("confirm");

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

function password_two_validation() {
    let password_two_error = document.getElementById("password_two_error");
    if (password.value !== confirm_password.value){
        password_two_error.style.display = "block";
        password_two_error.innerHTML = "Passwords don't match!";
        confirm_password.setCustomValidity("Inconsistent Password.");
    }
    else {
        password_two_error.style.display = "none";
        confirm_password.setCustomValidity("");
    }

}
confirm_password.onblur = password_two_validation;
confirm_password.onkeyup = password_two_validation;

first_name.onkeyup = function name_validation() {
    let first_name_error = document.getElementById("first_name_error");
    if (/^[a-zA-Z]{2,}$/.test(first_name.value)) {
        first_name_error.style.display = "none";
        first_name.setCustomValidity("");
    } else {
        first_name_error.style.display = "block";
        first_name_error.innerHTML = "Name must be more than one letter and only alphabets";
        first_name.setCustomValidity("Invalid Name.");
    }
}

last_name.onkeyup = function names_validation() {
    let last_name_error = document.getElementById("last_name_error");
    if (/^[a-zA-Z]{2,}$/.test(last_name.value)) {
        last_name_error.style.display = "none";
        last_name.setCustomValidity("");
    } else {
        last_name_error.style.display = "block";
        last_name_error.innerHTML = "Name must be more than one letter and only alphabets";
        last_name.setCustomValidity("Invalid Name.");
    }
}

function signup_user() {
    let url = "https://epicmail-sentongo-v2.herokuapp.com/api/v2/auth/signup";
    let new_user = {
        first_name: first_name.value,
        last_name: last_name.value,
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
            if (data.status === 400) {
                document.getElementById("page_response").style.display = "block";
                document.getElementById("page_response").innerHTML = data.error;
            }
            else if (data.status === 201) {
                document.getElementById("page_response").style.display = "block";
                document.getElementById("page_response").innerHTML = "Signed up Successfuly";
                token=data.data[0]['token'];
                localStorage.setItem('token', token);
                console.log(token);
                window.location.replace("./inbox.html");
            }

        })
}