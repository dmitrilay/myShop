let iconMenu = document.querySelector(".btn-burger");

if (iconMenu != null) {
  let menuBody = document.querySelector(".header__menu-burger");

  iconMenu.addEventListener("click", async (e) => {
    if (!iconMenu.classList.contains("wait")) {
      iconMenu.classList.toggle("_active");
      menuBody.classList.toggle("_active");
      sleep(iconMenu)
    }
  });
}


sleep = (obj) => {
  obj.classList.add('wait');
  resolve = () => {
    obj.classList.remove('wait');
  };
  setTimeout(resolve, 400)
}