document.querySelector('.publiaction').addEventListener('submit', (event)=> {
    event.preventDefault()
    document.querySelector('#bg').classList.remove('hidden')
    document.querySelector('#modalForm').classList.remove('hidden')
})
document.querySelector('.close').addEventListener('click', (event)=> {
    console.log('wrewererw')
    document.querySelector('#bg').classList.add('hidden')
    document.querySelector('#modalForm').classList.add('hidden')
})
document.querySelector('#bg').addEventListener('click', (event)=> {
    console.log('wrewererw')
    document.querySelector('#bg').classList.add('hidden')
    document.querySelector('#modalForm').classList.add('hidden')
})
console.log('conect')
let plus = document.querySelector(".plus")
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
    // trash
    // filesToUpload.splice(index, 1);
// .imagesDiv
        
        let div = document.createElement("div")
        div.id = `div${number}`
        let img = document.createElement("img")
        img.src = loadEvent.target.result
        // input = document.createElement("img")
        

        // try {
            
        //     input.value = JSON.stringify(JSON.parse(input.value) + [loadEvent.target.result])
        // } catch (error) {
            
        //     input.value = JSON.stringify([loadEvent.target.result])
        // }
        // console.log(loadEvent.target.result) images1
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