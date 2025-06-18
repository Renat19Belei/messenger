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

            let csrf = $('input')[0].value
            let list = []
            for (let i=0;i!=count;i++){
                list.push(current+i)
            }
            
            let postsList = []
            for (let post of document.querySelectorAll(".post")){
                postsList.push(post.id.split("post").join(''))
            }
            window.location.href
            let type = {}
            type[window.location.href] = window.location.href
            console.log("posts" in type,'eqwqewewqw',type,window.location.href)

            type = {}
            type["http://127.0.0.1:8000/post/posts/"] = "posts"
            console.log(window.location.href in type,'eqwqewewqw',type,window.location.href)
            if (window.location.href in type){
                console.log("posts yey")
                type = 'posts'
            }else if (window.location.href.split('/')[window.location.href.split('/').length-2]=='friends_account'){
                type = document.querySelector(".type").value
                console.log(type)
            }   
            else{
                type = 'main'
                console.log('ok')
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
                    console.log
                    $('.poster').append(request)
                    current+=count
                    // console.log(request)
                    let ellipsises =document.querySelectorAll(".ellipsis")
                    for (let ellipsis of ellipsises){
                        ellipsis.addEventListener('click', () => {
                            for (let object of document.querySelectorAll(`#${ellipsis.id}`)){
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
                                    document.querySelector('.linkInput').value = request.link[0]
                                    let links = request.link
                                    // document.querySelector('.themeInput').value = request.theme
                                    document.querySelector('.nameInput').value = request.name
                                    let count = 0
                                    for (let img of request.imgs){
                                        console.log('heh')
                                        img_tag = document.createElement('img')
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
                                        // imagesDiv
                                        document.querySelector('#imagesDiv').append(div)
                                    }
                                    document.querySelector('#imgs').value += JSON.stringify(request.imgs_pk)
                                    for (let tag of request.tags){
                                        console.log(tag,'tegso')
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
                                        // input.focus()
                                }
                                // for (let linkUrl of links){
                                // let input = document.createElement("input")
                                // input.textContent = linkUrl
                                // let plus = document.createElement("div")
                                // let imgClose = document.createElement("img")
                                // imgClose.src = document.querySelector('#linkClose').value
                                // // imgClose.style.marginRight = 15
                                // imgClose.className = 'imgClose'
                                // input.maxLength = 255
                                // input.required = false
                                // input.className = "formInput linkInput"
                                // input.placeholder = "вставте посилання публікації"
                                // input.name = 'link'
                                // //  name="link"
                                // plus.className = 'plus'
                                // plus.style.marginTop = 15
                                // imgClose.addEventListener('click',()=>{
                                //     plus.remove()
                                //     let plusList = document.querySelectorAll('.plus')
                                //     let elem = plusList[plusList.length-1]
                                //     console.log(elem.querySelector(".imgClose"),elem)
                                //     elem.append(imgPlus)
                                //     if (elem.querySelector(".imgClose")){
                                //         console.log('heh is not error')
                                //         elem.querySelector(".imgClose").remove()
                                //         elem.append(imgClose)
                                //     }
                                    
                                // })
                                // counts.append(plus)
                                // plus.append(input)
                                // plus.append(imgPlus)
                                // plus.append(imgClose)
                                // }
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