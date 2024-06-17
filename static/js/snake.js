const canvas = document.getElementById("game-canvas");
const ctx = canvas.getContext("2d");
const socket = io();

const restartButton = document.getElementById("restartButton");
const btnLogOut = document.querySelector(".logout-button");

let gameOverEmitted = false;
let username;
let color = "#234235";

btnLogOut.addEventListener("click", () => {
    window.localStorage.removeItem("playerData");
    let usernameElement = document.getElementById("player");
    usernameElement.textContent = "";
});


// const colorHeader = () => {
//   let gameHeader = document.querySelector(".game-header");
//   gameHeader.style.color = color;
// };

function displayName() {
    let usernameElement = document.getElementById("player");
    usernameElement.textContent = username;
}

function updateScore(state) {
    let score = document.getElementById("score");
    score.textContent = state.snake.length - 1;
}

const getDataFromLocalStorage = () => {
    let playerData = JSON.parse(window.localStorage.getItem("playerData"));
    username = playerData.username;
}

document.addEventListener("keydown", (event) => {
    if (event.keyCode === 37) socket.emit("change_direction", "LEFT");
    if (event.keyCode === 38) socket.emit("change_direction", "UP");
    if (event.keyCode === 39) socket.emit("change_direction", "RIGHT");
    if (event.keyCode === 40) socket.emit("change_direction", "DOWN");
});

function restartgame() {
    getDataFromLocalStorage();
    gameOverEmitted = false;
    socket.emit("restart_game");
}

restartgame();

restartButton.addEventListener("click", restartgame);

function draw(state) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "green";
    ctx.fillRect(state.food.x, state.food.y, 20, 20);


    for (let i = 0; i < state.snake.length; i++) {
        ctx.fillStyle = i === 0 ? "black" : color;
        ctx.fillRect(state.snake[i].x, state.snake[i].y, 20, 20);
    }

    if (state.game_over) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "black";
        ctx.font = "50px Arial";
        const textWidth = ctx.measureText("YOU LOST").width;
        const textX = (canvas.width - textWidth) / 2;
        const textY = canvas.height / 2;
        ctx.fillText("YOU LOST", textX, textY);

        let points = state.snake.length - 1;
        let mapSize = `${canvas.width}x${canvas.height}`;
        socket.emit("game_over", {username, map_size: mapSize, points});
        gameOverEmitted = true;
    }
}

socket.on("game_state", (state) => {
    draw(state);
    updateScore(state);
    displayName();
});

setInterval(() => {
    if (gameOverEmitted === true) {
    } else {
        socket.emit("update");
    }
}, 100);
