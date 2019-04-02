let email = document.getElementById("to");
let subject = document.getElementById("subject");
let body = document.getElementById("body");
let send = document.getElementById("send");
let token = localStorage.getItem('token')
console.log(token);

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

function send_mail() {
    let url = "https://epicmail-sentongo-v2.herokuapp.com/api/v2/messages";
    let new_mail = {
        subject: subject.value,
        parent_message_id: 0,
        sender_status: "sent",
        reciever_id: email.value,
        message_details: subject.value
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
                document.getElementById("page_response").innerHTML = "Message Sent";
                window.location.replace("./inbox.html");
            }

        })
}