var BACKEND_GAME_URL = "http://localhost:5000/game"


function startNewGame() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 201) {
        uuid = this.responseText;
        location.pathname = "game/" + uuid
        }
    };
    xhttp.open("POST", BACKEND_GAME_URL, true);
    xhttp.send();
}

function listGames() {
    main_div = document.getElementById("listGames");

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            game_list = JSON.parse(this.responseText);

            // iterate over games and generate list with link to each one
            for (i = 0; i < game_list.length; i++) {
                var p = document.createElement("pre");
                p.textContent = game_list[i];
                var a = document.createElement("a");
                a.href = location.href + "game/" + game_list[i];
                a.appendChild(p)
                main_div.appendChild(a);
            }
        }
    };
    xhttp.open("GET", BACKEND_GAME_URL, true);
    xhttp.send();

}

function doMove(id) {
    var uuid = location.pathname.split("/").pop();
    var player = document.getElementById(id).value;
    var line = id[1];
    var column = id[2];

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        document.getElementById(id).disabled = true;
        }
    };
    xhttp.open("POST", BACKEND_GAME_URL + "/" + uuid, true);
    xhttp.send(JSON.stringify({"player": player, "line": line, "column": column}));
}

function fillBoard() {
    var uuid = location.pathname.split("/").pop();
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        response = JSON.parse(this.responseText);
        board = response["board"];
        winner = response["winner"];
        for (line = 0; line < board.length; line++) {
            for (column = 0; column < board[line].length; column++) {
                if (board[line][column] != null) {
                    field = document.getElementById("p" + line + column);
                    field.value = board[line][column];
                    field.disabled = true;
                }
            }
        }
        if (winner != null) {
            setWinner(winner);
        }
    }};
    xhttp.open("GET", BACKEND_GAME_URL + "/" + uuid, true);
    xhttp.send();
}

function setWinner(player) {
    var inputs = document.getElementsByTagName("input")
    for (index in inputs) {
        inputs[index].disabled = true;
    }

    flash = document.getElementById("flash");
    h1 = document.createElement("h1");
    h1.textContent = "Player " + player + " won the game"
    flash.appendChild(h1);

    // set winner message
    window.clearInterval(main_interval);
}
