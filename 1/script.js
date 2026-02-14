const title = document.getElementById("title");
const statusDisplay = document.getElementById("status-display");
const progress = document.getElementById("progress-fill");
const code = document.getElementById("code-input");
const lBtn = document.getElementById("launch-btn");
const rBtn = document.getElementById("reset-btn");

let attempts=2;


lBtn.onclick = function() {
    let data = code.value;
    if (data === "1234") {
        statusDisplay.innerText = "Online";
        statusDisplay.style.color = "green";
        progress.style.width = "100%";
    } else {
        statusDisplay.innerText = "Access error";
        statusDisplay.style.color = "red";
        if (attempts>0)
        {
            attempts--;
        } else {
            lBtn.style.backgroundColor = "gray";
            lBtn.disabled = true;
        }
    }

}
rBtn.onclick = function() {
    
}
