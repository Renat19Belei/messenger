document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("albumModal");
  const openBtn = document.querySelector(".create-album-button");
  const closeBtn = document.querySelector(".close-modal");
  const cancelBtn = document.querySelector("#albumModal .modal-actions button[type='button']");
  

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
const add = document.querySelector(".add-photo-button")
add.addEventListener("click")