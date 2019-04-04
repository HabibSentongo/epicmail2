let name = document.getElementById("gname");
let token = localStorage.getItem('token')
console.log(token);

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

function create_group() {
    let url = "https://epicmail-sentongo-v2.herokuapp.com/api/v2/groups";
    let new_group = {
        group_name: name.value
    };

    fetch(url, {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(new_group)
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === 201) {
                document.getElementById("page_response").style.display = "block";
                document.getElementById("page_response").style.color = "green";
                document.getElementById("page_response").innerHTML = "Group Created";
                window.location.replace("./inbox.html");
            }
            else if (data.status === 400) {
                document.getElementById("page_response").style.display = "block";
                document.getElementById("page_response").style.color = "red";
                document.getElementById("page_response").innerHTML = data.error;
            }
            else if (data.msg === "Token has expired") {
                window.location.replace("./index.html");
            }

        })
}