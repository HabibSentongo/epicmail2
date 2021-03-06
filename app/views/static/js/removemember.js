let user_id = document.getElementById("user_id");
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

group_id.onkeyup = function group_id_validation() {
    let uid_error = document.getElementById("uid_error");
    if (/^[0-9]{1,}$/.test(group_id.value)) {
        uid_error.style.display = "none";
        user_id.setCustomValidity("");
        url = "./api/v2/groups/"+group_id.value+"/users/"+user_id.value;
        console.log(url)
    } else {
        uid_error.style.display = "block";
        uid_error.style.color = "red";
        uid_error.innerHTML = "User ID must be an integer";
        user_id.setCustomValidity("Invalid User ID.");
    }
}

function remove_member() {
    fetch(url, {
        method: "DELETE",
        headers: {
            "content-type": "application/json",
            "Authorization": `Bearer ${token}`
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === 200) {
                document.getElementById("page_response").style.display = "block";
                document.getElementById("page_response").style.color = "green";
                document.getElementById("page_response").innerHTML = "User Removed";
                window.location.replace("./mygroups.html");
            }
            else if (data.status === 400) {
                document.getElementById("page_response").style.display = "block";
                document.getElementById("page_response").style.color = "red";
                document.getElementById("page_response").innerHTML = data.error;
                ;
            }
            else if (data.status === 401) {
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