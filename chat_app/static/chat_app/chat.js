// contact-name
let users = document.querySelectorAll('.contact-item')
let currentIcon = document.querySelector('.current-group-avatar')
let checkMark = document.querySelector('#checkMark').value
// checkMark
const sendMessage = document.querySelector(".send-button")
const messageInput =  document.getElementById('messageInput')
const messages = document.querySelector('.messages')
sendMessage.addEventListener("click", (event)=>{
    let message = messageInput.value
    messageInput.value = ''
    console.log(message)
    socket.send(JSON.stringify({
        'message': message
    }))
})

// <main class="messages">
    //     <p class="my-message">
    //         Привіт! <span class="details-message"> <span class="time">10:01</span> <img src="{% static 'main_app/images/check_mark.png' %}" class="check-mark"> </span>
    //     </p>
    // </main>
// center-message
// chatCard
let socketUrl;
let socket;
for (let user of users){
    user.addEventListener('click',()=>{


        let pk = user.id.split('user').join('')-0
        let icon = user.querySelector('img')
        currentIcon.src = icon.src
        document.querySelector('.center-message').hidden = true
        document.querySelector('#haederCard').style.display = 'flex'
        document.querySelector('#chatCard').style.display = 'flex'
        if (socket){

            socket.close()
        }
        socketUrl = `ws://${window.location.host}/chat_group/${pk}`
        socket = new WebSocket(socketUrl)
        socket.addEventListener("message", function(event){
            // Перетворюємо повідомлення з json рядка на JS-об'єкт 
            const messageObject  = JSON.parse(event.data)
            // Створюємо html елемент, у якому буде зберігатись отримане повідомлення
            const messageElem = document.createElement('p')
            // Створюємо новий об'єкт класу "Date" з даними дати у фоматі iso
            let dateTime = new Date(messageObject['date_time'])
            // let dateTimeLocal = dateTime.toLocaleString()
            // Переносимо дату та час під формат та часовий пояс в залежності від налаштувань користувача
            // Вказуємо те, що буде всередині елемента з повідомленням
            // messageElem.innerHTML = `${messageObject['username']}: <b>${messageObject['message']}</b> (${dateTimeLocal})`
            // Додаємо елемент повідомлення до div з повідомленнями 
            // messages.append(messageElem)
            let p = document.createElement('p')
            let details = document.createElement('span')
            let time = document.createElement('span')
            let img = document.createElement('img')
            p.className = 'my-message'
            details.className = 'details-message'
            time.className = 'time'
            
            img.className = 'check-mark'
            time.textContent = `${dateTime.getHours()}:${dateTime.getMinutes()}`
            img.src = checkMark
            
            details.append(time)

            details.append(img)
            p.textContent = messageObject['message']
            p.append(details)
            messages.append(p)
        })
        // {}
        
        // chat-card exit-img
        // haederCard
        // icon.remove()
        // icon
    })
}

document.querySelector('.exit-img').addEventListener('click', () => {
    document.querySelector('.center-message').hidden = false
    document.querySelector('#haederCard').style.display = 'none'
    document.querySelector('#chatCard').style.display = 'none'
})
