$(document).ready(function(){
        
        function load(count){
            let error= NaN
            try {
                let removeLink = document.querySelector('#removeLink').value
                removeLink.split('1').join('1')
                error = true
            } catch (E) {
                 error = false
            }
            let link = $('#request')[0].value;
            let csrf = $('input')[0].value
            let list = []
            for (let i=0;i!=count;i++){
                list.push(current+i)
            }
            let postsList = []
            for (let post of document.querySelectorAll(".post")){
                postsList.push(post.id.split("post").join(''))
            }
            let type = {}
            type[window.location.href] = window.location.href
            type = {}
            type["http://127.0.0.1:8000/post/posts/"] = "posts"
            if (window.location.href in type){
                type = 'posts'
            }else if (window.location.href.split('/')[window.location.href.split('/').length-2]=='friends_account'){
                type = document.querySelector("#type").value
            }   
            else{
                type = 'main'
            }
            $.ajax({
                type: 'post',
                url: link,
                data: {csrfmiddlewaretoken:csrf,
                    posts: JSON.stringify(list), 
                    postsList: JSON.stringify(postsList), 
                    type: type
                },  
                success: function(request){
                    $('.poster').append(request)
                    current+=count
                    let ellipsises =document.querySelectorAll(".ellipsis")
                    for (let ellipsis of ellipsises){
                        ellipsis.addEventListener('click', () => {
                            for (let object of document.querySelectorAll(`#${ellipsis.id}`)){
                                object.classList.toggle("hidden")
                            }
                        })
                    }
                    if (error){
                        // Получаем все кнопки удаления постов
                        let removes =document.querySelectorAll(".remove")
                        // Для каждой кнопки удаления добавляем обработчик клика
                        for (let remove of removes){
                            // Формируем ссылку для удаления, подставляя id поста
                            let link1 = removeLink.value.split('1').join(remove.id)
                            remove.addEventListener('click', () => {
                                // Отправляем AJAX-запрос на удаление поста
                                $.ajax({
                                    type: 'post',
                                    url: link1,
                                    data: {csrfmiddlewaretoken:csrf,posts:JSON.stringify(list)}, 
                                    success: function(request){}
                                })
                                // Удаляем пост из DOM после успешного запроса
                                document.querySelector('#post'+remove.id).remove()
                            })
                        }
                        // Получаем все кнопки редактирования постов
                        let edits =document.querySelectorAll(".edit")
                        // Для каждой кнопки добавляем обработчик клика
                        for (let edit of edits){
                            edit.addEventListener('click', () => {
                                // Получаем id поста для редактирования
                                let index = edit.id
                                // Показываем модальное окно для редактирования поста
                                document.querySelector('#bg').classList.remove('hidden')
                                document.querySelector('#modalForm').classList.remove('hidden')
                                // Устанавливаем тип редактируемого поста
                                document.querySelector('#type').value = index
                                // Показываем/скрываем дополнительные элементы, связанные с этим постом
                                for (let object of document.querySelectorAll(`#heh${index}`)){
                                    object.classList.toggle("hidden")
                                }
                                // Формируем ссылку для получения данных поста
                                let link2 = removeLink.value.split('1')
                                link2 = link2.join(index)
                                link2 = link2.split('remove').join('get')
                                // Делаем AJAX-запрос для получения данных поста
                                $.ajax({
                                    type: 'get',
                                    url: link2,
                                    success: function(request){
                                        let trashUrl = document.querySelector('#trash').value
                                        // Заполняем поля формы данными поста
                                        document.querySelector('.textInput').value = request.text
                                        document.querySelector('.linkInput').value = request.link[0]
                                        document.querySelector('.nameInput').value = request.name
                                        let count = 0
                                        // Добавляем изображения поста в форму редактирования
                                        for (let img of request.imgs){
                                            let img_tag = document.createElement('img')
                                            img_tag.src = img
                                            img_tag.classList.add('image')
                                            let div = document.createElement("div")
                                            div.id = `div${img}`
                                            let trashImg = document.createElement("img")
                                            trashImg.src = trashUrl
                                            trashImg.id = count
                                            count++
                                            let button = document.createElement("button")
                                            button.type = 'button'
                                            button.className = 'removeImg'
                                            button.append(trashImg)
                                            div.classList.add('imagesDiv')
                                            div.append(img_tag)
                                            div.append(button)
                                            let input = document.querySelector('#images2')
                                            button.addEventListener('click',() => {
                                                div.remove()
                                                input.value += `${trashImg.id} `
                                            })
                                            document.querySelector('#imagesDiv').append(div)
                                        }
                                        // Сохраняем pk изображений
                                        document.querySelector('#imgs').value += JSON.stringify(request.imgs_pk)
                                        // Добавляем теги поста в форму редактирования
                                        for (let tag of request.tags){
                                            let span =document.createElement("span")
                                            span.style.zIndex = -999999999999999
                                            let input = document.createElement("input")
                                            input.className = "tag"
                                            input.value = '#' + tag
                                            input.name = 'tags'
                                            span.style.left = -13290808213787
                                            document.body.append(span)
                                            span.id = 'widthMeasurer'
                                            span.textContent = input.value
                                            input.style.width = `${span.scrollWidth}px`
                                            input.addEventListener('input', () => {
                                                span.textContent = input.value
                                                input.style.width = `${span.scrollWidth}px`
                                                if (input.value.split('')[0] != '#'){
                                                    input.remove()
                                                }
                                            })
                                            document.querySelector(".tags-div").append(input)
                                        }
                                    }})
                            })
                        }
                    }
                }
            })
    }
    let current = 1
    load(10)
    $('.content')[0].addEventListener('scroll', function() {
        const currentScrollTop = $('.content')[0].scrollTop;
        if (this.scrollHeight - $('.content')[0].clientHeight-100< currentScrollTop){
            load(1)
        }
    });
});