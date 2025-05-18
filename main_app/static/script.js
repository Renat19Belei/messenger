$(document).ready(function(){
    // Отримуємо форму по id та встановлюємо подію відправки форми 
    // $("#reviewForm").submit(function(event){
        // Запобігаємо стандартній поведінці (запобігаємо відправці форми та перезавантаженню сторінки)
        // event.preventDefault();
        // Формуємо AJAX-запит
        let current = 1
        $('.content')[0].addEventListener('scroll', function() {
            // This variable holds the current vertical scroll position in pixels
            const currentScrollTop = $('.content')[0].scrollTop;
            // ,$(".poster")[0].clientHeight [0] publiaction
            console.log('Element scrolled:', currentScrollTop, 'px');
            console.log(this.scrollHeight - $('.content')[0].clientHeight)
            if (this.scrollHeight - $('.content')[0].clientHeight-100< currentScrollTop){

                let link = $('#request')[0].value
                let csrf = $('input')[0].value
                // csrfmiddlewaretoken
                console.log(link,csrf)
                $.ajax({
                    type: 'post',
                    url: link,
                    data: {csrfmiddlewaretoken:csrf,posts:JSON.stringify([current])}, 
                    success: function(request){
                        // let s = window.location.href.split('/')
                        // s.pop()
                        // s.pop()
                        // window.location.replace(s.join('/')+'/user/login');
                        $('.poster').append(request)
                        current+=1
                        // document.createElement().
                        console.log(request)
                        // $('content').
                    }
                })
            }
        });
    // });
});