// $(document).ready(function(){
//     // Отримуємо форму по id та встановлюємо подію відправки форми 
//     $("#reviewForm").submit(function(event){
//         // Запобігаємо стандартній поведінці (запобігаємо відправці форми та перезавантаженню сторінки)
//         event.preventDefault();
//         // Формуємо AJAX-запит
//         $.ajax({
//             type: 'post', // Вказуємо тип запиту як post
//             URL: '/logout/',
//             data: $(this).serialize(), // Отримуємо усі поля цієї (this) форми у форматі пар ключ=значення
//             success: function(){
//                 let s = window.location.href.split('/')
//                 s.pop()
//                 s.pop()
//                 window.location.replace(s.join('/')+'/user/login');
//             }
//         })
//     });

// });