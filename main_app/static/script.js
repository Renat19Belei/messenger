$(document).ready(function(){
    // Отримуємо форму по id та встановлюємо подію відправки форми 
    // $("#reviewForm").submit(function(event){
        // Запобігаємо стандартній поведінці (запобігаємо відправці форми та перезавантаженню сторінки)
        // event.preventDefault();
        // Формуємо AJAX-запит
        // let s = window.location.href.split('/')
        // s.pop()
        // s.pop()
        // window.location.replace(s.join('/')+'/user/login');
        
        function load(count){
            let error= NaN
            try {
                let removeLink = document.querySelector('#removeLink').value
                removeLink.split('1').join('1')
                console.log(removeLink)
                error = true
            } catch (E) {
                 error = false
            }
                
            let link = $('#request')[0].value;
            // if (error){
                
            // }

            let csrf = $('input')[0].value
            let list = []
            for (let i=0;i!=count;i++){
                list.push(current+i)
            }
            
            let postsList = []
            for (let post of document.querySelectorAll(".post")){
                console.log(post)
                postsList.push(post.id.split("post").join(''))
            }
            console.log(postsList)
            
            // postsList
            $.ajax({
                type: 'post',
                url: link,
                data: {csrfmiddlewaretoken:csrf,posts:JSON.stringify(list),postsList:JSON.stringify(postsList)}, 
                success: function(request){
                    
                    $('.poster').append(request)
                    current+=count
                    // console.log(request)
                    let ellipsises =document.querySelectorAll(".ellipsis")
                    for (let ellipsis of ellipsises){
                        ellipsis.addEventListener('click', () => {
                            for (let object of document.querySelectorAll(`#${ellipsis.id}`)){
                                console.log(object)
                                object.classList.toggle("hidden")
                            }
                        })
                    }
                    if (error){
                        let removes =document.querySelectorAll(".remove")
                    
                    for (let remove of removes){
                        console.log(remove.id,removeLink)
                        let link1 = removeLink.value.split('1').join(remove.id)
                        remove.addEventListener('click', () => {
                            console.log('wrgfbv')
                            $.ajax({
                                type: 'post',
                                url: link1,
                                data: {csrfmiddlewaretoken:csrf,posts:JSON.stringify(list)}, 
                                success: function(request){

                                }})
                            document.querySelector('#post'+remove.id).remove()
                            
                        })
                    }
                    let edits =document.querySelectorAll(".edit")
                    for (let edit of edits){
                        edit.addEventListener('click', () => {
                        let index = edit.id
                        console.log(index)
                        document.querySelector('#bg').classList.remove('hidden')
                        document.querySelector('#modalForm').classList.remove('hidden')
                        document.querySelector('#type').value = index
                        for (let object of document.querySelectorAll(`#heh${index}`)){
                            object.classList.toggle("hidden")
                        }
                        console.log(removeLink)
                        let link2 = removeLink.value.split('1')
                        console.log(link2)
                        link2 = link2.join(index)
                        console.log(link2)
                        link2 = link2.split('remove').join('get')
                        console.log(link2)
                        $.ajax({
                                type: 'get',
                                url: link2,
                                success: function(request){
                                    let trashUrl = document.querySelector('#trash').value
                                    // data = JSON.parse(request)
                                    
                                    // document.querySelector('.formName').textContent = ''
                                    console.log(request.text)
                                    document.querySelector('.textInput').value = request.text
                                    document.querySelector('.linkInput').value = request.link
                                    document.querySelector('.themeInput').value = request.theme
                                    document.querySelector('.nameInput').value = request.name
                                    for (let img of request.imgs){
                                        console.log('heh')
                                        img_tag = document.createElement('img')
                                        img_tag.src = img
                                        img_tag.classList.add('image')
                                        let div = document.createElement("div")
                                        div.id = `div${img}`
                                        let trashImg = document.createElement("img")
                                        trashImg.src = trashUrl
                                        let button = document.createElement("button")
                                        button.type = 'button'
                                        button.className = 'removeImg'
                                        button.append(trashImg)
                                        div.classList.add('imagesDiv')
                                        div.append(img_tag)
                                        div.append(button)
                                        button.addEventListener('click',() => {
                                            div.remove()
                                        })
                                        // imagesDiv
                                        document.querySelector('#imagesDiv').append(div)
                                    }
                                    document.querySelector('#imgs').value += JSON.stringify(request.imgs_pk)
                                }})
                        // document.querySelector("#type").value = 
                    })}}
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
    // });
});