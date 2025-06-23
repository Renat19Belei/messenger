// document.addEventListener('DOMContentLoaded', function() {
const inputs = document.querySelectorAll('.code');
const button = document.querySelector('.save');
const form = document.querySelector('.email');
console.log(form)
inputs[0].focus()
document.addEventListener('keyup',function(event) {
    if (document.activeElement != document.body){
        let number =document.activeElement.name[document.activeElement.name.length-1]
        console.log(number)
        if (event.key=='Backspace'){
            if (1<number){
                inputs[number-2].focus()
            }
        }else{
            if (document.activeElement.value) {
                if (number != 6) {
                    inputs[number].focus()
                }else{
                    form.submit()
                }
            }
        }
    }
})
