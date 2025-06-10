$(document).ready(function(){
// let profileCard = document.querySelector("")  
let eyeUrl = document.querySelector("#eyeUrl")
let passwords = document.querySelectorAll(".password")
let ps = document.querySelectorAll("p")
let mark = document.querySelector("#mark")
// reader.onload = (loadEvent) =>{
//     mark.addEventListener("change", (event)=>{
//     const files = event.target.files
//     let count = 0
//     if (files.length > 0){
//         for (let file of files){
//             // reader.
//             readers[count].readAsDataURL(file)
//             count++
//         }
//     }
// }
//     )
// function toggleEdit() {
//   const view = document.getElementById("view-mode");
//   const edit = document.getElementById("edit-mode");

//   if (view.style.display === "none") {
//     view.style.display = "block";
//     edit.style.display = "none";
//   } else {
//     view.style.display = "none";
//     edit.style.display = "block";
//   }
// }
// eyeUrl.value
if (passwords.length == 0){
    passwords  = document.querySelectorAll("#id_password")
}
for (let p of ps){
    for (let passw of passwords){
        passw.requered = false
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
// edit-img
let info = document.querySelector('#info')
let inputs = document.querySelectorAll('.FormInput') 
let editImg = document.querySelector('.edit-img')
info.addEventListener('click',()=>{
    let info = document.querySelector('#info')
    let inputs = document.querySelectorAll('.FormInput') 
    console.log(editImg)
    if (info.classList.contains('active')){
        info.classList.remove('active')
        for (let input of inputs){
            input.requered = false
            input.readOnly = true
            input.classList.add('gray-input')
        }
            // fetch(document.querySelector('#personalUrl').value,{
            //     method: 'POST',
            //     headers: {
            //         'Content-Type': 'application/json',
            //         'X-CSRFToken': csrfToken
            //     },

            // })
            // DateInput
            $.ajax({
            type: 'post',
            url: document.querySelector('#personalUrl').value,
            data: {

                csrfmiddlewaretoken:document.querySelector('input').value,
                first_name: document.querySelector('[name="first_name"]').value,
                last_name: document.querySelector('[name="last_name"]').value,
                email: document.querySelector('[name="email"]').value,
                date_of_birthday: document.querySelector('[name="date_of_birthday"]').value

            },
            success:function(request){
                console.log('ok')
            }})
        
        

        info.textContent = ''
        info.append(editImg)
        info.innerHTML += `Редагувати інформацію`

    }else{
        info.classList.add('active')
        for (let input of inputs){
            console.log(!input.classList.contains('password'),input)
            if (!input.classList.contains('password')){
                input.requered = true
                input.readOnly = false
                input.classList.remove('gray-input')
            }
        }
        info.textContent = ''
        info.append(editImg)
        info.innerHTML += `Зберегти`
    }
})
let editImg2 = document.querySelector('.edit-avatar')
// avatar-div content-hidden
let contAvatar = document.querySelector('.avatar-div')
let editContAvatar = document.querySelector('.content-hidden')
let avatar = document.querySelector('#avatar')
avatar.addEventListener('click',()=>{
    if (!avatar.classList.contains('active')){
        avatar.textContent = ''
        avatar.append(editImg2)
        avatar.innerHTML += `Зберегти`
        avatar.classList.add('active')
        contAvatar.classList.add('hidden')
        editContAvatar.classList.remove('hidden')
    }else{
        avatar.textContent = ''
        avatar.append(editImg2)
        avatar.innerHTML += `Редагувати інформацію`
        avatar.classList.remove('active')
        contAvatar.classList.remove('hidden')
        editContAvatar.classList.add('hidden')
    }
})


let editImg3 = document.querySelector('.edit-elec-img')
// avatar-div content-hidden
let editElec = document.querySelector('.editElec')
// let editContAvatar = document.querySelector('.content-hidden')
let elecButton = document.querySelector('.edit-elec-button')
// let listOfchange = document.querySelectorAll(".checkInput") + [editElec]
console.log(elecButton)
elecButton.addEventListener('click',()=>{
    if (!elecButton.classList.contains('active')){
        elecButton.textContent = ''
        elecButton.append(editImg3)
        elecButton.innerHTML += `Зберегти`
        elecButton.classList.add('active')
        
        for (let inp of document.querySelectorAll(".checkInput")){
            inp.disabled = false
        }
        editElec.classList.remove('hidden')
        // contAvatar.classList.add('hidden')
        // editContAvatar.classList.remove('hidden')
    }else{
        elecButton.textContent = ''
        elecButton.append(editImg3)
        elecButton.innerHTML += `Редагувати інформацію`
        elecButton.classList.remove('active')
        // checkInput
        for (let inp of document.querySelectorAll(".checkInput")){
            inp.disabled = true
        }
        editElec.classList.add('hidden')
        // contAvatar.classList.remove('hidden')
        // editContAvatar.classList.add('hidden')
    }
})
editElec.addEventListener('click', () =>{
    document.querySelector('canvas').classList.toggle('hidden')
})
})
let avatar = document.querySelector('#avatar')
const fileInput = document.getElementById('fileInput');
fileInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();

                reader.addEventListener('load', function() {
                    profileImage.setAttribute('src', this.result);
                });

                reader.readAsDataURL(file);
            }
        });
// edit-avatar
