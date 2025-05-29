console.log(document.querySelectorAll('.friend-card'))
for (let card of document.querySelectorAll('.friend-card')){
    card.addEventListener("click",()=>{
        
        window.location.href = card.querySelector('input').value
    })  
}