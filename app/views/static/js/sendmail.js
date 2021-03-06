let email = document.getElementById("to");
let subject = document.getElementById("subject");
let mailbody = document.getElementById("body");
let token = localStorage.getItem('token');
console.log(token);

function logout() {
    localStorage.removeItem('token');
    window.location.replace("./index.html");
}
window.onload = function not_signedin(){
    if(token === null){
        window.location.replace("./index.html");
    }
}

email.onkeyup = function email_validation(){
    let email_error = document.getElementById("email_error");
    if (/\S+@\S+\.\S+/.test(email.value)){
        email_error.style.display = "none";
        email.setCustomValidity("");
    }
    else {
        email_error.style.display = "block";
        email_error.style.color = "red";
        email_error.innerHTML = "Enter correct email";
        email.setCustomValidity("Wrong Email Format.")
    }
}

function send_mail() {
    let url = "./api/v2/messages";
    let new_mail = {
        subject: subject.value,
        parent_message_id: 0,
        sender_status: "sent",
        reciever_email: email.value,
        message_details: mailbody.value
    };

    fetch(url, {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(new_mail)
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === 201) {
                document.getElementById("page_response").style.display = "block";
                document.getElementById("page_response").style.color = "green";
                document.getElementById("page_response").innerHTML = "Message Sent";
                window.location.replace("./sent.html");
            }
            else if (data.status === 404) {
                document.getElementById("page_response").style.display = "block";
                document.getElementById("page_response").style.color = "red";
                document.getElementById("page_response").innerHTML = "Unregistered Recipient";
                email.setCustomValidity("Unregistered Recipient.");
            }
            else if (data.status === 400) {
                document.getElementById("page_response").style.display = "block";
                document.getElementById("page_response").style.color = "red";
                document.getElementById("page_response").innerHTML = data.error;
                ;
            }
            else if (data.msg === "Token has expired") {
                window.location.replace("./index.html");
            }
        })
}