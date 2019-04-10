let email = document.getElementById("email");

function email_validation(){
    let email_error = document.getElementById("email_error");
    if (/\S+@\S+\.\S+/.test(email.value)){
        email_error.style.display = "none";
        email.setCustomValidity("")
    }
    else {
        email_error.style.display = "block";
        email_error.style.color = "red";
        email_error.innerHTML = "Enter correct email";
        email.setCustomValidity("Wrong Email Format.")
    }
}
email.onkeyup = email_validation;
email.onchange = email_validation;

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
                document.getElementById("page_response").style.color = "red";
                document.getElementById("page_response").innerHTML = data.error;
            }
            else if (data.status === 200) {
                document.getElementById("page_response").style.display = "block";
                document.getElementById("page_response").style.color = "green";
                document.getElementById("page_response").innerHTML = "Logged in Successfuly";
                token=data.data[0]['token'];
                localStorage.setItem('token', token);
                console.log(token);
                window.location.replace("./inbox.html");
            }
        })
}