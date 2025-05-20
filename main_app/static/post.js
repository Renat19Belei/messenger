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
const cont = document.querySelector("#imagesDiv")
let readers = []
// cont.innerHTML = ""
// let filesToUpload = [];
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
        let input = document.createElement("img")
        input = document.querySelector('#images1')

        try {
            
            input.value = JSON.stringify(JSON.parse(input.value) + [loadEvent.target.result])
        } catch (error) {
            
            input.value = JSON.stringify([loadEvent.target.result])
        }
        // console.log(loadEvent.target.result) images1
        img.classList.add('image')
        let trashImg = document.createElement("img")
        trashImg.src = trashUrl
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
        button.addEventListener('click',() => {
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