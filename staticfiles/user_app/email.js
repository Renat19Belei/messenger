// Получаем все инпуты для ввода кода подтверждения
const inputs = document.querySelectorAll('.code');
// Форма подтверждения email
const form = document.querySelector('.email');

// Ставим фокус на первый инпут
inputs[0].focus()

// Обработка ввода с клавиатуры для автоматического перехода между полями
document.addEventListener('keyup',function(event) {
    if (document.activeElement != document.body){
        // Получаем номер текущего поля
        let number =document.activeElement.name[document.activeElement.name.length-1]
        if (event.key=='Backspace'){
            // При удалении переходим к предыдущему полю
            if (1<number){
                inputs[number-2].focus()
            }
        }else{
            // Если поле заполнено, переходим к следующему или отправляем форму
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