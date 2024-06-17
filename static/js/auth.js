let usernameInput = document.getElementById("username");
let startButton = document.getElementById("start");
let usernameError = document.getElementById("username-error");


startButton.addEventListener("click", (event) => {
  let usernameCurrent = usernameInput.value.trim();

  if (usernameCurrent.length < 3) {
    event.preventDefault();
    usernameError.textContent = "Username must be at least 3 characters long.";
    usernameError.style.color = "red";
  } else {
    usernameError.textContent = "";
    window.localStorage.setItem(
      "playerData",
      JSON.stringify({ username: usernameCurrent})
    );
  }
});

usernameInput.addEventListener("keypress", function (event) {
  if (event.key === "Enter") {
    event.preventDefault();
    startButton.click();
  }
});

