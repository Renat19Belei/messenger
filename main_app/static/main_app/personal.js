// let profileCard = document.querySelector("")  
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
                    img.src = img.src.split('eye').join('eye_on')
                } else {
                    passw.type = 'password';
                    img.src = img.src.split('eye_on').join('eye')
                }
            })
            but.append(img)
            p.className = "password-p"
            p.append(but)
        }
    }
}
let canvas = document.querySelector('canvas')
canvas.style.padding = 0
let draw = canvas.getContext('2d')
draw.fillStyle = 'black'
let drawing = false

function coor(event){
    let rect = canvas.getBoundingClientRect()
    return [(event.clientX-rect.left+0.1)*canvas.width / rect.width,(event.clientY-rect.top+7)*canvas.height / rect.height]
}
canvas.addEventListener('mousedown', (event) => {
    pastplace = coor(event)
    drawing = true
})
document.addEventListener('mouseup',()=> {
    drawing = false
})
let pastplace = []
canvas.addEventListener('mousemove',(event)=>{
    if (drawing){
        draw.beginPath();
        draw.moveTo(pastplace[0], pastplace[1]);
        pastplace = coor(event)
        draw.lineTo(pastplace[0], pastplace[1]);
        draw.stroke();
    }
})