function mailDetails() {
    var dots = document.getElementById("dots");
    var msgContent = document.getElementById("msg");
  
    if (dots.style.display === "none") {
      dots.style.display = "inline";
      msgContent.style.display = "none";
    } else {
      dots.style.display = "none";
      msgContent.style.display = "inline";
    }
  }