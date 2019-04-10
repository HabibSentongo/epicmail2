let email = document.getElementById("user_email");
let group_id = document.getElementById("group_id");
let token = localStorage.getItem('token');
console.log(token);
let url = "";

function logout() {
    localStorage.removeItem('token');
    window.location.replace("./index.html");
}
window.onload = function not_signedin(){
    if(token === null){
        window.location.replace("./index.html");
    }
}

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

group_id.onkeyup = function group_id_validation() {
    let email_error = document.getElementById("gid_error");
    if (/^[0-9]{1,}$/.test(group_id.value)) {
        email_error.style.display = "none";
        group_id.setCustomValidity("");
        url = "https://epicmail-sentongo-v2.herokuapp.com/api/v2/groups/"+group_id.value+"/users";
        console.log(url)
    } else {
        email_error.style.display = "block";
        email_error.style.color = "red";
        email_error.innerHTML = "Group ID must be an integer";
        group_id.setCustomValidity("Invalid Group ID.");
    }
}

function add_member() {
    let user = {
        user_email: email.value
    };

    fetch(url, {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(user)
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === 200) {
                document.getElementById("page_response").style.display = "block";
                document.getElementById("page_response").style.color = "green";
                document.getElementById("page_response").innerHTML = "User Added";
                window.location.replace("./mygroups.html");
            }
            else if (data.status === 400) {
                document.getElementById("page_response").style.display = "block";
                document.getElementById("page_response").style.color = "red";
                document.getElementById("page_response").innerHTML = data.data[0]['message'];
                ;
            }
            else if (data.status === 401) {
                document.getElementById("page_response").style.display = "block";
                document.getElementById("page_response").style.color = "red";
                document.getElementById("page_response").innerHTML = data.error;
                ;
            }
            else if (data.status === 404) {
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