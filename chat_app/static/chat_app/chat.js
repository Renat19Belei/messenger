// contact-name
let users = document.querySelectorAll('.contact-item')
let currentIcon = document.querySelector('.current-group-avatar')

const sendMessage = document.querySelector(".send-button")
const messageInput =  document.getElementById('messageInput')
sendMessage.addEventListener("click", (event)=>{
    let message = messageInput.value
    messageInput.value = ''
    console.log(message)
    socket.send(JSON.parse({
        'message': message
    }))
})
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
