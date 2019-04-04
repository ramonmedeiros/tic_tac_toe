var BACKEND = "http://localhost:5000/"
var BACKEND_LOGIN = BACKEND + "login"
var BACKEND_GAME_URL = BACKEND + "game"
var BACKEND_LOGOUT = BACKEND + "logout"


function getToken() {
    var auth = localStorage.getItem("tic_tac_auth");
    if (auth != null) {
        return JSON.parse(auth)["token"];
    }
    return null;
}


function startNewGame() {
    
    var token = getToken();
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 201) {
        uuid = this.responseText;
        location.pathname = "game/" + uuid
    } else {
        setTimeout('document.getElementById("error").textContent = ""', 5000);
        document.getElementById("error").textContent = "Invalid token. Please log in";
    }
    };
    xhttp.open("POST", BACKEND_GAME_URL, true);
    xhttp.setRequestHeader('Content-type','application/json; charset=utf-8');
    xhttp.send(JSON.stringify({"token": token}));
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
    xhttp.setRequestHeader('Content-type','application/json; charset=utf-8');
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
    xhttp.setRequestHeader('Content-type','application/json; charset=utf-8');
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
    move.token = getToken();
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
    xhttp.setRequestHeader('Content-type','application/json; charset=utf-8');
    xhttp.send();
}

function setWinner(player) {
    var inputs = document.getElementsByTagName("input")
    for (index in inputs) {
        inputs[index].disabled = true;
    }

    flash = document.getElementById("error");
    flash.textContent = "Player " + player + " won the game"

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
    token = getToken();

    if (token == null) {
        localStorage.removeItem("tic_tac_auth");
        window.location.reload();
        return null;
    }

    user = JSON.parse(localStorage.getItem("tic_tac_auth"))["user"]
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        localStorage.removeItem("tic_tac_auth");
        window.location.reload();
    } else {
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


function setVisitor() {
    onlyOneRadio("visitor");
    enableBoard();

    board = document.getElementsByName("board");
    for (i = 0; i< board.length; i++) {
        board[i].disabled = true;
    }
}
 

function enableBoard() {
    document.getElementById("board").hidden = false;
    fillBoard();
    var main_interval = window.setInterval(fillBoard, 2000);
}


function onlyOneRadio(id) {
    radios = document.getElementsByName("player");

    for (i = 0; i< radios.length; i++) {
        if (radios[i].id == id) {
            radios[i].checked = true;
        } 
        radios[i].disabled = true;
    }
}

function isItRegistered() {
    // get token
    if (localStorage.getItem("tic_tac_auth") == null) {
        setVisitor();    
    }

    // get uuid and token
    var uuid = location.pathname.split("/").pop();
    token = JSON.parse(localStorage.getItem("tic_tac_auth"))["token"];

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        player = JSON.parse(this.responseText)["player"];
        onlyOneRadio(player);
        enableBoard();
    } else{
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            response = JSON.parse(this.responseText);
            available_players = response["players"];
            for (i = 0; i<available_players.length; i++){
                document.getElementById(available_players[i]).disabled = true;
            }
        }};
        xhttp.open("GET", BACKEND_GAME_URL + "/" + uuid, true);
        xhttp.setRequestHeader('Content-type','application/json; charset=utf-8');
        xhttp.send();
   
    }};
    xhttp.open("GET", BACKEND_GAME_URL + "/" + uuid + "/player?token=" + token , true);
    xhttp.send();

}

function registerPlayer(id) {
    if (id == "visitor") {
        setVisitor();
        return null;
    }

    var uuid = location.pathname.split("/").pop();
    token = JSON.parse(localStorage.getItem("tic_tac_auth"))["token"];
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        onlyOneRadio(id);
        enableBoard();
    }     
    };
    xhttp.open("POST", BACKEND_GAME_URL + "/" + uuid + "/player" , true);
    xhttp.setRequestHeader('Content-type','application/json; charset=utf-8');
    xhttp.send(JSON.stringify({"token": token, "player": id}));
}

