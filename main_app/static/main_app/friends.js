
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
        let type;
       
        if (pk.split('Підтвердити').length>1){
            type = 'confirm'
            pk = pk.split('Підтвердити')[1]
            
        }else if (pk.split('Додати').length>1){
            type = 'add'
            pk = pk.split('Додати')[1]

        }else if (pk.split('Повідомлення').length>1){
            // type = 'confirm'
            
            pk = pk.split('Повідомлення')[1]
            window.location.href = document.querySelector('#chatUrl').value
            // 
            
        }
        let card = document.querySelector('#card'+pk)
        let allFriends = document.querySelector('.allFriends')
        card.remove()
        if (type=='confirm'){
            allFriends.append(card)
        }
        // allFriends
        
        fetch(window.location.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('input').value
            },
            body: JSON.stringify({
                'pk': pk,
                'type':type
                })
        })

    })
} 
