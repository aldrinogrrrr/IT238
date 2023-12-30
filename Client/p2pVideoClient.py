<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebRTC Group Video Chat</title>
</head>
<body>

<script>
    const serverIp = "192.168.1.35";
    const serverPort = 12345;
    const socket = new WebSocket(`ws://${serverIp}:${serverPort}`);
    let userName = "";

    const configuration = {
        iceServers: [{urls: "stun:stun.l.google.com:19302"}]
    };

    const peerConnections = {};

    function createPeerConnection(sender) {
        const peerConnection = new RTCPeerConnection(configuration);

        peerConnection.onicecandidate = (event) => {
            if (event.candidate) {
                sendMessage({type: "ice-candidate", candidate: event.candidate, sender});
            }
        };

        peerConnection.onnegotiationneeded = async () => {
            try {
                const offer = await peerConnection.createOffer();
                await peerConnection.setLocalDescription(offer);
                sendMessage({type: "offer", offer, sender});
            } catch (err) {
                console.error("Error creating offer:", err);
            }
        };

        peerConnection.ontrack = (event) => {
            const remoteVideo = document.createElement("video");
            remoteVideo.srcObject = event.streams[0];
            document.body.appendChild(remoteVideo);
        };

        return peerConnection;
    }

    function handleChatMessage(data) {
        console.log(`${data.sender}: ${data.message}`);
    }

    function handleOffer(data) {
        const peerConnection = createPeerConnection(data.sender);

        peerConnection.setRemoteDescription(new RTCSessionDescription(data.offer))
            .then(() => peerConnection.createAnswer())
            .then(answer => peerConnection.setLocalDescription(answer))
            .then(() => sendMessage({type: "answer", answer, sender: userName}))
            .catch(error => console.error("Error handling offer:", error));
    }

    function handleAnswer(data) {
        const peerConnection = peerConnections[data.sender];
        peerConnection.setRemoteDescription(new RTCSessionDescription(data.answer))
            .catch(error => console.error("Error handling answer:", error));
    }

    function handleIceCandidate(data) {
        const peerConnection = peerConnections[data.sender];
        peerConnection.addIceCandidate(new RTCIceCandidate(data.candidate))
            .catch(error => console.error("Error handling ICE candidate:", error));
    }

    function handleInfoMessage(data) {
        console.log(data.message);
    }

    function sendMessage(message) {
        socket.send(JSON.stringify(message));
    }

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        switch (data.type) {
            case "chat":
                handleChatMessage(data);
                break;
            case "offer":
                handleOffer(data);
                break;
            case "answer":
                handleAnswer(data);
                break;
            case "ice-candidate":
                handleIceCandidate(data);
                break;
            case "info":
                handleInfoMessage(data);
                break;
            default:
                console.warn("Unknown message type:", data.type);
        }
    };

    socket.onopen = () => {
        userName = prompt("Enter your name:");
        sendMessage({type: "join", sender: userName});
    };

    socket.onclose = (event) => {
        console.log("Connection closed:", event);
    };

    function startVideoChat() {
        navigator.mediaDevices.getUserMedia({video: true, audio: true})
            .then(stream => {
                const localVideo = document.createElement("video");
                localVideo.srcObject = stream;
                document.body.appendChild(localVideo);

                stream.getTracks().forEach(track => {
                    peerConnections[userName].addTrack(track, stream);
                });
            })
            .catch(error => console.error("Error accessing media devices:", error));
    }

    startVideoChat();  // You can trigger this function based on user actions (e.g., button click).
</script>

</body>
</html>
