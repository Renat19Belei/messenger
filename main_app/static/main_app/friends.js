
// avatar{{ user.pk }}
for (let card of document.querySelectorAll('.friend-card')){
    card.addEventListener("click",(event)=>{
        console.log(event.target)
        if (event.target != card.querySelector('.btn-confirm') && event.target != card.querySelector('.btn-delete')){

            window.location.href = card.querySelector('input').value
        }
    })  
}
// for (let avatar of document.querySelectorAll('.friend-avatar')){
//     avatar.addEventListener("click",()=>{
//         let pk = avatar.className.split(' ')[1]

//         window.location.href = avatar.querySelector('input').value
//     })  
// }
// friend-avatar
// btn btn-confirm
let buttons = document.querySelectorAll(".btn-confirm")
console.log(buttons)
for (let button of buttons){
    button.addEventListener("click", () => {
        let pk = button.value
        let card = document.querySelector('#card'+pk)
        card.remove()
        // allFriends
        document.querySelector('.allFriends').append(card)
        console.log(card)
        fetch(window.location.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('input').value
            },
            body: JSON.stringify({
                'pk': pk
                })
        })

    })
} 
