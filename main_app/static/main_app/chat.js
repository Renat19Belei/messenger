// contact-name
let users = document.querySelectorAll('.contact-item')
let currentIcon = document.querySelector('.current-group-avatar')
// center-message
// chatCard
for (let user of users){
    user.addEventListener('click',()=>{


        let pk = user.id.split('user').join('')
        console.log(pk-0)
        let icon = user.querySelector('img')
        currentIcon.src = icon.src
        document.querySelector('.center-message').hidden = true
        document.querySelector('#haederCard').style.display = 'flex'
        document.querySelector('#chatCard').style.display = 'flex'
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