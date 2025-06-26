$(document).ready(function(){
// let profileCard = document.querySelector("")  
let eyeUrl = document.querySelector("#eyeUrl")
let passwords = document.querySelectorAll(".password")
let ps = document.querySelectorAll("p")
let mark = document.querySelector("#mark")
let back = document.querySelector(".back")
let editPasswordImg = document.querySelector(".edit-img-password")
let save = document.querySelector(".password-edit-inline-button")

let oldPassword = document.querySelector(".old-password")
let newPassword = document.querySelector(".new-password")
let acceptPassword  = document.querySelector(".confirm-password")
let codes = document.querySelectorAll(".code")
back.addEventListener("click", ()=>{
    document.querySelector('.email').classList.add('hidden')
    document.querySelector('.bg').classList.add('hidden')
    save.textContent = ''
    save.append(editPasswordImg)
    save.innerHTML += "Збергти пароль"
    save.classList.remove('active')
    oldPassword.parentElement.classList.remove("hidden")
    acceptPassword.parentElement.classList.add("hidden")
    newPassword.parentElement.classList.add("hidden")
})
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
function submitCode(event){
    
    let codes_list = []
    for (let code of codes){
        codes_list.push(code.value)
    }
    console.log(codes_list.join(''))
    $.ajax({
            type: 'post',
            url: document.querySelector('#personalUrl').value,
            data: {

                csrfmiddlewaretoken:document.querySelector('input').value,
                codes:codes_list.join(''),
                type:'check_code'
            },
            success:function(request){
            if (request.correct){
                console.log(request)
            // oldPassword.classList.add("hidden")
            oldPassword.parentElement.classList.add("hidden")
            acceptPassword.parentElement.classList.remove("hidden")
            newPassword.parentElement.classList.remove("hidden")
            save.classList.add('active')
            document.querySelector('.email').classList.add('hidden')
            document.querySelector('.bg').classList.add('hidden')
            save.textContent = ''
            save.append(editPasswordImg)
            save.innerHTML += "Збергти пароль"
        }
        }})
}

document.querySelector('.email').addEventListener('submit', (event)=>{
    event.preventDefault()
    submitCode()
})
const inputsOfcode = document.querySelectorAll('.code');
const form = document.querySelector('.email');
console.log(form)
inputsOfcode[0].focus()
document.addEventListener('keyup',function(event) {
    if (document.activeElement != document.body){
        let number =document.activeElement.name[document.activeElement.name.length-1]
        console.log(number)
        if (event.key=='Backspace'){
            if (1<number){
                inputsOfcode[number-2].focus()
            }
        }else{
            if (document.activeElement.value) {
                if (number != 6) {
                    inputsOfcode[number].focus()
                }else{
                    submitCode()
                }
            }
        }
    }
})
save.addEventListener("click", ()=>{
    
    let inputs = document.querySelectorAll('.password-change-div .FormInput') 
    if (save.classList.contains('active')){
            let news = document.querySelector('.new-password').value
            let confirm = document.querySelector('.confirm-password').value
            console.log(news,confirm)
            if (news==confirm){

                $.ajax({
                type: 'post',
                url: document.querySelector('#personalUrl').value,
                data: {
    
                    csrfmiddlewaretoken:document.querySelector('input').value,
                    password: news,
                    type:'edit_password'
    
                },
                success:function(request){
                    save.classList.remove('active')
                    oldPassword.parentElement.classList.remove("hidden")
                    acceptPassword.parentElement.classList.add("hidden")
                    newPassword.parentElement.classList.add("hidden")
                    save.textContent = ''
                    save.append(editPasswordImg)
                    save.innerHTML += `Редагувати пароль`
                    window.location.href = document.querySelector('#login').value
                }})
            }
    }else{
        $.ajax({
            type: 'post',
            url: document.querySelector('#personalUrl').value,
            data: {

                csrfmiddlewaretoken:document.querySelector('input').value,
                password:oldPassword.value,
                type:'check_password'
            },
            success:function(request){
                if (request.correct){
                    oldPassword.parentElement.classList.add("hidden")
                    acceptPassword.parentElement.classList.remove("hidden")
                    newPassword.parentElement.classList.remove("hidden")
                    save.classList.add('active')
                    for (let input of inputs){
                        if (!input.classList.contains('password')){
                            input.requered = true
                            input.readOnly = false
                            input.classList.remove('gray-input')
                        }
                    }
                    document.querySelector('.email').classList.remove('hidden')
                    document.querySelector('.bg').classList.remove('hidden')
                    save.textContent = ''
                    save.append(editPasswordImg)
                    save.innerHTML += "Зберегти пароль"
                }
            }
        })
    }
})
// Получаем canvas для рисования подписи
let canvas = document.querySelector('canvas')
// Убираем внутренние отступы
canvas.style.padding = 0
// Получаем контекст рисования 2D
let draw = canvas.getContext('2d')
// Устанавливаем цвет заливки (не используется для линий)
draw.fillStyle = 'black'
// Флаг, указывающий, идет ли сейчас рисование
let drawing = false

// Функция для вычисления координат относительно canvas
function coor(event){
    let rect = canvas.getBoundingClientRect()
    return [(event.clientX-rect.left+0.1)*canvas.width / rect.width,(event.clientY-rect.top+7)*canvas.height / rect.height]
}

// Начинаем рисование при нажатии мыши
canvas.addEventListener('mousedown', (event) => {
    pastplace = coor(event)
    drawing = true
})

// Завершаем рисование при отпускании мыши
document.addEventListener('mouseup',()=> {
    drawing = false
})

let pastplace = []

// Рисуем линию при движении мыши, если рисование активно
canvas.addEventListener('mousemove',(event)=>{
    if (drawing){
        // Для отладки: текущий цвет линии
        console.log(draw.fillStyle,'rtyuioupuoiouytreww')
        draw.beginPath();
        draw.moveTo(pastplace[0], pastplace[1]);
        pastplace = coor(event)
        draw.lineTo(pastplace[0], pastplace[1]);
        draw.stroke();
    }
})
// Получаем кнопку "Редагувати інформацію" и иконку редактирования
let info = document.querySelector('#info')
let editImg = document.querySelector('.edit-img')

// Обработчик клика по кнопке редактирования информации
info.addEventListener('click',()=>{
    let info = document.querySelector('#info')
    let inputs = document.querySelectorAll('.FormInput') 
    // Если уже активен режим редактирования — выключаем его и отправляем изменения на сервер
    if (info.classList.contains('active')){
        info.classList.remove('active')
        for (let input of inputs){
            input.requered = false
            input.readOnly = true
            input.classList.add('gray-input')
        }
        // Получаем значения из полей формы
        let first_name = document.querySelector('[name="first_name"]').value
        let last_name = document.querySelector('[name="last_name"]').value
        // Отправляем изменения на сервер через AJAX
        $.ajax({
            type: 'post',
            url: document.querySelector('#personalUrl').value,
            data: {
                csrfmiddlewaretoken:document.querySelector('input').value,
                first_name: first_name,
                last_name: last_name,
                email: document.querySelector('[name="email"]').value,
                date_of_birthday: document.querySelector('[name="date_of_birthday"]').value,
                type:'main_data' // вказуємо, що потрібно редагувати в нашому випадку основні дані
            },
            success:function(request){
                // Обновляем имя пользователя на странице
                let name_tags = document.querySelectorAll('.name-h2, h4')
                for(let tag of name_tags){
                    tag.textContent = `${first_name} ${last_name}`
                }
            }
        })
        info.textContent = ''
        info.append(editImg)
        info.innerHTML += `Редагувати інформацію`
    }else{
        // Включаем режим редактирования: делаем поля активными
        info.classList.add('active')
        for (let input of inputs){
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
let contAvatar = document.querySelector('.avatar-div')
let editContAvatar = document.querySelector('.content-hidden')
let avatarsInput = document.getElementById('avatarsInput')

// Получаем элементы: картинку смены аватарки и input для выбора файла
let avatar = document.querySelector('#avatar')
let fileInput = document.getElementById('fileInput')
// Создаем FileReader для чтения выбранного изображения
const reader = new FileReader()
// После выбора файла сразу отображаем превью аватарки на всех элементах с классом .avatar
reader.onload = (loadEvent) => {
    let avatars = document.querySelectorAll('.avatar')
    for (let avatar of avatars){
        avatar.src = loadEvent.target.result
    }
}
// При изменении файла (выбор нового изображения) запускаем чтение файла и обновление превью
fileInput.addEventListener('change',()=>{
    reader.readAsDataURL(fileInput.files[0])
})
avatar.addEventListener('click',()=>{
    // Если не активен режим редактирования аватарки — включаем его
    if (!avatar.classList.contains('active')){
        avatar.textContent = ''
        avatar.append(editImg2)
        avatar.innerHTML += `Зберегти`
        avatar.classList.add('active')
        contAvatar.classList.add('hidden')
        editContAvatar.classList.remove('hidden')
    }else{
        // Если режим редактирования активен — сохраняем изменения и возвращаемся к просмотру
        avatar.textContent = ''
        avatar.append(editImg2)
        avatar.innerHTML += `Редагувати інформацію`
        avatar.classList.remove('active')
        contAvatar.classList.remove('hidden')
        editContAvatar.classList.add('hidden')
        // Если выбран новый файл для аватарки — отправляем его на сервер через AJAX
        if (fileInput.files[0]!=undefined){
            let formData = new FormData()
            formData.append('profile_icon', fileInput.files[0])
            formData.append('csrfmiddlewaretoken',document.querySelector('input').value)
            formData.append('type', 'profile')
            let files = avatarsInput.files
            // Добавляем все дополнительные выбранные изображения (если есть)
            for (let i = 0; i < files.length; i++) {
                formData.append('avatars', files[i]);
            }
            $.ajax({
                type: 'post',
                url: document.querySelector('#personalUrl').value,
                data: formData,
                processData: false,
                contentType: false,
                success:function(request){}
            })
        }
    }
})


let editImg3 = document.querySelector('.edit-elec-img')
// avatar-div content-hidden
let editElec = document.querySelector('.editElec')
// let editContAvatar = document.querySelector('.content-hidden')
let elecButton = document.querySelector('.edit-elec-button')
let electronicSignature = document.querySelector('#electronicSignature')
// let listOfchange = document.querySelectorAll(".checkInput") + [editElec]
// console.log(elecButton)
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
        // toDataURL check
        
        // document.querySelector('#check').src = canvas.toDataURL('images/png')
        elecButton.classList.remove('active')
        // checkInput
        for (let inp of document.querySelectorAll(".checkInput")){
            inp.disabled = true
        }
        editElec.classList.add('hidden')
        // if (canvas.classList.contains('hidden')){
        let formData = new FormData()
        canvas.toBlob(function (blob){

            formData.append('elec', blob, 'canvas_image.png')
            // console.log(fileInput.files[0])
            formData.append('csrfmiddlewaretoken',document.querySelector('input').value)
            formData.append('type', 'elec')
            
            // elec
            $.ajax({
                type: 'post',
                url: document.querySelector('#personalUrl').value,
                data: formData,
                processData: false,
                contentType: false,
                success:function(request){
                   
                    
                    // electronicSignature
            }})

        },'images/png')
        electronicSignature.src = canvas.toDataURL('images/png')
        canvas.classList.add('hidden')
        editElec.classList.add('hidden')
        colors[0].classList.add('hidden')
        colors[1].classList.add('hidden')
        electronicSignature.classList.remove('hidden')
    }
})
function colorEdit(event){
    draw.strokeStyle = event.target.style.background
}
let colors = document.querySelectorAll('.color')
colors[0].addEventListener('click',colorEdit)
colors[1].addEventListener('click',colorEdit)
editElec.addEventListener('click', () =>{
    electronicSignature.classList.toggle('hidden')
    canvas.classList.toggle('hidden')
    editElec.classList.toggle('hidden')
    colors[0].classList.toggle('hidden')
    colors[1].classList.toggle('hidden')
})
})
// let avatar = document.querySelector('#avatar')