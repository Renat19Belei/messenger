// document.addEventListener('DOMContentLoaded', function() {
const inputs = document.querySelectorAll('.code');
const button = document.querySelector('.save');
const form = document.querySelector('form');
inputs[0].focus()
// inputs.forEach((input, index) => {
//     input.addEventListener('input', function() {
        
//         // Check if the current input has reached its maxlength
//         if (this.value) {
//             // If there is a next input field
//             if (index + 1 < inputs.length) {
//                 // Focus the next input field
//                 inputs[index + 1].focus();
//             }
//         }
//     });
// });
document.addEventListener('keyup',function(event) {
    // console.log(
    // console.log(document.activeElement)
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
