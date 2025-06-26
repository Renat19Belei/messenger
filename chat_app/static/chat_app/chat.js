// contact-name
$(document).ready(function(){
let users = document.querySelectorAll('.contact-item')
let groups = document.querySelectorAll('.group-item')
let time = new Date()
// let time2 = new Date(time.())
// imgFromInput
// console.log(time2.getHours(),time.getHours())
// group-item
let currentIcon = document.querySelector('.current-group-avatar')
let checkMark = document.querySelector('#checkMark').value
// currectTime
let currectTime = document.querySelector('#currectTime').value
let differentTime = time.getHours() - currectTime
console.log(differentTime)
// checkMark btn-back groupH1 addUsers
const groupH1 = document.querySelector(".groupH1")
const h1grouupcreation = document.querySelector(".h1grouupcreation")
const groupcreationButton = document.querySelector(".groupcreationButton")

// h1grouupcreation
// const addUsers = document.querySelector("#addUsers")
const btnBack = document.querySelector(".btn-back")
const imgFromInput = document.getElementById('imgFromInput')
const sendMessage = document.querySelector(".send-button")
const sendPart = document.querySelector(".send-part")
const fileSendInput = document.querySelector("#fileSendInput")
const fileInput = document.querySelector("#fileInput")
const changeGroupAvatar = document.querySelector("#changeGroupAvatar")
// /fileInput changeGroupAvatar
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
// grouupcreation members
createGroup.addEventListener('click',(event)=>{
    // if (selectUsers.hidden){
        selectUsers.classList.remove('hidden')
        bg.hidden = false
    // }
})
addUsers.addEventListener('click',(event)=>{
    selectUsers.classList.add('hidden')
    grouupcreation.classList.remove('hidden')
})
function currectTimes(){
    let times = document.querySelectorAll(".time")
    // messageTimeObject
    for (let time of times){
        
        
        let messageTime = new Date(time.textContent)
        // console.log(messageTime)
        if (messageTime!='Invalid Date'){
        // console.log()
        let now = new Date()
        if (now.getDay()==messageTime.getDay() && now.getFullYear()==messageTime.getFullYear() && now.getMonth()==messageTime.getMonth() || time.classList.contains('messageTime')){
            // if (messageTime.getHours()<)
            // time.textContent = `${messageTime.getHours()}:${messageTime.getMinutes()}`
            let messageTimeList = messageTime.toLocaleTimeString().split(':')
            messageTimeList.pop()
            time.textContent = messageTimeList.join(':')
        }else{
            time.textContent = messageTime.toLocaleDateString()
        }}
    }
}
currectTimes()
// addUsers
// <img src="{% static 'main_app/images/remove.png' %}" alt=""  class="icon">
selectUsers.addEventListener('submit',(event) =>{
    event.preventDefault()
    
    for (let contact of contacts){
        if (contact.querySelector('input').checked){
            contact = contact.cloneNode(true)
            contact.querySelector('input').remove()
            // selectedContacts.push(contact)
            // removeLink
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

btnBack.addEventListener('click', (event) =>{
    selectUsers.classList.remove('hidden')
    grouupcreation.classList.add('hidden')
    membersDiv.innerHTML =''

})
fileData = ''
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

function messageCreate(){
    // Формируем URL для WebSocket соединения с группой
    socketUrl = `ws://${window.location.host}/chat_group/${groupPk}`
    socket = new WebSocket(socketUrl)
    // Обработчик получения нового сообщения по WebSocket
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
let editChat =document.querySelector('.editChat')
editChat.addEventListener('click',()=>{
    console.log(groupPk)
    $.ajax({
        type: 'post',
        url: document.querySelector('#getLink').value,
        data: {

            csrfmiddlewaretoken:document.querySelector('input').value,
            pk: groupPk
        },
        success: function(request){
            grouupcreation.classList.remove('hidden')
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
                    // removeLink
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
let ellipsises =document.querySelectorAll(".ellipsis")
for (let ellipsis of ellipsises){
    ellipsis.addEventListener('click', () => {
        console.log(ellipsis.id)
        for (let object of document.querySelectorAll(`#${ellipsis.id}`)){
            object.classList.toggle("hidden")
        }
    })
}
// messages
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
function exit(){
document.querySelector('.center-message').hidden = false
    document.querySelector('#haederCard').style.display = 'none'
    document.querySelector('#chatCard').style.display = 'none'
}
document.querySelector('.exit-img').addEventListener('click', exit)
})