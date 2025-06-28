$(document).ready(function(){
  const modal = document.getElementById("albumModal");
  const openBtn = document.querySelector(".create-album-button");
  const closeBtn = document.querySelector(".close-modal");
  const cancelBtn = document.querySelector("#albumModal .modal-actions button[type='button']");
  const imageInputs = document.querySelectorAll('.imageInput')
  // imageInput
  
  let div = document.createElement("div")
  for (let imageInput of imageInputs){
    imageInput.addEventListener("change", (event)=>{
      console.log("img"+imageInput.id.split('imageInput').join(''))
      div = document.querySelector(".img"+imageInput.id.split('imageInput').join(''))
      console.log(div)
      const files = event.target.files
      let count = 0
      if (files.length > 0){
          for (let file of files){
              const reader = new FileReader();
              reader.onload = (loadEvent) => {
                    let div_img = document.createElement("div")
                    div_img.className = 'photo-container'
                    // photo-container
                    let div_actions = document.createElement("div")
                    div_actions.className = 'photo-overlay-actions'
                    let remove_button = document.createElement("button")
                    let remove_img = document.createElement("img")
                    remove_img.src = document.querySelector('#trash').value
                    remove_img.className = 'icon-img'
                    remove_button.className = 'action-icon-btn'
                    remove_button.append(remove_img)

                    let visible_img = document.createElement("img")
                    let visible_button = document.createElement("button")
                    visible_img.src = document.querySelector('#visible').value
                    visible_img.className = 'icon-img'
                    visible_button.className = 'action-icon-btn'
                    visible_button.append(visible_img)
                    // action-icon-btn

                    div_actions.append(remove_button)
                    div_actions.append(visible_button)
                    // photo-overlay-actions
                    let img = document.createElement("img")
                    img.src = loadEvent.target.result
                    img.className = 'image'
                    div_img.append(img)
                    div_img.append(div_actions)
                    div.prepend(div_img)
                    // return div_img
              }
              // visible
              console.log(imageInput.className,'yutrewq',imageInput)
              // document.querySelector(".img"+imageInput.className).prepend( )
              reader.readAsDataURL(file)
              // let label = document.querySelector("#label"+imageInput.className)
              // console.log(label)
              // label.remove()
              // console.log(div)
              // div.append(label)
          
            }}
          let formData = new FormData()
          
          console.log(imageInput.files)
          formData.append('csrfmiddlewaretoken',document.querySelector('input').value)
          formData.append('type', 'images')
          formData.append('pk', imageInput.id.split('imageInput').join(''))
          for (let i = 0; i < imageInput.files.length; i++) {
            formData.append('images', imageInput.files[i])
          }
          $.ajax({
                type: 'post',
                url: window.location.href,
                data: formData,  
                processData: false,
                contentType: false,
                success: function(request){
                
                }})
          })
  }
  if (openBtn && modal) {
    openBtn.addEventListener("click", () => {
      modal.style.display = "flex";
    });
  }

  if (closeBtn && modal) {
    closeBtn.addEventListener("click", () => {
      modal.style.display = "none";
    });
  }

  if (cancelBtn && modal) {
    cancelBtn.addEventListener("click", () => {
      modal.style.display = "none";
    });
  }

});
// const add = document.querySelector(".add-photo-button")
// add.addEventListener("click")
// yearSelect


let yearSelect = document.getElementById('yearSelect')
for (let year=new Date().getFullYear();year > 1900;year-=1){
    let option = document.createElement('option')
    option.textContent = year;
    yearSelect.append(option);
}

$(document).on('click', '.delete-photo-button', function(){
  const button = $(this);
  const imageID = button.data('image-id')
  
  // $.
  // function 
})

let ellipsises =document.querySelectorAll(".ellipsis")
for (let ellipsis of ellipsises){
    console.log(ellipsis.id)
    ellipsis.addEventListener('click', () => {
      console.log(document.querySelectorAll(`#${ellipsis.id}`))
        for (let object of document.querySelectorAll(`#${ellipsis.id}`)){
            object.classList.toggle("hidden")
        }
    })
}
// remove
let remove_buttons = document.querySelectorAll(".remove")
for (let remove_button of remove_buttons){
    remove_button.addEventListener('click', () => {
        $.ajax({
            type: 'post',
            url: window.location.href,
            data: {
                'csrfmiddlewaretoken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                'type': 'remove',
                'pk': remove_button.id
            },
            success: function(response) {
                // Handle success
                remove_button.parentElement.parentElement.parentElement.parentElement.remove();
            },
            error: function(xhr, status, error) {
                // Handle error
            }
        });
    })
}