let name = document.getElementById("new_name");
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

name.onkeyup = function name_validation() {
    let name_error = document.getElementById("name_error");
    if (/^[a-zA-Z]{2,}$/.test(name.value)) {
        name_error.style.display = "none";
        name.setCustomValidity("");
    } else {
        name_error.style.display = "block";
        name_error.style.color = "red";
        name_error.innerHTML = "Name must be more than one letter and only alphabets";
        name.setCustomValidity("Invalid Name.");
    }
}

group_id.onkeyup = function group_id_validation() {
    let email_error = document.getElementById("gid_error");
    if (/^[0-9]{1,}$/.test(group_id.value)) {
        email_error.style.display = "none";
        group_id.setCustomValidity("");
        url = "https://epicmail-sentongo-v2.herokuapp.com/api/v2/groups/"+group_id.value+"/name";
        console.log(url)
    } else {
        email_error.style.display = "block";
        email_error.style.color = "red";
        email_error.innerHTML = "Group ID must be an integer";
        group_id.setCustomValidity("Invalid Group ID.");
    }
}

function rename() {
    let group = {
        new_name: name.value
    };

    fetch(url, {
        method: "PATCH",
        headers: {
            "content-type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(group)
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === 200) {
                document.getElementById("page_response").style.display = "block";
                document.getElementById("page_response").style.color = "green";
                document.getElementById("page_response").innerHTML = "Group Renamed";
                window.location.replace("./mygroups.html");
            }
            else if (data.status === 401) {
                document.getElementById("page_response").style.display = "block";
                document.getElementById("page_response").style.color = "red";
                document.getElementById("page_response").innerHTML = data.error;
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