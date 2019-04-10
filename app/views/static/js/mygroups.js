let token = localStorage.getItem("token");

function logout() {
    localStorage.removeItem('token');
    window.location.replace("./index.html");
}
window.onload = function not_signedin(){
    if(token === null){
        window.location.replace("./index.html");
    }
}

function get_groups() {
    let url = "https://epicmail-sentongo-v2.herokuapp.com/api/v2/groups";
    let fetched = '';
    fetch(url, {
        method: "GET",
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
    })
        .then((response) => response.json())
        .then((data) => {
            console.log('test')
            if (data.msg === "Token has expired") {
                window.location.replace("./index.html");
            }
            console.log(data.status);
            console.log(data.error);
            if(data) {
                console.log(data)
                if(data.status === 200){
                    let groups = data["data"];
                    console.log(groups)
                    groups.forEach(group => {
                        id_dots="dots"+group.group_id;
                        id_body="msg"+group.group_id;
                    fetched +=`
                    <div class="email" onclick="mailDetails('${id_dots}','${id_body}')">
                    <p class="topic">Name: ${group.group_name} <span id='${id_dots}'>.....</span></p>
                    <p id='${id_body}' style="display: none">Members: ${group.members}<br>Group ID: ${group.group_id}<br><br></p>
                    </div>
                    `
                    })
                    }
                if(data.status === 404){
                    fetched +=`   
                    <div class="email">
                    <p class="topic">You Are Not in any Groups Yet!!<br><br></p>
                    </div>
                    `;
                    }
                    }
            document.getElementById('mailist').innerHTML = fetched;
        })
        .catch((error) => console.log(error));
}
get_groups()