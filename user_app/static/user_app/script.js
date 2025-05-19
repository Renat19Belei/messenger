let eyeUrl = document.querySelector("#eyeUrl")
let passwords = document.querySelectorAll(".password")
let ps = document.querySelectorAll("p")
// eyeUrl.value
if (passwords.length == 0){
    passwords  = document.querySelectorAll("#id_password")
}
for (let p of ps){
    for (let passw of passwords){
        // id_password
        if (p.contains(passw)){
            let but = document.createElement("button")
            but.className = "view-password-but"
            but.type = "button"
            let img = document.createElement("img")
            // document.createElement("p").contains
            img.className = "view-password-img"
            img.src = eyeUrl.value
            but.addEventListener("click", ()=>{
                
                if (passw.type == 'password') {
                    passw.type = "text"
                } else {
                    passw.type = 'password';
                }
            })
            but.append(img)
            p.className = "password-p"
            p.append(but)
        }
    }
}

// textElement.textContent = "•".repeat(textElement.dataset.originalText.length);
// button.id = 'close'