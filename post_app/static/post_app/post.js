document.querySelector('.publiaction').addEventListener('submit', (event)=> {
    event.preventDefault()
    document.querySelector('#bg').classList.remove('hidden')
    document.querySelector('#modalForm').classList.remove('hidden')
    const textMessage = document.querySelector('.textInput')
    const messageContent = document.querySelector('.input')
    textMessage.value = messageContent.value
    messageContent.value = '';
})

document.querySelector('.close').addEventListener('click', (event)=> {
    document.querySelector('#bg').classList.add('hidden')
    document.querySelector('#modalForm').classList.add('hidden')
})
document.querySelector('#bg').addEventListener('click', (event)=> {
    document.querySelector('#bg').classList.add('hidden')
    document.querySelector('#modalForm').classList.add('hidden')
})

let counts = document.querySelector('.countOfPlus')
let plus = document.querySelector(".plus")
let imgPlus = document.querySelector('.img-plus')
plus.remove()
counts.append(plus)
imgPlus.addEventListener("click", ()=>{
    let input = document.createElement("input")
    let plus = document.createElement("div")
    let imgClose = document.createElement("img")
    imgClose.src = document.querySelector('#linkClose').value
    imgClose.className = 'imgClose'
    input.maxLength = 255
    input.required = false
    input.className = "formInput linkInput"
    input.placeholder = "вставте посилання публікації"
    input.name = 'link'
    plus.className = 'plus'
    plus.style.marginTop = 15
    imgClose.addEventListener('click',()=>{
        plus.remove()
        let plusList = document.querySelectorAll('.plus')
        let elem = plusList[plusList.length-1]
        elem.append(imgPlus)
        if (elem.querySelector(".imgClose")){
            elem.querySelector(".imgClose").remove()
            elem.append(imgClose)
        }
    })
    counts.append(plus)
    plus.append(input)
    plus.append(imgPlus)
    plus.append(imgClose)
})

const cont = document.querySelector("#imagesDiv")
let readers = []
let count = 0
let filesToUpload = [];
for (let i of new Array(9)){
    let trashUrl = document.querySelector('#trash').value
    const reader = new FileReader();
    let number = 0
    reader.onload = (loadEvent) => {
        let div = document.createElement("div")
        div.id = `div${number}`
        let img = document.createElement("img")
        img.src = loadEvent.target.result
        img.classList.add('image')
        let trashImg = document.createElement("img")
        trashImg.src = trashUrl
        trashImg.id = count
        count++
        let button = document.createElement("button")
        button.type = 'button'
        button.className = 'removeImg'
        button.append(trashImg)
        img.classList.add('image')
        div.classList.add('imagesDiv')
        div.append(img)
        div.append(button)
        cont.append(div)
        let input = document.querySelector('#images1')
        button.addEventListener('click',() => {
            input.value += `${trashImg.id} `
            div.remove()
        })
        number +=1 
    }
    readers.push(reader)
}
document.querySelector("#imageInput").addEventListener('change', (event) => {
    const files = event.target.files
    let count = 0
    if (files.length > 0){
        for (let file of files){
            readers[count].readAsDataURL(file)
            count++
        }
    }
})

for (let tag of document.querySelectorAll('.tag')){
    let span =document.createElement("span")
    span.style.zIndex = -999999999999999
    span.style.left = -13290808213787
    document.body.append(span)
    span.id = 'widthMeasurer'
    span.textContent = tag.value
    tag.style.width = `${span.scrollWidth}px`
}

let textInput = document.querySelector('.textInput')
let p = textInput.parentElement
let input = document.createElement('span')
p.className = 'textWithTags'
input.textContent = ''
input.className = 'grayTags'
input.style.top = 0.83989501312*2+'vw'
input.style.left = '0.83989501312vw'
p.append(input)
textInput.addEventListener('input', (event) => {
    input.style.top = 0.83989501312 + 0.9*textInput.value.split('\n').length+'vw'
})

let objectOfStandard_tags = {}

// Получаем все элементы стандартных тегов
let standard_tags = document.querySelectorAll('.standard_tag')
// Для каждого стандартного тега добавляем обработчик клика
for (let standard_tag of standard_tags){
    standard_tag.addEventListener('click',()=>{
        // Если тег еще не был добавлен, добавляем его в объект и на страницу
        if (!(standard_tag.value in objectOfStandard_tags)){
            objectOfStandard_tags[standard_tag.value] = 1
            // Создаем span для отображения тега
            let sp = document.createElement('span')
            // Создаем скрытый input для передачи значения на сервер
            let inp = document.createElement('input')
            inp.type = 'hidden'
            inp.value = standard_tag.value
            inp.name = 'everyTag'
            sp.className = 'everyTag'
            sp.textContent = standard_tag.value + ' '
            // Добавляем тег и скрытый input в контейнер
            input.append(sp)
            input.append(inp)
        }
    })
}

let buttonTags  = document.querySelector("#addTags")
buttonTags.addEventListener("click", addTag)
function addTag(e){
    let buttonTags  = document.querySelector("#addTags")
    let span =document.createElement("span")
    span.style.zIndex = -999999999999999
    let input = document.createElement("input")
    input.className = "tag"
    input.value = '#'
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
    let buttonTags2 =buttonTags.cloneNode(true)
    buttonTags.remove()
    buttonTags2.addEventListener('click', addTag)
    let tagsDiv = document.querySelector(".tags-div")
    document.querySelector(".tags-div").append(input)
    tagsDiv.append(buttonTags2)
    input.focus()
}