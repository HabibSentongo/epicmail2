let group_id = document.getElementById("to");
let subject = document.getElementById("subject");
let mailbody = document.getElementById("mailbody");
let token = localStorage.getItem('token');
let url = "";
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

group_id.onkeyup = function group_id_validation() {
    let email_error = document.getElementById("email_error");
    if (/^[0-9]{1,}$/.test(group_id.value)) {
        email_error.style.display = "none";
        group_id.setCustomValidity("");
        url = "./api/v2/groups/"+group_id.value+"/messages";
        console.log(url);
    } else {
        email_error.style.display = "block";
        email_error.style.color = "red";
        email_error.innerHTML = "Group ID must be an integer";
        group_id.setCustomValidity("Invalid Group ID.");
    }
}

function send_group_mail() {
    let new_mail = {
        subject: subject.value,
        parent_message_id: 0,
        sender_status: "sent",
        reciever_id: group_id.value,
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
                document.getElementById("page_response").innerHTML = "Group Doesn't Exist";
                email.setCustomValidity("Unregistered Recipient.");
            }
            else if (data.status === 401) {
                document.getElementById("page_response").style.display = "block";
                document.getElementById("page_response").style.color = "red";
                document.getElementById("page_response").innerHTML = "You are not a member of this group";
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