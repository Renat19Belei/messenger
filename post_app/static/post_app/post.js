document.querySelector('.publiaction').addEventListener('submit', (event)=> {
    event.preventDefault()
    document.querySelector('#bg').classList.remove('hidden')
    document.querySelector('#modalForm').classList.remove('hidden')
    
    const textMessage = document.querySelector('.textInput')
    const messageContent = document.querySelector('.input')
        
    textMessage.value = messageContent.value
    messageContent.value = '';
})
// '1' - 1 = 0
// '1' + 1 = '11'
document.querySelector('.close').addEventListener('click', (event)=> {
    document.querySelector('#bg').classList.add('hidden')
    document.querySelector('#modalForm').classList.add('hidden')
})
document.querySelector('#bg').addEventListener('click', (event)=> {

    document.querySelector('#bg').classList.add('hidden')
    document.querySelector('#modalForm').classList.add('hidden')
})
console.log('connect')

// let plus = null
// let counts = null
// let imgPlus = null
// img-plus
let counts = document.querySelector('.countOfPlus')
// function plusFunc(){
//     let input = document.createElement("input")
//     let plus = document.createElement("div")
//     let imgClose = document.createElement("img")
//     imgClose.src = document.querySelector('#linkClose').value
//     // imgClose.style.marginRight = 15
//     imgClose.className = 'imgClose'
//     input.maxLength = 255
//     input.required = false
//     input.className = "formInput linkInput"
//     input.placeholder = "вставте посилання публікації"
//     input.id = 'link_id'
//     plus.className = 'plus'
//     plus.style.marginTop = 15
//     imgClose.addEventListener('click',()=>{
//         plus.remove()
//         let plusList = document.querySelectorAll('.plus')
//         let elem = plusList[plusList.length-1]
//         console.log(elem.querySelector(".imgClose"),elem)
//         elem.append(imgPlus)
//         if (elem.querySelector(".imgClose")){
//             console.log('heh is not error')
//             elem.querySelector(".imgClose").remove()
//             elem.append(imgClose)
//         }
        
//     })
//     counts.append(plus)
//     // imgPlus.remove()
//     plus.append(input)
//     plus.append(imgPlus)
//     plus.append(imgClose)
// }
// plusFunc()
let plus = document.querySelector(".plus")
let imgPlus = document.querySelector('.img-plus')
plus.remove()
counts.append(plus)
imgPlus.addEventListener("click", ()=>{
    let input = document.createElement("input")
    let plus = document.createElement("div")
    let imgClose = document.createElement("img")
    imgClose.src = document.querySelector('#linkClose').value
    // imgClose.style.marginRight = 15
    imgClose.className = 'imgClose'
    input.maxLength = 255
    input.required = false
    input.className = "formInput linkInput"
    input.placeholder = "вставте посилання публікації"
    input.name = 'link'
    //  name="link"
    plus.className = 'plus'
    plus.style.marginTop = 15
    imgClose.addEventListener('click',()=>{
        plus.remove()
        let plusList = document.querySelectorAll('.plus')
        let elem = plusList[plusList.length-1]
        console.log(elem.querySelector(".imgClose"),elem)
        elem.append(imgPlus)
        if (elem.querySelector(".imgClose")){
            console.log('heh is not error')
            elem.querySelector(".imgClose").remove()
            elem.append(imgClose)
        }
        
    })
    counts.append(plus)
    plus.append(input)
    plus.append(imgPlus)
    plus.append(imgClose)
})
//     link = forms.CharField(widget=forms.TextInput(attrs=
// {"placeholder": "вставте посилання публікації",
// "class": "formInput linkInput"}),
// label='Посилання',
// max_length=255, 
// required=False)

const cont = document.querySelector("#imagesDiv")
let readers = []
let count = 0
// cont.innerHTML = ""
let filesToUpload = [];
for (let i of new Array(9)){
    // console.log('ghe')
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
        // div.append(input)
        cont.append(div)
        let input = document.querySelector('#images1')
        button.addEventListener('click',() => {
            input.value += `${trashImg.id} `
            console.log('gerhtjyukiloikujyhtgrfews',input.value,input)
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
            // reader.
            readers[count].readAsDataURL(file)
            count++
        }
    }
}
)
for (let tag of document.querySelectorAll('.tag')){
    
    let span =document.createElement("span")
    span.style.zIndex = -999999999999999
    // let input = document.createElement("input")
    // input.className = "tag"
    // input.value = '#'
    // input.name = 'tags'
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
// input/
// input.style.top = textInput.scrollHeight
input.style.top = 0.83989501312*2+'vw'
input.style.left = '0.83989501312vw'
p.append(input)
textInput.addEventListener('input', (event) => {
console.log(textInput.value.split('\n'))
input.style.top = 0.83989501312 + 0.9*textInput.value.split('\n').length+'vw'
})
// standard_tag
let objectOfStandard_tags = {

}
let standard_tags = document.querySelectorAll('.standard_tag')
console.log(standard_tags,input)
for (let standard_tag of standard_tags){
    standard_tag.addEventListener('click',()=>{
        if (!(standard_tag.value in objectOfStandard_tags)){
            objectOfStandard_tags[standard_tag.value] = 1
            // .name = 'everyTag' 
            let sp = document.createElement('span')
            let inp = document.createElement('input')
            inp.type = 'hidden'
            inp.value = standard_tag.value
            inp.name = 'everyTag'
            sp.className = 'everyTag'
            // inp.value = standard_tag.value
            sp.textContent = standard_tag.value + ' '
            input.append(sp)
            input.append(inp)
        }
    })
}
// tag.style.width = `${span.scrollWidth}px`
// span.readOnly = true
// let span = document.createElement('div')
// span.textContent = 'hello'
// span.className = "grayTags"
// let div = document.createElement('div')
// div.name
// editableBox
// let innerDiv = document.createElement('textarea')
// div.className = "BigFormInput textInput"
// innerDiv.textContent = ''
// let textInput = document.querySelector(".textInput")
// let editableBox = document.querySelector(".editableBox")
// textInput.value = span
// span.contenteditable='false'
// div.contenteditable='true'
// div.append(editableBox)
// div.append(span)
// div.addEventListener('click',()=>{
//     editableBox.focus()
// })
// editableBox
// textInput.style.position
// span.style.bottom = '10px'
// div.name = textInput.name
// textInput.replaceWith(div)
// textInput.append(span)
// console.log(textInput)
// textInput
let buttonTags  = document.querySelector("#addTags")
buttonTags.addEventListener("click", (event)=>{
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
    document.querySelector(".tags-div").append(input)
    input.focus()
})
