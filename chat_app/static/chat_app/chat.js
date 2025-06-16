// contact-name
$(document).ready(function(){
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
let groupPk;

// <li class="contact-item" id="user{{contact.pk}}">
//     {% profile_icon contact.user "contact-avatar" %}
//         <div class="contact-info">
//         <span class="contact-name">{{ contact.user.first_name }} {{ contact.user.last_name }}</span>
//     </div>
// </li>
function messageCreate(){

}
for (let user of users){
    user.addEventListener('click',()=>{


        let pk = user.id.split('user').join('')-0
        let icon = user.querySelector('img')
        let name = user.querySelector('.contact-info .contact-name').textContent
        document.querySelector('.friend-current-name').textContent = name
        console.log(name)
        // friend-current-name
        currentIcon.src = icon.src
        let groupPk = pk
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
                // messages.innerHTML = request
                // messages.querySelector('pkInput').value
                // groupPk = messages.querySelector('pkInput').value
                groupPk = request.pk
                socketUrl = `ws://${window.location.host}/chat_group/${groupPk}`
                socket = new WebSocket(socketUrl)
                socket.addEventListener("message", function(event){
                    // Перетворюємо повідомлення з json рядка на JS-об'єкт 
                    const messageObject  = JSON.parse(event.data)
                    // Створюємо html елемент, у якому буде зберігатись отримане повідомлення
                    // const messageElem = document.createElement('p')
                    // Створюємо новий об'єкт класу "Date" з даними дати у фоматі iso
                    let dateTime = new Date(messageObject['date_time'])
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
            }
        })
        console.log(groupPk)
        
        // if (socket){

        //     socket.close()
        // }
        
        
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
})