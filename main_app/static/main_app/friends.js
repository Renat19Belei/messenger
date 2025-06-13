
// avatar{{ user.pk }}
// for (let card of document.querySelectorAll('.friend-card')){
//     card.addEventListener("click",()=>{
        
//         window.location.href = card.querySelector('input').value
//     })  
// }
// for (let card of document.querySelectorAll('.friend-avatar')){
//     card.addEventListener("click",()=>{
        
//         window.location.href = card.querySelector('input').value
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
