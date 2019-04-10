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
function get_recieved() {
    let url = "./api/v2/messages";
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
                    let mails = data["data"];
                    console.log(mails)
                    mails.forEach(mail => {
                        id_dots="dots"+mail.mail_id;
                        id_body="msg"+mail.mail_id;
                    fetched +=`
                    <div class="email" onclick="mailDetails('${id_dots}','${id_body}')">
                    <p class="topic">${mail.subject} <span id='${id_dots}'>.....</span></p>
                    <p id='${id_body}' style="display: none">${mail.message_details}<br><br></p>
                    <a href="new.html"><button class="inBtn">Reply</button></a><a href="new.html"><button class="inBtn">Foward</button></a>
                    </div>
                    `
                    })
                    }
                if(data.status === 404){
                    fetched +=`   
                    <div class="email">
                    <p class="topic">You Have Not Recieved any Emails Yet!!<br><br></p>
                    </div>
                    `;
                    }
                    }
            document.getElementById('mailist').innerHTML = fetched;
        })
}
get_recieved()