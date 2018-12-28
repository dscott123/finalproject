$(function() {
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/chat/stream/";
    console.log("Connecting to " + ws_path);
    var chatsock = new ReconnectingWebSocket(ws_path);
    
    chatsock.onmessage = function(message) {
        var data = JSON.parse(message.data);
        if (data.error) {
            alert(data.error);
            return;
        }
        if (data.join) {
            var roomdiv = $(
                "<div class='room' id='room-" + data.join + "'>" +
                "<h2>" + data.title + "</h2>" +
                "<div class='messages'></div>" +
                "<form><input><button>Send</button></form>" +
                "</div>"
            );
            roomdiv.find("form").on("submit", function() {
                chatsock.send(JSON.stringify({
                    "command": "send",
                    "room": data.join,
                    "message": roomdiv.find("input").val()
                }));
                roomdiv.find("input").val("");
                return false;
            });
            $("#chats").append(roomdiv);
        }
        else if (data.leave) {
            $("#room-" + data.leave).remove();
        }
        else if (data.message || data.msg_type != 0) {
            var msgdiv = $("#room-" + data.room + " .messages");
            var ok_msg = "";
            switch (data.msg_type) {
                case 0:
                    ok_msg = "<div class='message'>" +
                        "<span class='username'>" + data.username + ":&nbsp;&nbsp;&nbsp</span>" +
                        "<span class='body'>" + data.message + "</span>" +
                        "</div>";
                    break;
                case 1:
                    ok_msg = "<div class='contextual-message text-warning'>" + data.message +
                        "</div>";
                    break;
                case 3:
                    // "Muted" messages
                    ok_msg = "<div class='contextual-message text-muted'>" + data.message +
                            "</div>";
                    break;
                case 4:
                    // User joined room
                    ok_msg = "<div class='contextual-message text-muted'>" + data.username +
                            " joined the room!" +
                            "</div>";
                    break;
                case 5:
                    // User left room
                    ok_msg = "<div class='contextual-message text-muted'>" + data.username +
                            " left the room!" +
                            "</div>";
                    break;
                default:
                    console.log("Unsupported message type!");
                    return;
            }


            msgdiv.append(ok_msg);
            x = $("#room-" + data.room + " .message").length
            if (x > 20) {
                $("#room-" + data.room + " .message:first").remove();
            }
            msgdiv.scrollTop(msgdiv.prop('scrollHeight'));
        }
        else {
            console.log("Cannot handle message!");
        }
    };
    inRoom = function (roomId) {
        return $("#room-" + roomId).length > 0;
    };
    $("li.room-link").click(function() {
        roomId = $(this).attr("data-room-id");
        if (inRoom(roomId)) {
            $(this).removeClass("joined");
            chatsock.send(JSON.stringify({
                "command": "leave",
                "room": roomId
            }));
            console.log("Leave command sent");
        } else {
            $(this).addClass("joined");
            chatsock.send(JSON.stringify({
                "command": "join",
                "room": roomId
            }));
            console.log("Join command sent");
        }
    });
    chatsock.onopen = function () {
                console.log("Connected to chat socket");
    };
    chatsock.onclose = function () {
                console.log("Disconnected from chat socket");
    };
});