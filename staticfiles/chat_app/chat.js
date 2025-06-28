$(document).ready(function(){
let users = document.querySelectorAll('.contact-item')
let groups = document.querySelectorAll('.group-item')
let currentIcon = document.querySelector('.current-group-avatar')
let checkMark = document.querySelector('#checkMark').value
const groupH1 = document.querySelector(".groupH1")
const h1grouupcreation = document.querySelector(".h1grouupcreation")
const groupcreationButton = document.querySelector(".groupcreationButton")
const btnBack = document.querySelector(".btn-back")
const imgFromInput = document.getElementById('imgFromInput')
const sendPart = document.querySelector(".send-part")
const fileSendInput = document.querySelector("#fileSendInput")
const fileInput = document.querySelector("#fileInput")
const changeGroupAvatar = document.querySelector("#changeGroupAvatar")
const messageInput =  document.getElementById('messageInput')
const messages = document.querySelector('#messages')
const createGroup = document.querySelector('.create-group')
const addUsers = document.querySelector('#addUsers')
const selectUsers = document.querySelector('#selectUsers')
const grouupcreation = document.querySelector('#grouupcreation')
const membersDiv = document.querySelector('.members')
const contacts = document.querySelectorAll('.contact')
const bg = document.querySelector('.bg')
let selectedContacts = []

// Обработчик выбора аватара группы (отображение превью)
fileInput.addEventListener('change', (event) =>{
    let file = fileInput.files[0]
    console.log(file)
    if (file){
        let reader = new FileReader()

        reader.onload = (event) =>{
            changeGroupAvatar.src = reader.result
        }
        reader.readAsDataURL(file)
    }
})

// Открытие формы выбора участников для создания группы
createGroup.addEventListener('click',(event)=>{
    selectUsers.classList.remove('hidden')
    bg.hidden = false
})

// Переключение между выбором участников и созданием группы
addUsers.addEventListener('click',(event)=>{
    selectUsers.classList.add('hidden')
    grouupcreation.classList.remove('hidden')
})

// Функция форматирует отображение времени сообщений (часы:минуты або дата)
function currectTimes(){
    let times = document.querySelectorAll(".time")
    for (let time of times){
        let messageTime = new Date(time.textContent)
        if (messageTime!='Invalid Date'){
            let now = new Date()
            if (now.getDay()==messageTime.getDay() && now.getFullYear()==messageTime.getFullYear() && now.getMonth()==messageTime.getMonth() || time.classList.contains('messageTime')){
                let messageTimeList = messageTime.toLocaleTimeString().split(':')
                messageTimeList.pop()
                time.textContent = messageTimeList.join(':')
            }else{
                time.textContent = messageTime.toLocaleDateString()
            }
        }
    }
}
currectTimes()

// Обработка выбора участников для группы
selectUsers.addEventListener('submit',(event) =>{
    event.preventDefault()
    
    for (let contact of contacts){
        if (contact.querySelector('input').checked){
            contact = contact.cloneNode(true)
            contact.querySelector('input').remove()
            let img = document.createElement('img')
            img.src = document.querySelector('#removeLink').value
            img.className = 'removeImg'
            img.addEventListener('click', () =>{
                contact.remove()
            })
            contact.append(img)
            membersDiv.append(contact)
        }
    }
})

// Кнопка "Назад" при создании/редактировании группы
btnBack.addEventListener('click', (event) =>{
    selectUsers.classList.remove('hidden')
    grouupcreation.classList.add('hidden')
    membersDiv.innerHTML =''

})

// Обработка выбора файла для отправки в чат (отображение превью)
fileSendInput.addEventListener('change',function (){
    let file = fileSendInput.files[0]
    if (file){
        const reader = new FileReader();

        reader.onload = function(event){
            imgFromInput.src = event.target.result
        };
        reader.readAsDataURL(file)
    }

})

// Отправка сообщения (текст/файл) через WebSocket
sendPart.addEventListener("submit", (event)=>{
    event.preventDefault()
    let message = messageInput.value
    messageInput.value = ''
    let file = fileSendInput.files[0]
    if (file){
        const reader = new FileReader();

        reader.onload = function(event){
            socket.send(JSON.stringify({
                'message': message,
                'img':reader.result.split(',')[1],
                'imgType':file.type.split('/')[1]
            }))
        };
        reader.readAsDataURL(file)
        fileSendInput.value = ''
        imgFromInput.src = ''
    }else{

        socket.send(JSON.stringify({
            'message': message
        }))
    }
})

let socketUrl;
let socket;
let groupPk;

// Функция для создания WebSocket и отображения новых сообщений в чате
function messageCreate(){
    socketUrl = `ws://${window.location.host}/chat_group/${groupPk}`
    socket = new WebSocket(socketUrl)
    socket.addEventListener("message", function(event){
        // Перетворюємо повідомлення з json рядка на JS-об'єкт 
        const messageObject  = JSON.parse(event.data)
        // Создаем объект даты из строки времени сообщения
        let dateTime = new Date(messageObject['date_time'])
        // Создаем элемент для изображения, если оно есть в сообщении
        let imageFromUser = document.createElement('img')
        imageFromUser.src = messageObject['img']
        imageFromUser.className = 'imgFromUser'
        // Создаем элементы для отображения сообщения
        let p = document.createElement('p')
        let messageContent = document.createElement('span')
        messageContent.className = 'messageContent'
        let details = document.createElement('span')
        let time = document.createElement('span')
        let img = document.createElement('img')
        p.className = 'my message'
        details.className = 'details-message'
        time.className = 'time'
        
        img.className = 'check-mark'
        time.textContent = `${dateTime.getHours()}:${dateTime.getMinutes()}`
        img.src = checkMark
        
        details.append(time)

        details.append(img)
        messageContent.textContent = messageObject['message']
        messageContent.append(details)
        
        if (!messageObject['you']){
            let img = document.createElement('img')
            if (messageObject['avatar']){
                img.src = messageObject['avatar']
            }else{
                img.src = document.getElementById('avatarLink').value
            }
            let message_data = document.createElement('span')
            message_data.className = 'message-data'
            let username = document.createElement('span')
            username.className = 'username'
            username.textContent = messageObject['username']
            message_data.append(username)
            message_data.append(messageContent)
            if (messageObject['img']!=undefined){
                message_data.prepend(imageFromUser)
            }
            p.append(message_data)
            img.className= 'avatar'
            p.prepend(img)
            p.className = 'message'
        }else{
            if (messageObject['img']!=undefined){
                p.prepend(imageFromUser)
            }
            p.append(messageContent)
        }
        messages.prepend(p)
        currectTimes()
    })
}

// Обробка редагування групи (AJAX-запит на сервер)
let editChat =document.querySelector('.editChat')
editChat.addEventListener('click',()=>{
    $.ajax({
        type: 'post',
        url: document.querySelector('#getLink').value,
        data: {
            csrfmiddlewaretoken:document.querySelector('input').value,
            pk: groupPk
        },
        success: function(request){
            groupH1.textContent = 'Додати учасника'
            h1grouupcreation.textContent = 'Редагування групи'
            groupcreationButton.textContent = 'Зберегти зміни'
            bg.hidden = false
            if (request.avatar){
                document.querySelector('#changeGroupAvatar').src = request.avatar
            }
            document.querySelector('#nameGroupInput').value = request.name
            document.querySelector('#groupCreation').value = 'groupEdit'
            document.querySelector('#pkInput').value = groupPk
            for (let contact of contacts){
                if (contact.querySelector('#member').value in request.members){
                    contact.querySelector('input').remove()
                    selectedContacts.push(contact)
                    let img = document.createElement('img')
                    img.src = document.querySelector('#removeLink').value
                    img.className = 'removeImg'
                    img.addEventListener('click', () =>{
                        contact.remove()
                    })
                    contact.append(img)
                    membersDiv.append(contact)
                }
            }
        }})
})

// Обробка кліку по групі для відкриття чату
for (let group of groups){
    group.addEventListener('click',()=>{
        let pk = group.id.split('group').join('')-0
        let icon = group.querySelector('img')
        let name = group.querySelector('.text-group .groupName').textContent
        document.querySelector('.friend-current-name').textContent = name
        currentIcon.src = icon.src
        groupPk = pk
        document.querySelector('.center-message').hidden = true
        document.querySelector('#haederCard').style.display = 'flex'
        document.querySelector('#chatCard').style.display = 'flex'
        $.ajax({
            type: 'post',
            url: window.location.href,
            data: {
                csrfmiddlewaretoken:document.querySelector('input').value,
                pk: pk,
                type:'group'
            },
            success: function(request){
                messages.innerHTML = request
                groupPk = messages.querySelector('#pkInput').value
                let is_admin = document.querySelector('#is_admin').value-0
                if (!is_admin){
                    document.querySelector('#adminChat').classList.add('hidden')
                    document.querySelector('#userChat').classList.remove('hidden')
                    document.querySelector('.editChat').classList.add('hidden')
                    document.querySelector('dialog').style.height = '7.3490813648vw'
                }else{
                    document.querySelector('dialog').style.height = '9.23884514432vw'
                    document.querySelector('.editChat').classList.remove('hidden')
                    document.querySelector('#adminChat').classList.remove('hidden')
                    document.querySelector('#userChat').classList.add('hidden')
                }
                let leaveLink = document.querySelector('#leaveLink').value
                leaveLink = leaveLink.split('0').join(`${groupPk}`)
                for (let exitElem of document.querySelectorAll('.exitChat')){
                    exitElem.addEventListener('click', (event) => {
                        $.ajax({
                        type: 'get',
                        url: leaveLink,
                        success:function func(){
                            exit()
                            document.querySelector(`#group${groupPk}`).remove()
                        }
                    })
                    })
                }
                messageCreate()
                currectTimes()
            }
        })
    })
}

// Обробка кліку по елементу "три крапки" (ellipsis) для показу меню
let ellipsises =document.querySelectorAll(".ellipsis")
for (let ellipsis of ellipsises){
    ellipsis.addEventListener('click', () => {
        console.log(ellipsis.id)
        for (let object of document.querySelectorAll(`#${ellipsis.id}`)){
            object.classList.toggle("hidden")
        }
    })
}

// Функція для відкриття чату з користувачем або групою
function userOpen(users){
for (let user of users){
    user.addEventListener('click',()=>{
        let pk = user.id.split('user').join('')-0
        let icon = user.querySelector('img')
        let name = user.querySelector('.contact-info .contact-name')
        if (!name){
            name = user.querySelector('.groupName')
        }
        name = name.textContent
        document.querySelector('.friend-current-name').textContent = name
        currentIcon.src = icon.src
        groupPk = pk
        document.querySelector('.center-message').hidden = true
        document.querySelector('#haederCard').style.display = 'flex'
        document.querySelector('#chatCard').style.display = 'flex'
        $.ajax({
            type: 'post',
            url: window.location.href,
            data: {
                csrfmiddlewaretoken:document.querySelector('input').value,
                pk: pk,
                type:'personal'},
            success: function(request){
                messages.innerHTML = request
                groupPk = messages.querySelector('#pkInput').value
                messageCreate()
                currectTimes()
            }
        })
        
    })
}}
userOpen(document.querySelector('.messages').querySelectorAll('.contact-item'))
userOpen(users)

// Функція для виходу з чату (ховає чат і показує центр)
function exit(){
    document.querySelector('.center-message').hidden = false
    document.querySelector('#haederCard').style.display = 'none'
    document.querySelector('#chatCard').style.display = 'none'
}
document.querySelector('.exit-img').addEventListener('click', exit)
})