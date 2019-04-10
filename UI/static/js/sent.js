function get_sent() {
    let url = "https://epicmail-sentongo-v2.herokuapp.com/api/v2/messages/sent";
    let token = localStorage.getItem("token");
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
                    fetched +=`
                   <div class="email" onclick="mailDetails()">
                    <p class="topic">${mail.subject} <span id="dots">.....</span></p>
                    <p id="msg">${mail.message_details}<br><br></p>
                    <a href="sent.html"><button class="inBtn">Retract</button></a><a href="new.html"><button class="inBtn">Foward</button></a>
                    </div>
                    `
                    })
                    }
                if(data.status === 404){
                    fetched +=`   
                    <div class="email">
                    <p class="topic">You Have Not Sent any Emails Yet!!<br><br></p>
                    </div>
                    `;
                    }
                    }
            document.getElementById('mailist').innerHTML = fetched;
        })
        .catch((error) => console.log(error));
}
get_sent()