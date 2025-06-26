// Для каждой карточки друга добавляем обработчик клика
for (let card of document.querySelectorAll('.friend-card')){
    card.addEventListener("click",(event)=>{
        // Если клик не по кнопкам "Подтвердить" или "Удалить", переходим на страницу друга
        if (event.target != card.querySelector('.btn-confirm') && event.target != card.querySelector('.btn-delete')){
            window.location.href = card.querySelector('input').value
        }
    })  
}

// Для каждой кнопки "Подтвердить", "Додати" или "Повідомлення" добавляем обработчик
let buttons = document.querySelectorAll(".btn-confirm")
for (let button of buttons){
    button.addEventListener("click", () => {
        let pk = button.value
        let type;
        // Определяем тип действия по тексту кнопки и извлекаем pk пользователя
        if (pk.split('Підтвердити').length>1){
            type = 'confirm'
            pk = pk.split('Підтвердити')[1]
            
        }else if (pk.split('Додати').length>1){
            type = 'add'
            pk = pk.split('Додати')[1]

        }else if (pk.split('Повідомлення').length>1){
            pk = pk.split('Повідомлення')[1]
            // Переход к чату
            window.location.href = document.querySelector('#chatUrl').value
        }
        // Находим карточку друга и контейнер для всех друзей
        let card = document.querySelector('#card'+pk)
        let allFriends = document.querySelector('.allFriends')
        // Удаляем карточку из текущего списка
        card.remove()
        // Если подтверждение — добавляем карточку в список друзей
        if (type=='confirm'){
            allFriends.append(card)
        }
        // Отправляем POST-запрос на сервер для обработки действия (добавить/подтвердить)
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