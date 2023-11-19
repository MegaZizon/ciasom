// peer connection
var pc = null;


function createPeerConnection() {
    var config = {
    };

    config.iceServers = [{urls: ['stun:stun.l.google.com:19302']}];

    pc = new RTCPeerConnection(config);

    // register some listeners to help debugging
    

    pc.addEventListener('iceconnectionstatechange', function() {
        if(pc.iceConnectionState=="disconnected"){alert("방송 종료됨")}
        if(pc.iceConnectionState=="connected"){
            document.getElementById('load').style.display = 'none';
        }
    }, false);

   
    var remoteStream = new MediaStream();
    document.getElementById('video').srcObject = remoteStream;
    pc.addEventListener('track', function(evt) {
        remoteStream.addTrack(evt.track, remoteStream);
    });

    pc.addEventListener("ended", function(event) {
        console.log("stoped")
    });

    return pc;
}

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function negotiate() {
    try {
        const offer = await pc.createOffer();
        await pc.setLocalDescription(offer);

        // Wait for ICE gathering to complete
        
        await delay(3000);

        const offerToSend = pc.localDescription;

        const response = await fetch('/watch', {
            body: JSON.stringify({
                sdp: offerToSend.sdp,
                type: offerToSend.type,
                streamid: document.getElementById('streamid').value,
            }),
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            },
            method: 'POST'
        });

        const answer = await response.json();
        await pc.setRemoteDescription(answer);
    } catch (e) {
        alert(e);
    }
}


function start() {

    pc = createPeerConnection();

    streamid=
    pc.addTransceiver('video', {direction: 'recvonly'});
    pc.addTransceiver('audio', {direction: 'recvonly'});
    document.getElementById('media').style.display = 'block';
    negotiate();
    

}

function stop() {

    // close transceivers
    if (pc.getTransceivers) {
        pc.getTransceivers().forEach(function(transceiver) {
            if (transceiver.stop) {
                transceiver.stop();
            }
        });
    }

    // close peer connection
    setTimeout(function() {
        pc.close();
    }, 500);
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}