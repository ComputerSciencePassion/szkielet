window.addEventListener("scroll", function() {
  var menuBar = document.getElementById("menu_bar_container");
  var buttons = document.getElementsByTagName("button");

  if (window.scrollY > 0) {
    menuBar.classList.add("white");
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].classList.add("white");
    }
  } else {
    menuBar.classList.remove("white");
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].classList.remove("white");
    }
  }
});
