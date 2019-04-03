var BACKEND_LOGIN = "http://localhost:5000/login"
var BACKEND_GAME_URL = "http://localhost:5000/game"
var BACKEND_LOGOUT = "http://localhost:5000/logout"

function startNewGame() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 201) {
        uuid = this.responseText;
        location.pathname = "game/" + uuid
        }
    };
    xhttp.open("POST", BACKEND_GAME_URL, true);
    xhttp.setRequestHeader('Content-type','application/json; charset=utf-8');
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
                uuid = game_list[i];
                var p = document.createElement("pre");
                p.textContent = uuid;
                p.id = uuid;
                isFinished(uuid);
                var a = document.createElement("a");
                a.href = location.href + "game/" + uuid;
                a.appendChild(p)
                main_div.appendChild(a);
            }
        }
    };
    xhttp.open("GET", BACKEND_GAME_URL, true);
    xhttp.send();

}

function isFinished(uuid){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        game = JSON.parse(this.responseText);
        if (game['winner'] != null) {
            var link = document.getElementById(uuid);
            link.textContent = link.textContent + " [FINISHED]";
        }
            
    }};
    xhttp.open("GET", BACKEND_GAME_URL + "/" + uuid, true);
    xhttp.send();
}

function getSelection(){
    radios = document.getElementsByName("player");

    for (i = 0; i< radios.length; i++) {
        if (radios[i].checked == true) {
            selected = radios[i];
            return selected;
        }
    }

}

function doMove(id) {
    var uuid = location.pathname.split("/").pop();
    var move = {};
    var button_move = document.getElementById(id)

    // catch moves
    move.player = getSelection().id.toUpperCase();
    move.line = parseInt(id[1]);
    move.column = parseInt(id[2]);

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        document.getElementById(id).disabled = true;
        }
    if (this.readyState == 4 && this.status == 400) {
        error = JSON.parse(this.responseText);
        document.getElementById("error").textContent = error['message'];
        setTimeout('document.getElementById("error").textContent = ""', 5000)
        }
    };

    xhttp.open("POST", BACKEND_GAME_URL + "/" + uuid, true);
    xhttp.setRequestHeader('Content-type','application/json; charset=utf-8');
    xhttp.send(JSON.stringify(move));
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

function login(user) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        token = JSON.parse(this.responseText)["token"];
        localStorage.setItem("tic_tac_auth", JSON.stringify({"token": token, "user": user}));
        window.location.replace(window.location.origin);
    }};
    xhttp.open("POST", BACKEND_LOGIN, true);
    xhttp.setRequestHeader('Content-type','application/json; charset=utf-8');
    xhttp.send(JSON.stringify({"username": user}));
}

function logout() {
    user = JSON.parse(localStorage.getItem("tic_tac_auth"))["user"]
    token = JSON.parse(localStorage.getItem("tic_tac_auth"))["token"]
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        localStorage.removeItem("tic_tac_auth");
        window.location.reload();
    }};
    xhttp.open("POST", BACKEND_LOGOUT, true);
    xhttp.setRequestHeader('Content-type','application/json; charset=utf-8');
    xhttp.send(JSON.stringify({"username": user, "token": token}));
}


function loginBallon() {
    if (localStorage.getItem("tic_tac_auth") == null) {
        document.getElementById("login").textContent = "You are not logged in. Please ";
        document.getElementById("message_link").textContent = "login"
        document.getElementById("link").href = window.location.origin+ "/login";
    } else {
        user = JSON.parse(localStorage.getItem("tic_tac_auth"))["user"];
        document.getElementById("login").textContent = "You are logged as " + user + ". ";
        document.getElementById("message_link").textContent = "Logout";
        document.getElementById("link").href = "javascript:logout()";
    }
}
